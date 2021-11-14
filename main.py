import streamlit as st
import pandas as pd
import numpy as np
import json
from transactionParser import *
from portfolio import *

# Streamlit config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
    page_title="Portfolio Tracker",
    page_icon=None,
)


# Import Data
degiro_transactions = pd.read_csv("Transactions.csv")

with open("config.json") as json_data_file:
    data = json.load(json_data_file)

# Process Data
degiro_transactions = parseDegiro(degiro_transactions)
totalValue, group = getPortfolio(degiro_transactions)
lastYearDiff = totalValue - data["lastYearPortfolioValue"]
# Show Data
# ==========================================================================
st.title('Portfolio Tracker')


col1, col2, col3, col4 = st.columns(4)

col1.metric('Portfolio Value',
            "$" + "{:,}".format(round(totalValue, 2)), f"${round(lastYearDiff, 2)}")

col2.metric("Daily Change",
            f"${round(12312,2)}", f"{round(123132*100,2)}%")

col3.metric("Annual Volatility _expected return",
            f"{round(123123, 2)}%", f"{round(12312,2)*100}%")

col4.metric("Sharpe _sortino Raio",
            f"{round(12312, 2)}", f"{round(123123, 2)}")

# st.subheader('Transacciones')
# st.write(degiro_transactions)

st.subheader('Portfolio')
st.write(group)
