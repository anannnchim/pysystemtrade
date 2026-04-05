from sysbrokers.IB.ib_orders import ibExecutionStackData
from sysdata.mongodb.mongo_spread_costs import mongoSpreadCostData
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData

if __name__ == '__main__':
    from sysproduction.data.broker import dataBroker

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------
    csvData = csvFuturesSimData()
    dbData = dbFuturesSimData()
    broker = dataBroker()

    # --------------------------------------------------
    # GET INSTRUMENT LISTS
    # --------------------------------------------------
    csv_instruments = set(csvData.get_instrument_list())
    db_instruments = set(dbData.get_instrument_list())

    broker_df = broker.broker_futures_instrument_data.get_all_instrument_data_as_df()
    broker_instruments = set(broker_df.index)

    # --------------------------------------------------
    # PRINT RAW LISTS (optional)
    # --------------------------------------------------
    print("\n===== CSV INSTRUMENTS =====")
    print(len(csv_instruments))

    print("\n===== DB INSTRUMENTS =====")
    print(len(db_instruments))

    print("\n===== BROKER INSTRUMENTS =====")
    print(len(broker_instruments))

    # --------------------------------------------------
    # SET ANALYSIS
    # --------------------------------------------------
    all_sources = csv_instruments | db_instruments | broker_instruments

    in_all_3 = csv_instruments & db_instruments & broker_instruments

    in_csv_db = (csv_instruments & db_instruments) - broker_instruments
    in_csv_broker = (csv_instruments & broker_instruments) - db_instruments
    in_db_broker = (db_instruments & broker_instruments) - csv_instruments

    only_csv = csv_instruments - (db_instruments | broker_instruments)
    only_db = db_instruments - (csv_instruments | broker_instruments)
    only_broker = broker_instruments - (csv_instruments | db_instruments)

    # --------------------------------------------------
    # HELPER
    # --------------------------------------------------
    def print_group(title, s):
        print(f"\n===== {title} =====")
        print(f"Count: {len(s)}")
        if len(s) > 0:
            print(sorted(s))

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------
    print_group("IN ALL 3 (OK)", in_all_3)

    print_group("IN CSV + DB ONLY (Missing BROKER)", in_csv_db)
    print_group("IN CSV + BROKER ONLY (Missing DB)", in_csv_broker)
    print_group("IN DB + BROKER ONLY (Missing CSV)", in_db_broker)

    print_group("ONLY CSV", only_csv)
    print_group("ONLY DB", only_db)
    print_group("ONLY BROKER", only_broker)

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    print("\n===== SUMMARY =====")
    print(f"Total unique instruments: {len(all_sources)}")
    print(f"All 3 matched: {len(in_all_3)}")
    print(f"Mismatch total: {len(all_sources) - len(in_all_3)}")
