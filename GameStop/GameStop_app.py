import pandas as pd
import streamlit as st
import yfinance as yf
import datetime
 
yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1) 

t0='2020-01-01'
t1=yesterday

st.write(f"""
# Hold the Line

The short squeeze of the century.

GameStop stock from {t0} to today

This app followed guidance by Chanin Nantasenamat (aka Data Professor) http://youtube.com/dataprofessor
""")

#https://www.youtube.com/watch?v=JwSS70SZdyM&t=555s&ab_channel=freeCodeCamp.org
#define the ticker symbol
tickerSymbol = 'GME'
tickerData = yf.Ticker(tickerSymbol)
ticker_df = tickerData.history(period='1d', start= t0, end= t1)

st.write(f"""
## Trading Volume
{t0} to {t1}
""")
st.line_chart(ticker_df.Volume)

st.write(f"""
## Price Change
{t0} to {t1}
""")
st.line_chart(ticker_df.Close- ticker_df.Open)

st.write(f"""
## Closing Price
{t0} to {t1}
""")
st.line_chart(ticker_df.Close)

st.write("""
#### A comical little proof by contradiction.

#### If one is to assume secondary market trading to be a reliable source of information about the underlying company... 
 
#### this tale quickly demonstrates that stock market value is not a reliable source.
""")