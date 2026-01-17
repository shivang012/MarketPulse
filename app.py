import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import http.client
import os
import urllib.parse
import json
from alpha_vantage.fundamentaldata import FundamentalData
from dotenv import load_dotenv
import google.generativeai as gen_ai
from PIL import Image
from datetime import date
from streamlit_option_menu import option_menu

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="MarketPulse", 
    page_icon="💸", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean CSS
st.markdown("""
<style>
    /* Clean white background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* All text black */
    h1, h2, h3, h4, h5, h6, p, span, div, li, label {
        color: #000000 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4CAF50;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ddd;
        color: #000000 !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        color: #000000 !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stChatMessage p {
        color: #000000 !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Simple logo display
st.image("logo.png", width=100)

# Initialize API keys
alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
marketaux_api_key = os.getenv('MARKETAUX_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
# Initialize watchlist in session state
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Function to get stock data
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        if not data.empty:
            return {
                'Last Price': data['Close'].iloc[-1],
                'Open': data['Open'].iloc[-1],
                'High': data['High'].iloc[-1],
                'Low': data['Low'].iloc[-1],
                'Volume': data['Volume'].iloc[-1]
            }
        return None
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

# Safety settings for Gemini
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Main navigation
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Stock Dashboard", "AI ChatBot", "Chart Analysis"],
        icons=["house", "graph-up", "chat", "image"],
        default_index=0,
        orientation="vertical",
    )
    
    st.markdown("---")
    if st.session_state.watchlist:
        st.info(f"📊 Tracking {len(st.session_state.watchlist)} stocks")
# Welcome Section
if selected == "Home":
    st.title("💸 Welcome to MarketPulse")
    st.markdown("#### Your simple and powerful market intelligence platform")
    st.markdown("---")
    
    # Main Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Stock Dashboard")
        st.write("""
        - Track multiple stocks
        - Real-time price data
        - Latest market news
        - Custom watchlists
        """)
        
    with col2:
        st.markdown("### 🤖 AI ChatBot")
        st.write("""
        - Ask market questions
        - Get instant answers
        - Investment insights
        - Strategy guidance
        """)
        
    with col3:
        st.markdown("### 📸 Chart Analysis")
        st.write("""
        - Upload chart images
        - AI-powered analysis
        - Pattern recognition
        - Technical indicators
        - Trend analysis
        - Chart interpretation
        - Market signals
        """)
        
    
    # Key Features
    st.markdown("### Platform Capabilities")
    
    tab1, tab2, tab3 = st.tabs(["Market Analysis", "AI Insights", "Technical Tools"])
    
    with tab1:
        st.markdown("""
        **Market Analysis Suite**
        - Real-time price monitoring
        - Custom watchlist management
        - Financial statement analysis
        - Key performance metrics
        - Market news integration
        """)
        
    with tab2:
        st.markdown("""
        **AI-Powered Insights**
        - Market sentiment analysis
        - Investment strategy validation
        - Risk assessment tools
        - Performance forecasting
        - Pattern recognition
        """)
        
    with tab3:
        st.markdown("""
        **Technical Analysis Tools**
        - Advanced chart analysis
        - Technical indicator suite
        - Pattern identification
        - Trend analysis
        - Visual market intelligence
        """)
    
    # How to use
    st.markdown("### 🚀 How to Get Started")
    st.info("""
    **Step 1:** Go to Stock Dashboard to add stocks to your watchlist
    
    **Step 2:** Use AI ChatBot to ask questions about markets and investments
    
    **Step 3:** Upload charts to Chart Analysis for technical insights
    """)
    
    st.markdown("---")
    st.caption("💡 Market data is for informational purposes. Always do your own research before investing.")

# Stock Dashboard Section
if selected == "Stock Dashboard":
    st.title('📈 Stock Dashboard')
    
    # Add stock to watchlist
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_stock = st.text_input("Enter stock symbol (e.g., AAPL, GOOGL)", key="stock_input")
    
    with col2:
        if st.button("Add to Watchlist"):
            if new_stock:
                if new_stock not in st.session_state.watchlist:
                    st.session_state.watchlist.append(new_stock.upper())
                    st.success(f"Added {new_stock.upper()} to watchlist!")
                else:
                    st.warning("Stock already in watchlist!")
    
    # Display watchlist
    if st.session_state.watchlist:
        st.subheader("Your Watchlist")
        
        # Create a container for the watchlist table
        watchlist_container = st.container()
        
        # Create columns for the table header
        cols = watchlist_container.columns([1, 1, 1, 1, 1, 1, 1])
        headers = ["Symbol", "Last Price", "Open", "High", "Low", "Volume", "Action"]
        
        for col, header in zip(cols, headers):
            col.markdown(f"**{header}**")
        
        # Display stock data
        for symbol in st.session_state.watchlist:
            stock_data = get_stock_data(symbol)
            
            if stock_data:
                change = stock_data['Last Price'] - stock_data['Open']
                change_pct = (change / stock_data['Open']) * 100 if stock_data['Open'] != 0 else 0
                
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    st.markdown(f"### {symbol}")
                    st.markdown(f"**${stock_data['Last Price']:.2f}**")
                
                with col2:
                    color = "🟢" if change >= 0 else "🔴"
                    st.write("")
                    st.write(f"{color} {change:+.2f} ({change_pct:+.2f}%)")
                
                with col3:
                    st.write(f"**Open:** ${stock_data['Open']:.2f}")
                    st.write(f"**High:** ${stock_data['High']:.2f}")
                    st.write(f"**Low:** ${stock_data['Low']:.2f}")
                
                with col4:
                    st.write("")
                    if st.button("Remove", key=f"remove_{symbol}"):
                        st.session_state.watchlist.remove(symbol)
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("📊 No stocks in your watchlist. Add some above to get started!")
    
    st.markdown("---")
    st.link_button("🔗 Full Dashboard", "https://stocks-dashboard-404.streamlit.app/", use_container_width=True)

    
# ChatBot Section
elif selected == "AI ChatBot":
    st.title("🤖 AI ChatBot")
    st.markdown("Ask me anything about stocks and markets")
    st.markdown("---")
    
    # Display chat history
    if "chat_session" in st.session_state and st.session_state.chat_session.history:
        for message in st.session_state.chat_session.history:
            role = "user" if message.role == "user" else "assistant"
            with st.chat_message(role):
                st.markdown(message.parts[0].text)
    
    # Chat input
    user_prompt = st.chat_input("Type your question here...")
    
    if user_prompt:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chat_session.send_message(user_prompt, safety_settings=safety_settings)
                st.markdown(response.text)

# VisionBot Section
elif selected == "Chart Analysis":
    st.title("📸 Chart Analysis")
    st.markdown("Upload charts for AI-powered technical analysis")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Upload a chart image", 
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload a stock chart or technical analysis image"
    )
    
    image_prompt = st.text_area(
        "What would you like to know about this chart?", 
        placeholder="E.g., Analyze this pattern, identify support levels, what's the trend...",
        height=100
    )

    if uploaded_file is not None:
        st.subheader("📊 Your Chart")
        st.image(Image.open(uploaded_file), use_column_width=True)

    st.markdown("---")
    
    if st.button("🔍 Analyze Chart", use_container_width=True):
        if uploaded_file is not None:
            if image_prompt:
                with st.spinner("🤖 Analyzing your chart..."):
                    model = gen_ai.GenerativeModel("gemini-1.5-flash")
                    image = Image.open(uploaded_file)
                    
                    response = model.generate_content(
                        [image_prompt, image],
                        safety_settings=safety_settings
                    )
                    
                    st.subheader("📝 Analysis Results")
                    st.write(response.text)
            else:
                st.error("❌ Please describe what you want to know about the chart")
        else:
            st.error("❌ Please upload a chart image first")
