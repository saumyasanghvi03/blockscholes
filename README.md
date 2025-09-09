# blockscholes

🧮 BlockScholes – Crypto Futures Margin Calculator
A Streamlit application that helps you compute the required margin, liquidation price, and P&L for any crypto futures contract. It features live crypto price fetching via CoinMarketCap API and displays results with a finance-friendly UI!

Features
Live Price Fetching: Get the latest price for any crypto symbol (BTC, ETH, SOL, etc.) using CoinMarketCap.

Futures Calculations:

Initial Margin

Maintenance Margin

Liquidation Price (for both long and short positions)

P&L at exit price

Custom Styling: Stylish dark mode, highlighted result blocks, and user-friendly interface.

Summary Table: Quick overview of results with green/red color cues.

Educational Notice: Built-in reminders to cross-verify calculations before trading.

How to Run
Clone the Repository

bash
git clone https://github.com/saumyasanghvi03/blockscholes.git
cd blockscholes
Install Dependencies

bash
pip install streamlit pandas requests
Configure API Key

Replace the provided placeholder API key in app.py:

python
CMC_API_KEY = "YOUR_CMC_API_KEY"
Start the Streamlit App

bash
streamlit run app.py
Open in Browser

Go to http://localhost:8501 to use the app.

Parameters & Usage
Crypto Symbol: e.g. BTC, ETH, SOL (case-insensitive)

Contract Size: USD value or coin units of your contract

Leverage: Select from 1x, 3x, 5x, 10x, 20x, 50x, 100x

Maintenance Margin %: Enter the exchange's maintenance margin value

Account Balance (optional): Your wallet balance for information only

Entry/Exit Price: Leave entry price at 0 to fetch live, or set manually; provide exit price for P&L

Side: "long" or "short" position

Calculated Outputs
Initial Margin: Funds needed to open your position

Maintenance Margin: Minimum required to avoid liquidation

Liquidation Price: Estimated trigger for forced closure

P&L: Projected profit or loss at exit price

Example
Input	Value
Crypto Symbol	BTC
Contract Size	1000
Leverage	10
Maintenance %	0.5
Entry Price	30000
Side	long
Output:

Initial Margin: $100.0000

Maintenance Margin: $5.0000

Liquidation Price: $27,200.0000

P&L (at exit): (based on exit price)

Customization
Update UI styles and color themes in the markdown CSS section of app.py.

Disclaimer
For educational use only. Double-check all calculations with your broker/platform before live trading!

Author: Saumya Sanghvi
License: MIT
Feedback: Create an issue or pull request on the repo.
