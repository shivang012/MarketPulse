# MarketPulse 💸

A simple and powerful market intelligence platform built with Streamlit. Track stocks in real-time, chat with AI about market insights, and analyze charts with AI-powered technical analysis.

![MarketPulse](logo.png)

## What is MarketPulse?

MarketPulse is a web application that helps you monitor stock markets and get AI-powered insights. It combines three powerful features:

- **Stock Dashboard**: Track your favorite stocks with real-time price data
- **AI ChatBot**: Ask questions about stocks, markets, and investment strategies
- **Chart Analysis**: Upload chart images and get AI-powered technical analysis

## Features

### 📊 Stock Dashboard
- Track multiple stocks in real-time
- View current prices, highs, lows, and volume
- Create a custom watchlist
- Simple add/remove functionality

### 🤖 AI ChatBot
- Ask questions about any stock or market
- Get instant AI-powered answers
- Validate investment strategies
- Understand market trends

### 📸 Chart Analysis
- Upload stock chart images
- Get AI-powered technical analysis
- Identify patterns and trends
- Understand support and resistance levels

## How to Run

### Prerequisites

- Python 3.8 or higher
- API Keys (optional but recommended):
  - Google AI API key (for AI features)
  - Alpha Vantage API key (for additional data)
  - Marketaux API key (for news)

### Installation Steps

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/MarketPulse-main.git
   cd MarketPulse-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys (optional)**
   
   Create a `.env` file in the project folder and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
   MARKETAUX_API_KEY=your_marketaux_key_here
   ```
   
   Note: The stock dashboard will work without API keys, but AI features require a Google API key.

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   
   The app will automatically open at `http://localhost:8501`

## How to Use

### Stock Dashboard
1. Click "Stock Dashboard" in the sidebar
2. Enter a stock symbol (e.g., AAPL, TSLA, GOOGL)
3. Click "Add Stock" to add it to your watchlist
4. View real-time price data and changes
5. Click "Remove" to remove stocks from your watchlist

### AI ChatBot
1. Click "AI ChatBot" in the sidebar
2. Type your question in the chat box
3. Press Enter to get AI-powered answers
4. Ask about stocks, market trends, investment strategies, etc.

### Chart Analysis
1. Click "Chart Analysis" in the sidebar
2. Upload a stock chart image (PNG, JPG, etc.)
3. Describe what you want to know about the chart
4. Click "Analyze Chart" to get AI insights

## Get API Keys

- **Google AI**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get a free API key
- **Alpha Vantage**: Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key) for a free API key
- **Marketaux**: Visit [Marketaux](https://www.marketaux.com/) to get an API key

## Technologies Used

- Streamlit - Web framework
- yfinance - Stock market data
- Google Gemini AI - AI-powered chat and image analysis
- Python - Programming language

## Troubleshooting

**App won't start?**
- Make sure Python 3.8+ is installed
- Install all dependencies: `pip install -r requirements.txt`

**Can't see stock data?**
- Check your internet connection
- Try a different stock symbol
- Stock markets may be closed (check trading hours)

**AI features not working?**
- Make sure you have a Google API key in your `.env` file
- Check that your API key is valid

## License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Created with ❤️ by [Shivang]



## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the Help Center in the application

### Planned Features
- [ ] Portfolio tracking and performance analytics
- [ ] Advanced technical indicators
- [ ] Automated trading signals
- [ ] Multi-language support
- [ ] Mobile responsive design
- [ ] Export reports functionality
- [ ] Historical data analysis
- [ ] Comparison tools for multiple stocks

---

**Note**: Remember to keep your API keys secure and never commit them to version control. Always use environment variables for sensitive information.
