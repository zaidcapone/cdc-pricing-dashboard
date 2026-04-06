# ============================================
# MULTI-CLIENT PRICING DASHBOARD - PROFESSIONAL EDITION
# ============================================
# Author: Zaid F. Al-Shami
# Version: 5.0 (Professional UI Redesign)
# Last Updated: 05 April 2026
# ============================================

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO
import re

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Multi-Client Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CSS
# ============================================
st.markdown("""
<style>
    /* ===== GLOBAL STYLES ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        padding: 0rem 1rem;
    }
    
    /* Modern Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* ===== HEADER STYLES ===== */
    .dashboard-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .dashboard-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: white;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .dashboard-subtitle {
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    /* ===== CARD STYLES ===== */
    .modern-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .modern-card:hover {
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.25rem;
        color: white;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .subsection-header {
        font-size: 1rem;
        font-weight: 600;
        color: #475569;
        margin: 1rem 0 0.75rem 0;
    }
    
    /* ===== PRICE CARDS ===== */
    .price-card-primary {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid #dc2626;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .price-card-secondary {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .price-card-info {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .price-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    /* ===== FIX FOR CLIENT'S ORDERS TEXT COLOR ===== */
    .price-card-primary,
    .price-card-secondary,
    .price-card-info {
        color: #1e293b !important;
    }
    
    .price-card-primary div,
    .price-card-secondary div,
    .price-card-info div,
    .price-card-primary p,
    .price-card-secondary p,
    .price-card-info p,
    .price-card-primary strong,
    .price-card-secondary strong,
    .price-card-info strong,
    .price-card-primary span,
    .price-card-secondary span,
    .price-card-info span {
        color: #1e293b !important;
    }
    
    /* ===== TABLE STYLES ===== */
    .dataframe-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    
    /* ===== BADGES ===== */
    .badge-success {
        background: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .badge-warning {
        background: #fed7aa;
        color: #9a3412;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 8px;
        font-weight: 500;
        border: 1px solid #e2e8f0;
    }
    
    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* ===== LOGIN CONTAINER ===== */
    .login-wrapper {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .login-card {
        background: white;
        border-radius: 24px;
        padding: 2.5rem;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .login-title {
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* ===== SIDEBAR NAVIGATION PANEL - DARK THEME ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        border-right: 1px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    /* Sidebar text and labels */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar buttons - navigation tabs */
    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        color: #cbd5e1 !important;
        border: 1px solid #334155 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: #334155 !important;
        color: white !important;
        border-color: #475569 !important;
        transform: translateX(4px);
    }
    
    /* Primary button style in sidebar (active tab) */
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Announcement cards in sidebar */
    [data-testid="stSidebar"] .announcement-item {
        background: linear-gradient(135deg, #1e3a5f 0%, #1e293b 100%) !important;
        border-left: 3px solid #3b82f6 !important;
        color: #bae6fd !important;
    }
    
    /* Sidebar dividers */
    [data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }
    
    /* Sidebar select boxes */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #334155 !important;
        border-color: #475569 !important;
    }
    
    /* Sidebar number input, text input */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stNumberInput input {
        background-color: #334155 !important;
        border-color: #475569 !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Sidebar info/warning/success messages */
    [data-testid="stSidebar"] .stAlert {
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }
    
    [data-testid="stSidebar"] .stAlert .stMarkdown p {
        color: #e2e8f0 !important;
    }
    
    /* Sidebar metrics */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetric"] label,
    [data-testid="stSidebar"] [data-testid="stMetric"] .stMarkdown p {
        color: #e2e8f0 !important;
    }
    
    /* Scrollbar in sidebar */
    [data-testid="stSidebar"] ::-webkit-scrollbar-track {
        background: #1e293b !important;
    }
    
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
        background: #475569 !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {
        background: #64748b !important;
    }
    
    /* User info badge in sidebar */
    [data-testid="stSidebar"] .badge-info {
        background: #334155 !important;
        color: #93c5fd !important;
    }
    
    /* Sidebar expander */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #1e293b !important;
        border-color: #334155 !important;
        color: #e2e8f0 !important;
    }
    
    /* Logout button in sidebar */
    [data-testid="stSidebar"] button:has(.stMarkdown:contains("Logout")) {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        color: white !important;
        border: none !important;
        margin-top: 1rem !important;
    }
    
    [data-testid="stSidebar"] button:has(.stMarkdown:contains("Logout")):hover {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        transform: translateY(-2px);
    }
    
    /* ===== FOOTER ===== */
    .dashboard-footer {
        text-align: center;
        padding: 1.5rem;
        color: #94a3b8;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    /* ===== ANNOUNCEMENTS ===== */
    .announcement-item {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 0.75rem;
        border-radius: 10px;
        border-left: 3px solid #0ea5e9;
        margin: 0.5rem 0;
        font-size: 0.8rem;
        color: #0c4a6e;
    }
    
    /* ===== DIVIDERS ===== */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 1rem 0;
    }
    
    /* Print Styles */
    @media print {
        .stSidebar, header, footer, .stButton button {
            display: none !important;
        }
        .modern-card, .stat-card {
            break-inside: avoid;
            print-color-adjust: exact;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"

# User authentication
USERS = {
    "admin": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron", "Qzine", "MEPT"]},
    "ceo": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron", "Qzine", "MEPT"]},
    "zaid": {"password": "123456", "clients": ["CDC"]},
    "mohammad": {"password": "123456", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "123456", "clients": ["CakeArt", "SweetHouse"]},
    "Rotana": {"password": "123456", "clients": ["CDC"]},
    "Abed": {"password": "123456", "clients": ["Qzine", "MEPT"]}
}

# Client data sheets mapping
CLIENT_SHEETS = {
    "CDC": {
        "ceo_special": "CDC_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    },
    "CoteDivoire": {
        "backaldrin": "Backaldrin_CoteDivoire",
        "bateel": "Bateel_CoteDivoire", 
        "ceo_special": "CoteDivoire_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    },
    "CakeArt": {
        "backaldrin": "Backaldrin_CakeArt",
        "bateel": "Bateel_CakeArt",
        "ceo_special": "CakeArt_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    },
    "SweetHouse": {
        "backaldrin": "Backaldrin_SweetHouse",
        "bateel": "Bateel_SweetHouse",
        "ceo_special": "SweetHouse_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    },
    "Cameron": {
        "backaldrin": "Backaldrin_Cameron",
        "bateel": "Bateel_Cameron", 
        "ceo_special": "Cameron_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    },
    "Qzine": {
        "backaldrin": "Backaldrin_Qzine",
        "bateel": "Bateel_Qzine",
        "ceo_special": "Qzine_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    },
    "MEPT": {
        "backaldrin": "Backaldrin_MEPT",
        "bateel": "Bateel_MEPT",
        "ceo_special": "MEPT_CEO_Special_Prices",
        "palletizing": "Palletizing_Data"
    }
}

# Sheet names
PRODUCT_CATALOG_SHEET = "FullProductList"
PRICES_SHEET = "Prices"
GENERAL_PRICES_SHEET = "General_prices"

# ============================================
# HELPER FUNCTIONS (Preserved from original)
# ============================================

def get_smart_suggestions(search_term, supplier_data, search_type="all"):
    """Get smart suggestions with scoring system for better match quality"""
    if not search_term or len(search_term) < 2:
        return []
    
    suggestions = []
    search_lower = search_term.lower()
    
    for article_num, article_data in supplier_data.items():
        score = 0
        match_type = ""
        
        if search_lower == article_num.lower():
            score = 100
            match_type = "exact_article"
        elif search_lower in article_num.lower():
            score = 80
            match_type = "partial_article"
        
        for name in article_data.get('names', []):
            name_lower = str(name).lower()
            if search_lower == name_lower:
                score = max(score, 90)
                match_type = "exact_product"
            elif search_lower in name_lower:
                score = max(score, 70)
                match_type = "partial_product"
        
        for order in article_data.get('orders', []):
            hs_code = str(order.get('hs_code', '')).lower()
            if search_lower in hs_code:
                score = max(score, 60)
                match_type = "hs_code"
        
        if score >= 50:
            best_name = ""
            if article_data.get('names'):
                for name in article_data['names']:
                    if search_lower in str(name).lower():
                        best_name = str(name)
                        break
                if not best_name and article_data['names']:
                    best_name = str(article_data['names'][0])
            
            suggestions.append({
                "article": article_num,
                "name": best_name,
                "score": score,
                "match_type": match_type,
                "display": f"{article_num} - {best_name}",
                "has_orders": len(article_data.get('orders', [])) > 0,
                "has_prices": len(article_data.get('prices', [])) > 0
            })
    
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    unique_suggestions = []
    seen_articles = set()
    for sugg in suggestions:
        if sugg["article"] not in seen_articles:
            unique_suggestions.append(sugg)
            seen_articles.add(sugg["article"])
    
    return unique_suggestions[:10]

def initialize_search_history():
    """Initialize search history in session state"""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'max_history_items' not in st.session_state:
        st.session_state.max_history_items = 20

def add_to_search_history(search_term, client, supplier, article_num=None):
    """Add a search to the history"""
    initialize_search_history()
    
    st.session_state.search_history = [
        h for h in st.session_state.search_history 
        if not (h.get('search_term') == search_term and 
                h.get('client') == client and 
                h.get('supplier') == supplier)
    ]
    
    history_entry = {
        'timestamp': datetime.now(),
        'search_term': search_term,
        'client': client,
        'supplier': supplier,
        'article_num': article_num,
        'display_time': datetime.now().strftime("%H:%M")
    }
    
    st.session_state.search_history.insert(0, history_entry)
    
    if len(st.session_state.search_history) > st.session_state.max_history_items:
        st.session_state.search_history = st.session_state.search_history[:st.session_state.max_history_items]

def format_time_ago(timestamp):
    """Format timestamp as 'time ago'"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        if diff.days == 1:
            return "1 day ago"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return timestamp.strftime("%b %d")
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "Just now"

def initialize_favorites():
    """Initialize favorites in session state"""
    if 'favorite_searches' not in st.session_state:
        st.session_state.favorite_searches = []
    if 'show_favorites' not in st.session_state:
        st.session_state.show_favorites = False
    if 'show_favorites_modal' not in st.session_state:
        st.session_state.show_favorites_modal = False

def save_search_to_favorites(search_term, client, supplier, article_num=None):
    """Save a search to favorites"""
    initialize_favorites()
    
    for fav in st.session_state.favorite_searches:
        if (fav.get('search_term') == search_term and 
            fav.get('client') == client and 
            fav.get('supplier') == supplier):
            return False
    
    favorite_entry = {
        'timestamp': datetime.now(),
        'search_term': search_term,
        'client': client,
        'supplier': supplier,
        'article_num': article_num,
        'notes': ''
    }
    
    st.session_state.favorite_searches.append(favorite_entry)
    return True

def remove_search_from_favorites(search_term, client, supplier):
    """Remove a search from favorites"""
    st.session_state.favorite_searches = [
        fav for fav in st.session_state.favorite_searches 
        if not (fav.get('search_term') == search_term and 
                fav.get('client') == client and 
                fav.get('supplier') == supplier)
    ]

def is_search_favorited(search_term, client, supplier):
    """Check if a search is favorited"""
    if 'favorite_searches' not in st.session_state:
        return False
    
    for fav in st.session_state.favorite_searches:
        if (fav.get('search_term') == search_term and 
            fav.get('client') == client and 
            fav.get('supplier') == supplier):
            return True
    return False

def display_favorites_modal():
    """Display favorites in a modal"""
    if st.session_state.get('show_favorites_modal'):
        st.markdown('<div class="modal-overlay"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); z-index: 1000; min-width: 400px; max-height: 70vh; overflow-y: auto;">
            <h2 style="margin-top: 0; color: #1e293b;">⭐ Favorite Searches</h2>
        """, unsafe_allow_html=True)
        
        if not st.session_state.get('favorite_searches'):
            st.write("No favorites yet. Star a search to save it!")
        else:
            for i, fav in enumerate(st.session_state.favorite_searches):
                display_text = f"{fav['search_term']}"
                if fav.get('article_num'):
                    display_text += f" → {fav['article_num']}"
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    if st.button(
                        display_text, 
                        key=f"fav_modal_{i}",
                        use_container_width=True,
                        help=f"{fav['client']} • {fav['supplier']}"
                    ):
                        st.session_state[f"{fav['client']}_article"] = fav['search_term']
                        st.session_state[f"{fav['client']}_supplier"] = fav['supplier']
                        st.session_state.search_results = {
                            "article": fav.get('article_num', fav['search_term']),
                            "supplier": fav['supplier'],
                            "client": fav['client']
                        }
                        st.session_state.show_favorites_modal = False
                        st.rerun()
                
                with col2:
                    if st.button("📝", key=f"fav_note_modal_{i}", help="Edit notes"):
                        st.session_state.editing_favorite = i
                        st.session_state.editing_favorite_notes = fav.get('notes', '')
                
                with col3:
                    if st.button("🗑️", key=f"fav_remove_modal_{i}", help="Remove favorite"):
                        remove_search_from_favorites(fav['search_term'], fav['client'], fav['supplier'])
                        st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Close", use_container_width=True):
                st.session_state.show_favorites_modal = False
                st.rerun()
        with col2:
            if st.button("Clear All Favorites", use_container_width=True):
                st.session_state.favorite_searches = []
                st.success("All favorites cleared!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_sheet_data(sheet_name, start_row=0):
    """Universal Google Sheets loader for all data types - CACHED"""
    try:
        import urllib.parse
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{encoded_sheet}!A:Z?key={API_KEY}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if len(values) > start_row:
                headers = values[start_row]
                headers_count = len(headers)
                rows = values[start_row + 1:] if len(values) > start_row + 1 else []
                
                padded_rows = []
                for row in rows:
                    if len(row) < headers_count:
                        row = row + [''] * (headers_count - len(row))
                    elif len(row) > headers_count:
                        row = row[:headers_count]
                    padded_rows.append(row)
                
                df = pd.DataFrame(padded_rows, columns=headers)
                df = df.replace('', pd.NA)
                return df
                
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {str(e)}")
        return pd.DataFrame()

def get_all_clients_from_master():
    """Get list of all unique clients from Clients_CoC sheet"""
    try:
        master_df = load_sheet_data("Clients_CoC")
        if not master_df.empty and 'Client' in master_df.columns:
            return sorted(master_df['Client'].dropna().unique().tolist())
        return []
    except:
        return []

@st.cache_data(ttl=300)
def get_google_sheets_data(client="CDC"):
    """Load client data from Clients_CoC master sheet"""
    try:
        master_df = load_sheet_data("Clients_CoC")
        
        if master_df.empty:
            st.warning("⚠️ Clients_CoC sheet is empty or not found")
            return {"Backaldrin": {}, "Bateel": {}}
        
        client_df = master_df[master_df['Client'] == client].copy()
        
        if client_df.empty:
            st.warning(f"⚠️ No data found for client: {client}")
            return {"Backaldrin": {}, "Bateel": {}}
        
        backaldrin_df = client_df[client_df['Supplier'] == 'Backaldrin']
        bateel_df = client_df[client_df['Supplier'] == 'Bateel']
        
        def convert_df_to_dict(df):
            result = {}
            
            if df.empty:
                return result
            
            article_col = 'Article_Number'
            product_col = 'Product_Name'
            price_col = 'Price'
            order_col = 'Order_Number'
            date_col = 'Order_Date'
            year_col = 'Year'
            hs_code_col = 'HS_Code'
            packaging_col = 'Packaging'
            quantity_col = 'Quantity'
            weight_col = 'Total_Weight'
            total_price_col = 'Total_Price'
            status_col = 'Status'
            notes_col = 'Notes'
            
            if article_col not in df.columns:
                st.error(f"❌ Missing column: {article_col}. Available: {list(df.columns)}")
                return result
            
            for _, row in df.iterrows():
                article = str(row.get(article_col, '')).strip()
                if not article or article == 'nan':
                    continue
                    
                if article not in result:
                    result[article] = {
                        'names': [],
                        'prices': [],
                        'orders': []
                    }
                
                product_name = str(row.get(product_col, '')).strip()
                if product_name and product_name != 'nan' and product_name not in result[article]['names']:
                    result[article]['names'].append(product_name)
                
                price_str = str(row.get(price_col, '')).strip()
                if price_str and price_str != 'nan':
                    try:
                        price_float = float(price_str)
                        result[article]['prices'].append(price_float)
                    except:
                        pass
                
                order_details = {
                    'order_no': str(row.get(order_col, '')).strip() if order_col in df else '',
                    'date': str(row.get(date_col, '')).strip() if date_col in df else '',
                    'year': str(row.get(year_col, '')).strip() if year_col in df else '',
                    'product_name': product_name,
                    'article': article,
                    'hs_code': str(row.get(hs_code_col, '')).strip() if hs_code_col in df else '',
                    'packaging': str(row.get(packaging_col, '')).strip() if packaging_col in df else '',
                    'quantity': str(row.get(quantity_col, '')).strip() if quantity_col in df else '',
                    'total_weight': str(row.get(weight_col, '')).strip() if weight_col in df else '',
                    'price': str(row.get(price_col, '')).strip() if price_col in df else '',
                    'total_price': str(row.get(total_price_col, '')).strip() if total_price_col in df else '',
                    'status': str(row.get(status_col, '')).strip() if status_col in df else '',
                    'notes': str(row.get(notes_col, '')).strip() if notes_col in df else ''
                }
                result[article]['orders'].append(order_details)
            
            return result
        
        return {
            "Backaldrin": convert_df_to_dict(backaldrin_df),
            "Bateel": convert_df_to_dict(bateel_df)
        }
        
    except Exception as e:
        st.error(f"Error loading data for {client}: {str(e)}")
        return {"Backaldrin": {}, "Bateel": {}}
    
@st.cache_data(ttl=600)
def load_product_catalog():
    """Load product catalog from Google Sheets - CACHED"""
    try:
        sheet_name = PRODUCT_CATALOG_SHEET
        catalog_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(catalog_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                df = pd.DataFrame(rows, columns=headers)
                df = df.fillna('')
                
                if len(df) > 0 and 'Article_Number' in df.columns:
                    return df
                else:
                    st.error(f"Product catalog loaded but missing required columns. Found: {list(df.columns)}")
                    return pd.DataFrame()
            else:
                st.warning("Product catalog sheet exists but has no data or only headers")
                return pd.DataFrame()
        else:
            st.error(f"Failed to load product catalog. HTTP Status: {response.status_code}")
            return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading product catalog: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def load_prices_data():
    """Load all prices data from Google Sheets - CACHED"""
    try:
        prices_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{PRICES_SHEET}!A:Z?key={API_KEY}"
        response = requests.get(prices_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                df = pd.DataFrame(rows, columns=headers)
                
                required_cols = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 
                               'Customer Article No', 'Customer Label', 'Packing/kg', 'Price']
                
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = ''
                
                if 'Price' in df.columns:
                    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
                if 'Packing/kg' in df.columns:
                    df['Packing/kg'] = pd.to_numeric(df['Packing/kg'], errors='coerce')
                
                text_cols = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 
                           'Customer Article No', 'Customer Label']
                for col in text_cols:
                    if col in df.columns:
                        df[col] = df[col].fillna('')
                
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading prices data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def load_general_prices_data():
    """Load General_prices data from Google Sheets - CACHED"""
    try:
        prices_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{GENERAL_PRICES_SHEET}!A:Z?key={API_KEY}"
        response = requests.get(prices_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 0:
                headers = values[0]
                rows = values[1:] if len(values) > 1 else []
                
                df = pd.DataFrame(rows, columns=headers)
                df.columns = [str(col).strip() for col in df.columns]
                
                if 'NEW EXW' in df.columns:
                    df['NEW EXW'] = pd.to_numeric(df['NEW EXW'], errors='coerce')
                
                if 'UNT WGT' in df.columns:
                    df['UNT WGT'] = pd.to_numeric(df['UNT WGT'], errors='coerce')
                
                df = df.replace('', pd.NA)
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading general prices data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_ceo_special_prices(client="CDC"):
    """Load CEO special prices from Google Sheets for specific client - CACHED"""
    try:
        sheet_name = CLIENT_SHEETS[client]["ceo_special"]
        ceo_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(ceo_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                df = pd.DataFrame(rows, columns=headers)
                
                required_cols = ['Article_Number', 'Product_Name', 'Special_Price', 'Currency', 'Incoterm']
                if all(col in df.columns for col in required_cols):
                    df = df[required_cols + [col for col in df.columns if col not in required_cols]]
                    
                    if 'Notes' not in df.columns:
                        df['Notes'] = ''
                    if 'Effective_Date' not in df.columns:
                        df['Effective_Date'] = datetime.now().strftime('%Y-%m-%d')
                    if 'Expiry_Date' not in df.columns:
                        df['Expiry_Date'] = (datetime.now() + pd.Timedelta(days=365)).strftime('%Y-%m-%d')
                    
                    return df
                else:
                    st.error(f"Missing required columns in {sheet_name}. Found: {list(df.columns)}")
                    return pd.DataFrame()
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading CEO special prices for {client}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=180)
def load_etd_data(sheet_id, sheet_name):
    """Optimized ETD loader using universal function - CACHED"""
    return load_sheet_data(sheet_name, start_row=13)

@st.cache_data(ttl=300)
def load_palletizing_data(client):
    """Load palletizing data from Google Sheets"""
    try:
        sheet_name = CLIENT_SHEETS[client]["palletizing"]
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                df = pd.DataFrame(rows, columns=headers)
                
                required_cols = ['Client', 'Item Code', 'Item Name', 'Unit/KG', 'Unit/Carton', 
                               'Unit Pack/Pallet', 'Total Unit', 'Pallet Order', 'Total Weight', 'Factory']
                
                missing_cols = [col for col in required_cols if col not in df.columns]
                if missing_cols:
                    st.error(f"Missing columns in palletizing data: {', '.join(missing_cols)}")
                    return pd.DataFrame()
                
                numeric_cols = ['Unit/KG', 'Unit/Carton', 'Unit Pack/Pallet', 'Total Unit', 'Pallet Order', 'Total Weight']
                for col in numeric_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading palletizing data for {client}: {str(e)}")
        return pd.DataFrame()

def check_login():
    """Check if user is logged in"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_clients' not in st.session_state:
        st.session_state.user_clients = []
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "🏢 CLIENTS"
    
    return st.session_state.logged_in

def login_page():
    """Login page"""
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-title">📊 Multi-Client Dashboard</div>
            <p style="text-align: center; color: #64748b; margin-bottom: 1.5rem;">Sign in to access your dashboard</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Sign In", use_container_width=True)
        
        if submit:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_clients = USERS[username]["clients"]
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def logout_button():
    """Logout button"""
    if st.button("Logout", key="logout_header", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_clients = []
        st.rerun()

# ============================================
# MAIN DASHBOARD
# ============================================
def main_dashboard():
    """Main dashboard with professional UI"""
    
    # Header
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="dashboard-title">
                    <span>📊</span> Multi-Client Command Center
                </div>
                <div class="dashboard-subtitle">
                    Real-time pricing intelligence • Order tracking • Client analytics
                </div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span class="badge-info">👤 {st.session_state.username}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons Row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        if st.button("⭐ Favorites", use_container_width=True):
            st.session_state.show_favorites_modal = True
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col3:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
    
    display_favorites_modal()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        
        tabs = [
            "🏢 CLIENTS",
            "💰 PRICES", 
            "📅 ETD SHEET",
            "⭐ CEO SPECIAL PRICES",
            "💰 PRICE INTELLIGENCE",
            "📦 PRODUCT CATALOG",
            "📦 PALLETIZING",
            "📊 ALL PRICES",
            "📋 CLIENT'S ORDERS",
            "🎁 SAMPLES REQUEST"
        ]
        
        for tab in tabs:
            is_active = st.session_state.get('active_tab', '🏢 CLIENTS') == tab
            button_label = f"▶️ {tab}" if is_active else tab
            
            if st.button(
                button_label,
                key=f"tab_{tab}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.active_tab = tab
                st.rerun()
        
        st.markdown("---")
        
        # Announcements
        st.markdown("### 📢 Updates")
        announcements = [
            "🎁 Samples Request tab added!",
            "🚨 ETD is officially working!",
            "⭐ Save favorite searches!",
            "📊 All Prices tab added!"
        ]
        
        for announcement in announcements:
            st.markdown(f'<div class="announcement-item">{announcement}</div>', unsafe_allow_html=True)
        
        # Recent Searches
        if st.session_state.get('search_history'):
            st.markdown("---")
            st.markdown("### 🔍 Recent")
            
            for i, history_item in enumerate(st.session_state.search_history[:3]):
                time_ago = format_time_ago(history_item['timestamp'])
                display_text = f"{history_item['search_term']}"
                if history_item.get('article_num'):
                    display_text += f" → {history_item['article_num']}"
                
                if st.button(
                    f"{display_text[:35]}",
                    key=f"hist_{i}",
                    use_container_width=True,
                    help=f"{history_item['client']} • {time_ago}"
                ):
                    st.session_state[f"{history_item['client']}_article"] = history_item['search_term']
                    st.session_state[f"{history_item['client']}_supplier"] = history_item['supplier']
                    st.session_state.search_results = {
                        "article": history_item.get('article_num', history_item['search_term']),
                        "supplier": history_item['supplier'],
                        "client": history_item['client']
                    }
                    st.session_state.active_tab = "🏢 CLIENTS"
                    st.rerun()
    
    # Main Content
    st.markdown(f"<div class='section-header'>{st.session_state.active_tab}</div>", unsafe_allow_html=True)
    
    # Tab Content
    if st.session_state.active_tab == "🏢 CLIENTS":
        clients_tab()
    elif st.session_state.active_tab == "💰 PRICES":
        prices_tab()
    elif st.session_state.active_tab == "📅 ETD SHEET":
        etd_tab()
    elif st.session_state.active_tab == "⭐ CEO SPECIAL PRICES":
        ceo_specials_tab()
    elif st.session_state.active_tab == "💰 PRICE INTELLIGENCE":
        price_intelligence_tab()
    elif st.session_state.active_tab == "📦 PRODUCT CATALOG":
        product_catalog_tab()
    elif st.session_state.active_tab == "📦 PALLETIZING":
        palletizing_tab()
    elif st.session_state.active_tab == "📊 ALL PRICES":
        all_prices_tab()
    elif st.session_state.active_tab == "📋 CLIENT'S ORDERS":
        clients_orders_tab()
    elif st.session_state.active_tab == "🎁 SAMPLES REQUEST":
        samples_request_tab()
    
    # Footer
    st.markdown(f"""
    <div class="dashboard-footer">
        Multi-Client Dashboard v5.0 | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    logout_button()

# ============================================
# SAMPLES REQUEST TAB
# ============================================

def samples_request_tab():
    """Samples Request Tab with auto-fill and export capabilities"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dc2626, #b91c1c); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">🎁 Samples Request</h2>
        <p style="margin:0; opacity:0.9; color: white;">Request product samples • Fill out the form below</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'sample_items' not in st.session_state:
        st.session_state.sample_items = []
    if 'sample_request_submitted' not in st.session_state:
        st.session_state.sample_request_submitted = False
    if 'last_submission_data' not in st.session_state:
        st.session_state.last_submission_data = None
    if 'show_confirmation' not in st.session_state:
        st.session_state.show_confirmation = False
    
    catalog_data = load_product_catalog()
    
    # Build lookup dictionaries for auto-fill
    article_to_product = {}
    product_to_article = {}
    
    if not catalog_data.empty and 'Article_Number' in catalog_data.columns and 'Product_Name' in catalog_data.columns:
        for _, row in catalog_data.iterrows():
            article = str(row['Article_Number']).strip()
            product = str(row['Product_Name']).strip()
            if article and article != 'nan' and product and product != 'nan':
                article_to_product[article] = product
                product_to_article[product.lower()] = article
    
    # Show confirmation if recently submitted
    if st.session_state.show_confirmation and st.session_state.last_submission_data:
        display_submission_confirmation()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Download Excel", use_container_width=True, key="download_excel_confirmation"):
                export_samples_to_excel(st.session_state.last_submission_data, st.session_state.sample_items)
        with col2:
            if st.button("📄 Print", use_container_width=True, key="print_confirmation"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
        with col3:
            if st.button("🔄 New Request", use_container_width=True, key="new_request"):
                reset_sample_form()
                st.rerun()
        
        # Don't show the form again
        return
    
    # Export options at the top (only show if there are items)
    if st.session_state.sample_items:
        st.markdown("### 📎 Export Options")
        col_export1, col_export2, col_export3 = st.columns(3)
        with col_export1:
            if st.button("📥 Download Excel", use_container_width=True, key="download_excel_top"):
                # Create export data from current items
                export_data = {
                    'items': st.session_state.sample_items,
                    'requested_by': st.session_state.get('sample_requested_by', ''),
                    'going_to': st.session_state.get('sample_going_to', ''),
                    'address': st.session_state.get('sample_address', ''),
                    'request_date': st.session_state.get('sample_request_date', datetime.now().date()),
                    'department': st.session_state.get('sample_department', ''),
                    'delivery_method': st.session_state.get('sample_delivery_method', '')
                }
                export_samples_to_excel(export_data, st.session_state.sample_items)
        with col_export2:
            if st.button("📄 Print Form", use_container_width=True, key="print_form"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
        with col_export3:
            if st.button("📋 Copy Summary", use_container_width=True, key="copy_summary"):
                copy_to_clipboard(st.session_state.sample_items, st.session_state)
        st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='subsection-header'>📋 Request Information</div>", unsafe_allow_html=True)
        
        request_date = st.date_input("Request Date", value=datetime.now().date(), key="sample_request_date")
        samples_eta = st.date_input("Samples ETA", value=datetime.now().date(), key="sample_eta")
        requested_by = st.text_input("Requested By", placeholder="Enter your full name", key="sample_requested_by")
        department = st.selectbox("Department", ["Sales", "Marketing", "R&D", "Production", "Quality Control", "Procurement", "Other"], key="sample_department")
        department_value = department
        if department == "Other":
            department_other = st.text_input("Please specify department", placeholder="Enter department name", key="sample_department_other")
            department_value = department_other if department_other else department
    
    with col2:
        st.markdown("<div class='subsection-header'>📍 Delivery Information</div>", unsafe_allow_html=True)
        
        requester_title = st.selectbox("Requester Title", ["Manager", "Supervisor", "Specialist", "Coordinator", "Director", "Executive", "Other"], key="sample_requester_title")
        requester_title_value = requester_title
        if requester_title == "Other":
            title_other = st.text_input("Please specify title", placeholder="Enter your title", key="sample_title_other")
            requester_title_value = title_other if title_other else requester_title
        
        going_to = st.text_input("Recipient Name", placeholder="Enter recipient name", key="sample_going_to")
        address = st.text_area("Address", placeholder="Enter complete delivery address", height=80, key="sample_address")
        delivery_method = st.selectbox("Delivery Method", ["Courier", "Pickup", "Mail", "Express Delivery", "Freight", "Other"], key="sample_delivery_method")
        delivery_method_value = delivery_method
        if delivery_method == "Other":
            delivery_other = st.text_input("Please specify delivery method", placeholder="Enter delivery method", key="sample_delivery_other")
            delivery_method_value = delivery_other if delivery_other else delivery_method
    
    st.markdown("---")
    st.markdown("<div class='subsection-header'>📦 Sample Items</div>", unsafe_allow_html=True)
    
    # Use a separate container for the form
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            article_input = st.text_input(
                "Article Number *", 
                placeholder="e.g., 1-366, 1-367...", 
                key="sample_article_input"
            )
            
            # Show suggestions while typing
            if article_input and len(article_input) >= 2 and not catalog_data.empty:
                matching_articles = catalog_data[
                    catalog_data['Article_Number'].astype(str).str.contains(article_input, case=False, na=False)
                ].head(5)
                if not matching_articles.empty:
                    st.caption("💡 Suggestions (click to use):")
                    for _, row in matching_articles.iterrows():
                        if st.button(f"📦 {row['Article_Number']}", key=f"suggest_{row['Article_Number']}"):
                            st.session_state.sample_article_input = row['Article_Number']
                            st.session_state.sample_product_input = row.get('Product_Name', '')
                            st.rerun()
            
            # Auto-fill product when article is entered
            default_product = ""
            if article_input:
                if article_input in article_to_product:
                    default_product = article_to_product[article_input]
                else:
                    for art, prod in article_to_product.items():
                        if article_input.lower() in art.lower():
                            default_product = prod
                            break
            
            product_input = st.text_input(
                "Product Name *", 
                placeholder="Enter product name", 
                value=default_product,
                key="sample_product_input"
            )
            
            item_type = st.selectbox("Item Type", ["Raw Material", "Packaging", "Finished Good", "Semi-Finished", "Auxiliary Material", "Other"], key="sample_item_type")
        
        with col2:
            pack_type = st.selectbox("Pack Type", ["Bag", "Box", "Carton", "Drum", "Pallet", "Roll", "Tin", "Other"], key="sample_pack_type")
            unit_weight = st.number_input("Unit Weight (kg)", min_value=0.0, step=0.1, format="%.2f", key="sample_unit_weight", value=0.0)
            quantity = st.number_input("Total Quantity", min_value=1, step=1, value=1, key="sample_quantity")
        
        with col3:
            logo_requirement = st.radio("Logo Required?", options=["No", "Yes - Standard", "Yes - Custom"], key="sample_logo", horizontal=True)
            st.markdown("---")
            item_notes = st.text_area("Item Notes (Optional)", placeholder="Any special requirements...", key="sample_item_notes")
        
        # Add item button
        if st.button("➕ Add Sample Item", use_container_width=True, key="add_sample_item_btn"):
            if article_input and product_input:
                new_item = {
                    'article_number': article_input,
                    'product_name': product_input,
                    'item_type': item_type,
                    'pack_type': pack_type,
                    'unit_weight': unit_weight,
                    'quantity': quantity,
                    'logo_requirement': logo_requirement,
                    'notes': item_notes
                }
                st.session_state.sample_items.append(new_item)
                st.success(f"✅ Added: {article_input} - {product_input}")
                # Clear inputs
                for key in ['sample_article_input', 'sample_product_input', 'sample_item_notes']:
                    if key in st.session_state:
                        st.session_state[key] = ""
                st.rerun()
            else:
                st.error("❌ Please enter both Article Number and Product Name")
    
    # Display existing items
    if st.session_state.sample_items:
        st.markdown(f"<div class='subsection-header'>📋 Sample Items ({len(st.session_state.sample_items)})</div>", unsafe_allow_html=True)
        
        # Display items in a table
        items_df = pd.DataFrame(st.session_state.sample_items)
        display_cols = ['article_number', 'product_name', 'item_type', 'pack_type', 'unit_weight', 'quantity', 'logo_requirement']
        if all(col in items_df.columns for col in display_cols):
            display_df = items_df[display_cols].copy()
            display_df['unit_weight'] = display_df['unit_weight'].apply(lambda x: f"{x:.2f} kg" if x > 0 else "N/A")
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Delete buttons
        st.markdown("**Remove items:**")
        cols = st.columns(min(4, len(st.session_state.sample_items)))
        for idx, item in enumerate(st.session_state.sample_items):
            col_idx = idx % 4
            with cols[col_idx]:
                if st.button(f"🗑️ {item['article_number'][:15]}", key=f"remove_item_{idx}"):
                    st.session_state.sample_items.pop(idx)
                    st.rerun()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", len(st.session_state.sample_items))
        with col2:
            total_qty = sum(item.get('quantity', 0) for item in st.session_state.sample_items)
            st.metric("Total Quantity", total_qty)
        with col3:
            unique_articles = len(set(item.get('article_number', '') for item in st.session_state.sample_items))
            st.metric("Unique Articles", unique_articles)
        
        if st.button("🗑️ Clear All Items", use_container_width=True):
            st.session_state.sample_items = []
            st.rerun()
    
    st.markdown("---")
    request_notes = st.text_area("Additional Request Notes (Optional)", placeholder="Any additional information...", height=80, key="sample_request_notes")
    
    # Submit button
    if st.button("📤 SUBMIT SAMPLES REQUEST", use_container_width=True, type="primary"):
        # Get all form values safely
        req_date = st.session_state.get('sample_request_date', datetime.now().date())
        samples_eta_val = st.session_state.get('sample_eta', datetime.now().date())
        req_by = st.session_state.get('sample_requested_by', '')
        dept = st.session_state.get('sample_department', '')
        if dept == "Other":
            dept = st.session_state.get('sample_department_other', dept)
        req_title = st.session_state.get('sample_requester_title', '')
        if req_title == "Other":
            req_title = st.session_state.get('sample_title_other', req_title)
        going_to_val = st.session_state.get('sample_going_to', '')
        address_val = st.session_state.get('sample_address', '')
        delivery_method_val = st.session_state.get('sample_delivery_method', '')
        if delivery_method_val == "Other":
            delivery_method_val = st.session_state.get('sample_delivery_other', delivery_method_val)
        
        errors = []
        if not req_by:
            errors.append("Requested By is required")
        if not going_to_val:
            errors.append("Recipient Name is required")
        if not address_val:
            errors.append("Address is required")
        if not st.session_state.sample_items:
            errors.append("At least one sample item is required")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Store submission data
            st.session_state.last_submission_data = {
                'request_id': f"SAMP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                'request_date': req_date,
                'samples_eta': samples_eta_val,
                'requested_by': req_by,
                'department': dept,
                'requester_title': req_title,
                'going_to': going_to_val,
                'address': address_val,
                'delivery_method': delivery_method_val,
                'items': st.session_state.sample_items.copy(),
                'notes': request_notes,
                'submitted_by': st.session_state.username,
                'submission_time': datetime.now()
            }
            st.session_state.show_confirmation = True
            st.rerun()


def display_submission_confirmation():
    """Display the submission confirmation"""
    data = st.session_state.last_submission_data
    if not data:
        return
    
    st.markdown("### ✅ SAMPLES REQUEST CONFIRMATION")
    st.balloons()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <h3 style="margin:0; color: white;">✓ Request Submitted Successfully!</h3>
        <p style="margin:0; opacity:0.9; color: white;">Request ID: {data['request_id']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Submitted By:** {data['submitted_by']}")
    st.markdown(f"**Submission Time:** {data['submission_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **📋 Request Information:**
        - **Request Date:** {data['request_date'].strftime('%Y-%m-%d') if hasattr(data['request_date'], 'strftime') else data['request_date']}
        - **Samples ETA:** {data['samples_eta'].strftime('%Y-%m-%d') if hasattr(data['samples_eta'], 'strftime') else data['samples_eta']}
        - **Requested By:** {data['requested_by']}
        - **Department:** {data['department']}
        - **Requester Title:** {data['requester_title']}
        """)
    with col2:
        st.markdown(f"""
        **📍 Delivery Information:**
        - **Recipient:** {data['going_to']}
        - **Address:** {data['address']}
        - **Delivery Method:** {data['delivery_method']}
        """)
    
    st.markdown("**📦 Sample Items:**")
    summary_df = pd.DataFrame(data['items'])
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    if data['notes']:
        st.markdown(f"**📝 Additional Notes:** {data['notes']}")
    
    st.markdown("---")


def export_samples_to_excel(data, items):
    """Export sample request to Excel file"""
    from io import BytesIO
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Export items
        if items:
            items_df = pd.DataFrame(items)
            items_df.to_excel(writer, sheet_name='Sample Items', index=False)
        
        # Export summary if data is a dict with form data
        if isinstance(data, dict) and 'request_id' in data:
            summary_data = {
                'Field': ['Request ID', 'Request Date', 'Samples ETA', 'Requested By', 'Department', 
                         'Requester Title', 'Recipient Name', 'Address', 'Delivery Method', 
                         'Submitted By', 'Submission Time', 'Additional Notes'],
                'Value': [
                    data.get('request_id', ''),
                    data.get('request_date', ''),
                    data.get('samples_eta', ''),
                    data.get('requested_by', ''),
                    data.get('department', ''),
                    data.get('requester_title', ''),
                    data.get('going_to', ''),
                    data.get('address', ''),
                    data.get('delivery_method', ''),
                    data.get('submitted_by', ''),
                    data.get('submission_time', ''),
                    data.get('notes', '')
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Request Summary', index=False)
        else:
            # Simple export with just items and basic info
            basic_info = {
                'Field': ['Export Date', 'Total Items', 'Total Quantity'],
                'Value': [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(items), sum(item.get('quantity', 0) for item in items)]
            }
            basic_df = pd.DataFrame(basic_info)
            basic_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"samples_request_{timestamp}.xlsx"
    
    st.download_button(
        label="💾 Click to Download Excel File",
        data=output,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


def copy_to_clipboard(items, session_state):
    """Copy form data to clipboard"""
    lines = []
    lines.append("=" * 60)
    lines.append("SAMPLES REQUEST FORM")
    lines.append("=" * 60)
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"User: {session_state.get('username', 'Unknown')}")
    lines.append("")
    
    # Get form data
    req_by = session_state.get('sample_requested_by', '')
    going_to = session_state.get('sample_going_to', '')
    address = session_state.get('sample_address', '')
    
    lines.append("REQUEST INFORMATION:")
    lines.append(f"  Requested By: {req_by}")
    lines.append(f"  Recipient: {going_to}")
    lines.append(f"  Address: {address}")
    lines.append("")
    
    lines.append("SAMPLE ITEMS:")
    for i, item in enumerate(items, 1):
        lines.append(f"  {i}. {item['article_number']} - {item['product_name']}")
        lines.append(f"     Type: {item['item_type']}, Pack: {item['pack_type']}")
        lines.append(f"     Weight: {item['unit_weight']} kg, Quantity: {item['quantity']}")
        lines.append(f"     Logo: {item['logo_requirement']}")
        if item.get('notes'):
            lines.append(f"     Notes: {item['notes']}")
        lines.append("")
    
    lines.append("=" * 60)
    
    text_to_copy = "\n".join(lines)
    
    # JavaScript to copy to clipboard
    copy_js = f"""
    <script>
        const text = `{text_to_copy.replace('`', '\\`')}`;
        navigator.clipboard.writeText(text).then(function() {{
            alert('Form data copied to clipboard!');
        }});
    </script>
    """
    st.markdown(copy_js, unsafe_allow_html=True)
    st.success("✅ Data copied to clipboard!")


def reset_sample_form():
    """Reset the sample request form"""
    st.session_state.sample_items = []
    st.session_state.sample_request_submitted = False
    st.session_state.last_submission_data = None
    st.session_state.show_confirmation = False
    
    # Clear all input fields
    keys_to_clear = [
        'sample_requested_by', 'sample_going_to', 'sample_address',
        'sample_article_input', 'sample_product_input', 'sample_item_notes',
        'sample_department_other', 'sample_title_other', 'sample_delivery_other'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# ============================================
# CLIENT'S ORDERS TAB
# ============================================

def clients_orders_tab():
    """Client's Orders Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0891b2, #0e7c8c); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📋 Client's Orders</h2>
        <p style="margin:0; opacity:0.9; color: white;">Direct access to Clients_CoC sheet • Search by article, product, or HS code</p>
    </div>
    """, unsafe_allow_html=True)
    
    all_clients = get_all_clients_from_master()
    
    if not all_clients:
        st.warning("No clients found in Clients_CoC sheet")
        return
    
    st.success(f"Found {len(all_clients)} clients")
    
    client = st.selectbox("Select Client:", all_clients, key="clients_orders_client_select")
    
    with st.spinner(f"Loading data for {client}..."):
        DATA = get_google_sheets_data(client)
    
    if not DATA.get("Backaldrin") and not DATA.get("Bateel"):
        st.error(f"No data found for {client}")
        return
    
    supplier = st.radio("Select Supplier:", ["Backaldrin", "Bateel"], horizontal=True, key="clients_orders_supplier")
    
    st.markdown("<div class='subsection-header'>🔍 Search Orders</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("Search by Article, Product, or HS Code:", placeholder="e.g., 1-366, Chocolate...", key="clients_orders_search")
    with col2:
        search_type = st.selectbox("Search Type:", ["All", "Article Number", "Product Name", "HS Code"], key="clients_orders_search_type")
    with col3:
        if st.button("🔍 Search", type="primary", use_container_width=True, key="clients_orders_search_btn"):
            if search_term:
                add_to_search_history(search_term, client, supplier)
    
    # Initialize supplier_data before using it
    supplier_data = DATA.get(supplier, {})
    
    # ===== DATE FILTER SECTION =====
    st.markdown("<div class='subsection-header'>📅 Date Filter (Optional)</div>", unsafe_allow_html=True)
    
    # Initialize filter variables
    filter_type = "All Time"
    selected_year = None
    start_date = None
    end_date = None
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_type = st.radio("Filter by:", ["All Time", "Year", "Date Range"], horizontal=False, key="clients_orders_filter_type")
    
    with col2:
        if filter_type == "Year":
            # Get available years from orders
            available_years = set()
            for article_num, article_data in supplier_data.items():
                for order in article_data.get('orders', []):
                    year = order.get('year', '')
                    if year and year != 'nan':
                        year_str = str(year).strip()
                        if year_str.isdigit() and len(year_str) == 4:
                            available_years.add(year_str)
                        elif '-' in year_str:
                            parts = year_str.split('-')
                            if parts[0].isdigit() and len(parts[0]) == 4:
                                available_years.add(parts[0])
            available_years = sorted(list(available_years), reverse=True)
            if available_years:
                selected_year = st.selectbox("Select Year:", available_years, key="clients_orders_year")
            else:
                st.info("No year data available")
    
    with col3:
        if filter_type == "Date Range":
            start_date = st.date_input("From Date:", value=datetime.now().date() - pd.Timedelta(days=365), key="clients_orders_start_date")
    
    with col4:
        if filter_type == "Date Range":
            end_date = st.date_input("To Date:", value=datetime.now().date(), key="clients_orders_end_date")
    
    if 'clients_orders_results' not in st.session_state:
        st.session_state.clients_orders_results = None
    
    if search_term:
        search_results = []
        search_lower = search_term.lower()
        
        for article_num, article_data in supplier_data.items():
            match_found = False
            match_type = ""
            
            if search_type in ["All", "Article Number"]:
                if search_lower in article_num.lower():
                    match_found = True
                    match_type = "Article Number"
            
            if not match_found and search_type in ["All", "Product Name"]:
                for name in article_data.get('names', []):
                    if search_lower in str(name).lower():
                        match_found = True
                        match_type = "Product Name"
                        break
            
            if not match_found and search_type in ["All", "HS Code"]:
                for order in article_data.get('orders', []):
                    hs_code = str(order.get('hs_code', '')).lower()
                    if search_lower in hs_code:
                        match_found = True
                        match_type = "HS Code"
                        break
            
            if match_found and article_data.get('orders'):
                product_name = article_data['names'][0] if article_data.get('names') else ""
                prices = article_data.get('prices', [])
                min_price = min(prices) if prices else None
                max_price = max(prices) if prices else None
                
                search_results.append({
                    'article': article_num,
                    'product_name': product_name,
                    'match_type': match_type,
                    'orders_count': len(article_data.get('orders', [])),
                    'price_count': len(prices),
                    'min_price': min_price,
                    'max_price': max_price,
                    'article_data': article_data
                })
        
        if search_results:
            st.success(f"Found {len(search_results)} matching items")
            st.session_state.clients_orders_results = {
                'client': client,
                'supplier': supplier,
                'search_term': search_term,
                'results': search_results
            }
        else:
            st.warning(f"No results found for '{search_term}'")
    
    if st.session_state.clients_orders_results and st.session_state.clients_orders_results.get('client') == client:
        results_data = st.session_state.clients_orders_results
        search_results = results_data.get('results', [])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Items Found", len(search_results))
        col2.metric("Total Orders", sum(r['orders_count'] for r in search_results))
        
        all_prices = []
        for r in search_results:
            if r['min_price']:
                all_prices.append(r['min_price'])
            if r['max_price']:
                all_prices.append(r['max_price'])
        if all_prices:
            col3.metric("Price Range", f"${min(all_prices):.2f} - ${max(all_prices):.2f}")
        
        for result in search_results:
            # Filter orders by date if selected
            filtered_orders = result['article_data'].get('orders', []).copy()
            
            if filter_type == "Year" and selected_year:
                filtered_orders = []
                for order in result['article_data'].get('orders', []):
                    order_year = order.get('year', '')
                    if order_year and order_year != 'nan':
                        year_str = str(order_year).strip()
                        if year_str.isdigit() and len(year_str) == 4:
                            if year_str == selected_year:
                                filtered_orders.append(order)
                        elif '-' in year_str:
                            parts = year_str.split('-')
                            if parts[0].isdigit() and len(parts[0]) == 4 and parts[0] == selected_year:
                                filtered_orders.append(order)
                    # Also try to extract year from date field
                    elif order.get('date', ''):
                        date_str = str(order.get('date', '')).strip()
                        for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                if str(date_obj.year) == selected_year:
                                    filtered_orders.append(order)
                                break
                            except:
                                continue
            
            elif filter_type == "Date Range" and start_date and end_date:
                filtered_orders = []
                for order in result['article_data'].get('orders', []):
                    date_str = str(order.get('date', '')).strip()
                    if date_str and date_str != 'nan':
                        for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                            try:
                                date_obj = datetime.strptime(date_str, fmt)
                                if start_date <= date_obj.date() <= end_date:
                                    filtered_orders.append(order)
                                break
                            except:
                                continue
            
            # Calculate filtered stats
            filtered_prices = []
            for order in filtered_orders:
                price_str = order.get('price', '')
                try:
                    price_val = float(str(price_str).replace('$', '').replace(',', '').strip())
                    filtered_prices.append(price_val)
                except:
                    pass
            
            filtered_min_price = min(filtered_prices) if filtered_prices else None
            filtered_max_price = max(filtered_prices) if filtered_prices else None
            filtered_count = len(filtered_orders)
            
            # Show filter info in expander title
            filter_info = ""
            if filter_type == "Year" and selected_year:
                filter_info = f" | Filtered: {selected_year}"
            elif filter_type == "Date Range" and start_date and end_date:
                filter_info = f" | Filtered: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            
            with st.expander(f"📦 {result['article']} - {result['product_name']} | {filtered_count} orders (of {result['orders_count']}){filter_info} | Found by: {result['match_type']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Article Number:** {result['article']}")
                    st.markdown(f"**Product Name:** {result['product_name']}")
                with col2:
                    st.markdown(f"**Orders in Filter:** {filtered_count}")
                    if filtered_min_price and filtered_max_price:
                        st.markdown(f"**Price Range:** ${filtered_min_price:.2f} - ${filtered_max_price:.2f}/kg")
                    elif result['min_price'] and result['max_price'] and filtered_count == 0:
                        st.markdown(f"**Price Range:** No orders in selected date range")
                    elif result['min_price'] and result['max_price']:
                        st.markdown(f"**Price Range:** ${result['min_price']:.2f} - ${result['max_price']:.2f}/kg (all time)")
                
                if not filtered_orders:
                    st.info(f"No orders found in the selected date range. Total orders available: {result['orders_count']}")
                else:
                    st.markdown("---")
                    st.markdown("**Order History (Filtered)**")
                    
                    for idx, order in enumerate(filtered_orders):
                        price_display = order.get('price', 'N/A')
                        try:
                            price_value = float(str(price_display).replace('$', '').replace(',', '').strip())
                            price_display = f"${price_value:.2f}"
                        except:
                            price_display = f"${price_display}" if price_display != 'N/A' else 'N/A'
                        
                        st.markdown(f"""
                        <div class="price-card-primary" style="margin-bottom: 0.5rem;">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <strong>Order:</strong> {order.get('order_no', 'N/A')}<br>
                                    <strong>Date:</strong> {order.get('date', 'N/A')}
                                </div>
                                <div>
                                    <strong>Price:</strong> {price_display}/kg
                                </div>
                            </div>
                            <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #64748b;">
                                {order.get('quantity', 'N/A')} units • {order.get('total_weight', 'N/A')} kg
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    elif not search_term:
        st.info("Enter a search term above to find order history")

# ============================================
# ALL PRICES TAB
# ============================================

def all_prices_tab():
    """All Prices Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #7c3aed, #6d28d9); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📊 All Items Price Database</h2>
        <p style="margin:0; opacity:0.9; color: white;">Complete item catalog • Pricing information • Category analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Loading all prices data..."):
        prices_data = load_general_prices_data()
    
    if prices_data.empty:
        st.warning("General_prices data not found or empty")
        return
    
    st.success(f"Loaded {len(prices_data)} items")
    
    # Overview Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Items", len(prices_data))
    
    if 'CATEG.' in prices_data.columns:
        col2.metric("Categories", prices_data['CATEG.'].nunique())
    
    if 'NEW EXW' in prices_data.columns:
        col3.metric("Avg Price", f"${prices_data['NEW EXW'].mean():.2f}")
        col4.metric("Price Range", f"${prices_data['NEW EXW'].min():.2f} - ${prices_data['NEW EXW'].max():.2f}")
    
    # Search
    st.markdown("<div class='subsection-header'>🔍 Search & Filter</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("Search by article, description, or any field:", placeholder="Enter search term...", key="all_prices_search")
    with col2:
        if 'CATEG.' in prices_data.columns:
            category_filter = st.selectbox("Category:", ["All"] + sorted(prices_data['CATEG.'].dropna().unique().tolist()), key="all_prices_category")
        else:
            category_filter = "All"
    
    filtered_data = prices_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_data = filtered_data[mask]
    
    if category_filter != "All" and 'CATEG.' in prices_data.columns:
        filtered_data = filtered_data[filtered_data['CATEG.'] == category_filter]
    
    st.markdown(f"<div class='subsection-header'>📋 Items Found: {len(filtered_data)}</div>", unsafe_allow_html=True)
    
    if not filtered_data.empty:
        for _, item in filtered_data.head(20).iterrows():
            with st.expander(f"{item.get('ART#', 'N/A')} - {item.get('DESCRIPTION', 'N/A')}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Article:** {item.get('ART#', 'N/A')}")
                    st.markdown(f"**Description:** {item.get('DESCRIPTION', 'N/A')}")
                    st.markdown(f"**Category:** {item.get('CATEG.', 'N/A')}")
                with col2:
                    if 'NEW EXW' in item and pd.notna(item.get('NEW EXW')):
                        st.markdown(f"**Price:** <span style='font-size: 1.25rem; font-weight: 700; color: #059669;'>${item['NEW EXW']:.2f}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Unit Weight:** {item.get('UNT WGT', 'N/A')}")
                    st.markdown(f"**UOM:** {item.get('UOM', 'N/A')}")
        
        if len(filtered_data) > 20:
            st.info(f"Showing 20 of {len(filtered_data)} items. Use filters to narrow down results.")

# ============================================
# ORIGINAL TAB FUNCTIONS (Preserved)
# ============================================

def clients_tab():
    """Clients management tab"""
    st.markdown("<div class='subsection-header'>Client Selection</div>", unsafe_allow_html=True)
    
    available_clients = st.session_state.user_clients
    client = st.selectbox("Select Client:", available_clients, key="client_select")
    
    if client:
        cdc_dashboard(client)

def cdc_dashboard(client):
    """Client pricing dashboard"""
    
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'export_data' not in st.session_state:
        st.session_state.export_data = None
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #991b1b, #7f1d1d); padding: 1rem 1.25rem; border-radius: 12px; margin-bottom: 1rem;">
        <h2 style="margin:0; color: white;">📊 {client} Pricing Dashboard</h2>
        <p style="margin:0; opacity:0.9; color: white;">Smart search • History • Favorites</p>
    </div>
    """, unsafe_allow_html=True)

    DATA = get_google_sheets_data(client)
    st.success(f"Connected to live data for {client}")
    
    if st.button("🔄 Refresh Data", use_container_width=True, key=f"{client}_refresh"):
        st.rerun()

    st.markdown("<div class='subsection-header'>Select Supplier</div>", unsafe_allow_html=True)
    supplier = st.radio("", ["Backaldrin", "Bateel"], horizontal=True, label_visibility="collapsed", key=f"{client}_supplier")

    st.markdown("<div class='subsection-header'>🔍 Smart Search</div>", unsafe_allow_html=True)
    
    search_container = st.container()
    
    with search_container:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search_input = st.text_input("Search by Article, Product, or HS Code:", placeholder="Start typing for smart suggestions...", key=f"{client}_smart_search")
        with col2:
            search_type = st.selectbox("Search Type", ["All", "Article", "Product", "HS Code"], key=f"{client}_search_type")
        with col3:
            if st.button("🔍 Smart Search", use_container_width=True, type="primary", key=f"{client}_smart_search_btn"):
                if search_input:
                    add_to_search_history(search_input, client, supplier)
                    handle_search(search_input, "", "", supplier, DATA, client)
    
    if search_input and len(search_input) >= 2:
        supplier_data = DATA.get(supplier, {})
        suggestions = get_smart_suggestions(search_input, supplier_data, search_type)
        
        if suggestions:
            st.markdown("**Smart Suggestions (click to select):**")
            for i, sugg in enumerate(suggestions[:5]):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"{sugg['article']} - {sugg['name']}", key=f"smart_{i}", use_container_width=True):
                        st.session_state.search_results = {
                            "article": sugg["article"],
                            "supplier": supplier,
                            "client": client
                        }
                        article_data = DATA[supplier].get(sugg["article"], {})
                        st.session_state.export_data = create_export_data(article_data, sugg["article"], supplier, client)
                        add_to_search_history(search_input, client, supplier, sugg["article"])
                        st.rerun()
                with col2:
                    st.markdown(f"<span class='badge-info'>{sugg['score']}</span>", unsafe_allow_html=True)
    
    with st.form(key=f"{client}_search_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            article = st.text_input("Article Number", placeholder="e.g., 1-366, 1-367...", key=f"{client}_article")
        with col2:
            product = st.text_input("Product Name", placeholder="e.g., Moist Muffin, Date Mix...", key=f"{client}_product")
        with col3:
            hs_code = st.text_input("HS Code", placeholder="e.g., 1901200000, 180690...", key=f"{client}_hscode")
        
        submitted = st.form_submit_button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary")
        
        if submitted:
            search_term = article or product or hs_code
            if search_term:
                add_to_search_history(search_term, client, supplier)
                handle_search(article, product, hs_code, supplier, DATA, client)

    if st.session_state.search_results and st.session_state.search_results.get("client") == client:
        display_from_session_state(DATA, client)

def handle_search(article, product, hs_code, supplier, data, client):
    """Handle search across article, product name, and HS code"""
    search_term = article or product or hs_code
    if not search_term:
        st.error("Please enter an article number, product name, or HS code")
        return
    
    found = False
    found_article = None
    
    for article_num, article_data in data[supplier].items():
        article_match = article and article == article_num
        product_match = product and any(product.lower() in name.lower() for name in article_data['names'])
        hs_code_match = hs_code and any(
            hs_code.lower() in str(order.get('hs_code', '')).lower() 
            for order in article_data['orders']
        )
        
        if article_match or product_match or hs_code_match:
            st.session_state.search_results = {
                "article": article_num,
                "supplier": supplier,
                "client": client
            }
            st.session_state.export_data = create_export_data(article_data, article_num, supplier, client)
            found = True
            found_article = article_num
            break
    
    if found:
        add_to_search_history(search_term, client, supplier, found_article)
    else:
        st.error(f"No results found for '{search_term}' in {supplier}")
        add_to_search_history(search_term, client, supplier)

def create_export_data(article_data, article, supplier, client):
    """Create export data"""
    export_data = []
    for order in article_data['orders']:
        export_data.append({
            'Client': client,
            'order_number': order.get('order_no', ''),
            'order_date': order.get('date', ''),
            'year': order.get('year', ''),
            'product_name': order.get('product_name', ''),
            'article_number': article,
            'hs_code': order.get('hs_code', ''),
            'packaging': order.get('packaging', ''),
            'quantity': order.get('quantity', ''),
            'total_weight': order.get('total_weight', ''),
            'price_per_': order.get('price', ''),
            'total_price': order.get('total_price', ''),
            'Supplier': supplier,
            'Export_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(export_data)

def display_from_session_state(data, client):
    """Display search results"""
    results = st.session_state.search_results
    article = results["article"]
    supplier = results["supplier"]
    
    if article not in data[supplier]:
        st.error("Article not found in current data")
        return
        
    article_data = data[supplier][article]
    
    search_term = ""
    for key in [f"{client}_article", f"{client}_product", f"{client}_hscode", f"{client}_smart_search"]:
        if key in st.session_state:
            search_term = st.session_state[key]
            if search_term:
                break
    
    is_favorited = is_search_favorited(search_term, client, supplier)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"**Article {article}** found in **{supplier}** for **{client}**")
    with col2:
        if is_favorited:
            if st.button("⭐ Remove Favorite", key="remove_fav", use_container_width=True):
                remove_search_from_favorites(search_term, client, supplier)
                st.rerun()
        else:
            if st.button("☆ Add to Favorites", key="add_fav", use_container_width=True):
                if save_search_to_favorites(search_term, client, supplier, article):
                    st.success("Added to favorites!")
                    st.rerun()
    
    st.markdown("<div class='subsection-header'>📝 Product Name</div>", unsafe_allow_html=True)
    
    most_recent_name = ""
    orders = article_data.get('orders', [])
    if orders:
        try:
            orders_with_dates = []
            for order in orders:
                date_str = order.get('date', '')
                if date_str:
                    for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d %b %Y', '%d %B %Y']:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt)
                            orders_with_dates.append((parsed_date, order))
                            break
                        except:
                            continue
            orders_with_dates.sort(key=lambda x: x[0], reverse=True)
            if orders_with_dates:
                most_recent_name = orders_with_dates[0][1].get('product_name', '')
        except:
            most_recent_name = orders[0].get('product_name', '')
    
    if not most_recent_name and article_data['names']:
        most_recent_name = article_data['names'][0]
    
    st.markdown(f'<div class="price-card-primary">{most_recent_name}</div>', unsafe_allow_html=True)
    
    prices = article_data['prices']
    orders = article_data.get('orders', [])
    
    st.markdown("<div class='subsection-header'>📊 Price Statistics</div>", unsafe_allow_html=True)
    
    total_records = len(prices)
    
    last_sold_price = None
    second_last_price = None
    
    if orders and prices:
        try:
            order_price_list = []
            for order in orders:
                price_str = order.get('price', '')
                date_str = order.get('date', '')
                
                if price_str and date_str:
                    try:
                        price = float(str(price_str).replace('$', '').replace(',', '').strip())
                        parsed_date = None
                        for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d %b %Y', '%d %B %Y']:
                            try:
                                parsed_date = datetime.strptime(date_str, fmt)
                                break
                            except:
                                continue
                        if parsed_date:
                            order_price_list.append((parsed_date, price))
                    except:
                        continue
            order_price_list.sort(key=lambda x: x[0], reverse=True)
            if len(order_price_list) > 0:
                last_sold_price = order_price_list[0][1]
            if len(order_price_list) > 1:
                second_last_price = order_price_list[1][1]
        except:
            if len(prices) > 0:
                last_sold_price = prices[-1]
            if len(prices) > 1:
                second_last_price = prices[-2]
    
    if last_sold_price is None and prices:
        last_sold_price = prices[-1] if prices else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_records}</div>
            <div class="stat-label">Total Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        price_display = f"${last_sold_price:.2f}" if last_sold_price is not None else "N/A"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{price_display}</div>
            <div class="stat-label">Last Sold Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        price_display = f"${second_last_price:.2f}" if second_last_price is not None else "N/A"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{price_display}</div>
            <div class="stat-label">Previous Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="font-size: 1.2rem;">${min_price:.2f} - ${max_price:.2f}</div>
                <div class="stat-label">Price Range/kg</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">N/A</div>
                <div class="stat-label">Price Range/kg</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div class='subsection-header'>💵 Historical Prices</div>", unsafe_allow_html=True)
    
    for i, order in enumerate(article_data['orders']):
        price_display = order.get('price', 'N/A')
        try:
            price_value = float(str(price_display).replace('$', '').replace(',', '').strip())
            price_display = f"${price_value:.2f}"
        except:
            price_display = f"${price_display}" if price_display != 'N/A' else 'N/A'
        
        with st.expander(f"📦 {order.get('order_no', 'N/A')} | 📅 {order.get('date', 'N/A')} | 💰 {price_display}/kg", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Product:** {order.get('product_name', 'N/A')}")
                st.markdown(f"**Article:** {order.get('article', 'N/A')}")
                if order.get('year'):
                    st.markdown(f"**Year:** {order['year']}")
                if order.get('hs_code'):
                    st.markdown(f"**HS Code:** {order['hs_code']}")
            with col2:
                if order.get('packaging'):
                    st.markdown(f"**Packaging:** {order['packaging']}")
                if order.get('quantity'):
                    st.markdown(f"**Quantity:** {order['quantity']}")
                if order.get('total_weight'):
                    st.markdown(f"**Total Weight:** {order['total_weight']}")
                if order.get('total_price'):
                    st.markdown(f"**Total Price:** {order['total_price']}")

def prices_tab():
    """All Customers Prices Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0ea5e9, #0284c7); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">💰 All Customers Prices</h2>
        <p style="margin:0; opacity:0.9; color: white;">Complete price database • Cross-customer analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Loading prices data..."):
        prices_data = load_prices_data()
    
    if prices_data.empty:
        st.warning("Prices data not found or empty")
        return
    
    st.success(f"Loaded {len(prices_data)} price records")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(prices_data))
    col2.metric("Unique Customers", prices_data['Customer'].nunique())
    col3.metric("Unique Items", prices_data['Item Code'].nunique())
    col4.metric("Average Price", f"${prices_data['Price'].mean():.2f}")
    
    st.markdown("<div class='subsection-header'>🔍 Advanced Search</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        customers = ["All"] + sorted(prices_data['Customer'].dropna().unique().tolist())
        selected_customer = st.selectbox("Customer:", customers, key="price_customer_filter")
    with col2:
        salesmen = ["All"] + sorted(prices_data['Salesman'].dropna().unique().tolist())
        selected_salesman = st.selectbox("Salesman:", salesmen, key="price_salesman_filter")
    with col3:
        min_price = float(prices_data['Price'].min())
        max_price = float(prices_data['Price'].max())
        price_range = st.slider("Price Range:", min_value=min_price, max_value=max_price, value=(min_price, max_price), key="price_range_filter")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        article_search = st.text_input("Article Number:", placeholder="Enter article number...", key="price_article_search")
    with col2:
        item_name_search = st.text_input("Item Name:", placeholder="Enter item name...", key="price_item_name_search")
    with col3:
        customer_article_search = st.text_input("Customer Article No:", placeholder="Enter customer article...", key="price_customer_article_search")
    
    global_search = st.text_input("Global Search:", placeholder="Search across all columns...", key="price_global_search")
    
    filtered_data = prices_data.copy()
    
    if selected_customer != "All":
        filtered_data = filtered_data[filtered_data['Customer'] == selected_customer]
    if selected_salesman != "All":
        filtered_data = filtered_data[filtered_data['Salesman'] == selected_salesman]
    
    filtered_data = filtered_data[(filtered_data['Price'] >= price_range[0]) & (filtered_data['Price'] <= price_range[1])]
    
    if article_search:
        filtered_data = filtered_data[filtered_data['Item Code'].astype(str).str.contains(article_search, case=False, na=False)]
    if item_name_search:
        filtered_data = filtered_data[filtered_data['Item Name'].astype(str).str.contains(item_name_search, case=False, na=False)]
    if customer_article_search:
        filtered_data = filtered_data[filtered_data['Customer Article No'].astype(str).str.contains(customer_article_search, case=False, na=False)]
    
    if global_search and not (article_search or item_name_search or customer_article_search):
        search_columns = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 'Customer Article No', 'Customer Label']
        mask = filtered_data[search_columns].astype(str).apply(lambda x: x.str.contains(global_search, case=False, na=False)).any(axis=1)
        filtered_data = filtered_data[mask]
    
    st.markdown(f"<div class='subsection-header'>📋 Price Records ({len(filtered_data)} found)</div>", unsafe_allow_html=True)
    
    if not filtered_data.empty:
        for _, record in filtered_data.iterrows():
            with st.expander(f"💰 {record['Item Code']} - {record['Item Name']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Customer:** {record['Customer']}")
                    st.markdown(f"**Customer Name:** {record['Customer Name']}")
                    st.markdown(f"**Salesman:** {record['Salesman']}")
                with col2:
                    st.markdown(f"**Item Code:** {record['Item Code']}")
                    st.markdown(f"**Customer Article No:** {record['Customer Article No']}")
                    st.markdown(f"**Packing:** {record['Packing/kg']}")
                    st.markdown(f"**Price:** <span style='font-size: 1.25rem; font-weight: 700; color: #059669;'>${record['Price']:.2f}</span>", unsafe_allow_html=True)

def etd_tab():
    """ETD Sheet Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #059669, #047857); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📅 ETD Management Dashboard</h2>
        <p style="margin:0; opacity:0.9; color: white;">Live order tracking • Multi-supplier ETD</p>
    </div>
    """, unsafe_allow_html=True)

    ETD_SHEET_ID = "1eA-mtD3aK_n9VYNV_bxnmqm58IywF0f5-7vr3PT51hs"
    AVAILABLE_MONTHS = ["October 2025 ", "November 2025 "]

    try:
        selected_month = st.radio("Select month:", AVAILABLE_MONTHS, horizontal=True, key="etd_month_selector")
        
        with st.spinner(f"Loading {selected_month.strip()} ETD data..."):
            etd_data = load_etd_data(ETD_SHEET_ID, selected_month)
        
        if etd_data.empty:
            st.warning(f"No ETD data found in {selected_month}")
            return

        st.success(f"Connected to {selected_month.strip()}! Loaded {len(etd_data)} orders")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Orders", len(etd_data))
        col2.metric("Shipped", len(etd_data[etd_data['Status'].str.lower() == 'shipped']))
        col3.metric("In Production", len(etd_data[etd_data['Status'].str.lower().str.contains('production', na=False)]))
        col4.metric("Pending", len(etd_data[etd_data['Status'].str.lower().str.contains('pending', na=False)]))
        
        need_etd = len(etd_data[
            (etd_data['ETD _ Backaldrine'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
            (etd_data['ETD_bateel'].astype(str).str.contains('NEED ETD', case=False, na=False))
        ])
        col5.metric("Need ETD", need_etd)

        st.markdown("<div class='subsection-header'>🔍 Filter Orders</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            client_filter = st.selectbox("Client", ["All"] + sorted(etd_data['Client Name'].dropna().unique()), key="etd_client_filter")
        with col2:
            status_filter = st.selectbox("Status", ["All", "Shipped", "In Production", "Pending", "Need ETD"], key="etd_status_filter")
        with col3:
            search_term = st.text_input("Search Order No...", key="etd_search")

        filtered_data = etd_data.copy()
        
        if client_filter != "All":
            filtered_data = filtered_data[filtered_data['Client Name'] == client_filter]
        
        if status_filter != "All":
            if status_filter == "Need ETD":
                filtered_data = filtered_data[
                    (filtered_data['ETD _ Backaldrine'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (filtered_data['ETD_bateel'].astype(str).str.contains('NEED ETD', case=False, na=False))
                ]
            else:
                filtered_data = filtered_data[filtered_data['Status'] == status_filter]
        
        if search_term:
            filtered_data = filtered_data[filtered_data['Order No.'].astype(str).str.contains(search_term, case=False, na=False)]

        st.markdown(f"<div class='subsection-header'>📋 {selected_month.strip()} Orders ({len(filtered_data)} found)</div>", unsafe_allow_html=True)
        
        if not filtered_data.empty:
            for _, order in filtered_data.iterrows():
                display_etd_order_card(order, selected_month.strip())
        else:
            st.info("No orders match your filter criteria.")

    except Exception as e:
        st.error(f"Error loading ETD data: {str(e)}")

def display_etd_order_card(order, month):
    """Display ETD order card"""
    status = order.get('Status', 'Unknown')
    status_color = {'Shipped': '🟢', 'In Production': '🟡', 'Pending': '🟠'}.get(status, '⚫')
    
    needs_etd = []
    for supplier in ['Backaldrine', 'bateel']:
        etd_col = f"ETD _{supplier}" if supplier != 'bateel' else 'ETD_bateel'
        etd_value = order.get(etd_col, '')
        if pd.notna(etd_value) and 'NEED ETD' in str(etd_value).upper():
            needs_etd.append(supplier)
    
    with st.expander(f"{status_color} {order.get('Order No.', 'N/A')} - {order.get('Client Name', 'N/A')} | {month}", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Client:** {order.get('Client Name', 'N/A')}")
            st.markdown(f"**Employee:** {order.get('Concerned Employee', 'N/A')}")
        with col2:
            st.markdown(f"**Status:** {status}")
            st.markdown(f"**Confirmation:** {order.get('Confirmation Date', 'N/A')}")
        with col3:
            if needs_etd:
                st.markdown(f"<span class='badge-danger'>NEED ETD: {', '.join(needs_etd)}</span>", unsafe_allow_html=True)
            st.markdown(f"**Loading:** {order.get('Scheduled Date For Loading', 'N/A')}")
        
        st.markdown("---")
        st.markdown("**Supplier ETD Status**")
        
        for supplier in ['Backaldrine', 'bateel']:
            etd_col = f"ETD _{supplier}" if supplier != 'bateel' else 'ETD_bateel'
            order_col = f"{supplier} Order #" if supplier != 'bateel' else 'bateel Order #'
            etd_value = order.get(etd_col, '')
            order_value = order.get(order_col, '')
            
            if pd.isna(etd_value) or str(etd_value).strip() == '':
                st.markdown(f"**{supplier}:** ❌ No ETD")
            elif 'NEED ETD' in str(etd_value).upper():
                st.markdown(f"**{supplier}:** <span class='badge-danger'>NEED ETD</span>", unsafe_allow_html=True)
            elif 'READY' in str(etd_value).upper():
                st.markdown(f"**{supplier}:** <span class='badge-success'>Ready</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**{supplier}:** 📅 {etd_value}")
            
            if pd.notna(order_value) and str(order_value).strip() != '':
                st.caption(f"Order: {order_value}")

def ceo_specials_tab():
    """CEO Special Prices Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #d97706, #b45309); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">⭐ CEO Special Prices</h2>
        <p style="margin:0; opacity:0.9; color: white;">Exclusive pricing • Limited time offers • VIP client rates</p>
    </div>
    """, unsafe_allow_html=True)
    
    available_clients = st.session_state.user_clients
    client = st.selectbox("Select Client:", available_clients, key="ceo_client_select")
    
    if not client:
        st.warning("No clients available")
        return
    
    ceo_data = load_ceo_special_prices(client)
    
    if ceo_data.empty:
        st.warning(f"No CEO special prices found for {client}")
        return
     
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Special Offers", len(ceo_data))
    col2.metric("Active Offers", len(ceo_data[ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')]))
    col3.metric("Currencies", ceo_data['Currency'].nunique())
    col4.metric("Expiring Soon", len(ceo_data[(ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')) & (ceo_data['Expiry_Date'] <= (datetime.now() + pd.Timedelta(days=30)).strftime('%Y-%m-%d'))]))
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("Search by article or product name...", key="ceo_search")
    with col2:
        show_active = st.checkbox("Show Active Only", value=True, key="ceo_active")
    
    filtered_data = ceo_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_data = filtered_data[mask]
    if show_active:
        filtered_data = filtered_data[filtered_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')]
    
    st.markdown(f"<div class='subsection-header'>🎯 {client} Special Price List</div>", unsafe_allow_html=True)
    
    if not filtered_data.empty:
        for _, special in filtered_data.iterrows():
            is_active = special['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')
            status_color = "🟢 Active" if is_active else "🔴 Expired"
            
            try:
                price_display = f"{float(special['Special_Price']):.2f}"
            except:
                price_display = str(special['Special_Price'])
            
            st.markdown(f"""
            <div class="price-card-secondary">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{special['Article_Number']} - {special['Product_Name']}</strong>
                        <div style="font-size: 1.1rem; font-weight: 700; color: #b45309;">Special Price: {price_display} {special['Currency']}/kg</div>
                        <div style="font-size: 0.8rem; color: #64748b;">{status_color} • Valid until: {special['Expiry_Date']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def price_intelligence_tab():
    """CEO Price Intelligence Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #059669, #047857); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">💰 CEO Price Intelligence</h2>
        <p style="margin:0; opacity:0.9; color: white;">Cross-client price comparison • Market intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    available_clients = st.session_state.user_clients
    
    if len(available_clients) < 2:
        st.warning(f"You need access to at least 2 clients to compare prices. Current access: {', '.join(available_clients)}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        client_selection = st.multiselect("Select clients to analyze:", options=available_clients, default=available_clients, key="intelligence_clients")
    with col2:
        search_term = st.text_input("Article or product name:", placeholder="e.g., 281, Chocolate...", key="intelligence_search")
    
    if st.button("Analyze Prices", use_container_width=True, type="primary", key="intelligence_analyze"):
        if search_term and client_selection:
            analyze_cross_client_prices(search_term, client_selection, "All")
        else:
            if not search_term:
                st.error("Please enter an article number or product name")
            if not client_selection:
                st.error("Please select at least one client")

def analyze_cross_client_prices(search_term, selected_clients, supplier_filter="All"):
    """Analyze prices across selected clients"""
    st.markdown(f"<div class='subsection-header'>Analysis Results: '{search_term}'</div>", unsafe_allow_html=True)
    
    all_results = {}
    total_records = 0
    found_articles = set()
    all_prices = []
    
    for client in selected_clients:
        client_data = get_google_sheets_data(client)
        
        for supplier in ["Backaldrin", "Bateel"]:
            if supplier_filter != "All" and supplier != supplier_filter:
                continue
                
            supplier_data = client_data[supplier]
            client_results = []
            
            for article_num, article_data in supplier_data.items():
                article_match = search_term.lower() in article_num.lower()
                product_match = any(search_term.lower() in name.lower() for name in article_data['names'])
                
                if article_match or product_match:
                    found_articles.add(article_num)
                    if article_data['prices']:
                        avg_price = sum(article_data['prices']) / len(article_data['prices'])
                        min_price = min(article_data['prices'])
                        max_price = max(article_data['prices'])
                        all_prices.extend(article_data['prices'])
                        
                        client_results.append({
                            'article': article_num,
                            'product_names': list(set(article_data['names'])),
                            'avg_price': avg_price,
                            'min_price': min_price,
                            'max_price': max_price,
                            'records': len(article_data['prices']),
                            'supplier': supplier,
                            'all_prices': article_data['prices'],
                            'orders': article_data['orders'],
                            'has_data': True
                        })
                        total_records += len(article_data['prices'])
                    else:
                        client_results.append({
                            'article': article_num,
                            'product_names': list(set(article_data['names'])),
                            'avg_price': None,
                            'min_price': None,
                            'max_price': None,
                            'records': 0,
                            'supplier': supplier,
                            'all_prices': [],
                            'orders': [],
                            'has_data': False
                        })
            
            all_results[f"{client} - {supplier}"] = client_results
    
    if not found_articles:
        st.warning(f"No results found for '{search_term}'")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Price Records", total_records)
    if all_prices:
        col2.metric("Price Range", f"${max(all_prices) - min(all_prices):.2f}/kg")
        col3.metric("Lowest Price", f"${min(all_prices):.2f}/kg")
        col4.metric("Highest Price", f"${max(all_prices):.2f}/kg")
    
    st.markdown("<div class='subsection-header'>Client-by-Client Comparison</div>", unsafe_allow_html=True)
    
    articles_data = {}
    for client_supplier, results in all_results.items():
        client_name, supplier_name = client_supplier.split(" - ")
        for result in results:
            article_num = result['article']
            if article_num not in articles_data:
                articles_data[article_num] = {'product_names': result['product_names'], 'client_data': {}}
            articles_data[article_num]['client_data'][client_supplier] = result
    
    for article_num, article_data in articles_data.items():
        st.markdown(f"### 📦 Article: {article_num}")
        st.caption(f"Product: {', '.join(article_data['product_names'])}")
        
        comparison_data = []
        for client_supplier in all_results.keys():
            result = article_data['client_data'].get(client_supplier)
            client_name, supplier_name = client_supplier.split(" - ")
            
            if result and result['has_data']:
                comparison_data.append({
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min Price': f"${result['min_price']:.2f}",
                    'Max Price': f"${result['max_price']:.2f}",
                    'Records': result['records']
                })
            else:
                comparison_data.append({
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min Price': "N/A",
                    'Max Price': "N/A",
                    'Records': 0
                })
        
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

def product_catalog_tab():
    """Product Catalog Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0ea5e9, #0284c7); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📦 Full Product Catalog</h2>
        <p style="margin:0; opacity:0.9; color: white;">Complete product database • Technical specifications</p>
    </div>
    """, unsafe_allow_html=True)
    
    catalog_data = load_product_catalog()
    
    if catalog_data.empty:
        st.warning("Product catalog not found or empty")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", len(catalog_data))
    if 'Supplier' in catalog_data.columns:
        col2.metric("Suppliers", catalog_data['Supplier'].nunique())
    if 'Category' in catalog_data.columns:
        col3.metric("Categories", catalog_data['Category'].nunique())
    col4.metric("Unique Articles", catalog_data['Article_Number'].nunique())
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("Search by article, product name, or description...", key="catalog_search")
    with col2:
        if 'Supplier' in catalog_data.columns:
            supplier_filter = st.selectbox("Supplier", ["All"] + list(catalog_data['Supplier'].unique()), key="catalog_supplier")
        else:
            supplier_filter = "All"
    
    filtered_data = catalog_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_data = filtered_data[mask]
    if supplier_filter != "All" and 'Supplier' in catalog_data.columns:
        filtered_data = filtered_data[filtered_data['Supplier'] == supplier_filter]
    
    st.markdown(f"<div class='subsection-header'>📋 Products Found: {len(filtered_data)}</div>", unsafe_allow_html=True)
    
    if not filtered_data.empty:
        for _, product in filtered_data.iterrows():
            card_class = "price-card-primary" if product.get('Supplier') == 'Backaldrin' else "price-card-secondary"
            with st.expander(f"📦 {product['Article_Number']} - {product['Product_Name']}", expanded=False):
                st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Article Number:** {product['Article_Number']}")
                    st.markdown(f"**Product Name:** {product['Product_Name']}")
                    if 'Supplier' in product:
                        st.markdown(f"**Supplier:** {product['Supplier']}")
                with col2:
                    if 'Category' in product and product['Category']:
                        st.markdown(f"**Category:** {product['Category']}")
                    if 'UOM' in product and product['UOM']:
                        st.markdown(f"**UOM:** {product['UOM']}")
                    if 'Current_Price' in product and product['Current_Price']:
                        st.markdown(f"**Price:** ${product['Current_Price']}/kg")
                if 'Common_Description' in product and product['Common_Description']:
                    st.markdown(f"**Description:** {product['Common_Description']}")
                st.markdown('</div>', unsafe_allow_html=True)

def palletizing_tab():
    """Palletizing Tab"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #7c3aed, #6d28d9); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin:0; color: white;">📦 Quick Pallet Calculator</h2>
        <p style="margin:0; opacity:0.9; color: white;">Instant pallet calculations • CDC standard items</p>
    </div>
    """, unsafe_allow_html=True)
    
    quick_pallet_calculator()

def quick_pallet_calculator():
    """Quick Pallet Calculator"""
    cdc_items = {
        "Vermicelli Color": {"packing": "5kg", "cartons_per_pallet": 100, "weight_per_carton": 5},
        "Vermicelli Dark": {"packing": "5kg", "cartons_per_pallet": 100, "weight_per_carton": 5},
        "Vermicelli White": {"packing": "5kg", "cartons_per_pallet": 100, "weight_per_carton": 5},
        "Chocolate Chips": {"packing": "25kg", "cartons_per_pallet": 40, "weight_per_carton": 25},
        "Date Mix": {"packing": "30kg", "cartons_per_pallet": 36, "weight_per_carton": 30},
        "Vanilla Powder": {"packing": "15kg", "cartons_per_pallet": 60, "weight_per_carton": 15},
        "Custom Item": {"packing": "Custom", "cartons_per_pallet": 0, "weight_per_carton": 0}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_item = st.selectbox("Select Item:", list(cdc_items.keys()), key="item_select")
        quantity = st.number_input("Quantity:", min_value=1, value=100, step=1, key="quantity")
        uom = st.selectbox("Unit of Measure:", ["Cartons", "KGs", "Pallets"], key="uom")
    
    with col2:
        if selected_item == "Custom Item":
            st.info("Enter custom item details:")
            packing = st.text_input("Packing:", value="5kg", key="custom_packing")
            cartons_per_pallet = st.number_input("Cartons per Pallet:", min_value=1, value=100, step=1, key="custom_cartons")
            weight_per_carton = st.number_input("Weight per Carton (kg):", min_value=0.1, value=5.0, step=0.1, key="custom_weight")
        else:
            item_data = cdc_items[selected_item]
            packing = item_data["packing"]
            cartons_per_pallet = item_data["cartons_per_pallet"]
            weight_per_carton = item_data["weight_per_carton"]
            st.info(f"**Standard Packing:** {packing}")
            st.info(f"**Cartons per Pallet:** {cartons_per_pallet}")
            st.info(f"**Weight per Carton:** {weight_per_carton} kg")
    
    if quantity > 0:
        if uom == "Cartons":
            total_cartons = quantity
        elif uom == "KGs":
            total_cartons = quantity / weight_per_carton
        else:
            total_cartons = quantity * cartons_per_pallet
        
        full_pallets = total_cartons // cartons_per_pallet
        partial_pallet_cartons = total_cartons % cartons_per_pallet
        partial_pallet_percentage = (partial_pallet_cartons / cartons_per_pallet) * 100 if cartons_per_pallet > 0 else 0
        total_weight = total_cartons * weight_per_carton
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{full_pallets:,.0f}</div>
                <div class="stat-label">Full Pallets</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{partial_pallet_cartons:,.0f}</div>
                <div class="stat-label">Partial Cartons</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{total_weight:,.0f} kg</div>
                <div class="stat-label">Total Weight</div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("View Details", expanded=False):
            st.write(f"**Item:** {selected_item} ({packing})")
            st.write(f"**Calculation:** {total_cartons:,.0f} cartons ÷ {cartons_per_pallet} cartons/pallet")
            st.write(f"**Result:** {full_pallets:,.0f} full pallets + {partial_pallet_cartons:,.0f} cartons ({partial_pallet_percentage:.1f}% of a pallet)")
        
        st.info(f"**Container Info:** 40ft container holds 30 pallets max. Your order fills {(full_pallets / 30 * 100):.1f}% of container capacity.")

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
