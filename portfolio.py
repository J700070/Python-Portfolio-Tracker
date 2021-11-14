import pandas as pd
from stockInfo import *
import json


def getPortfolio(df):
    # We obtain open positions
    portfolio = df.groupby('Producto').sum().reset_index()
    portfolio = portfolio.loc[portfolio['Número'] != 0]

    # We format the dataframe, correct errors & process the information

    portfolio["Total Invertido"] = portfolio["Valor local"] * -1

    # Extra Data
    total_value = portfolio['Total Invertido'].sum()
    number_of_positions = len(portfolio.index)

    portfolio["Precio Medio ($)"] = portfolio["Total Invertido"] / \
        portfolio["Número"]

    portfolio.drop(['Precio', 'Valor local', 'Valor', 'Tipo de cambio', 'Costes de transacción', 'Total'],
                   axis=1, inplace=True)

    # Move columns
    col1 = portfolio.pop('Total Invertido')
    portfolio.insert(len(portfolio.columns), "Total Invertido ($)", col1)

    # ================== Manual Input In Config ===========================
    # Required because Degiro doesn't provide the tickers
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    tickers = data["tickers"]
    # =====================================================================
    prices = []
    for ticker in tickers:
        prices.append(getPrice(ticker))

    portfolio.insert(0, 'Ticker', tickers)
    portfolio = portfolio.set_index('Ticker')
    portfolio.insert(2, 'Precio Actual ($)', prices)
    portfolio.insert(3, 'Total Actual ($)',
                     portfolio["Número"] * portfolio["Precio Actual ($)"])
    portfolio.insert(4, '% Portfolio',
                     portfolio["Total Actual ($)"] / total_value * 100)
    portfolio.insert(len(portfolio.columns),
                     'Ganancia ($)', portfolio["Total Actual ($)"] - portfolio["Total Invertido ($)"])
    portfolio.insert(len(portfolio.columns), 'Ganancia %',
                     portfolio["Ganancia ($)"] / portfolio["Total Invertido ($)"] * 100)

    return total_value, number_of_positions, portfolio
