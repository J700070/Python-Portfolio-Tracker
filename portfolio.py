
import numpy as np
import pandas as pd
from stockInfo import *
import json


def getPortfolio(df):
    raw_data = df.groupby('Producto').sum().reset_index()
    closed_positions = df.groupby('Producto').sum().reset_index()
    closed_positions = closed_positions.loc[closed_positions['Número'] == 0]
    # We obtain open positions
    portfolio = df.groupby('Producto').sum().reset_index()
    portfolio = portfolio.loc[portfolio['Número'] != 0]

    # We format the dataframe, correct errors & process the information

    portfolio["Total Invertido"] = portfolio["Valor local"] * -1

    portfolio["Precio Medio ($)"] = portfolio["Total Invertido"] / \
        portfolio["Número"]

    portfolio.drop(['Precio', 'Valor local', 'Valor', 'Tipo de cambio', 'Costes de transacción', 'Total'],
                   axis=1, inplace=True)

    # Move columns
    col1 = portfolio.pop('Total Invertido')
    portfolio.insert(len(portfolio.columns), "Total Invertido ($)", col1)

    # ================== Manual Input In Config ===========================
    # Required because Degiro doesn't provide the tickers + We can add custom holdings
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    tickers = data["tickers"]
    btc = data["other_holdings"][0]
    btc_holding = {
        "Producto": [btc["Producto"]],
        "Número": [float(btc["Número"])],
        "Precio Medio ($)": [float(btc["Precio Medio"])],
        "Total Invertido ($)": [float(btc["Total Invertido"])],
    }
    portfolio = portfolio.append(pd.DataFrame.from_dict(btc_holding))
    # =====================================================================

    # Other Data
    total_invested = portfolio['Total Invertido ($)'].sum()
    number_of_positions = len(portfolio.index)

    # Sumamos las posiciones cerradas
    total_gains = closed_positions['Total'].sum()
    # =====================================================================

    prices = []
    for ticker in tickers:
        prices.append(getPrice(ticker))

    portfolio.insert(0, 'Ticker', tickers)
    portfolio = portfolio.set_index('Ticker')
    portfolio.insert(2, 'Precio Actual ($)', prices)
    portfolio.insert(3, 'Total Actual ($)',
                     portfolio["Número"] * portfolio["Precio Actual ($)"])

    # Total Value
    total_value = portfolio['Total Actual ($)'].sum()

    portfolio.insert(4, '% Portfolio',
                     portfolio["Total Actual ($)"] / total_value * 100)
    portfolio.insert(len(portfolio.columns),
                     'Ganancia ($)', portfolio["Total Actual ($)"] - portfolio["Total Invertido ($)"])

    # Sumamos las posiciones abiertas
    total_gains += portfolio['Ganancia ($)'].sum()

    portfolio.insert(len(portfolio.columns), 'Ganancia %',
                     portfolio["Ganancia ($)"] / portfolio["Total Invertido ($)"] * 100)

    # Name formatting
    portfolio["Producto"] = portfolio["Producto"].apply(lambda x: x.title())

    # Type Adjusting and Rounding
    portfolio["Precio Actual ($)"] = portfolio["Precio Actual ($)"].astype(int)
    portfolio["Total Actual ($)"] = portfolio["Total Actual ($)"].astype(int)

    portfolio["Precio Medio ($)"] = portfolio["Precio Medio ($)"].astype(int)
    portfolio["Total Invertido ($)"] = portfolio["Total Invertido ($)"].astype(
        int)
    portfolio["Ganancia ($)"] = portfolio["Ganancia ($)"].astype(int)

    return total_value, number_of_positions, total_invested, total_gains, portfolio, closed_positions
