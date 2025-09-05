import streamlit as st
import requests
import pandas as pd

# ---- CONFIG ----
CMC_API_KEY = "142f0bad-d682-4cc0-ac74-a0cfc7ea4c55"  # Replace with your CoinMarketCap API key

def fetch_price(symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": symbol.upper()}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        price = data['data'][symbol.upper()]['quote']['USD']['price']
        return price
    except Exception as e:
        st.error(f"Error fetching price: {e}")
        return None

def calculate_initial_margin(contract_size, leverage):
    try: return float(contract_size) / float(leverage)
    except: return None

def calculate_maintenance_margin(contract_size, maintenance_margin_pct):
    try: return float(contract_size) * (float(maintenance_margin_pct) / 100)
    except: return None

def calculate_liquidation_price(entry_price, leverage, maintenance_margin_pct, side='long'):
    try:
        entry_price, leverage, mm = float(entry_price), float(leverage), float(maintenance_margin_pct)/100
        if side == 'long':
            return entry_price * (1 - (1 / leverage) + mm)
        else:
            return entry_price * (1 + (1 / leverage) - mm)
    except: return None

def calculate_pnl(entry_price, exit_price, contract_size, side='long'):
    try:
        entry_price, exit_price, contract_size = float(entry_price), float(exit_price), float(contract_size)
        if side == 'long':
            return (exit_price - entry_price) * contract_size
        else:
            return (entry_price - exit_price) * contract_size
    except: return None

# ---- UI ----
st.title("Crypto Futures Margin Calculator")
st.write("🔗 **Live calculator for margin, liquidation level, and risk!** \nPowered by CoinMarketCap API.")

symbol = st.text_input("Crypto Symbol (e.g., BTC, ETH, SOL)", value="BTC")
entry_price = st.number_input("Entry Price (leave 0 & fetch live)", min_value=0.0, value=0.0)
contract_size = st.number_input("Contract Size (USD or Coin Units)", min_value=0.0, value=100.0)
leverage = st.selectbox("Leverage", [1, 3, 5, 10, 20, 50, 100], index=3)
maintenance_margin_pct = st.number_input("Maintenance Margin %", min_value=0.1, value=0.5)
account_balance = st.number_input("Account Balance (optional)", min_value=0.0, value=0.0)
side = st.radio("Position Side", ["long", "short"], index=0)
exit_price = st.number_input("Exit Price (for P&L)", min_value=0.0, value=0.0, help="Enter to compute hypothetical PNL")

if st.button("Fetch Latest Price"):
    live_price = fetch_price(symbol)
    if live_price:
        st.success(f"Current {symbol.upper()} Price: ${live_price:.2f}")
        entry_price = live_price

# Only display output table if inputs are sufficient
if entry_price > 0.0 and contract_size > 0.0 and leverage > 0:
    ini_margin = calculate_initial_margin(contract_size, leverage)
    maint_margin = calculate_maintenance_margin(contract_size, maintenance_margin_pct)
    liq_price = calculate_liquidation_price(entry_price, leverage, maintenance_margin_pct, side)
    result = {
        "Initial Margin Required": [ini_margin],
        "Maintenance Margin": [maint_margin],
        "Est. Liquidation Price": [liq_price]
    }
    if exit_price > 0:
        pnl = calculate_pnl(entry_price, exit_price, contract_size, side)
        result["PNL (at Exit Price)"] = [pnl]
    df = pd.DataFrame(result)
    st.dataframe(df)

st.caption("Made for students and traders. Double-check before executing live orders.")
