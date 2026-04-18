import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="TradePredict AI", layout="wide")
st.title("TradePredict AI Dashboard")

symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AAPL", "TSLA"]
selected_symbol = st.selectbox("Select Asset", symbols)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Price Prediction")
    try:
        pred_response = requests.get(f"{API_URL}/predict/{selected_symbol}", timeout=10)
        if pred_response.status_code == 200:
            pred_data = pred_response.json()
            st.metric("Current Price", f"${pred_data['current_price']:.2f}")
            st.metric("Predicted Price", f"${pred_data['predicted_price']:.2f}", 
                     delta=f"{((pred_data['predicted_price'] - pred_data['current_price']) / pred_data['current_price'] * 100):.2f}%")
        else:
            st.error("Failed to fetch prediction")
    except:
        st.warning("API not available. Run with docker-compose up")

with col2:
    st.subheader("Trading Signal")
    try:
        signal_response = requests.get(f"{API_URL}/signals/{selected_symbol}", timeout=10)
        if signal_response.status_code == 200:
            signal_data = signal_response.json()
            signal_color = {"BUY": "green", "SELL": "red", "HOLD": "gray"}
            st.markdown(f"### {signal_data['signal']}")
            st.write(f"**RSI:** {signal_data['rsi']:.2f}" if signal_data.get('rsi') else "RSI: N/A")
            st.write(f"**SMA 20:** ${signal_data['sma_20']:.2f}" if signal_data.get('sma_20') else "SMA 20: N/A")
            st.write(f"**SMA 50:** ${signal_data['sma_50']:.2f}" if signal_data.get('sma_50') else "SMA 50: N/A")
        else:
            st.error("Failed to fetch signals")
    except:
        st.warning("API not available")

with col3:
    st.subheader("Quick Stats")
    st.write("Select an option below to view detailed analysis")

option = st.radio("Select View", ["Price Chart", "Backtest Results"])

if option == "Price Chart":
    try:
        hist_response = requests.get(f"{API_URL}/historical/{selected_symbol}", timeout=10)
        if hist_response.status_code == 200:
            df = pd.DataFrame(hist_response.json())
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df["timestamp"],
                open=df["open"], high=df["high"], low=df["low"], close=df["close"],
                name="Price"
            ))
            fig.update_layout(title=f"{selected_symbol} Price Chart", template="plotly_dark", height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Failed to fetch historical data")
    except:
        st.warning("API not available")

elif option == "Backtest Results":
    try:
        with st.spinner("Running backtest..."):
            bt_response = requests.post(
                f"{API_URL}/backtest",
                json={"symbol": selected_symbol, "initial_capital": 10000},
                timeout=30
            )
        if bt_response.status_code == 200:
            bt_data = bt_response.json()
            
            st.subheader("Performance Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Return", f"{bt_data['total_return']:.2f}%")
            m2.metric("Sharpe Ratio", f"{bt_data['sharpe_ratio']:.2f}")
            m3.metric("Max Drawdown", f"{bt_data['max_drawdown']:.2f}%")
            
            m4, m5 = st.columns(2)
            m4.metric("Final Value", f"${bt_data['final_value']:,.2f}")
            m5.metric("Win Rate", f"{bt_data['win_rate']:.2f}%")
            
            st.write(f"**Total Trades:** {bt_data['total_trades']}")
        else:
            st.error("Backtest failed")
    except Exception as e:
        st.warning(f"API not available: {e}")

st.markdown("---")
st.caption(f"TradePredict AI | {datetime.now().strftime('%Y-%m-%d %H:%M')}")