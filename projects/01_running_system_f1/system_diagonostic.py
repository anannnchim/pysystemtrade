"""
Objective: Access system data.

"""
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
from program.googlesheet.googlesheet_access import GoogleSheetAccess
from systems.risk import Risk

# INPUT
sheet_url = 'https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1248180211#gid=1248180211'
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")
c1 = "GF10"

data = csvFuturesSimData()
s = futures_system(config=config, data=data)

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

# Initialize data source
sheet_access = GoogleSheetAccess()


if __name__ == '__main__':
    s.accounts.portfolio().percent.curve().plot()
    plt.show()

    # Note: Data
    c = pd.DataFrame({

        # A) Instrument level
        # Price
        "Price": s.accounts.get_instrument_prices_for_position_or_forecast(c1),
        "ChangePerCont": s.accounts.get_instrument_prices_for_position_or_forecast(c1).diff(
            1) * s.accounts.get_value_of_block_price_move(c1),
        "DailyRisk":  s.rawdata.daily_returns_volatility(c1) ,

        # CombineForecast
        "Forecast": s.combForecast.get_combined_forecast(c1),

        # B) Subsystem level

        # 1. VolScalar
        "VolScalar": s.positionSize.get_average_position_at_subsystem_level(c1),  # vol_scalar =  target vol / instru vol

        # 2. SubsystemPosition
        "SubSystemPosition": s.positionSize.get_subsystem_position(c1),  # Main: (vol_scalr * combForecast)/10 [assume full fixed cap]

        # C) Portfolio level
        # 1. IDM
        "IDM": s.portfolio.get_instrument_diversification_multiplier(),

        # 2. Portfolio weight
        "Weight": s.portfolio.get_instrument_weights()[c1],

        # 3. NotionalPosition
        "Position": s.portfolio.get_notional_position(c1),

        # 4,5,6 Buffer
        "Buffer": s.portfolio.get_buffers(c1),
        "TopBuffer": s.portfolio.get_buffers_for_position(c1).iloc[:,0],
        "BotBuffer": s.portfolio.get_buffers_for_position(c1).iloc[:,1],

        # D) Account level
        "BufferedPos": s.accounts.get_buffered_position(c1),

        # E) Calculate PNL

        # Individual PNL
        "Gross": s.accounts.pandl_for_instrument(c1).gross,
        "Costs": s.accounts.pandl_for_instrument(c1).costs,
        "Net": s.accounts.pandl_for_instrument(c1).net,

        # Portfolio PNL
        "PNL": s.accounts.portfolio(),
    })

    # Note: Send to google-sheet
    c = c.tail(20)
    # c = c.head(300)
    c.fillna(0, inplace=True)  # Replace NaN with zero (or another value)

    # Write to sheet
    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "03-System-diagnostic",
        c,
        "B11",
        header=False)
