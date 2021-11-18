import streamlit as st
import pandas as pd
import numpy as np
import json
from transactionParser import *
from portfolio import *
from style import *
import datetime

# Streamlit config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
    page_title="Portfolio Tracker",
    page_icon=None,
)
# Pandas config
pd.options.display.float_format = "{:,.2f}".format

# Import Data
degiro_transactions = pd.read_csv("Transactions.csv")

with open("config.json") as json_data_file:
    data = json.load(json_data_file)

# Process Data
# ==========================================================================
degiro_transactions = parseDegiro(degiro_transactions)
total_value, number_of_positions, total_invested, total_gains, portfolio, raw_data = getPortfolio(
    degiro_transactions)
lastYearDiff = total_value - data["lastYearPortfolioValue"]
start_date = datetime.datetime.strptime(data["start_date"], "%d-%m-%Y").date()
today = datetime.date.today()
years = round((today - start_date).days / 365, 2)
total_return = total_gains/total_invested
cagr = ((1+1*total_return) ** (1 / years) - 1) * 100
# Show Data
# ==========================================================================
st.title('Portfolio Tracker')


col1, col2, col3, col4 = st.columns(4)

col1.metric('Portfolio Value',
            "$" + "{:,}".format(round(total_value, 2)), "Anterior: " + "{:,}".format(round(data["lastYearPortfolioValue"], 2)) + "$", delta_color="off")

col2.metric('1 Year Diff',
            "$" + "{:,}".format(round(lastYearDiff, 2)), f"{round(lastYearDiff / total_value * 100, 2)} %")

col3.metric("Total Gains",
            "$" + "{:,}".format(round(total_gains, 2)), f"{round(total_return * 100, 2)} %")

col4.metric("CAGR",
            f"{round(cagr, 2)}%", "In " + str(years) + " years", delta_color="off")

# st.subheader('Transacciones')
# st.write(degiro_transactions)

st.subheader('Portfolio')

# Styling
portfolio = portfolio.style.applymap(font_color,
                                     subset=["Ganancia ($)", "Ganancia %"])
st.dataframe(portfolio.applymap(font_size))

# st.dataframe(raw_data)


def toYearFraction(date):
    def sinceEpoch(date):  # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction
