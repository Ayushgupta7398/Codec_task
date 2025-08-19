import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import date, timedelta

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

# Sidebar Inputs
st.sidebar.header("Select Stock")
ticker = st.sidebar.text_input("Ticker Symbol (e.g., AAPL, TSLA)", value="AAPL")

# Date range
start_date = st.sidebar.date_input("Start Date", value=date.today() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", value=date.today())

# Fetch data
@st.cache_data(ttl=3600)  # cache for 1 hour
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    data["Date"] = pd.to_datetime(data["Date"])
    return data

try:
    df = load_data(ticker, start_date, end_date)
    st.subheader(f"Showing data for: {ticker.upper()}")

    if len(df) < 2:
        st.warning("Not enough data to calculate metrics. Please select a longer date range.")
    else:
        latest_close = float(df["Close"].iloc[-1])
        change = float(df["Close"].iloc[-1] - df["Close"].iloc[-2])
        pct_change = float((change / df["Close"].iloc[-2]) * 100)

        col1, col2, col3 = st.columns(3)
        col1.metric("Last Close", f"${latest_close:.2f}")
        col2.metric("Change", f"${change:.2f}")
        col3.metric("Change %", f"{pct_change:.2f}%")

        # Line Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Close Price", line=dict(color='royalblue')))
        fig.update_layout(title="Closing Price Over Time", xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)

        # Candlestick Chart
        st.subheader("Candlestick Chart")
        candlestick = go.Figure(data=[go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])
        candlestick.update_layout(xaxis_title="Date", yaxis_title="Price", height=500)
        st.plotly_chart(candlestick, use_container_width=True)

        # Show raw data
        with st.expander("📄 View Raw Data"):
            st.dataframe(df)

        # Export CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name=f"{ticker}_data.csv", mime='text/csv')

except Exception as e:
    st.error(f"Error fetching data: {e}")


# COMMAND FOR RUN THIS PROGRAM 

# streamlit run f:\practice\stock_dashboard\app.py
#  streamlit run app.py

