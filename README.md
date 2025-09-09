# 🧮 BlockScholes – Crypto Futures Margin Calculator

A **Streamlit application** for quick, reliable crypto futures margin, liquidation, and P&L calculations with live crypto pricing.

---

## 🚀 Features

- **Live Crypto Prices:** Fetches the latest prices from CoinMarketCap for symbols like BTC, ETH, SOL, etc.
- **Comprehensive Futures Calculations:**
  - Initial Margin
  - Maintenance Margin
  - Liquidation Price (long & short)
  - P&L at exit price
- **Modern UI:**  
  - Dark mode  
  - Highlighted results in summary blocks  
  - Clear parameter entry and error handling
- **Instant Summary Table:**  
  Green/red visual cues for quick reading.
- **Built-in Educational Notice:**  
  Reminds users to double-check values before trading.

---

## ⚙️ Getting Started

**1. Clone the Repository**

```bash
git clone https://github.com/saumyasanghvi03/blockscholes.git
cd blockscholes
```

**2. Install Dependencies**

```bash
pip install streamlit pandas requests
```

**3. Add Your CoinMarketCap API Key**

Edit `app.py` and set:

```python
CMC_API_KEY = "YOUR_CMC_API_KEY"
```

**4. Launch the App**

```bash
streamlit run app.py
```

Then, open [http://localhost:8501](http://localhost:8501/) in your browser.

---

## 📝 Parameters & Usage

| Parameter           | Description                                   | Example    |
|---------------------|-----------------------------------------------|------------|
| Crypto Symbol       | Ticker (case-insensitive)                     | BTC, ETH   |
| Contract Size       | Value in USD or number of coins                | 1000       |
| Leverage            | Select leverage                                | 10         |
| Maintenance Margin  | Enter exchange's maintenance margin (%)        | 0.5        |
| Account Balance     | (Optional) Wallet size in USD                  | 2000       |
| Entry / Exit Price  | Set manual or leave entry at 0 for live price  | 30000      |
| Side                | `long` or `short`                             | long       |

---

## 📊 Outputs

- **Initial Margin:** Required to open position
- **Maintenance Margin:** Minimum to avoid liquidation
- **Liquidation Price:** Trigger for forced closure (long/short)
- **P&L:** Projected profit/loss at exit price

---

## 🧪 Example Calculation

| Input           | Value   |
|-----------------|---------|  
| Crypto Symbol   | BTC     |
| Contract Size   | 1000    |
| Leverage        | 10      |
| Maintenance %   | 0.5     |
| Entry Price     | 30000   |
| Side            | long    |

**Sample Output:**

- Initial Margin: `$100.00`
- Maintenance Margin: `$5.00`
- Liquidation Price: `$27,200.00`
- P&L (at exit): _(depends on exit price)_

---

## 🎨 Customization

Modify UI styles and colors in the markdown/CSS portion of `app.py` for a tailored look.

---

## ⚠️ Disclaimer

_For educational use only. Always verify calculations with your trading platform before making any real trades._

---

**Author:** Saumya Sanghvi  
**License:** MIT  
**Feedback:** File an issue or PR on this repo.

---
