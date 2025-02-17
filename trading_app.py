from flask import Flask, jsonify, request
import requests
import json
import os
import sqlite3
import bcrypt
import time
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Load API keys securely from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
AI_TRADE_API_URL = os.getenv("AI_TRADE_API_URL")
SENTIMENT_API_URL = os.getenv("SENTIMENT_API_URL")
PORTFOLIO_ANALYTICS_API = os.getenv("PORTFOLIO_ANALYTICS_API")

# Secure Database Setup
conn = sqlite3.connect("neurotrade.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS paper_trading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    stock_symbol TEXT,
    quantity INTEGER,
    purchase_price REAL,
    FOREIGN KEY (username) REFERENCES users(username)
)
""")
conn.commit()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to NeuroTrade API"})

@app.route('/candlestick/<symbol>', methods=['GET'])
def view_chart(symbol):
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}")
    data = response.json()
    if "Time Series (Daily)" in data:
        dates = list(data["Time Series (Daily)"].keys())[:30]
        prices = [float(data["Time Series (Daily)"][date]["4. close"]) for date in dates]
        dates.reverse()
        prices.reverse()
        fig, ax = plt.subplots()
        ax.plot(dates, prices, label=f"{symbol} Closing Prices")
        ax.set_title("Candlestick Chart")
        ax.legend()
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode('utf8')
        return jsonify({"chart": chart_url})
    else:
        return jsonify({"error": "Failed to fetch chart data"}), 400

@app.route('/paper_trade', methods=['POST'])
def start_paper_trading():
    data = request.json
    username = data.get("username")
    stock_symbol = data.get("stock_symbol")
    quantity = data.get("quantity")
    purchase_price = data.get("purchase_price")
    cursor.execute("INSERT INTO paper_trading (username, stock_symbol, quantity, purchase_price) VALUES (?, ?, ?, ?)",
                   (username, stock_symbol, quantity, purchase_price))
    conn.commit()
    return jsonify({"message": "Started trading with virtual money!"})

@app.route('/sentiment', methods=['GET'])
def get_sentiment_analysis():
    response = requests.get(SENTIMENT_API_URL)
    if response.status_code == 200:
        sentiment_data = response.json()
        return jsonify(sentiment_data)
    else:
        return jsonify({"error": "Failed to fetch sentiment analysis"}), 400

@app.route('/portfolio_analytics', methods=['GET'])
def get_portfolio_analytics():
    response = requests.get(PORTFOLIO_ANALYTICS_API)
    if response.status_code == 200:
        analytics_data = response.json()
        return jsonify(analytics_data)
    else:
        return jsonify({"error": "Failed to fetch portfolio analytics"}), 400

if __name__ == "__main__":
    app.run(debug=True)
