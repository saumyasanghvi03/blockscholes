import streamlit as st
import requests
import pandas as pd

# ---- CONFIG ----
CMC_API_KEY = "142f0bad-d682-4cc0-ac74-a0cfc7ea4c55"  # Replace with your actual CoinMarketCap API key

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

# ---- Custom Styling ----
st.markdown("""
<style>
body, .main, .block-container  {background: #0a0c14 !important;}
[data-testid="stAppViewContainer"] { background-color: #14171c;}
[data-testid="stSidebarContent"] { background: #181d27;}
h1, h2, h3, .stTextInput>div>div>input, label { color: #fbfbfb !important; }
.st-bw { color: #fbfbfb; }
thead th {background: #223322 !important;}
.css-ffhzg2 { color: #fbfbfb !important;}

.metric-green {background: #243923; color: #00ff84; border-radius: 8px; padding: 8px 14px; margin: 3px;}
.metric-red {background: #401818; color: #ff4747; border-radius: 8px; padding: 8px 14px; margin: 3px;}
.metric-neutral {background: #23272c; color: #e3e3e3; border-radius: 8px; padding: 8px 14px; margin: 3px;}
</style>
""", unsafe_allow_html=True)

# ---- UI ----
st.markdown("<h1 style='color:#00ff84;'>🧮 Crypto Futures Margin Calculator</h1>", unsafe_allow_html=True)
st.markdown(
    """<p style='color:#b2ffb2'>Live margin, liquidation, and risk calculator
    <span style='color:#00fff7'>powered by CoinMarketCap API</span>.</p>""",
    unsafe_allow_html=True
)

col1, col2 = st.columns([2, 1])
with col1:
    symbol = st.text_input("Crypto Symbol (e.g., BTC, ETH, SOL)", value="BTC")
    contract_size = st.number_input("Contract Size (USD or Coin Units)", min_value=0.0, value=100.0)
    leverage = st.selectbox("Leverage", [1, 3, 5, 10, 20, 50, 100], index=3)
    maintenance_margin_pct = st.number_input("Maintenance Margin %", min_value=0.1, value=0.5)
    account_balance = st.number_input("Account Balance (optional)", min_value=0.0, value=0.0)
with col2:
    entry_price = st.number_input("Entry Price (leave 0 & fetch live)", min_value=0.0, value=0.0)
    exit_price = st.number_input("Exit Price (for P&L)", min_value=0.0, value=0.0)
    side = st.radio("Position Side", ["long", "short"], horizontal=True)
    fetch_btn = st.button("🔄 Fetch Latest Price")

if fetch_btn:
    live_price = fetch_price(symbol)
    if live_price:
        st.markdown(
            f"<div class='metric-green'>Live {symbol.upper()} Price: <b>${live_price:,.2f}</b></div>",
            unsafe_allow_html=True,
        )
        entry_price = live_price

if entry_price > 0.0 and contract_size > 0.0 and leverage > 0:
    ini_margin = calculate_initial_margin(contract_size, leverage)
    maint_margin = calculate_maintenance_margin(contract_size, maintenance_margin_pct)
    liq_price = calculate_liquidation_price(entry_price, leverage, maintenance_margin_pct, side)
    pnl = None
    if exit_price > 0:
        pnl = calculate_pnl(entry_price, exit_price, contract_size, side)

    # --- Result Metrics ---
    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f"<div class='metric-green'><b>Initial Margin</b><br>${ini_margin:,.4f}</div>",
        unsafe_allow_html=True)
    c2.markdown(
        f"<div class='metric-red'><b>Maintenance Margin</b><br>${maint_margin:,.4f}</div>",
        unsafe_allow_html=True)
    c3.markdown(
        f"<div class='metric-red'><b>Liquidation Price</b><br>${liq_price:,.4f}</div>",
        unsafe_allow_html=True)
    if pnl is not None:
        pnl_col = 'metric-green' if pnl > 0 else 'metric-red'
        st.markdown(
            f"<div class='{pnl_col}'><b>P&L (at Exit Price)</b> <br>${pnl:,.4f}</div>",
            unsafe_allow_html=True)

    # --- Table Summary with Color Highlights ---
    df = pd.DataFrame({
        "Metric": ["Initial Margin", "Maintenance Margin", "Est. Liquidation Price", "PNL (at Exit Price)" if pnl is not None else ""],
        "Value": [ini_margin, maint_margin, liq_price, pnl if pnl is not None else ""]
    })

    def color_table(val):
        if isinstance(val, (float, int)):
            if val < 0:
                return 'color: #ff4747'
            elif val > 0:
                return 'color: #00ff84'
        return 'color: #b2ffb2'

    st.markdown("<h4 style='margin-top:30px;color:#fecb2f'>Summary Table</h4>", unsafe_allow_html=True)
    st.dataframe(df.style.applymap(color_table, subset=['Value']))

st.caption("<b style='color:#888888'>For educational use. Double-check before trading!</b>", unsafe_allow_html=True)
