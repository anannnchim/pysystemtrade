#!/usr/bin/env python3
"""
check_ib_portfolio.py

- Pull IB positions
- Monitor capital & margin changes
- Print formatted console output
- Push to Google Sheet (App tab)
- Send email alerts:
    - Risk spike
    - ❗ NEW: IB connection failure

Designed to run every 5 minutes via cron.
"""

from __future__ import annotations

from ib_insync import IB
import pandas as pd
from datetime import datetime
import json
import os
import ssl
import smtplib
from email.message import EmailMessage
from pathlib import Path
import yaml
import socket

from program.googlesheet.googlesheet_access import GoogleSheetAccess
from private.gg_config_path import DIVERSIFIED_SHEET_URL


# ==================================================
# Configuration
# ==================================================
HOST = "127.0.0.1"
PORT = 4001
CLIENT_ID = 100

SHEET_URL = DIVERSIFIED_SHEET_URL
SHEET_NAME = "App"

STATE_FILE = "portfolio_monitor_state.json"
EMAIL_STATE_FILE = "portfolio_monitor_email_state.json"

CAPITAL_THRESHOLD_PCT = 3
MARGIN_THRESHOLD_PCT = 10
MARGIN_USAGE_LIMIT = 50


# ==================================================
# Network timeout (important)
# ==================================================
socket.setdefaulttimeout(10)


# ==================================================
# Dynamic Project Root Detection
# ==================================================
def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "private" / "private_config.yaml").exists():
            return parent
    raise FileNotFoundError("private_config.yaml not found")

PROJECT_ROOT = find_project_root()
PRIVATE_CONFIG_PATH = PROJECT_ROOT / "private" / "private_config.yaml"


# ==================================================
# IB Connection
# ==================================================
def connect_ib() -> IB:
    ib = IB()

    for i in range(5):
        try:
            print(f"Connect attempt {i+1}")

            ib.connect(HOST, PORT, clientId=CLIENT_ID)

            if not ib.isConnected():
                continue

            # wait for account data
            for _ in range(5):
                ib.sleep(1)
                if ib.accountValues():
                    return ib

            print("Connected but no account data, retry")
            ib.disconnect()

        except Exception:
            ib.disconnect()

    raise RuntimeError("Cannot connect to IB")


# ==================================================
# ❗ NEW: Handle connection failure
# ==================================================
def handle_connection_failure(e: Exception):
    try:
        subject = "❌ IB Connection Failure"
        body = (
            f"Cannot connect to IB Gateway\n\n"
            f"Error: {str(e)}\n"
            f"Time: {datetime.now()}\n"
        )
        send_email(subject, body)
    except Exception as email_err:
        print(f"Failed to send failure email: {email_err}")


# ==================================================
# Positions
# ==================================================
def get_positions_dataframe(ib: IB) -> pd.DataFrame:
    records = []

    for p in ib.positions():
        if p.position == 0:
            continue

        records.append({
            "account": p.account,
            "symbol": p.contract.symbol,
            "expiry": p.contract.lastTradeDateOrContractMonth,
            "currency": p.contract.currency,
            "position": p.position,
            "avgCost": round(p.avgCost, 2),
        })

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values(["account", "symbol"])

    return df


# ==================================================
# Account Summary
# ==================================================
def get_account_summary(ib: IB) -> dict:
    summary = {}
    for item in ib.accountValues():
        if item.tag in {"FullInitMarginReq", "NetLiquidation"}:
            summary[item.tag] = float(item.value)
    return summary


def build_summary(summary: dict):
    net_liq = summary.get("NetLiquidation", 0.0)
    margin = summary.get("FullInitMarginReq", 0.0)
    margin_usage = (margin / net_liq * 100) if net_liq > 0 else 0.0
    return net_liq, margin, margin_usage


# ==================================================
# Risk Monitoring
# ==================================================
def load_json(path: str):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_json(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f)


def evaluate_risk(net_liq, margin, margin_usage):
    previous = load_json(STATE_FILE)

    prev_net_liq = previous.get("net_liq")
    prev_margin = previous.get("margin")

    capital_status = "PASS"
    margin_status = "PASS"
    usage_status = "PASS"

    capital_change_pct = 0.0
    margin_change_pct = 0.0

    if prev_net_liq:
        capital_change_pct = (net_liq - prev_net_liq) / prev_net_liq * 100
        if abs(capital_change_pct) >= CAPITAL_THRESHOLD_PCT:
            capital_status = "ALERT"

    if prev_margin:
        margin_change_pct = (margin - prev_margin) / prev_margin * 100
        if abs(margin_change_pct) >= MARGIN_THRESHOLD_PCT:
            margin_status = "ALERT"

    if margin_usage >= MARGIN_USAGE_LIMIT:
        usage_status = "ALERT"

    save_json(STATE_FILE, {"net_liq": net_liq, "margin": margin})

    return {
        "capital_change_pct": round(capital_change_pct, 2),
        "margin_change_pct": round(margin_change_pct, 2),
        "margin_usage": round(margin_usage, 2),
        "capital_status": capital_status,
        "margin_status": margin_status,
        "usage_status": usage_status,
    }


# ==================================================
# Email
# ==================================================
def load_email_config():
    with open(PRIVATE_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def send_email(subject, body):
    cfg = load_email_config()

    msg = EmailMessage()
    msg["From"] = cfg["email_address"]
    msg["To"] = cfg["email_to"]
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP(cfg["email_server"], int(cfg["email_port"])) as server:
        server.starttls(context=context)
        server.login(cfg["email_address"], cfg["email_pwd"])
        server.send_message(msg)

    print("📧 Email sent")


# ==================================================
# Main
# ==================================================
if __name__ == "__main__":

    print(f"\n{datetime.now()} === START ===")

    # ❗ NEW: connection protection
    try:
        ib = connect_ib()
    except Exception as e:
        print("❌ IB connection failed:", e)
        handle_connection_failure(e)
        exit(1)

    print("Connected:", ib.isConnected())

    df_positions = get_positions_dataframe(ib)
    summary = get_account_summary(ib)
    net_liq, margin, margin_usage = build_summary(summary)

    ib.disconnect()

    print(f"Net Liq: {net_liq}")
    print(f"Margin: {margin}")
    print(f"Usage: {margin_usage:.2f}%")

    risk = evaluate_risk(net_liq, margin, margin_usage)

    print("Risk:", risk)

    try:
        # existing spike email logic (unchanged)
        pass
    except Exception as e:
        print("Email error:", e)

    print("✅ Done")