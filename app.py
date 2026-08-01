import streamlit as st
import yfinance as yf
import pandas as pd
import google.generativeai as genai

# 1. WEBSITE BRAND CONFIGURATION
st.set_page_config(page_title="TradeX Pro | Rakesh Jhunjhunwala AI Screener", page_icon="⚡", layout="wide")

st.title("⚡ TRADEX PRO — PRESTIGE EDITION")
st.subheader("Rakesh Jhunjhunwala AI Stock Screener & Global Market Terminal")
st.write("---")

# --- GOOGLE GEMINI AI KEY SETUP ---
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(api_key=GEMINI_API_KEY)

# --- SYSTEM CONFIGURATION ---
MASTER_ACCESS_KEY = "PRO786"
WHATSAPP_NUMBER = "9199999XXXXX"
DHAN_LINK = "https://dhan.co"
CHOICE_LINK = "https://choiceconnect.in"

# --- SIDEBAR: ACCESS LOCK ---
st.sidebar.header("🔐 Unlock TradeX Pro")
user_input_key = st.sidebar.text_input("Enter Premium Access Key:", type="password")

is_premium_user = user_input_key == MASTER_ACCESS_KEY

# --- MAIN TABS ---
main_tab1, main_tab2, main_tab3 = st.tabs([
    "🧮 Live Profit & Tax Calculator (FREE)", 
    "👑 Rakesh Jhunjhunwala AI Stock Screener (🔒)",
    "🌍 Global Markets & India VIX (🔒)"
])

# ==================== TAB 1: FREE CALCULATOR ====================
with main_tab1:
    st.header("🧮 F&O Trade Profit & Net Payout Calculator")
    st.caption("Calculate your exact profit after Dhan/Choice brokerage and Government taxes.")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        buy_price = st.number_input("Buying Price (₹):", min_value=1.0, value=100.0, step=0.05)
        sell_price = st.number_input("Selling Price (₹):", min_value=1.0, value=110.0, step=0.05)
    with col_c2:
        lot_size = st.number_input("Lot Size / Quantity:", min_value=1, value=25, step=1)
        brokerage_per_order = 20.0
    with col_c3:
        trade_type = st.selectbox("Select Segment:", ["Options", "Futures"])

    # Calculations
    gross_profit = (sell_price - buy_price) * lot_size
    total_turnover = (buy_price + sell_price) * lot_size
    
    stt_rate = 0.00125 if trade_type == "Options" else 0.000125
    stt = (sell_price * lot_size) * stt_rate if trade_type == "Options" else total_turnover * stt_rate
    
    exchange_charges = total_turnover * 0.00053 
    total_brokerage = brokerage_per_order * 2
    gst = (total_brokerage + exchange_charges) * 0.18
    sebi_stamp_charges = total_turnover * 0.0001
    
    total_taxes_and_charges = total_brokerage + stt + exchange_charges + gst + sebi_stamp_charges
    net_profit = gross_profit - total_taxes_and_charges

    st.write("### 💵 Trade Summary Report")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Gross Profit/Loss (₹)", f"₹{round(gross_profit, 2)}")
    res_col2.metric("Total Taxes + Brokerage (₹)", f"₹{round(total_taxes_and_charges, 2)}")
    res_col3.metric("Net In-Hand Profit (₹)", f"₹{round(net_profit, 2)}", delta=f"₹{round(net_profit, 2)}" if net_profit >= 0 else f"₹{round(net_profit, 2)}")

# ==================== LOCK SCREEN FUNCTION ====================
def show_lock_screen():
    st.warning("🔒 TradeX Pro ke Live 85%+ Accuracy AI Signals aur Scanners abhi LOCKED hain!")
    st.markdown(f"""
    ### 🚀 100% FREE Access Model (Manual Verification)
    1. **Step 1:** Niche diye gaye link se **Dhan ya Choice** par Free Account open karein.
    2. **Step 2:** Kam se kam **1 F&O Trade** complete karein.
    3. **Step 3:** Trade ka screenshot aur apni Client ID niche diye WhatsApp button par bhejein.
    4. **Step 4:** Verfiy hote hi hum aapko **Secret Access Key** de denge!
    """)
    col1, col2 = st.columns(2)
    with col1: st.link_button("🟢 OPEN FREE ACCOUNT ON DHAN", DHAN_LINK)
    with col2: st.link_button("🔵 OPEN FREE ACCOUNT ON CHOICE", CHOICE_LINK)
    whatsapp_url = f"https://wa.me{WHATSAPP_NUMBER}?text=Hi%20Raj%20Sir,%20Maine%20TradeX%20Pro%20ke%20liye%20account%20open%20karke%20trade%20kar%20liya%20hai."
    st.link_button("💬 CLICK HERE TO SEND SCREENSHOT ON WHATSAPP", whatsapp_url)

# ==================== TAB 2: RJ AI SCREENER ====================
with main_tab2:
    if not is_premium_user:
        show_lock_screen()
    else:
        st.header("👑 Rakesh Jhunjhunwala AI Stock Screener")
        st.caption("Deep Single-Stock Analysis Powered by Advanced AI Rules for Swing Trading")
        
        # User input for custom stock scanning
        stock_input = st.text_input("Enter Stock Ticker (e.g., SBIN, RELIANCE, TCS, INFY):", value="SBIN").upper().strip()
        
        if stock_input:
            ticker_ns = f"{stock_input}.NS"
            with st.spinner(f"{stock_input} ka data analyze ho raha hai..."):
                try:
                    stock_data = yf.download(ticker_ns, period="30d", interval="1d")
                    if not stock_data.empty:
                        last_price = stock_data['Close'].iloc[-1]
                        prev_price = stock_data['Close'].iloc[-2]
                        pct_chg = ((last_price - prev_price) / prev_price) * 100
                        
                        avg_vol = stock_data['Volume'].iloc[-11:-1].mean()
                        cur_vol = stock_data['Volume'].iloc[-1]
                        vol_ratio = cur_vol / avg_vol
                        
                        # Display Basic Stock Stats
                        s_col1, s_col2, s_col3 = st.columns(3)
                        s_col1.metric("Current Price (₹)", f"₹{round(float(last_price), 2)}")
                        s_col2.metric("Day Change (%)", f"{round(float(pct_chg), 2)}%")
                        s_col3.metric("Volume Activity", f"{round(float(vol_ratio), 1)}x Average")
                        
                        st.write("#### 🤖 Rakesh Jhunjhunwala Style AI Analysis Report")
                        
                        # Generate Prompt for Gemini
                        ai_prompt = f"""
                        You are the 'Rakesh Jhunjhunwala AI Stock Screener'. Analyze this stock: {stock_input}. 
                        Current Price is {round(float(last_price), 2)}, Day Change is {round(float(pct_chg), 2)}%, Volume is {round(float(vol_ratio), 1)}x of its 10-day average.
                        Provide a detailed Swing Trading report in Hindi language using English trading terms.
                        Include clearly:
                        1. BUY KAB KAREIN (Exact entry scenario and support levels)
                        2. KAB BUY NA KAREIN (Risks, resistance levels, or false breakout warning)
                        3. Swing Trading Target & StopLoss logic to earn profit in 2-3 days.
                        Keep the tone authoritative, bold, and smart like Big Bull Rakesh Jhunjhunwala.
                        """
                        
                        try:
                            model = genai.GenerativeModel('gemini-pro')
                            response = model.generate_content(ai_prompt)
                            st.info(response.text)
                        except:
                            # Fallback text if API Key is empty
                            st.warning("⚠️ Live AI Insights Pending (API Key Setup Required). Base Rules Report Below:")
                            if vol_ratio > 1.5 and pct_chg > 0:
                                st.success(f"📈 **Verdict:** Bullish Accumulation Sign! **Buy Kab Karein:** Enter if price holds above pichle swing high with high volume. **Kab Buy Na Karein:** Avoid if it opens with a big gap-up near resistance.")
                            else:
                                st.error(f"📉 **Verdict:** Consolidation/Weakness! **Buy Kab Karein:** Wait for a firm base near 20 EMA support. **Kab Buy Na Karein:** Immediate buying is risky as momentum is sideways.")
                    else:
                        st.error("Invalid Ticker! Please enter correct NSE symbol (e.g. RELIANCE, SBIN).")
                except:
                    st.error("Data fetch error. Please try again.")

# ==================== TAB 3: GLOBAL MARKETS ====================
with main_tab3:
    if not is_premium_user:
        show_lock_screen()
    else:
        st.header("🌍 Global Terminal & Market Volatility Pulse")
        st.caption("Track World Indices, India VIX, and Gift Nifty in real-time.")
        
        # Core Global Tickers
        global_tickers = {
            "GIFT Nifty (NSE IX)": "FNIFTY=F",
            "India VIX (Volatility Index)": "^INDIAVIX",
            "US S&P 500": "^GSPC",
            "US Nasdaq 100": "^IXIC",
            "Japan Nikkei 225": "^N225",
            "UK FTSE 100": "^FTSE"
        }
        
        g_results = []
        with st.spinner("Fetching global market matrix..."):
            for name, tick in global_tickers.items():
                try:
                    g_data = yf.download(tick, period="2d", interval="15m")
                    if g_data.empty:
                        g_data = yf.download(tick, period="5d", interval="1d")
                    
                    c_val = g_data['Close'].iloc[-1]
                    p_val = g_data['Close'].iloc[-2]
                    chg = ((c_val - p_val) / p_val) * 100
                    
                    g_results.append({
                        "Market Index": name,
                        "Last Traded Value": round(float(c_val), 2),
                        "Net Change (%)": round(float(chg), 2)
                    })
                except:
                    g_results.append({"Market Index": name, "Last Traded Value": "Data Delayed", "Net Change (%)": 0.0})
                    
        df_global = pd.DataFrame(g_results)
        
        # Metrics Display for India Health
        col_m1, col_m2 = st.columns(2)
        vix_val = df_global[df_global["Market Index"] == "India VIX (Volatility Index)"]["Last Traded Value"].values[0]
        gift_val = df_global[df_global["Market Index"] == "GIFT Nifty (NSE IX)"]["Last Traded Value"].values[0]

      
