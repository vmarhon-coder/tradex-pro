import streamlit as st
import yfinance as yf
import pandas as pd
import google.generativeai as genai

# 1. WEBSITE BRAND CONFIGURATION
st.set_page_config(page_title="TradeX Pro | AI Live Scanner", page_icon="⚡", layout="wide")

st.title("⚡ TRADEX PRO — PRESTIGE EDITION")
st.subheader("AI-Powered Real-Time Advanced Trading Terminal & Calculators")
st.write("---")

# --- GOOGLE GEMINI AI KEY SETUP ---
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(api_key=GEMINI_API_KEY)

# --- SYSTEM CONFIGURATION ---
MASTER_ACCESS_KEY = "PRO786"
WHATSAPP_NUMBER = "9199999XXXXX" # Yeh baad me badlenge
DHAN_LINK = "https://dhan.co"    # Yeh baad me badlenge
CHOICE_LINK = "https://choiceconnect.in" # Yeh baad me badlenge

# --- SIDEBAR: ACCESS LOCK ---
st.sidebar.header("🔐 Unlock TradeX Pro")
user_input_key = st.sidebar.text_input("Enter Premium Access Key:", type="password")

is_premium_user = user_input_key == MASTER_ACCESS_KEY

# --- MAIN TABS: YAHA CALCULATOR SABKE LIYE FREE RAHEGA ---
main_tab1, main_tab2 = st.tabs(["📊 Live Profit & Tax Calculator (FREE)", "👑 AI Premium Dashboard (🔒)"])

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
    
    # Taxes Slabs
    stt_rate = 0.00125 if trade_type == "Options" else 0.000125
    stt = (sell_price * lot_size) * stt_rate if trade_type == "Options" else total_turnover * stt_rate
    
    exchange_charges = total_turnover * 0.00053 
    total_brokerage = brokerage_per_order * 2
    gst = (total_brokerage + exchange_charges) * 0.18
    sebi_stamp_charges = total_turnover * 0.0001
    
    total_taxes_and_charges = total_brokerage + stt + exchange_charges + gst + sebi_stamp_charges
    net_profit = gross_profit - total_taxes_and_charges

    # UI Display
    st.write("### 💵 Trade Summary Report")
    res_col1, res_col2, res_col3 = st.columns(3)
    
    res_col1.metric("Gross Profit/Loss (₹)", f"₹{round(gross_profit, 2)}", delta=f"₹{round(gross_profit, 2)}")
    res_col2.metric("Total Government Taxes + Brokerage (₹)", f"₹{round(total_taxes_and_charges, 2)}", delta_color="inverse")
    
    if net_profit >= 0:
        res_col3.metric("Net In-Hand Profit (₹)", f"₹{round(net_profit, 2)}", delta=f"₹{round(net_profit, 2)}")
    else:
        res_col3.metric("Net In-Hand Loss (₹)", f"₹{round(net_profit, 2)}", delta=f"₹{round(net_profit, 2)}", delta_color="inverse")

    st.write("---")
    st.markdown(f"💡 **Brokerage Alert:** Aapka yeh standard ₹40 brokerage tabhi bachega jab aap hamare partner benefit program ke tahat trade karenge. [👉 Dhan Par Free Account Kholein]({DHAN_LINK}) | [👉 Choice Connect Par Free Account Kholein]({CHOICE_LINK})")

# ==================== TAB 2: PREMIUM DASHBOARD ====================
with main_tab2:
    if not is_premium_user:
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
    else:
        st.success("🎯 Welcome to TradeX Pro Premium Dashboard!")
        tickers = ["^NSEI", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS"]
        scan_results = []
        for t in tickers:
            try:
                d = yf.download(t, period="5d", interval="15m")
                if d.empty: continue
                close_p = d['Close'].iloc[-1]
                vol_burst = d['Volume'].iloc[-1] > (d['Volume'].mean() * 2)
                signal = "🚀 STRONG BUY" if (vol_burst and close_p > d['High'].iloc[-5:-1].max()) else "⏳ Consolidation"
                t_name = "NIFTY 50" if t == "^NSEI" else t.replace(".NS", "")
                scan_results.append({"Asset": t_name, "Live Price (₹)": round(close_p, 2), "Volume Shock": "Active" if vol_burst else "Normal", "Signal": signal})
            except: pass
        st.dataframe(pd.DataFrame(scan_results), use_container_width=True)
  
