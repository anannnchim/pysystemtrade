#!/usr/bin/env python3
"""
check_ib_portfolio.py

- Pull IB positions
- Monitor capital & margin changes
- Print formatted console output
- Push to Google Sheet (App tab)
- Write spike-checking labels + PASS/ALERT statuses to fixed cells
- Send email if any spike detected (PASS -> ALERT)

Designed to run every 5 minutes via cron.

Safe: Read-only (IB). Writes to Google Sheet + sends email alerts.
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
from ib_insync import IB
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
# Dynamic Project Root Detection
# ==================================================
def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "private" / "private_config.yaml").exists():
            return parent
    raise FileNotFoundError("private_config.yaml not found in parent directories")


PROJECT_ROOT = find_project_root()
PRIVATE_CONFIG_PATH = PROJECT_ROOT / "private" / "private_config.yaml"


# ==================================================
# IB Connection
# ==================================================

# V1
#def connect_ib() -> IB:
#    ib = IB()
#    ib.connect(HOST, PORT, clientId=CLIENT_ID)
#    return ib
#

# V3
def connect_ib() -> IB:
    ib = IB()

    for i in range(5):
        try:
            print(f"Connect attempt {i+1}")

            ib.connect(HOST, PORT, clientId=CLIENT_ID)

            if not ib.isConnected():
                continue

            # wait for gateway ready
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


def build_summary(summary: dict) -> tuple[float, float, float]:
    net_liq = summary.get("NetLiquidation", 0.0)
    margin = summary.get("FullInitMarginReq", 0.0)
    margin_usage = (margin / net_liq * 100) if net_liq > 0 else 0.0
    return net_liq, margin, margin_usage


# ==================================================
# Risk Monitoring
# ==================================================
def load_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f)


def evaluate_risk(net_liq: float, margin: float, margin_usage: float) -> dict:
    previous = load_json(STATE_FILE)

    prev_net_liq = previous.get("net_liq")
    prev_margin = previous.get("margin")

    capital_change_pct = 0.0
    margin_change_pct = 0.0

    capital_status = "PASS"
    margin_status = "PASS"
    usage_status = "PASS"

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
# Email Alert
# ==================================================
def load_email_config() -> dict:
    with open(PRIVATE_CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f) or {}

    required = ["email_address", "email_pwd", "email_server", "email_to", "email_port"]
    missing = [k for k in required if k not in cfg]
    if missing:
        raise KeyError(f"Missing keys in private_config.yaml: {missing}")

    return cfg


def send_email(subject: str, body: str) -> None:
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

    print("📧 Email alert sent.")


def maybe_send_spike_email(risk: dict, net_liq: float, margin: float) -> None:
    any_alert = any([
        risk["capital_status"] == "ALERT",
        risk["margin_status"] == "ALERT",
        risk["usage_status"] == "ALERT",
    ])

    signature = (
        f"{risk['capital_status']}-"
        f"{risk['margin_status']}-"
        f"{risk['usage_status']}-"
        f"{risk['capital_change_pct']}-"
        f"{risk['margin_change_pct']}-"
        f"{risk['margin_usage']}"
    )

    last = load_json(EMAIL_STATE_FILE).get("last_alert_signature", "")

    if any_alert and signature != last:
        subject = "🚨 Anan Capital Risk Alert"
        body = (
            f"Spike Detected\n\n"
            f"Capital Move % : {risk['capital_change_pct']} ({risk['capital_status']})\n"
            f"Margin Move %  : {risk['margin_change_pct']} ({risk['margin_status']})\n"
            f"Margin Usage % : {risk['margin_usage']} ({risk['usage_status']})\n\n"
            f"Net Liquidation     : {net_liq:,.2f}\n"
            f"Full Init Margin Req: {margin:,.2f}\n"
            f"Time: {datetime.now()}\n"
        )
        send_email(subject, body)
        save_json(EMAIL_STATE_FILE, {"last_alert_signature": signature})

    if not any_alert and last != "":
        save_json(EMAIL_STATE_FILE, {"last_alert_signature": ""})


# ==================================================
# Google Sheet Push
# ==================================================
def push_to_google_sheet(df_positions, net_liq, margin, margin_usage, risk):
    sheet_access = GoogleSheetAccess()
    sheet_access.clear_sheet(SHEET_URL, SHEET_NAME)

    sheet_access.write_dataframe_to_sheet(
        SHEET_URL, SHEET_NAME,
        pd.DataFrame({"A": ["LIVE PORTFOLIO"]}),
        start_cell="A1", header=False
    )

    sheet_access.write_dataframe_to_sheet(
        SHEET_URL, SHEET_NAME,
        pd.DataFrame({"A": ["Last Update"], "B": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]}),
        start_cell="A2", header=False
    )

    summary_df = pd.DataFrame({
        "Metric": ["Net Liquidation", "Full Init Margin Req", "Margin Usage %"],
        "Value": [round(net_liq, 2), round(margin, 2), round(margin_usage, 2)]
    })

    sheet_access.write_dataframe_to_sheet(
        SHEET_URL, SHEET_NAME,
        summary_df,
        start_cell="A4", header=True
    )

    sheet_access.write_dataframe_to_sheet(
        SHEET_URL, SHEET_NAME,
        pd.DataFrame([["Spiked Checking"]]),
        start_cell="D4", header=False
    )

    sheet_access.write_dataframe_to_sheet(
        SHEET_URL, SHEET_NAME,
        pd.DataFrame([
            [risk["capital_change_pct"]],
            [risk["margin_change_pct"]],
            [risk["margin_usage"]],
        ]),
        start_cell="D5", header=False
    )

    sheet_access.write_dataframe_to_sheet(
        SHEET_URL, SHEET_NAME,
        pd.DataFrame({
            "E": [
                risk["capital_status"],
                risk["margin_status"],
                risk["usage_status"],
            ]
        }),
        start_cell="E5", header=False
    )

    if not df_positions.empty:
        sheet_access.write_dataframe_to_sheet(
            SHEET_URL, SHEET_NAME,
            df_positions,
            start_cell="A9", header=True
        )


# ==================================================
# Main
# ==================================================
if __name__ == "__main__":

    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} === START: Connecting to IB Gateway ===")

    ib = connect_ib()

    print("Connected:", ib.isConnected())
    print("Managed Accounts:", ib.managedAccounts())

    df_positions = get_positions_dataframe(ib)
    summary = get_account_summary(ib)
    net_liq, margin, margin_usage = build_summary(summary)

    ib.disconnect()

    print("\n=== Account Summary ===")
    print(f"Net Liquidation     : {net_liq:,.2f}")
    print(f"Full Init Margin Req: {margin:,.2f}")
    print(f"Margin Usage        : {margin_usage:.2f}%")

    risk = evaluate_risk(net_liq, margin, margin_usage)

    print("\n=== Risk Status ===")
    print(risk)

    try:
        maybe_send_spike_email(risk, net_liq, margin)
    except Exception as e:
        print(f"Email alert error: {e}")

    push_to_google_sheet(df_positions, net_liq, margin, margin_usage, risk)

    print("\nGoogle Sheet updated successfully.")