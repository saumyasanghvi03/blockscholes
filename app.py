# --- Margin/P&L area (unchanged) ---
if entry_price > 0.0 and contract_size > 0.0 and leverage > 0:
    ini_margin = calculate_initial_margin(contract_size, leverage)
    maint_margin = calculate_maintenance_margin(contract_size, maintenance_margin_pct)
    liq_price = calculate_liquidation_price(entry_price, leverage, maintenance_margin_pct, side)
    pnl = None
    if exit_price > 0:
        pnl = calculate_pnl(entry_price, exit_price, contract_size, side)
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

# --- Greeks Calculator is LAST and outputs are right below its input section ---
st.markdown("---")
with st.expander("Option Greeks Calculator (Black-Scholes)", expanded=True):
    st.markdown("<h3 style='color:#e9f28d;'>Option Greeks Calculator (Black-Scholes)</h3>", unsafe_allow_html=True)
    override_spot = st.checkbox("Override Spot Price (S) manually", value=False)
    if override_spot:
        S = st.number_input("Custom Spot Price (S)", min_value=0.0, value=float(st.session_state.live_price if st.session_state.live_price > 0 else 50000.0), key="override_spot")
    else:
        S = float(st.session_state.live_price if st.session_state.live_price > 0 else 50000.0)
        st.markdown(f"Using Live Spot Price (S): **{S:,.2f}**", unsafe_allow_html=True)
    K = st.number_input("Strike Price (K)", min_value=0.0, value=50000.0, key="greek_k")
    T = st.number_input("Time to Expiry (years, e.g. 0.25)", min_value=0.001, value=0.25, key="greek_t")
    r = st.number_input("Risk-Free Rate (annual, decimal, e.g. 0.06)", min_value=0.0, value=0.06, key="greek_r")
    sigma = st.number_input("Volatility (annual, decimal, e.g. 0.80)", min_value=0.01, value=0.80, key="greek_sigma")
    option_type = st.selectbox("Option Type", ["call", "put"], index=0, key="greek_type")

    st.markdown("----")
    if S > 0 and K > 0 and T > 0 and sigma > 0:
        greeks = blackscholes_greeks(S, K, T, r, sigma, option_type)
        gcol1, gcol2, gcol3 = st.columns(3)
        gcol1.metric("Delta", f"{greeks['Delta']:.4f}")
        gcol1.metric("Gamma", f"{greeks['Gamma']:.4f}")
        gcol2.metric("Vega (per 1%)", f"{greeks['Vega']:.4f}")
        gcol2.metric("Theta (per day)", f"{greeks['Theta']:.4f}")
        gcol3.metric("Rho", f"{greeks['Rho']:.4f}")

        gdf = pd.DataFrame({"Greek": list(greeks.keys()), "Value": list(greeks.values())})
        st.markdown("<h4 style='margin-top:20px;color:#fecb2f'>Greeks Table</h4>", unsafe_allow_html=True)
        st.dataframe(gdf)
    else:
        st.info("Waiting for valid input parameters...")

    if override_spot:
        st.caption("Currently using manually overridden spot price for all calculations.", unsafe_allow_html=True)
    else:
        st.caption("Currently using latest live-fetched spot price for all calculations.", unsafe_allow_html=True)
