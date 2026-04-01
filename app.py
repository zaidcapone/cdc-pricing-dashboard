# ============================================
# MULTI-CLIENT PRICING DASHBOARD
# ============================================
# Author: Zaid F. Al-Shami
# Version: 3.3 (Streamlined Version - Removed Unused Tabs)
# Last Updated: 01 April 2026
# ============================================
# REMOVED TABS (Keep for reference - can be restored):
# 
# 1. 📋 NEW ORDERS TAB - Removed on 01 April 2026
#    - Function: new_orders_tab()
#    - Purpose: Client Orders Management for order preparation and PI generation
#    - Restoration: Add back the new_orders_tab() function and add tab to tabs list
#
# 2. 📊 ORDERS MANAGEMENT TAB - Removed on 01 April 2026
#    - Function: orders_management_tab()
#    - Purpose: Order tracking with status monitoring and payment updates
#    - Restoration: Add back orders_management_tab() function and add tab to tabs list
#
# 3. 🔴 PRICE MATCHING TAB - Removed on 01 April 2026
#    - Function: price_matching_tab()
#    - Purpose: PI Price Validation Tool with historical price comparison
#    - Restoration: Add back price_matching_tab() function and add tab to tabs list
#
# 4. 📈 VISUAL ANALYTICS TAB - Removed on 01 April 2026
#    - Function: visual_analytics_tab()
#    - Purpose: Interactive charts, price trends, and visual analysis
#    - Restoration: Add back visual_analytics_tab() function and add tab to tabs list
#
# 5. 📊 ITEM ANALYSIS TAB - Removed on 01 April 2026
#    - Function: item_analysis_tab()
#    - Purpose: Advanced item analysis with month-over-month and YoY growth
#    - Restoration: Add back item_analysis_tab() function and add tab to tabs list
#
# ============================================
# IMPORTANT NOTES:
# 1. This dashboard connects to Google Sheets for real-time data
# 2. All data is cached for 5 minutes to improve performance
# 3. Supports multiple clients: CDC, CoteDivoire, CakeArt, SweetHouse, Cameron, Qzine, MEPT
# 4. Features: Smart Search, Price Intelligence, Palletizing, Client Orders Search
# 5. Client's Orders tab - Fetches data directly from Clients_CoC sheet
# ============================================

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO
import re

# Page config
st.set_page_config(
    page_title="Multi-Client Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for main dashboard
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #991B1B, #7F1D1D);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cdc-header {
        background: linear-gradient(135deg, #991B1B, #7F1D1D);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .ceo-header {
        background: linear-gradient(135deg, #D97706, #B45309);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .intelligence-header {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .visual-header {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .palletizing-header {
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .price-matching-header {
        background: linear-gradient(135deg, #DC2626, #B91C1C);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .clients-orders-header {
        background: linear-gradient(135deg, #0891B2, #0E7C8C);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .price-card {
        background: linear-gradient(135deg, #FEE2E2, #FECACA);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #991B1B;
        margin: 0.5rem 0;
        color: #1F2937;
        font-weight: 500;
    }
    .special-price-card {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #D97706;
        margin: 0.5rem 0;
        color: #1F2937;
        font-weight: 500;
        border: 2px solid #D97706;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #991B1B;
        text-align: center;
        color: #1F2937;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .intelligence-stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #059669;
        text-align: center;
        color: #1F2937;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .pallet-stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #7C3AED;
        text-align: center;
        color: #1F2937;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #991B1B;
        margin: 0;
    }
    .intelligence-stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #059669;
        margin: 0;
    }
    .pallet-stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #7C3AED;
        margin: 0;
    }
    .price-box {
        background: #991B1B;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    .intelligence-price-box {
        background: #059669;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    .special-price-box {
        background: #D97706;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
        border: 2px solid #B45309;
    }
    .order-info {
        background: #F3F4F6;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        font-size: 0.8em;
        color: #6B7280;
    }
    .export-section {
        background: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #0EA5E9;
        margin: 1rem 0;
    }
    .ceo-section {
        background: #FFFBEB;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #D97706;
        margin: 1rem 0;
    }
    .intelligence-section {
        background: #ECFDF5;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #059669;
        margin: 1rem 0;
    }
    .palletizing-section {
        background: #FAF5FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #7C3AED;
        margin: 1rem 0;
    }
    .price-matching-section {
        background: #FEF2F2;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #DC2626;
        margin: 1rem 0;
    }
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #991B1B;
    }
    .orders-header {
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .product-catalog-header {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .new-orders-header {
        background: linear-gradient(135deg, #DC2626, #B91C1C);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .prices-header {
        background: linear-gradient(135deg, #0EA5E9, #0284C7);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .search-suggestion {
        padding: 0.5rem 1rem;
        cursor: pointer;
        border-bottom: 1px solid #E5E7EB;
    }
    .search-suggestion:hover {
        background-color: #F3F4F6;
    }
    .history-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: #F9FAFB;
        border-radius: 6px;
        cursor: pointer;
    }
    .history-item:hover {
        background: #F3F4F6;
    }
    .favorite-badge {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        color: #92400E;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        border: 1px solid #FBBF24;
    }
    .time-ago {
        font-size: 0.75rem;
        color: #6B7280;
        margin-left: 0.5rem;
    }
    .sidebar-tab {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        border-left: 4px solid transparent;
    }
    .sidebar-tab:hover {
        background-color: #F3F4F6;
    }
    .sidebar-tab.active {
        background-color: #991B1B;
        color: white;
        border-left: 4px solid #FEF3C7;
    }
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .header-icons {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    .icon-button {
        padding: 0.5rem;
        border-radius: 6px;
        background: #F3F4F6;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .icon-button:hover {
        background: #E5E7EB;
    }
    .favorites-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 1000;
        min-width: 400px;
        max-height: 70vh;
        overflow-y: auto;
    }
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 999;
    }
    .validation-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #DC2626;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .match-badge {
        background: #D1FAE5;
        color: #065F46;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .mismatch-badge {
        background: #FEF3C7;
        color: #92400E;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .no-history-badge {
        background: #FEE2E2;
        color: #991B1B;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .decision-selector {
        background: #F0F9FF;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #0EA5E9;
    }
    .item-analysis-header {
        background: linear-gradient(135deg, #1E40AF, #1E3A8A);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .item-stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #1E40AF;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .item-stat-number {
        font-size: 1.8em;
        font-weight: bold;
        color: #1E40AF;
        margin: 0;
    }
    .comparison-card {
        background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #0EA5E9;
        margin: 1rem 0;
    }
    .all-prices-header {
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .all-prices-card {
        background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #7C3AED;
        margin: 1rem 0;
    }
    .all-prices-stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #7C3AED;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .all-prices-stat-number {
        font-size: 1.8em;
        font-weight: bold;
        color: #7C3AED;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
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
# FEATURE 1: SMART SEARCH WITH AI SUGGESTIONS
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
        
        # Article number exact match (highest priority)
        if search_lower == article_num.lower():
            score = 100
            match_type = "exact_article"
        # Article number partial match
        elif search_lower in article_num.lower():
            score = 80
            match_type = "partial_article"
        
        # Product name matching
        for name in article_data.get('names', []):
            name_lower = str(name).lower()
            if search_lower == name_lower:
                score = max(score, 90)
                match_type = "exact_product"
            elif search_lower in name_lower:
                score = max(score, 70)
                match_type = "partial_product"
        
        # HS Code matching
        for order in article_data.get('orders', []):
            hs_code = str(order.get('hs_code', '')).lower()
            if search_lower in hs_code:
                score = max(score, 60)
                match_type = "hs_code"
        
        # Add suggestion if score is above threshold
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
    
    # Sort by score (highest first) and remove duplicates
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    
    # Remove duplicates based on article number
    unique_suggestions = []
    seen_articles = set()
    for sugg in suggestions:
        if sugg["article"] not in seen_articles:
            unique_suggestions.append(sugg)
            seen_articles.add(sugg["article"])
    
    return unique_suggestions[:10]

# ============================================
# FEATURE 2: SEARCH HISTORY
# ============================================

def initialize_search_history():
    """Initialize search history in session state"""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'max_history_items' not in st.session_state:
        st.session_state.max_history_items = 20

def add_to_search_history(search_term, client, supplier, article_num=None):
    """Add a search to the history"""
    initialize_search_history()
    
    # Remove duplicates (keep only latest)
    st.session_state.search_history = [
        h for h in st.session_state.search_history 
        if not (h.get('search_term') == search_term and 
                h.get('client') == client and 
                h.get('supplier') == supplier)
    ]
    
    # Add new entry
    history_entry = {
        'timestamp': datetime.now(),
        'search_term': search_term,
        'client': client,
        'supplier': supplier,
        'article_num': article_num,
        'display_time': datetime.now().strftime("%H:%M")
    }
    
    st.session_state.search_history.insert(0, history_entry)
    
    # Keep only last N items
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

def display_search_history_sidebar():
    """Display search history in sidebar"""
    if not st.session_state.get('search_history'):
        return
    
    st.sidebar.markdown("### 🔍 Recent Searches")
    
    for i, history_item in enumerate(st.session_state.search_history[:5]):
        time_ago = format_time_ago(history_item['timestamp'])
        
        display_text = f"{history_item['search_term']}"
        if history_item.get('article_num'):
            display_text += f" → {history_item['article_num']}"
        
        is_favorite = False
        if 'favorite_searches' in st.session_state:
            for fav in st.session_state.favorite_searches:
                if (fav.get('search_term') == history_item['search_term'] and 
                    fav.get('client') == history_item['client'] and 
                    fav.get('supplier') == history_item['supplier']):
                    is_favorite = True
                    break
        
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            if st.sidebar.button(
                display_text, 
                key=f"hist_sidebar_{i}",
                use_container_width=True,
                help=f"{history_item['client']} • {history_item['supplier']} • {time_ago}"
            ):
                st.session_state[f"{history_item['client']}_article"] = history_item['search_term']
                st.session_state[f"{history_item['client']}_supplier"] = history_item['supplier']
                st.session_state.search_results = {
                    "article": history_item.get('article_num', history_item['search_term']),
                    "supplier": history_item['supplier'],
                    "client": history_item['client']
                }
                st.rerun()
        with col2:
            if is_favorite:
                st.sidebar.markdown("⭐")
    
    if len(st.session_state.search_history) > 5:
        if st.sidebar.button("View All History", use_container_width=True):
            st.session_state.show_full_history = True

# ============================================
# FEATURE 3: SAVED SEARCHES/FAVORITES
# ============================================

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
    
    # Check if already favorited
    for fav in st.session_state.favorite_searches:
        if (fav.get('search_term') == search_term and 
            fav.get('client') == client and 
            fav.get('supplier') == supplier):
            return False
    
    # Add to favorites
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
        # Create modal overlay
        st.markdown('<div class="modal-overlay"></div>', unsafe_allow_html=True)
        
        # Create modal content
        st.markdown("""
        <div class="favorites-modal">
    <h2 style="margin-top: 0; color: #991B1B;">&#9733; Favorite Searches</h2>
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
            if st.button("Clear All Favorites", use_container_width=True, type="secondary"):
                st.session_state.favorite_searches = []
                st.success("All favorites cleared!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# CACHED FUNCTIONS
# ============================================

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
                # Get headers from first row
                headers = values[start_row]
                headers_count = len(headers)
                
                # Get data rows
                rows = values[start_row + 1:] if len(values) > start_row + 1 else []
                
                # FORCE all rows to have exactly headers_count columns
                padded_rows = []
                for row in rows:
                    # If row has fewer columns, pad with empty strings
                    if len(row) < headers_count:
                        row = row + [''] * (headers_count - len(row))
                    # If row has more columns, trim to headers_count
                    elif len(row) > headers_count:
                        row = row[:headers_count]
                    padded_rows.append(row)
                
                # Create DataFrame
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
        # Load master sheet
        master_df = load_sheet_data("Clients_CoC")
        
        if master_df.empty:
            st.warning("⚠️ Clients_CoC sheet is empty or not found")
            return {"Backaldrin": {}, "Bateel": {}}
        
        # Filter by client
        client_df = master_df[master_df['Client'] == client].copy()
        
        if client_df.empty:
            st.warning(f"⚠️ No data found for client: {client}")
            return {"Backaldrin": {}, "Bateel": {}}
        
        # Process Backaldrin data
        backaldrin_df = client_df[client_df['Supplier'] == 'Backaldrin']
        bateel_df = client_df[client_df['Supplier'] == 'Bateel']
        
        def convert_df_to_dict(df):
            """Convert dataframe to article dictionary structure"""
            result = {}
            
            if df.empty:
                return result
            
            # Column names
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
            
            # Check if required columns exist
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
                
                # Product name
                product_name = str(row.get(product_col, '')).strip()
                if product_name and product_name != 'nan' and product_name not in result[article]['names']:
                    result[article]['names'].append(product_name)
                
                # Price
                price_str = str(row.get(price_col, '')).strip()
                if price_str and price_str != 'nan':
                    try:
                        price_float = float(price_str)
                        result[article]['prices'].append(price_float)
                    except:
                        pass
                
                # Order details
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
    """Load product catalog from Google Sheets - FLEXIBLE VERSION - CACHED"""
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
    """NEW: Load General_prices data from Google Sheets - CACHED"""
    try:
        prices_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{GENERAL_PRICES_SHEET}!A:Z?key={API_KEY}"
        response = requests.get(prices_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 0:
                # Get headers (first row)
                headers = values[0]
                
                # Get all data rows (skip header)
                rows = values[1:] if len(values) > 1 else []
                
                # Create DataFrame
                df = pd.DataFrame(rows, columns=headers)
                
                # Clean up column names (remove extra spaces)
                df.columns = [str(col).strip() for col in df.columns]
                
                # Convert numeric columns
                if 'NEW EXW' in df.columns:
                    df['NEW EXW'] = pd.to_numeric(df['NEW EXW'], errors='coerce')
                
                if 'UNT WGT' in df.columns:
                    df['UNT WGT'] = pd.to_numeric(df['UNT WGT'], errors='coerce')
                
                # Fill empty strings with NaN
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
        st.session_state.active_tab = "CLIENTS"
    
    return st.session_state.logged_in

def login_page():
    """Login page"""
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center; color: #991B1B;">🔐 Multi-Client Dashboard</h2>
        <p style="text-align: center; color: #6B7280;">Please login to continue</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if submit:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_clients = USERS[username]["clients"]
                st.success(f"✅ Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    st.markdown('</div>', unsafe_allow_html=True)

def logout_button():
    """Logout button in header"""
    if st.button("🚪 Logout", key="logout_header"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_clients = []
        st.rerun()

def main_dashboard():
    """Main dashboard with tabs in sidebar"""
    
    # Top Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 👤 Welcome, {st.session_state.username}")
    with col2:
        # Header icons
        icon_col1, icon_col2, icon_col3 = st.columns(3)
        with icon_col1:
            if st.button("⭐", key="favorites_icon", help="Favorites"):
                st.session_state.show_favorites_modal = True
        with icon_col2:
            if st.button("🔄", key="refresh_icon", help="Refresh"):
                st.cache_data.clear()
                st.rerun()
        with icon_col3:
            if st.button("🗑️", key="clear_cache_icon", help="Clear Cache"):
                st.cache_data.clear()
                st.success("✅ Cache cleared!")
                st.rerun()
    
    # Favorites Modal
    display_favorites_modal()
    
    # Sidebar with tabs
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        
        # Define tabs based on user role
        if st.session_state.username in ["ceo", "admin"]:
            tabs = [
                "🏢 CLIENTS",
                "💰 PRICES", 
                "📅 ETD SHEET",
                "⭐ CEO SPECIAL PRICES",
                "💰 PRICE INTELLIGENCE",
                "📦 PRODUCT CATALOG",
                "📦 PALLETIZING",
                "📊 ALL PRICES",
                "📋 CLIENT'S ORDERS"
            ]
        else:
            tabs = [
                "🏢 CLIENTS",
                "💰 PRICES", 
                "📅 ETD SHEET",
                "⭐ CEO SPECIAL PRICES",
                "💰 PRICE INTELLIGENCE",
                "📦 PRODUCT CATALOG",
                "📦 PALLETIZING",
                "📊 ALL PRICES",
                "📋 CLIENT'S ORDERS"
            ]
        
        # Display tabs as clickable buttons
        for tab in tabs:
            is_active = st.session_state.get('active_tab', 'CLIENTS') == tab
            button_label = tab
            if is_active:
                button_label = f"▶️ {tab}"
            
            if st.button(
                button_label,
                key=f"tab_{tab}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.active_tab = tab
                st.rerun()
        
        st.markdown("---")
        
        # General Announcements
        st.markdown("### 📢 General Announcements")
        
        announcements = [
            "🚨 ETD is officially working!",
            "📦 Working on palletizing",
            "⭐ **SPECIAL OFFER**",
            "🔔 **REMINDER**:",
            "📊 **NEW FEATURE**: HS Code search now available across all clients",
            "📦 **NEW**: Palletizing Calculator added!",
            "💰 **NEW**: All Customers Prices tab added!",
            "🤖 **NEW**: Smart Search with AI suggestions!",
            "⭐ **NEW**: Save favorite searches!",
            "📁 **NEW**: Bulk article search available!",
            "📊 **NEW**: All Prices tab added! View General_prices sheet data!",
            "📋 **NEW**: Client's Orders tab added! Search orders directly from Clients_CoC sheet!"
        ]
        
        for announcement in announcements:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
                padding: 0.8rem;
                border-radius: 8px;
                border-left: 4px solid #0EA5E9;
                margin: 0.5rem 0;
                font-size: 0.9em;
                color: #1E293B;
            ">
                {announcement}
            </div>
            """, unsafe_allow_html=True)
        
        # Search History (kept in sidebar)
        if st.session_state.get('search_history'):
            st.markdown("---")
            st.markdown("### 🔍 Recent Searches")
            
            for i, history_item in enumerate(st.session_state.search_history[:3]):
                time_ago = format_time_ago(history_item['timestamp'])
                
                display_text = f"{history_item['search_term']}"
                if history_item.get('article_num'):
                    display_text += f" → {history_item['article_num']}"
                
                if st.button(
                    f"{display_text[:30]}...",
                    key=f"hist_{i}",
                    use_container_width=True,
                    help=f"{history_item['client']} • {history_item['supplier']} • {time_ago}"
                ):
                    st.session_state[f"{history_item['client']}_article"] = history_item['search_term']
                    st.session_state[f"{history_item['client']}_supplier"] = history_item['supplier']
                    st.session_state.search_results = {
                        "article": history_item.get('article_num', history_item['search_term']),
                        "supplier": history_item['supplier'],
                        "client": history_item['client']
                    }
                    st.session_state.active_tab = "CLIENTS"
                    st.rerun()
    
    # REMOVED: Main header box with "Backaldrin Arab Jordan Dashboard"
    # The tab content will now start directly with its own header
    
    # Display the active tab content
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
    
    # Logout button at bottom
    st.markdown("---")
    logout_button()

# ============================================
# CLIENT'S ORDERS TAB FUNCTION
# ============================================

def clients_orders_tab():
    """
    Client's Orders Tab - Fetches data directly from Clients_CoC sheet
    Allows client selection and search by article number, product name, or HS code
    NEW: Added Year filter for better search precision
    """
    st.markdown("""
    <div class="clients-orders-header">
        <h2 style="margin:0;">📋 Client's Orders</h2>
        <p style="margin:0; opacity:0.9;">Direct Access to Clients_CoC Sheet • Search by Article, Product Name, HS Code, or Year</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all clients from the master sheet
    all_clients = get_all_clients_from_master()
    
    if not all_clients:
        st.warning("""
        ⚠️ **No clients found in Clients_CoC sheet!**
        
        **To get started:**
        1. Go to your Google Sheet
        2. Add a tab called **'Clients_CoC'**
        3. Use these exact headers:
           - Client
           - Supplier
           - Article_Number
           - Product_Name
           - Price
           - Order_Number
           - Order_Date
           - Year
           - HS_Code
           - Packaging
           - Quantity
           - Total_Weight
           - Total_Price
           - Status
           - Notes
        """)
        return
    
    st.success(f"✅ Found {len(all_clients)} clients in Clients_CoC sheet")
    
    # Client selection
    client = st.selectbox(
        "Select Client:",
        all_clients,
        key="clients_orders_client_select"
    )
    
    # Load client data using the existing get_google_sheets_data function
    with st.spinner(f"📥 Loading orders data for {client}..."):
        DATA = get_google_sheets_data(client)
    
    if not DATA.get("Backaldrin") and not DATA.get("Bateel"):
        st.error(f"❌ No data found for {client} in Clients_CoC sheet")
        return
    
    st.success(f"✅ Connected to {client} data")
    
    # Supplier selection
    supplier = st.radio(
        "Select Supplier:",
        ["Backaldrin", "Bateel"],
        horizontal=True,
        key="clients_orders_supplier"
    )
    
    # ============================================
    # SEARCH SECTION WITH YEAR FILTER
    # ============================================
    st.subheader("🔍 Search Orders")
    
    # Create 4 columns for search inputs (increased from 3 to 4)
    search_col1, search_col2, search_col3, search_col4 = st.columns([2, 1, 1, 1])
    
    with search_col1:
        search_term = st.text_input(
            "Search by Article Number, Product Name, or HS Code:",
            placeholder="e.g., 1-366, Chocolate Chips, 1901200000...",
            key="clients_orders_search"
        )
    
    with search_col2:
        search_type = st.selectbox(
            "Search Type:",
            ["All", "Article Number", "Product Name", "HS Code"],
            key="clients_orders_search_type"
        )
    
    with search_col3:
        # NEW: Year filter dropdown
        # First, get all available years from the data
        all_years = set()
        supplier_data = DATA.get(supplier, {})
        for article_num, article_data in supplier_data.items():
            for order in article_data.get('orders', []):
                year = order.get('year', '')
                if year and year != '' and year != 'nan':
                    all_years.add(str(year))
        
        # Sort years descending (newest first)
        year_options = ["All Years"] + sorted(list(all_years), reverse=True)
        
        selected_year = st.selectbox(
            "Filter by Year:",
            year_options,
            key="clients_orders_year_filter"
        )
    
    with search_col4:
        if st.button("🔍 Search", type="primary", use_container_width=True, key="clients_orders_search_btn"):
            if search_term or selected_year != "All Years":
                add_to_search_history(search_term if search_term else f"Year: {selected_year}", client, supplier)
    
    # Initialize session state for search results
    if 'clients_orders_results' not in st.session_state:
        st.session_state.clients_orders_results = None
    
    # Get supplier data
    supplier_data = DATA.get(supplier, {})
    
    # Perform search if search term exists OR year filter is active
    if search_term or selected_year != "All Years":
        search_results = []
        search_lower = search_term.lower() if search_term else ""
        
        for article_num, article_data in supplier_data.items():
            match_found = False
            match_type = ""
            
            # Search by article number (only if search_term exists)
            if search_term and search_type in ["All", "Article Number"]:
                if search_lower in article_num.lower():
                    match_found = True
                    match_type = "Article Number"
            
            # Search by product name (only if search_term exists)
            if not match_found and search_term and search_type in ["All", "Product Name"]:
                for name in article_data.get('names', []):
                    if search_lower in str(name).lower():
                        match_found = True
                        match_type = "Product Name"
                        break
            
            # Search by HS code (only if search_term exists)
            if not match_found and search_term and search_type in ["All", "HS Code"]:
                for order in article_data.get('orders', []):
                    hs_code = str(order.get('hs_code', '')).lower()
                    if search_lower in hs_code:
                        match_found = True
                        match_type = "HS Code"
                        break
            
            # If no search term, we still need to check if we should include this article based on year filter
            if not search_term and selected_year != "All Years":
                # We'll include if any order matches the year filter
                for order in article_data.get('orders', []):
                    order_year = str(order.get('year', ''))
                    if order_year == selected_year:
                        match_found = True
                        match_type = f"Year {selected_year}"
                        break
            
            # If we already have a match from search, but year filter is active, filter further
            if match_found and selected_year != "All Years":
                # Check if any order matches the selected year
                year_match_found = False
                for order in article_data.get('orders', []):
                    order_year = str(order.get('year', ''))
                    if order_year == selected_year:
                        year_match_found = True
                        break
                
                if not year_match_found:
                    match_found = False
            
            if match_found and article_data.get('orders'):
                # Get the latest product name
                product_name = ""
                if article_data.get('names'):
                    product_name = article_data['names'][0]
                
                # Filter orders by year if year filter is active
                filtered_orders = article_data.get('orders', [])
                if selected_year != "All Years":
                    filtered_orders = [
                        order for order in filtered_orders 
                        if str(order.get('year', '')) == selected_year
                    ]
                
                # Count orders and get price range from filtered orders
                prices = []
                for order in filtered_orders:
                    price_str = order.get('price', '')
                    if price_str:
                        try:
                            price_val = float(str(price_str).replace('$', '').replace(',', '').strip())
                            prices.append(price_val)
                        except:
                            pass
                
                min_price = min(prices) if prices else None
                max_price = max(prices) if prices else None
                
                # Store filtered article data with filtered orders
                filtered_article_data = article_data.copy()
                filtered_article_data['orders'] = filtered_orders
                filtered_article_data['prices'] = prices
                
                search_results.append({
                    'article': article_num,
                    'product_name': product_name,
                    'match_type': match_type,
                    'orders_count': len(filtered_orders),
                    'price_count': len(prices),
                    'min_price': min_price,
                    'max_price': max_price,
                    'has_orders': True,
                    'article_data': filtered_article_data
                })
        
        if search_results:
            st.success(f"✅ Found {len(search_results)} matching items")
            if search_term and selected_year != "All Years":
                st.info(f"🔍 Searching for: '{search_term}' | 📅 Year: {selected_year}")
            elif search_term:
                st.info(f"🔍 Searching for: '{search_term}'")
            elif selected_year != "All Years":
                st.info(f"📅 Showing all orders from year: {selected_year}")
            
            st.session_state.clients_orders_results = {
                'client': client,
                'supplier': supplier,
                'search_term': search_term if search_term else f"All items - Year: {selected_year}",
                'selected_year': selected_year,
                'results': search_results
            }
        else:
            st.warning(f"❌ No results found")
            if search_term and selected_year != "All Years":
                st.info(f"No orders found for '{search_term}' in {client} - {supplier} for year {selected_year}")
            elif search_term:
                st.info(f"No orders found for '{search_term}' in {client} - {supplier}")
            elif selected_year != "All Years":
                st.info(f"No orders found for year {selected_year} in {client} - {supplier}")
    
    # Display results if they exist
    if st.session_state.clients_orders_results and st.session_state.clients_orders_results.get('client') == client:
        results_data = st.session_state.clients_orders_results
        search_results = results_data.get('results', [])
        
        # Display results overview with year info
        st.subheader(f"📊 Search Results")
        
        # Show filter info if year was selected
        if results_data.get('selected_year') and results_data.get('selected_year') != "All Years":
            st.info(f"📅 Filtered by Year: {results_data['selected_year']}")
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Items Found", len(search_results))
        with col2:
            total_orders = sum(r['orders_count'] for r in search_results)
            st.metric("Total Orders", total_orders)
        with col3:
            # Get all prices from all results
            all_prices = []
            for r in search_results:
                if r['min_price']:
                    all_prices.append(r['min_price'])
                if r['max_price']:
                    all_prices.append(r['max_price'])
            if all_prices:
                st.metric("Price Range", f"${min(all_prices):.2f} - ${max(all_prices):.2f}")
            else:
                st.metric("Price Range", "N/A")
        
        # Display each result in an expander
        for result in search_results:
            article_num = result['article']
            article_data = result['article_data']
            
            with st.expander(f"📦 {article_num} - {result['product_name']} | {result['orders_count']} orders | Found by: {result['match_type']}", expanded=False):
                
                # Article information
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**📋 Article Details**")
                    st.write(f"**Article Number:** {article_num}")
                    st.write(f"**Product Name:** {result['product_name']}")
                    
                    if result['min_price'] and result['max_price']:
                        st.write(f"**Price Range:** ${result['min_price']:.2f} - ${result['max_price']:.2f}/kg")
                        st.write(f"**Total Price Records:** {result['price_count']}")
                
                with col2:
                    st.markdown("**📊 Statistics**")
                    st.write(f"**Total Orders:** {result['orders_count']}")
                    if result['min_price'] and result['max_price']:
                        avg_price = (result['min_price'] + result['max_price']) / 2
                        st.write(f"**Average Price:** ${avg_price:.2f}/kg")
                
                # Order history
                st.markdown("---")
                st.subheader("📜 Order History")
                
                # Get orders sorted by date (newest first)
                orders = article_data.get('orders', [])
                
                # Sort orders by date if possible
                try:
                    orders_with_dates = []
                    for order in orders:
                        date_str = order.get('date', '')
                        if date_str:
                            for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                                try:
                                    parsed_date = datetime.strptime(date_str, fmt)
                                    orders_with_dates.append((parsed_date, order))
                                    break
                                except:
                                    continue
                        else:
                            orders_with_dates.append((None, order))
                    
                    # Sort by date descending (newest first)
                    orders_with_dates.sort(key=lambda x: x[0] if x[0] else datetime.min, reverse=True)
                    orders = [order for _, order in orders_with_dates]
                except:
                    pass
                
                # Display orders
                for idx, order in enumerate(orders):
                    # Format price for display
                    price_display = order.get('price', 'N/A')
                    try:
                        price_value = float(str(price_display).replace('$', '').replace(',', '').strip())
                        price_display = f"${price_value:.2f}"
                    except:
                        price_display = f"${price_display}" if price_display != 'N/A' else 'N/A'
                    
                    # Create order card with year badge
                    order_year = order.get('year', '')
                    year_badge = f" | 📅 Year: {order_year}" if order_year else ""
                    
                    st.markdown(f"""
                    <div class="price-box" style="margin-bottom: 1rem;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <div style="margin-bottom: 0.5rem;">
                                    <strong>📦 Order:</strong> {order.get('order_no', 'N/A')}
                                </div>
                                <div style="margin-bottom: 0.5rem;">
                                    <strong>📅 Date:</strong> {order.get('date', 'N/A')}{year_badge}
                                </div>
                                {f'<div style="margin-bottom: 0.5rem;"><strong>🏷️ HS Code:</strong> {order.get("hs_code", "N/A")}</div>' if order.get('hs_code') else ''}
                            </div>
                            <div>
                                {f'<div style="margin-bottom: 0.5rem;"><strong>📦 Packaging:</strong> {order.get("packaging", "N/A")}</div>' if order.get('packaging') else ''}
                                {f'<div style="margin-bottom: 0.5rem;"><strong>🔢 Quantity:</strong> {order.get("quantity", "N/A")}</div>' if order.get('quantity') else ''}
                                {f'<div style="margin-bottom: 0.5rem;"><strong>⚖️ Weight:</strong> {order.get("total_weight", "N/A")} kg</div>' if order.get('total_weight') else ''}
                                {f'<div style="margin-bottom: 0.5rem;"><strong>💰 Total Price:</strong> {order.get("total_price", "N/A")}</div>' if order.get('total_price') else ''}
                            </div>
                        </div>
                        <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                            <div style="font-size: 1.2em; font-weight: bold; color: #FEF3C7;">
                                Price: {price_display}/kg
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Search Results")
        
        # Prepare export data
        export_data = []
        for result in search_results:
            article_data = result['article_data']
            for order in article_data.get('orders', []):
                export_data.append({
                    'Client': client,
                    'Supplier': supplier,
                    'Article_Number': result['article'],
                    'Product_Name': result['product_name'],
                    'Order_Number': order.get('order_no', ''),
                    'Order_Date': order.get('date', ''),
                    'Year': order.get('year', ''),
                    'HS_Code': order.get('hs_code', ''),
                    'Packaging': order.get('packaging', ''),
                    'Quantity': order.get('quantity', ''),
                    'Total_Weight_kg': order.get('total_weight', ''),
                    'Price_per_kg': order.get('price', ''),
                    'Total_Price': order.get('total_price', ''),
                    'Status': order.get('status', ''),
                    'Notes': order.get('notes', ''),
                    'Search_Term': results_data['search_term'],
                    'Search_Type': search_type,
                    'Year_Filter': results_data.get('selected_year', 'All Years'),
                    'Export_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        if export_data:
            export_df = pd.DataFrame(export_data)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = export_df.to_csv(index=False)
                file_name = f"{client}_orders"
                if search_term:
                    file_name += f"_{results_data['search_term'].replace(' ', '_')}"
                if results_data.get('selected_year') and results_data['selected_year'] != "All Years":
                    file_name += f"_{results_data['selected_year']}"
                file_name += f"_{datetime.now().strftime('%Y%m%d')}.csv"
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=file_name,
                    mime="text/csv",
                    use_container_width=True,
                    key="clients_orders_csv"
                )
            
            with col2:
                try:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        export_df.to_excel(writer, index=False, sheet_name='Client_Orders')
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_data,
                        file_name=f"{client}_orders_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.ms-excel",
                        use_container_width=True,
                        key="clients_orders_excel"
                    )
                except:
                    st.info("📊 Excel export requires openpyxl package")
            
            with col3:
                # Generate summary report with year info
                summary_text = f"""
CLIENT'S ORDERS REPORT
======================

Client: {client}
Supplier: {supplier}
Search Term: "{results_data['search_term']}"
Search Type: {search_type}
Year Filter: {results_data.get('selected_year', 'All Years')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SUMMARY:
• Items Found: {len(search_results)}
• Total Orders: {len(export_data)}
• Unique Articles: {export_df['Article_Number'].nunique()}
• Years Included: {', '.join(sorted(export_df['Year'].dropna().unique())) if not export_df['Year'].isna().all() else 'N/A'}
• Date Range: {export_df['Order_Date'].min() if export_df['Order_Date'].notna().any() else 'N/A'} to {export_df['Order_Date'].max() if export_df['Order_Date'].notna().any() else 'N/A'}

ITEMS FOUND:
{chr(10).join([f"• {r['article']} - {r['product_name']}: {r['orders_count']} orders" for r in search_results])}

ORDER DETAILS:
{chr(10).join([f"• {row['Order_Number']} - {row['Article_Number']} - {row['Price_per_kg']}/kg ({row['Order_Date']}) - Year: {row['Year']}" for _, row in export_df.head(20).iterrows()])}

{'... and ' + str(len(export_df) - 20) + ' more orders' if len(export_df) > 20 else ''}
                """
                
                st.download_button(
                    label="📄 Download Summary",
                    data=summary_text,
                    file_name=f"{client}_orders_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="clients_orders_summary"
                )
            
            # Preview data
            with st.expander("👀 Preview Export Data", expanded=False):
                st.dataframe(export_df, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif not search_term and selected_year == "All Years":
        # Show example when no search is performed and no year filter
        st.info("""
        ### 🔍 How to use this tab:
        
        1. **Select a client** from the dropdown list
        2. **Choose a supplier** (Backaldrin or Bateel)
        3. **Enter a search term** (article number, product name, or HS code) OR **select a year** to filter orders
        4. **Click Search** to view all historical orders
        
        **Examples:**
        - Try searching for article number: `1-366`
        - Try searching for product name: `Chocolate`
        - Try searching for HS code: `190120`
        - Try selecting a year: `2025` to see all orders from that year
        - Combine search with year filter for more precise results
        
        The results will show all orders matching your search criteria, including:
        - Order number and date
        - Price history
        - Quantity and weight details
        - HS code and packaging information
        """)
        
        # Show sample data if available
        if all_clients:
            st.subheader("📋 Available Clients")
            st.write(f"**Clients with data:** {', '.join(all_clients)}")
            
            # Show available years for the selected client
            if client and supplier:
                supplier_data = DATA.get(supplier, {})
                available_years = set()
                for article_num, article_data in supplier_data.items():
                    for order in article_data.get('orders', []):
                        year = order.get('year', '')
                        if year and year != '' and year != 'nan':
                            available_years.add(str(year))
                
                if available_years:
                    st.subheader("📅 Available Years in Data")
                    st.write(f"**Years with orders:** {', '.join(sorted(available_years, reverse=True))}")
            
            # Show first few rows from the first client as preview
            first_client = all_clients[0]
            with st.expander(f"🔍 Preview data for {first_client} (first 5 orders)", expanded=False):
                try:
                    preview_data = get_google_sheets_data(first_client)
                    if preview_data.get("Backaldrin"):
                        preview_articles = list(preview_data["Backaldrin"].keys())[:3]
                        for article in preview_articles:
                            article_data = preview_data["Backaldrin"][article]
                            if article_data.get('orders'):
                                st.write(f"**Article:** {article}")
                                for order in article_data['orders'][:2]:
                                    year_info = f" | Year: {order.get('year', 'N/A')}" if order.get('year') else ""
                                    st.write(f"  - Order: {order.get('order_no', 'N/A')} | Date: {order.get('date', 'N/A')}{year_info} | Price: {order.get('price', 'N/A')}/kg")
                except:
                    pass

# ============================================
# ALL PRICES TAB FUNCTION
# ============================================

def all_prices_tab():
    """
    NEW: All Prices Tab - Displays data from General_prices sheet
    Shows complete pricing information with filtering and search capabilities
    """
    st.markdown("""
    <div class="all-prices-header">
        <h2 style="margin:0;">📊 All Items Price Database</h2>
        <p style="margin:0; opacity:0.9;">Complete Item Catalog • Pricing Information • Category-wise Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load general prices data
    with st.spinner("📥 Loading all prices data from General_prices sheet..."):
        prices_data = load_general_prices_data()
    
    if prices_data.empty:
        st.warning("""
        ⚠️ **General_prices data not found or empty!**
        
        **To get started:**
        1. Go to your Google Sheet
        2. Add a new tab called **'General_prices'**
        3. Use these exact headers:
           - # (Number)
           - CATEG. (Category)
           - SUB CATEG. (Sub Category)
           - SUB. SUB. (Sub Sub Category)
           - DESCRIPTION
           - ART# (Article Number)
           - UOM (Unit of Measure)
           - UNT WGT (Unit Weight)
           - NEW EXW (New EXW Price)
        """)
        return
    
    st.success(f"✅ Loaded {len(prices_data)} items from General_prices sheet")
    
    # ============================================
    # DATA OVERVIEW
    # ============================================
    st.subheader("📊 Data Overview")
    
    # Calculate statistics
    total_items = len(prices_data)
    
    # Check if expected columns exist
    has_category = 'CATEG.' in prices_data.columns
    has_subcategory = 'SUB CATEG.' in prices_data.columns
    has_subsubcategory = 'SUB. SUB.' in prices_data.columns
    has_price = 'NEW EXW' in prices_data.columns
    
    if has_category:
        categories = prices_data['CATEG.'].nunique()
    else:
        categories = 0
    
    if has_subcategory:
        subcategories = prices_data['SUB CATEG.'].nunique()
    else:
        subcategories = 0
    
    if has_price:
        avg_price = prices_data['NEW EXW'].mean()
        min_price = prices_data['NEW EXW'].min()
        max_price = prices_data['NEW EXW'].max()
    else:
        avg_price = min_price = max_price = 0
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Items", total_items)
    
    with col2:
        st.metric("Categories", categories if has_category else "N/A")
    
    with col3:
        st.metric("Sub Categories", subcategories if has_subcategory else "N/A")
    
    with col4:
        if has_price:
            st.metric("Avg Price", f"${avg_price:.2f}")
        else:
            st.metric("Avg Price", "N/A")
    
    # ============================================
    # SEARCH AND FILTER SECTION
    # ============================================
    st.subheader("🔍 Search & Filter Items")
    
    # Search options in columns
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "Search by article, description, or any field:",
            placeholder="Enter search term...",
            key="all_prices_search"
        )
    
    with col2:
        if has_category:
            category_options = ["All"] + sorted(prices_data['CATEG.'].dropna().unique().tolist())
            category_filter = st.selectbox("Category:", category_options, key="all_prices_category")
        else:
            category_filter = "All"
            st.selectbox("Category:", ["No category data"], key="all_prices_category", disabled=True)
    
    with col3:
        if has_price:
            price_range_min = float(prices_data['NEW EXW'].min()) if not prices_data['NEW EXW'].isna().all() else 0
            price_range_max = float(prices_data['NEW EXW'].max()) if not prices_data['NEW EXW'].isna().all() else 1000
            price_range = st.slider(
                "Price Range:",
                min_value=price_range_min,
                max_value=price_range_max,
                value=(price_range_min, price_range_max),
                key="all_prices_price_range"
            )
        else:
            price_range = (0, 1000)
            st.slider("Price Range:", 0, 1000, (0, 1000), key="all_prices_price_range", disabled=True)
    
    # Advanced search options in expander
    with st.expander("🔧 Advanced Search Options", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if has_subcategory:
                subcategory_options = ["All"] + sorted(prices_data['SUB CATEG.'].dropna().unique().tolist())
                subcategory_filter = st.selectbox("Sub Category:", subcategory_options, key="all_prices_subcategory")
            else:
                subcategory_filter = "All"
                st.selectbox("Sub Category:", ["No subcategory data"], key="all_prices_subcategory", disabled=True)
        
        with col2:
            if has_subsubcategory:
                subsubcategory_options = ["All"] + sorted(prices_data['SUB. SUB.'].dropna().unique().tolist())
                subsubcategory_filter = st.selectbox("Sub Sub Category:", subsubcategory_options, key="all_prices_subsubcategory")
            else:
                subsubcategory_filter = "All"
                st.selectbox("Sub Sub Category:", ["No sub-subcategory data"], key="all_prices_subsubcategory", disabled=True)
        
        with col3:
            if 'UOM' in prices_data.columns:
                uom_options = ["All"] + sorted(prices_data['UOM'].dropna().unique().tolist())
                uom_filter = st.selectbox("Unit of Measure:", uom_options, key="all_prices_uom")
            else:
                uom_filter = "All"
                st.selectbox("Unit of Measure:", ["No UOM data"], key="all_prices_uom", disabled=True)
    
    # ============================================
    # APPLY FILTERS
    # ============================================
    filtered_data = prices_data.copy()
    
    # Apply text search
    if search_term:
        search_columns = []
        for col in filtered_data.columns:
            search_columns.append(col)
        
        mask = filtered_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    # Apply category filter
    if has_category and category_filter != "All":
        filtered_data = filtered_data[filtered_data['CATEG.'] == category_filter]
    
    # Apply subcategory filter
    if has_subcategory and subcategory_filter != "All":
        filtered_data = filtered_data[filtered_data['SUB CATEG.'] == subcategory_filter]
    
    # Apply subsubcategory filter
    if has_subsubcategory and subsubcategory_filter != "All":
        filtered_data = filtered_data[filtered_data['SUB. SUB.'] == subsubcategory_filter]
    
    # Apply UOM filter
    if 'UOM' in filtered_data.columns and uom_filter != "All":
        filtered_data = filtered_data[filtered_data['UOM'] == uom_filter]
    
    # Apply price range filter
    if has_price:
        filtered_data = filtered_data[
            (filtered_data['NEW EXW'] >= price_range[0]) & 
            (filtered_data['NEW EXW'] <= price_range[1])
        ]
    
    # ============================================
    # DISPLAY RESULTS
    # ============================================
    st.subheader(f"📋 Items Found: {len(filtered_data)}")
    
    if not filtered_data.empty:
        # Display results as cards
        for idx, item in filtered_data.iterrows():
            with st.expander(f"{item.get('ART#', 'N/A')} - {item.get('DESCRIPTION', 'N/A')}", expanded=False):
                
                # Create a nice card display
                st.markdown(f"""
                <div class="all-prices-card">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <h3 style="margin:0; color: #7C3AED;">{item.get('ART#', 'N/A')}</h3>
                            <p style="margin:0; font-weight: bold; color: #1E293B;">{item.get('DESCRIPTION', 'N/A')}</p>
                        </div>
                        <div style="text-align: right;">
                            {f"<h2 style='margin:0; color: #059669;'>${item.get('NEW EXW', 'N/A'):.2f}</h2>" if has_price and pd.notna(item.get('NEW EXW')) else "<p style='margin:0; color: #6B7280;'>Price: N/A</p>"}
                            {f"<p style='margin:0; color: #6B7280;'>Unit Weight: {item.get('UNT WGT', 'N/A')}</p>" if 'UNT WGT' in item and pd.notna(item.get('UNT WGT')) else ""}
                            {f"<p style='margin:0; color: #6B7280;'>UOM: {item.get('UOM', 'N/A')}</p>" if 'UOM' in item and pd.notna(item.get('UOM')) else ""}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; background: rgba(124, 58, 237, 0.1); padding: 0.75rem; border-radius: 6px;">
                        <div>
                            <p style="margin:0; font-size: 0.8em; color: #6B7280;">Category</p>
                            <p style="margin:0; font-weight: bold;">{item.get('CATEG.', 'N/A')}</p>
                        </div>
                        <div>
                            <p style="margin:0; font-size: 0.8em; color: #6B7280;">Sub Category</p>
                            <p style="margin:0; font-weight: bold;">{item.get('SUB CATEG.', 'N/A')}</p>
                        </div>
                        <div>
                            <p style="margin:0; font-size: 0.8em; color: #6B7280;">Sub Sub Category</p>
                            <p style="margin:0; font-weight: bold;">{item.get('SUB. SUB.', 'N/A')}</p>
                        </div>
                    </div>
                    
                    {f"<div style='margin-top: 1rem;'><p style='margin:0; font-size: 0.8em; color: #6B7280;'>#</p><p style='margin:0;'>{item.get('#', 'N/A')}</p></div>" if '#' in item and pd.notna(item.get('#')) else ""}
                </div>
                """, unsafe_allow_html=True)
        
        # ============================================
        # SUMMARY STATISTICS FOR FILTERED DATA
        # ============================================
        st.subheader("📈 Filtered Data Statistics")
        
        if len(filtered_data) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Filtered Items", len(filtered_data))
            
            with col2:
                if has_price and 'NEW EXW' in filtered_data.columns:
                    filtered_avg_price = filtered_data['NEW EXW'].mean()
                    st.metric("Avg Price", f"${filtered_avg_price:.2f}")
                else:
                    st.metric("Avg Price", "N/A")
            
            with col3:
                if has_price and 'NEW EXW' in filtered_data.columns:
                    filtered_min_price = filtered_data['NEW EXW'].min()
                    st.metric("Min Price", f"${filtered_min_price:.2f}")
                else:
                    st.metric("Min Price", "N/A")
            
            with col4:
                if has_price and 'NEW EXW' in filtered_data.columns:
                    filtered_max_price = filtered_data['NEW EXW'].max()
                    st.metric("Max Price", f"${filtered_max_price:.2f}")
                else:
                    st.metric("Max Price", "N/A")
            
            # Category distribution if available
            if has_category and len(filtered_data) > 0:
                st.subheader("📊 Category Distribution")
                category_counts = filtered_data['CATEG.'].value_counts().head(10)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.bar_chart(category_counts)
                
                with col2:
                    st.write("**Top Categories:**")
                    for category, count in category_counts.head(5).items():
                        st.write(f"• {category}: {count}")
        
        # ============================================
        # EXPORT FUNCTIONALITY
        # ============================================
        st.markdown("---")
        st.subheader("📤 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download CSV
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"all_prices_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="all_prices_csv"
            )
        
        with col2:
            # Download Excel
            try:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    filtered_data.to_excel(writer, index=False, sheet_name='All_Prices')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"all_prices_export_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True,
                    key="all_prices_excel"
                )
            except:
                st.info("📊 Excel export requires openpyxl")
        
        with col3:
            # Generate summary report
            summary_text = f"""
All Prices Export - General_prices Sheet
========================================

Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Items: {len(filtered_data)}
Search Term: "{search_term}"
Category Filter: {category_filter}
Price Range: ${price_range[0]:.2f} - ${price_range[1]:.2f}

Statistics:
• Average Price: ${filtered_data['NEW EXW'].mean():.2f if has_price and 'NEW EXW' in filtered_data.columns else 'N/A'}
• Minimum Price: ${filtered_data['NEW EXW'].min():.2f if has_price and 'NEW EXW' in filtered_data.columns else 'N/A'}
• Maximum Price: ${filtered_data['NEW EXW'].max():.2f if has_price and 'NEW EXW' in filtered_data.columns else 'N/A'}

Top Items by Price:
{chr(10).join([f"• {row.get('ART#', 'N/A')} - {row.get('DESCRIPTION', 'N/A')}: ${row.get('NEW EXW', 'N/A'):.2f}" 
               for _, row in filtered_data.nlargest(10, 'NEW EXW').iterrows()]) if has_price else 'No price data available'}

Export Generated by: {st.session_state.username}
            """
            
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"all_prices_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="all_prices_summary"
            )
    
    else:
        st.info("No items match your search criteria. Try broadening your search filters.")
    
    # ============================================
    # DATA PREVIEW (RAW DATA)
    # ============================================
    with st.expander("👀 View Raw Data Preview", expanded=False):
        st.dataframe(
            filtered_data,
            use_container_width=True,
            hide_index=True
        )
    
    # ============================================
    # QUICK TIPS
    # ============================================
    with st.expander("💡 How to use this section", expanded=False):
        st.markdown("""
        **📊 All Prices Database Guide:**
        
        1. **Search Items** - Use the search box to find items by article number, description, or any field
        2. **Filter by Category** - Narrow down results by main category
        3. **Price Range Filter** - Set minimum and maximum price limits
        4. **Advanced Filters** - Use the expander for sub-category and UOM filters
        5. **Export Data** - Download filtered results in CSV, Excel, or summary format
        
        **Available Columns:**
        - **#**: Item number
        - **CATEG.**: Main category
        - **SUB CATEG.**: Sub category
        - **SUB. SUB.**: Sub sub category
        - **DESCRIPTION**: Item description
        - **ART#**: Article number
        - **UOM**: Unit of measure
        - **UNT WGT**: Unit weight
        - **NEW EXW**: New EXW price
        
        **Pro Tips:**
        - Use wildcards in search (e.g., "choc*" for chocolate, chocolates, etc.)
        - Export data for offline analysis
        - Combine filters for precise results
        - Check raw data preview for complete information
        """)

# ============================================
# ORIGINAL TAB FUNCTIONS (Kept from original)
# ============================================

def clients_tab():
    """Clients management tab"""
    st.subheader("Client Selection")
    
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="client_select"
    )
    
    if client:
        cdc_dashboard(client)

def cdc_dashboard(client):
    """Client pricing dashboard with smart features"""
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'export_data' not in st.session_state:
        st.session_state.export_data = None
    
    st.markdown(f"""
    <div class="cdc-header">
        <h2 style="margin:0;"> {client} Pricing Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Smart Search • History • Favorites • Bulk Upload</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data directly from Google Sheets
    DATA = get_google_sheets_data(client)
    st.success(f"✅ Connected to Google Sheets - Live Data for {client}!")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True, type="secondary", key=f"{client}_refresh"):
        st.rerun()

    # Supplier selection
    st.subheader("Select Supplier")
    supplier = st.radio("", ["Backaldrin", "Bateel"], horizontal=True, label_visibility="collapsed", key=f"{client}_supplier")

    # ============================================
    # FEATURE 1: SMART SEARCH WITH AI SUGGESTIONS
    # ============================================
    st.subheader("🔍 Smart Search")
    
    search_container = st.container()
    
    with search_container:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search_input = st.text_input(
                "**Search by Article, Product, or HS Code:**",
                placeholder="Start typing for smart suggestions...",
                key=f"{client}_smart_search"
            )
        
        with col2:
            search_type = st.selectbox(
                "Search Type",
                ["All", "Article", "Product", "HS Code"],
                key=f"{client}_search_type"
            )
        
        with col3:
            if st.button("🔍 Smart Search", use_container_width=True, type="primary", key=f"{client}_smart_search_btn"):
                if search_input:
                    add_to_search_history(search_input, client, supplier)
                    handle_search(search_input, "", "", supplier, DATA, client)
    
    # Show smart suggestions as user types
    if search_input and len(search_input) >= 2:
        supplier_data = DATA.get(supplier, {})
        suggestions = get_smart_suggestions(search_input, supplier_data, search_type)
        
        if suggestions:
            st.markdown("**🤖 Smart Suggestions (click to select):**")
            for i, sugg in enumerate(suggestions[:5]):
                score_color = "#059669" if sugg["score"] >= 90 else "#D97706" if sugg["score"] >= 70 else "#6B7280"
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"{sugg['article']} - {sugg['name']}",
                        key=f"smart_{i}",
                        use_container_width=True,
                        help=f"Match score: {sugg['score']}/100"
                    ):
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
                    st.markdown(f"<span style='color:{score_color}; font-weight:bold;'>{sugg['score']}</span>", unsafe_allow_html=True)
    
    # Use a form for Enter key support
    with st.form(key=f"{client}_search_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            article = st.text_input("**ARTICLE NUMBER**", placeholder="e.g., 1-366, 1-367...", key=f"{client}_article")
        with col2:
            product = st.text_input("**PRODUCT NAME**", placeholder="e.g., Moist Muffin, Date Mix...", key=f"{client}_product")
        with col3:
            hs_code = st.text_input("**HS CODE**", placeholder="e.g., 1901200000, 180690...", key=f"{client}_hscode")
        
        # Search button - now responds to Enter key
        submitted = st.form_submit_button("🚀 SEARCH HISTORICAL PRICES", use_container_width=True, type="primary")
        
        if submitted:
            search_term = article or product or hs_code
            if search_term:
                add_to_search_history(search_term, client, supplier)
                handle_search(article, product, hs_code, supplier, DATA, client)

    # Display results from session state
    if st.session_state.search_results and st.session_state.search_results.get("client") == client:
        display_from_session_state(DATA, client)

def get_suggestions(search_term, supplier, data):
    """Get search suggestions for article, product name, or HS code"""
    suggestions = []
    supplier_data = data.get(supplier, {})
    
    for article_num, article_data in supplier_data.items():
        if not isinstance(article_data, dict) or 'names' not in article_data:
            continue
            
        # Article number search
        if search_term.lower() in str(article_num).lower():
            display_name = article_data['names'][0] if article_data['names'] else 'No Name'
            suggestions.append({
                "type": "article",
                "value": article_num,
                "display": f"🔢 {article_num} - {display_name}"
            })
        
        # Product name search
        for name in article_data['names']:
            if search_term.lower() in str(name).lower():
                suggestions.append({
                    "type": "product", 
                    "value": article_num,
                    "display": f"📝 {article_num} - {name}"
                })
        
        # HS Code search
        for order in article_data.get('orders', []):
            if (order.get('hs_code') and 
                search_term.lower() in str(order['hs_code']).lower() and
                article_num not in [s['value'] for s in suggestions]):
                display_name = article_data['names'][0] if article_data['names'] else 'No Name'
                suggestions.append({
                    "type": "hs_code",
                    "value": article_num,
                    "display": f"🏷️ {article_num} - HS: {order['hs_code']} - {display_name}"
                })
    
    # Remove duplicates
    unique_suggestions = {}
    for sugg in suggestions:
        if sugg["value"] not in unique_suggestions:
            unique_suggestions[sugg["value"]] = sugg
    
    return list(unique_suggestions.values())

def handle_search(article, product, hs_code, supplier, data, client):
    """Handle search across article, product name, and HS code"""
    search_term = article or product or hs_code
    if not search_term:
        st.error("❌ Please enter an article number, product name, or HS code")
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
        st.error(f"❌ No results found for '{search_term}' in {supplier}")
        add_to_search_history(search_term, client, supplier)

def create_export_data(article_data, article, supplier, client):
    """Create export data in different formats"""
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
    """Display search results with card design and favorites feature"""
    results = st.session_state.search_results
    article = results["article"]
    supplier = results["supplier"]
    
    if article not in data[supplier]:
        st.error("❌ Article not found in current data")
        return
        
    article_data = data[supplier][article]
    
    # ============================================
    # FEATURE 3: SAVED SEARCHES/FAVORITES
    # ============================================
    # Get search term from session state
    search_term = ""
    for key in [f"{client}_article", f"{client}_product", f"{client}_hscode", f"{client}_smart_search"]:
        if key in st.session_state:
            search_term = st.session_state[key]
            if search_term:
                break
    
    # Check if this search is favorited
    is_favorited = is_search_favorited(search_term, client, supplier)
    
    # Favorites button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"✅ **Article {article}** found in **{supplier}** for **{client}**")
    with col2:
        if is_favorited:
            if st.button("⭐ Remove Favorite", key="remove_fav", use_container_width=True):
                remove_search_from_favorites(search_term, client, supplier)
                st.rerun()
        else:
            if st.button("☆ Add to Favorites", key="add_fav", use_container_width=True):
                if save_search_to_favorites(search_term, client, supplier, article):
                    st.success("⭐ Added to favorites!")
                    st.rerun()
    
    # Product names - SHOW ONLY ONE (most recent)
    st.subheader("📝 Product Name")
    
    # Get the most recent product name from orders
    most_recent_name = ""
    
    # Try to find from orders (sorted by date)
    orders = article_data.get('orders', [])
    if orders:
        # Sort orders by date if possible
        try:
            # Create list of orders with parsed dates
            orders_with_dates = []
            for order in orders:
                date_str = order.get('date', '')
                if date_str:
                    # Try different date formats
                    for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d %b %Y', '%d %B %Y']:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt)
                            orders_with_dates.append((parsed_date, order))
                            break
                        except:
                            continue
            
            # Sort by date descending (newest first)
            orders_with_dates.sort(key=lambda x: x[0], reverse=True)
            
            # Get most recent product name
            if orders_with_dates:
                most_recent_name = orders_with_dates[0][1].get('product_name', '')
        except:
            # If date parsing fails, use first order
            most_recent_name = orders[0].get('product_name', '')
    
    # If no orders or no product name in orders, use the first name from names list
    if not most_recent_name and article_data['names']:
        most_recent_name = article_data['names'][0]
    
    st.markdown(f'<div class="price-card">{most_recent_name}</div>', unsafe_allow_html=True)
    
    # Statistics
    prices = article_data['prices']
    orders = article_data.get('orders', [])
    
    st.subheader("📊 Price Statistics")
    
    # Calculate required metrics
    total_records = len(prices)
    
    # Get last sold price (most recent)
    last_sold_price = None
    second_last_price = None
    
    if orders and prices:
        try:
            # Create list of orders with prices and dates
            order_price_list = []
            for order in orders:
                price_str = order.get('price', '')
                date_str = order.get('date', '')
                
                if price_str and date_str:
                    # Try to parse price
                    try:
                        price = float(str(price_str).replace('$', '').replace(',', '').strip())
                        
                        # Try to parse date
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
            
            # Sort by date descending (newest first)
            order_price_list.sort(key=lambda x: x[0], reverse=True)
            
            # Get last and second last prices
            if len(order_price_list) > 0:
                last_sold_price = order_price_list[0][1]
            if len(order_price_list) > 1:
                second_last_price = order_price_list[1][1]
                
        except:
            # Fallback: use the last prices from the prices list
            if len(prices) > 0:
                last_sold_price = prices[-1]
            if len(prices) > 1:
                second_last_price = prices[-2]
    
    # If still None, use min/max as fallback
    if last_sold_price is None and prices:
        last_sold_price = prices[-1] if prices else 0
    
    if second_last_price is None and len(prices) > 1:
        second_last_price = prices[-2] if len(prices) > 1 else 0
    elif second_last_price is None and prices:
        second_last_price = prices[0]  # Use first as fallback
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_records}</div>
            <div class="stat-label">Total Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        price_display = f"${last_sold_price:.2f}" if last_sold_price is not None else "N/A"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{price_display}</div>
            <div class="stat-label">Last Sold Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        price_display = f"${second_last_price:.2f}" if second_last_price is not None else "N/A"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{price_display}</div>
            <div class="stat-label">Previous Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="font-size: 1.4em;">${min_price:.2f} - ${max_price:.2f}</div>
                <div class="stat-label">Price Range (Min - Max)/kg</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">N/A</div>
                <div class="stat-label">Price Range/kg</div>
            </div>
            """, unsafe_allow_html=True)
    
    # NEW: COLLAPSIBLE ORDER CARDS
    st.subheader("💵 Historical Prices with Order Details")
    
    # Create expandable cards using Streamlit's native expander
    for i, order in enumerate(article_data['orders']):
        # Get price for display
        price_display = order.get('price', 'N/A')
        try:
            # Try to format as currency
            price_value = float(str(price_display).replace('$', '').replace(',', '').strip())
            price_display = f"${price_value:.2f}"
        except:
            price_display = f"${price_display}" if price_display != 'N/A' else 'N/A'
        
        # Create expander header
        expander_label = f"📦 {order.get('order_no', 'N/A')} | 📅 {order.get('date', 'N/A')} | 💰 {price_display}/kg"
        
        with st.expander(expander_label, expanded=False):
            # Card content inside expander
            order_card = f"""
            <div class="price-box" style="margin: 0; border: none; box-shadow: none;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <div style="margin-bottom: 0.5rem;">
                            <strong>📦 Product:</strong> {order.get('product_name', 'N/A')}
                        </div>
                        <div style="margin-bottom: 0.5rem;">
                            <strong>🔢 Article:</strong> {order.get('article', 'N/A')}
                        </div>
                        {f'<div style="margin-bottom: 0.5rem;"><strong>📅 Year:</strong> {order.get("year", "N/A")}</div>' if order.get('year') else ''}
                        {f'<div style="margin-bottom: 0.5rem;"><strong>🏷️ HS Code:</strong> {order.get("hs_code", "N/A")}</div>' if order.get('hs_code') else ''}
                    </div>
                    <div>
                        {f'<div style="margin-bottom: 0.5rem;"><strong>📦 Packaging:</strong> {order.get("packaging", "N/A")}</div>' if order.get('packaging') else ''}
                        {f'<div style="margin-bottom: 0.5rem;"><strong>🔢 Quantity:</strong> {order.get("quantity", "N/A")}</div>' if order.get('quantity') else ''}
                        {f'<div style="margin-bottom: 0.5rem;"><strong>⚖️ Total Weight:</strong> {order.get("total_weight", "N/A")}</div>' if order.get('total_weight') else ''}
                        {f'<div style="margin-bottom: 0.5rem;"><strong>💰 Total Price:</strong> {order.get("total_price", "N/A")}</div>' if order.get('total_price') else ''}
                    </div>
                </div>
                <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 1.5em; font-weight: bold; color: #FEF3C7;">
                        {price_display}/kg
                    </div>
                </div>
            </div>
            """
            st.markdown(order_card, unsafe_allow_html=True)
    
    # ============================================
    # FEATURE 2: SEARCH HISTORY DISPLAY
    # ============================================
    if st.session_state.get('search_history'):
        client_history = [
            h for h in st.session_state.search_history 
            if h.get('client') == client and h.get('supplier') == supplier
        ][:3]
        
        if client_history:
            st.subheader("🕐 Recent Searches for this Client")
            for i, history_item in enumerate(client_history):
                time_ago = format_time_ago(history_item['timestamp'])
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(
                        f"{history_item['search_term']}",
                        key=f"recent_{i}",
                        use_container_width=True,
                        help=f"Searched {time_ago}"
                    ):
                        st.session_state[f"{client}_article"] = history_item['search_term']
                        st.session_state.search_results = {
                            "article": history_item.get('article_num', history_item['search_term']),
                            "supplier": supplier,
                            "client": client
                        }
                        st.rerun()
                with col2:
                    st.caption(time_ago)
    
    # EXPORT SECTION
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.subheader("📤 Export Data")
    
    if st.session_state.export_data is not None:
        export_df = st.session_state.export_data
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{client}_pricing_{article}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
                key=f"{client}_csv"
            )
        
        with col2:
            try:
                excel_data = convert_df_to_excel(export_df)
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"{client}_pricing_{article}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True,
                    key=f"{client}_excel"
                )
            except:
                st.info("📊 Excel export requires openpyxl package")
        
        with col3:
            st.download_button(
                label="📄 Download Summary",
                data=f"""
{client} Pricing Summary Report
===============================

Article: {article}
Supplier: {supplier}
Client: {client}
Product: {export_df['product_name'].iloc[0]}
Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Price Statistics:
• Total Records: {len(export_df)}
• Minimum Price: ${min(prices):.2f}/kg
• Maximum Price: ${max(prices):.2f}/kg  
• Price Range: ${max(prices) - min(prices):.2f}/kg

Orders Included: {', '.join(export_df['order_number'].tolist())}
                """,
                file_name=f"{client}_summary_{article}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"{client}_summary"
            )
        
        with st.expander("👀 Preview Export Data"):
            st.dataframe(export_df, use_container_width=True)
            
    else:
        st.info("Search for an article to enable export options")
    
    st.markdown('</div>', unsafe_allow_html=True)

def convert_df_to_excel(df):
    """Convert DataFrame to Excel format"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Price_History')
    processed_data = output.getvalue()
    return processed_data

def prices_tab():
    """All Customers Prices Tab"""
    st.markdown("""
    <div class="prices-header">
        <h2 style="margin:0;">💰 All Customers Prices</h2>
        <p style="margin:0; opacity:0.9;">Complete Price Database • Cross-Customer Analysis • Flexible Search</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("📥 Loading prices data from Google Sheets..."):
        prices_data = load_prices_data()
    
    if prices_data.empty:
        st.warning("""
        ⚠️ **Prices data not found or empty!**
        
        **To get started:**
        1. Go to your Google Sheet
        2. Add a new tab called **'Prices'**
        3. Use these exact headers:
           - Customer
           - Customer Name
           - Salesman
           - Item Code
           - Item Name
           - Customer Article No
           - Customer Label
           - Packing/kg
           - Price
        """)
        return
    
    st.success(f"✅ Loaded {len(prices_data)} price records")
    
    # Overview Statistics
    st.subheader("📊 Price Database Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(prices_data)
        st.metric("Total Records", total_records)
    
    with col2:
        unique_customers = prices_data['Customer'].nunique()
        st.metric("Unique Customers", unique_customers)
    
    with col3:
        unique_items = prices_data['Item Code'].nunique()
        st.metric("Unique Items", unique_items)
    
    with col4:
        avg_price = prices_data['Price'].mean()
        st.metric("Average Price", f"${avg_price:.2f}")
    
    # Search and Filter Section
    st.subheader("🔍 Advanced Search & Filter")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        customers = ["All"] + sorted(prices_data['Customer'].dropna().unique().tolist())
        selected_customer = st.selectbox("Filter by Customer:", customers, key="price_customer_filter")
    
    with col2:
        salesmen = ["All"] + sorted(prices_data['Salesman'].dropna().unique().tolist())
        selected_salesman = st.selectbox("Filter by Salesman:", salesmen, key="price_salesman_filter")
    
    with col3:
        min_price = float(prices_data['Price'].min())
        max_price = float(prices_data['Price'].max())
        price_range = st.slider(
            "Price Range:",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            key="price_range_filter"
        )
    
    # Specific search options
    st.subheader("🎯 Specific Search Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        article_search = st.text_input(
            "🔢 Search by Article Number:",
            placeholder="Enter article number...",
            key="price_article_search"
        )
    
    with col2:
        item_name_search = st.text_input(
            "📝 Search by Item Name:",
            placeholder="Enter item name...",
            key="price_item_name_search"
        )
    
    with col3:
        customer_article_search = st.text_input(
            "🏷️ Search by Customer Article No:",
            placeholder="Enter customer article no...",
            key="price_customer_article_search"
        )
    
    # Global search
    global_search = st.text_input(
        "🌐 Global Search (search across all columns):",
        placeholder="Enter any term to search across all columns...",
        key="price_global_search"
    )
    
    # Apply filters
    filtered_data = prices_data.copy()
    
    if selected_customer != "All":
        filtered_data = filtered_data[filtered_data['Customer'] == selected_customer]
    
    if selected_salesman != "All":
        filtered_data = filtered_data[filtered_data['Salesman'] == selected_salesman]
    
    filtered_data = filtered_data[
        (filtered_data['Price'] >= price_range[0]) & 
        (filtered_data['Price'] <= price_range[1])
    ]
    
    if article_search:
        filtered_data = filtered_data[
            filtered_data['Item Code'].astype(str).str.contains(article_search, case=False, na=False)
        ]
    
    if item_name_search:
        filtered_data = filtered_data[
            filtered_data['Item Name'].astype(str).str.contains(item_name_search, case=False, na=False)
        ]
    
    if customer_article_search:
        filtered_data = filtered_data[
            filtered_data['Customer Article No'].astype(str).str.contains(customer_article_search, case=False, na=False)
        ]
    
    if global_search and not (article_search or item_name_search or customer_article_search):
        search_columns = ['Customer', 'Customer Name', 'Salesman', 'Item Code', 'Item Name', 
                         'Customer Article No', 'Customer Label', 'Packing/kg']
        mask = filtered_data[search_columns].astype(str).apply(
            lambda x: x.str.contains(global_search, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    # Display Results
    st.subheader(f"📋 Price Records ({len(filtered_data)} found)")
    
    if not filtered_data.empty:
        for _, record in filtered_data.iterrows():
            with st.expander(f"💰 {record['Item Code']} - {record['Item Name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Customer:** {record['Customer']}")
                    st.write(f"**Customer Name:** {record['Customer Name']}")
                    st.write(f"**Salesman:** {record['Salesman']}")
                    st.write(f"**Item Code:** {record['Item Code']}")
                    st.write(f"**Item Name:** {record['Item Name']}")
                    
                with col2:
                    st.write(f"**Customer Article No:** {record['Customer Article No']}")
                    st.write(f"**Customer Label:** {record['Customer Label']}")
                    st.write(f"**Packing/kg:** {record['Packing/kg']}")
                    st.markdown(f"<h3 style='color: #059669;'>Price: ${record['Price']:.2f}</h3>", unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Price Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"all_prices_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="prices_csv"
            )
        
        with col2:
            summary_text = f"""
All Customers Prices Report
===========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Records: {len(filtered_data)}
Unique Customers: {filtered_data['Customer'].nunique()}
Unique Items: {filtered_data['Item Code'].nunique()}
Average Price: ${filtered_data['Price'].mean():.2f}
Price Range: ${filtered_data['Price'].min():.2f} - ${filtered_data['Price'].max():.2f}

Filters Applied:
- Customer: {selected_customer}
- Salesman: {selected_salesman}
- Price Range: ${price_range[0]:.2f} - ${price_range[1]:.2f}
- Article Search: {article_search if article_search else 'None'}
- Item Name Search: {item_name_search if item_name_search else 'None'}
- Customer Article Search: {customer_article_search if customer_article_search else 'None'}
- Global Search: {global_search if global_search and not (article_search or item_name_search or customer_article_search) else 'None'}

Top Items by Price:
{chr(10).join([f"• {row['Item Code']} - {row['Item Name']}: ${row['Price']:.2f} ({row['Customer']})" 
               for _, row in filtered_data.nlargest(10, 'Price').iterrows()])}
            """
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"prices_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="prices_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Statistics for filtered data
        st.subheader("📈 Filtered Data Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Filtered Records", len(filtered_data))
        
        with col2:
            filtered_avg_price = filtered_data['Price'].mean()
            st.metric("Average Price", f"${filtered_avg_price:.2f}")
        
        with col3:
            min_filtered_price = filtered_data['Price'].min()
            st.metric("Min Price", f"${min_filtered_price:.2f}")
        
        with col4:
            max_filtered_price = filtered_data['Price'].max()
            st.metric("Max Price", f"${max_filtered_price:.2f}")
            
    else:
        st.info("No price records match your search criteria.")

def etd_tab():
    """ETD Sheet - Live Google Sheets Integration with Multi-Month Support"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">📅 ETD Management Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Live Order Tracking • Multi-Supplier ETD • Multi-Month View</p>
    </div>
    """, unsafe_allow_html=True)

    # ETD Sheet configuration
    ETD_SHEET_ID = "1eA-mtD3aK_n9VYNV_bxnmqm58IywF0f5-7vr3PT51hs"
    
    AVAILABLE_MONTHS = ["October 2025 ", "November 2025 "]

    try:
        # Month Selection
        st.subheader("📅 Select Month")
        selected_month = st.radio(
            "Choose month to view:",
            AVAILABLE_MONTHS,
            horizontal=True,
            key="etd_month_selector"
        )
        
        # Load ETD data for selected month
        with st.spinner(f"🔄 Loading {selected_month.strip()} ETD data..."):
            etd_data = load_etd_data(ETD_SHEET_ID, selected_month)
        
        if etd_data.empty:
            st.warning(f"No ETD data found in {selected_month}. Please check the sheet.")
            return

        st.success(f"✅ Connected to {selected_month.strip()}! Loaded {len(etd_data)} orders")

        # Overview Metrics
        st.subheader("📊 ETD Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_orders = len(etd_data)
            st.metric("Total Orders", total_orders)
        
        with col2:
            shipped_orders = len(etd_data[etd_data['Status'].str.lower() == 'shipped'])
            st.metric("Shipped", shipped_orders)
        
        with col3:
            production_orders = len(etd_data[etd_data['Status'].str.lower().str.contains('production', na=False)])
            st.metric("In Production", production_orders)
        
        with col4:
            pending_orders = len(etd_data[etd_data['Status'].str.lower().str.contains('pending', na=False)])
            st.metric("Pending", pending_orders)
        
        with col5:
            need_etd = len(etd_data[
                (etd_data['ETD _ Backaldrine'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                (etd_data['ETD_bateel'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                (etd_data['ETD _ Kasih'].astype(str).str.contains('NEETD', case=False, na=False)) |
                (etd_data['ETD_PMC'].astype(str).str.contains('NEED ETD', case=False, na=False))
            ])
            st.metric("Need ETD", need_etd)

        # Cross-Month Summary
        if len(AVAILABLE_MONTHS) > 1:
            st.subheader("🌐 Cross-Month Summary")
            month_cols = st.columns(len(AVAILABLE_MONTHS))
            
            for i, month in enumerate(AVAILABLE_MONTHS):
                with month_cols[i]:
                    if month == selected_month:
                        st.info(f"**{month.strip()}**\n**{len(etd_data)} orders**")
                    else:
                        try:
                            other_month_data = load_etd_data(ETD_SHEET_ID, month)
                            if not other_month_data.empty:
                                st.metric(month.strip(), len(other_month_data))
                            else:
                                st.write(f"**{month.strip()}**\n0 orders")
                        except:
                            st.write(f"**{month.strip()}**\n–")

        # Search and Filter Section
        st.subheader("🔍 Filter & Search Orders")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            client_filter = st.selectbox(
                "Client",
                ["All"] + sorted(etd_data['Client Name'].dropna().unique()),
                key="etd_client_filter"
            )
        
        with col2:
            employee_filter = st.selectbox(
                "Employee", 
                ["All"] + sorted(etd_data['Concerned Employee'].dropna().unique()),
                key="etd_employee_filter"
            )
        
        with col3:
            status_filter = st.selectbox(
                "Status",
                ["All", "Shipped", "In Production", "Pending", "Need ETD"],
                key="etd_status_filter"
            )
        
        with col4:
            search_term = st.text_input("Search Order No...", key="etd_search")

        # Apply filters
        filtered_data = etd_data.copy()
        
        if client_filter != "All":
            filtered_data = filtered_data[filtered_data['Client Name'] == client_filter]
        
        if employee_filter != "All":
            filtered_data = filtered_data[filtered_data['Concerned Employee'] == employee_filter]
        
        if status_filter != "All":
            if status_filter == "Need ETD":
                filtered_data = filtered_data[
                    (filtered_data['ETD _ Backaldrine'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (filtered_data['ETD_bateel'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (etd_data['ETD _ Kasih'].astype(str).str.contains('NEED ETD', case=False, na=False)) |
                    (etd_data['ETD_PMC'].astype(str).str.contains('NEED ETD', case=False, na=False))
                ]
            else:
                filtered_data = filtered_data[filtered_data['Status'] == status_filter]
        
        if search_term:
            filtered_data = filtered_data[
                filtered_data['Order No.'].astype(str).str.contains(search_term, case=False, na=False)
            ]

        # Display filtered results
        st.subheader(f"📋 {selected_month.strip()} Orders ({len(filtered_data)} found)")
        
        if not filtered_data.empty:
            for _, order in filtered_data.iterrows():
                display_etd_order_card(order, selected_month.strip())
        else:
            st.info("No orders match your filter criteria.")

        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export ETD Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"etd_data_{selected_month.strip().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="etd_csv"
            )
        
        with col2:
            summary_text = f"""
ETD Data Export - {selected_month.strip()}
===============================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Orders: {len(filtered_data)}
Filters: Client={client_filter}, Employee={employee_filter}, Status={status_filter}

Orders Summary:
{chr(10).join([f"• {row['Order No.']} - {row['Client Name']} - {row['Status']}" for _, row in filtered_data.iterrows()])}
            """
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"etd_summary_{selected_month.strip().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="etd_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error loading ETD data: {str(e)}")
        st.info("Please check: 1) Google Sheet is shared, 2) Sheet name is correct, 3) Internet connection")

def display_etd_order_card(order, month):
    """Display individual ETD order card with supplier tracking"""
    
    status = order.get('Status', 'Unknown')
    status_color = {
        'Shipped': '🟢',
        'In Production': '🟡', 
        'Pending': '🟠',
        'Unknown': '⚫'
    }.get(status, '⚫')
    
    needs_etd = []
    for supplier in ['Backaldrine', 'bateel', 'Kasih', 'PMC']:
        etd_col = f"ETD _{supplier}" if supplier != 'bateel' else 'ETD_bateel'
        etd_value = order.get(etd_col, '')
        if pd.notna(etd_value) and 'NEED ETD' in str(etd_value).upper():
            needs_etd.append(supplier)
    
    with st.expander(f"{status_color} {order.get('Order No.', 'N/A')} - {order.get('Client Name', 'N/A')} | {month}", expanded=False):
        
        # Order Header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**Client:** {order.get('Client Name', 'N/A')}")
            st.write(f"**Employee:** {order.get('Concerned Employee', 'N/A')}")
            st.write(f"**Month:** {month}")
            
        with col2:
            st.write(f"**Status:** {status}")
            st.write(f"**Confirmation:** {order.get('Confirmation Date', 'N/A')}")
            
        with col3:
            if needs_etd:
                st.error(f"🚨 NEED ETD: {', '.join(needs_etd)}")
            st.write(f"**Loading:** {order.get('Scheduled Date For Loading', 'N/A')}")
        
        # Supplier ETD Tracking
        st.write("---")
        st.write("**🚚 Supplier ETD Status**")
        
        suppliers = [
            ('Backaldrine', 'ETD _ Backaldrine', 'bateel Order #'),
            ('bateel', 'ETD_bateel', 'bateel Order #'),
            ('Kasih', 'ETD _ Kasih', 'Kasih Order #'), 
            ('PMC', 'ETD_PMC', 'PMC Order #')
        ]
        
        cols = st.columns(4)
        for idx, (supplier, etd_col, order_col) in enumerate(suppliers):
            with cols[idx]:
                etd_value = order.get(etd_col, '')
                order_value = order.get(order_col, '')
                
                if pd.isna(etd_value) or str(etd_value).strip() == '':
                    st.write(f"**{supplier}:** ❌ No ETD")
                elif 'NEED ETD' in str(etd_value).upper():
                    st.error(f"**{supplier}:** 🚨 NEED ETD")
                elif 'READY' in str(etd_value).upper():
                    st.success(f"**{supplier}:** ✅ Ready")
                else:
                    st.info(f"**{supplier}:** 📅 {etd_value}")
                
                if pd.notna(order_value) and str(order_value).strip() != '':
                    st.caption(f"Order: {order_value}")
        
        # Additional Information
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            stock_notes = order.get('Stock Notes', '')
            if pd.notna(stock_notes) and str(stock_notes).strip() != '':
                st.write("**📦 Stock Notes:**")
                st.info(stock_notes)
                
        with col2:
            transport = order.get('transport Company', '')
            if pd.notna(transport) and str(transport).strip() != '':
                st.write("**🚛 Transport:**")
                st.write(transport)

def ceo_specials_tab():
    """CEO Special Prices tab - NOW CLIENT SPECIFIC"""
    st.markdown("""
    <div class="ceo-header">
        <h2 style="margin:0;">⭐ CEO Special Prices</h2>
        <p style="margin:0; opacity:0.9;">Exclusive Pricing • Limited Time Offers • VIP Client Rates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection for CEO specials
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client for CEO Special Prices:",
        available_clients,
        key="ceo_client_select"
    )
    
    if not client:
        st.warning("No clients available for your account")
        return
        
    st.info(f"📊 Showing CEO Special Prices for **{client}**")
    
    # Load CEO special prices for selected client
    ceo_data = load_ceo_special_prices(client)
    
    if ceo_data.empty:
        sheet_name = CLIENT_SHEETS[client]["ceo_special"]
        st.warning(f"⚠️ No CEO special prices found for {client}. Please add data to '{sheet_name}' sheet.")
        st.info(f"""
        **To add CEO special prices for {client}:**
        1. Go to your Google Sheet
        2. Add a new tab called **'{sheet_name}'**
        3. Use these columns:
           - Article_Number
           - Product_Name  
           - Special_Price
           - Currency
           - Incoterm
           - Notes
           - Effective_Date
           - Expiry_Date
        """)
        return
     
    # CEO Special Prices Overview
    st.subheader(f"📊 {client} CEO Specials Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Special Offers", len(ceo_data))
    with col2:
        active_offers = len(ceo_data[ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])
        st.metric("Active Offers", active_offers)
    with col3:
        unique_currencies = ceo_data['Currency'].nunique()
        st.metric("Currencies Used", unique_currencies)
    with col4:
        expiring_soon = len(ceo_data[
            (ceo_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')) &
            (ceo_data['Expiry_Date'] <= (datetime.now() + pd.Timedelta(days=30)).strftime('%Y-%m-%d'))
        ])
        st.metric("Expiring Soon", expiring_soon)
    
    # Search and Filter
    st.subheader("🔍 Search CEO Special Prices")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("Search by article or product name...", key="ceo_search")
    with col2:
        show_active = st.checkbox("Show Active Only", value=True, key="ceo_active")
    with col3:
        currency_filter = st.selectbox("Currency", ["All"] + list(ceo_data['Currency'].unique()), key="ceo_currency")
    
    # Filter data
    filtered_data = ceo_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    if show_active:
        filtered_data = filtered_data[filtered_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')]
    
    if currency_filter != "All":
        filtered_data = filtered_data[filtered_data['Currency'] == currency_filter]
    
    # Display CEO Special Prices
    st.subheader(f"🎯 {client} Special Price List")
    
    if not filtered_data.empty:
        for _, special in filtered_data.iterrows():
            is_active = special['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')
            status_color = "🟢" if is_active else "🔴"
            status_text = "Active" if is_active else "Expired"
            
            try:
                price_display = f"{float(special['Special_Price']):.2f}"
            except:
                price_display = str(special['Special_Price'])
            
            st.markdown(f"""
            <div class="special-price-card">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div>
                        <h3 style="margin:0; color: #D97706;">{special['Article_Number']} - {special['Product_Name']}</h3>
                        <p style="margin:0; font-size: 1.2em; font-weight: bold; color: #B45309;">
                            Special Price: {price_display} {special['Currency']}/kg
                        </p>
                        <p style="margin:0; color: #6B7280;">
                            {status_color} {status_text} • Valid until: {special['Expiry_Date']}
                            {f" • Incoterm: {special['Incoterm']}" if pd.notna(special['Incoterm']) and special['Incoterm'] != '' else ''}
                        </p>
                        {f"<p style='margin:5px 0 0 0; color: #6B7280;'><strong>Notes:</strong> {special['Notes']}</p>" if pd.notna(special['Notes']) and special['Notes'] != '' else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export CEO Specials
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export CEO Special Prices")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{client}_ceo_special_prices_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="ceo_csv"
            )
        
        with col2:
            st.download_button(
                label="📄 Download Summary",
                data=f"""
{client} CEO Special Prices Summary
===================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Offers: {len(filtered_data)}
Active Offers: {len(filtered_data[filtered_data['Expiry_Date'] >= datetime.now().strftime('%Y-%m-%d')])}

Special Prices:
{chr(10).join([f"• {row['Article_Number']} - {row['Product_Name']}: {row['Special_Price']} {row['Currency']} (Incoterm: {row['Incoterm']}, Until: {row['Expiry_Date']})" for _, row in filtered_data.iterrows()])}
                """,
                file_name=f"{client}_ceo_specials_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="ceo_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No CEO special prices match your search criteria.")

def price_intelligence_tab():
    """CEO Price Intelligence - Cross-client price comparison"""
    st.markdown("""
    <div class="intelligence-header">
        <h2 style="margin:0;">💰 CEO Price Intelligence</h2>
        <p style="margin:0; opacity:0.9;">Cross-Client Price Comparison • Market Intelligence • Strategic Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🔍 **Search across selected clients to compare pricing strategies and identify opportunities**")
    
    available_clients = st.session_state.user_clients
    
    if len(available_clients) < 2:
        st.warning("🔒 You need access to at least 2 clients to compare prices. Currently you only have access to: " + ", ".join(available_clients))
    
    # Search Configuration Section
    st.subheader("🔧 Search Configuration")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        client_selection = st.multiselect(
            "**SELECT CLIENTS TO ANALYZE**",
            options=available_clients,
            default=available_clients,
            key="intelligence_clients"
        )
    
    with col2:
        search_term = st.text_input("**ENTER ARTICLE NUMBER OR PRODUCT NAME**", 
                                  placeholder="e.g., 281, Chocolate, Date Mix...", 
                                  key="intelligence_search")
    
    with col3:
        supplier_filter = st.selectbox("**SUPPLIER**", ["All", "Backaldrin", "Bateel"], key="intelligence_supplier")
    
    # Analyze Button
    if st.button("🚀 ANALYZE PRICES ACROSS SELECTED CLIENTS", use_container_width=True, type="primary", key="intelligence_analyze"):
        if search_term and client_selection:
            analyze_cross_client_prices(search_term, client_selection, supplier_filter)
        else:
            if not search_term:
                st.error("❌ Please enter an article number or product name to analyze")
            if not client_selection:
                st.error("❌ Please select at least one client to analyze")

def analyze_cross_client_prices(search_term, selected_clients, supplier_filter="All"):
    """Analyze prices across selected clients for a given search term"""
    st.subheader(f"🔍 Analysis Results: '{search_term}'")
    st.info(f"**Clients Analyzed:** {', '.join(selected_clients)}")
    
    all_results = {}
    total_records = 0
    found_articles = set()
    
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
        st.warning(f"❌ No results found for '{search_term}' across selected clients")
        return
    
    all_prices = []
    for client_supplier, results in all_results.items():
        for result in results:
            if result['has_data']:
                all_prices.extend(result['all_prices'])
    
    # Display overview statistics
    st.subheader("📊 Cross-Client Price Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Price Records", total_records)
    with col2:
        if all_prices:
            price_range = max(all_prices) - min(all_prices) if all_prices else 0
            st.metric("Price Range", f"${price_range:.2f}/kg")
        else:
            st.metric("Price Range", "N/A")
    with col3:
        overall_min = min(all_prices) if all_prices else "N/A"
        st.metric("Lowest Price", f"${overall_min}/kg" if all_prices else "N/A")
    with col4:
        overall_max = max(all_prices) if all_prices else "N/A"
        st.metric("Highest Price", f"${overall_max}/kg" if all_prices else "N/A")
    
    # Display detailed comparison
    st.subheader("🏢 Client-by-Client Price Comparison")
    
    articles_data = {}
    
    for client_supplier, results in all_results.items():
        client_name, supplier_name = client_supplier.split(" - ")
        for result in results:
            article_num = result['article']
            if article_num not in articles_data:
                articles_data[article_num] = {
                    'product_names': result['product_names'],
                    'client_data': {}
                }
            articles_data[article_num]['client_data'][client_supplier] = result
    
    for article_num, article_data in articles_data.items():
        st.markdown(f"### 📦 Article: {article_num}")
        st.caption(f"**Product Names:** {', '.join(article_data['product_names'])}")
        
        comparison_data = []

        for client_supplier in all_results.keys():
            client_name, supplier_name = client_supplier.split(" - ")
            result = article_data['client_data'].get(client_supplier)
            
            if result and result['has_data']:
                comparison_data.append({
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min Price': f"${result['min_price']:.2f}",
                    'Max Price': f"${result['max_price']:.2f}",
                    'Records': result['records'],
                    'Status': '✅ Available'
                })
            else:
                comparison_data.append({
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min Price': "N/A",
                    'Max Price': "N/A", 
                    'Records': "0",
                    'Status': '❌ Not Available'
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        st.markdown("#### 📈 Detailed Price History")
        
        for client_supplier, result in article_data['client_data'].items():
            client_name, supplier_name = client_supplier.split(" - ")
            
            if result['has_data']:
                is_best = result['min_price'] == overall_min if all_prices else False
                is_worst = result['max_price'] == overall_max if all_prices else False
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{client_name} - {supplier_name}**")
                    
                with col2:
                    st.markdown(f"**${result['min_price']:.2f} - ${result['max_price']:.2f}**/kg")
                    st.caption(f"Range: ${result['max_price'] - result['min_price']:.2f}")
                    st.caption(f"{result['records']} records")
                
                badge_col1, badge_col2 = st.columns(2)
                with badge_col1:
                    if is_best:
                        st.success("🎯 BEST PRICE")
                with badge_col2:
                    if is_worst:
                        st.error("⚠️ HIGHEST PRICE")
                
                with st.expander(f"View price history for {client_name}"):
                    cols = st.columns(2)
                    for i, order in enumerate(result['orders']):
                        with cols[i % 2]:
                            try:
                                price_value = float(order['price']) if order['price'] else 0
                                price_display = f"${price_value:.2f}"
                            except (ValueError, TypeError):
                                price_display = f"${order['price']}" if order['price'] else "$N/A"
                            
                            st.markdown(f"""
                            <div class="price-box">
                                <div style="font-size: 1.1em; font-weight: bold;">{price_display}/kg</div>
                                <div class="order-info">
                                    <strong>Order:</strong> {order['order_no']}<br>
                                    <strong>Date:</strong> {order['date']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.warning(f"**{client_name} - {supplier_name}**: ❌ No pricing data available for this article")
        
        st.markdown("---")
    
    # Export intelligence report
    st.subheader("📤 Export Price Intelligence Report")
    
    export_data = []
    for article_num, article_data in articles_data.items():
        for client_supplier, result in article_data['client_data'].items():
            client_name, supplier_name = client_supplier.split(" - ")
            
            if result['has_data']:
                export_data.append({
                    'Article_Number': article_num,
                    'Product_Names': ', '.join(result['product_names']),
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min_Price': result['min_price'],
                    'Max_Price': result['max_price'], 
                    'Records_Count': result['records'],
                    'Status': 'Available',
                    'Analysis_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                export_data.append({
                    'Article_Number': article_num,
                    'Product_Names': ', '.join(result['product_names']),
                    'Client': client_name,
                    'Supplier': supplier_name,
                    'Min_Price': 'N/A',
                    'Max_Price': 'N/A',
                    'Records_Count': 0,
                    'Status': 'Not Available',
                    'Analysis_Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    if export_data:
        export_df = pd.DataFrame(export_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Report",
                data=csv,
                file_name=f"price_intelligence_{search_term}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="intelligence_csv"
            )
        
        with col2:
            st.download_button(
                label="📄 Download Summary",
                data=f"""
Price Intelligence Report
=========================

Search Term: {search_term}
Clients Analyzed: {', '.join(selected_clients)}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Records Analyzed: {total_records}

Overall Price Range: ${overall_min if all_prices else 'N/A'} - ${overall_max if all_prices else 'N/A'}/kg

Detailed Findings:
{chr(10).join([f"• {row['Client']} - {row['Supplier']}: {row['Article_Number']} - Min:${row['Min_Price'] if row['Status'] == 'Available' else 'N/A'}, Max:${row['Max_Price'] if row['Status'] == 'Available' else 'N/A'}/kg ({row['Status']})" for row in export_data])}
                """,
                file_name=f"price_intelligence_summary_{search_term}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="intelligence_summary"
            )
            
    
    st.markdown('</div>', unsafe_allow_html=True)

def product_catalog_tab():
    """Full Product Catalog with comprehensive product information"""
    
    st.markdown("""
    <div class="product-catalog-header">
        <h2 style="margin:0;">📦 Full Product Catalog</h2>
        <p style="margin:0; opacity:0.9;">Complete Product Database • Technical Specifications • Search & Filter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load product catalog data
    catalog_data = load_product_catalog()
    
    if catalog_data.empty:
        st.warning("""
        ⚠️ **Product catalog not found or empty!**
        
        **To get started:**
        1. Go to your Google Sheet
        2. Add a new tab called **'FullProductList'**
        3. Use these columns (at minimum):
           - Article_Number
           - Product_Name
           - Supplier
        """)
        return
    
    # Catalog Overview
    st.subheader("📊 Catalog Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", len(catalog_data))
    
    with col2:
        if 'Supplier' in catalog_data.columns:
            suppliers = catalog_data['Supplier'].nunique()
            st.metric("Suppliers", suppliers)
        else:
            st.metric("Suppliers", "N/A")
    
    with col3:
        if 'Category' in catalog_data.columns:
            categories = catalog_data['Category'].nunique()
            st.metric("Categories", categories)
        else:
            st.metric("Categories", "N/A")
    
    with col4:
        articles_with_data = catalog_data['Article_Number'].nunique()
        st.metric("Unique Articles", articles_with_data)
    
    # Search and Filter Section
    st.subheader("🔍 Search & Filter Products")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search by article, product name, or description...", key="catalog_search")
    
    with col2:
        if 'Supplier' in catalog_data.columns:
            supplier_filter = st.selectbox("Supplier", ["All"] + list(catalog_data['Supplier'].unique()), key="catalog_supplier")
        else:
            supplier_filter = "All"
            st.selectbox("Supplier", ["No supplier data"], key="catalog_supplier", disabled=True)
    
    with col3:
        if 'Category' in catalog_data.columns:
            category_filter = st.selectbox("Category", ["All"] + list(catalog_data['Category'].unique()), key="catalog_category")
        else:
            category_filter = "All"
            st.selectbox("Category", ["No category data"], key="catalog_category", disabled=True)
    
    # Filter data
    filtered_data = catalog_data.copy()
    
    if search_term:
        mask = filtered_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_data = filtered_data[mask]
    
    if supplier_filter != "All" and 'Supplier' in catalog_data.columns:
        filtered_data = filtered_data[filtered_data['Supplier'] == supplier_filter]
    
    if category_filter != "All" and 'Category' in catalog_data.columns:
        filtered_data = filtered_data[filtered_data['Category'] == category_filter]
    
    # Display Results
    st.subheader(f"📋 Products Found: {len(filtered_data)}")
    
    if not filtered_data.empty:
        # Show product cards
        for _, product in filtered_data.iterrows():
            display_product_card_flexible(product, catalog_data.columns)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Product Catalog")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"product_catalog_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="catalog_csv"
            )
        
        with col2:
            export_text = f"""Product Catalog Export
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Products: {len(filtered_data)}

Products:
{chr(10).join([f"• {row['Article_Number']} - {row['Product_Name']} " + (f"({row['Supplier']})" if 'Supplier' in row and row['Supplier'] else '') for _, row in filtered_data.iterrows()])}
"""
            st.download_button(
                label="📄 Download Summary",
                data=export_text,
                file_name=f"product_catalog_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="catalog_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No products match your search criteria.")

def display_product_card_flexible(product, available_columns):
    """Display individual product card with available columns only"""
    
    if 'Supplier' in available_columns and product['Supplier'] == 'Backaldrin':
        card_class = "price-card"
        border_color = "#991B1B"
    elif 'Supplier' in available_columns and product['Supplier'] == 'Bateel':
        card_class = "special-price-card"
        border_color = "#D97706"
    else:
        card_class = "intelligence-stat-card"
        border_color = "#059669"
    
    with st.expander(f"📦 {product['Article_Number']} - {product['Product_Name']}", expanded=False):
        # Build HTML content as a single line string
        html_content = f'<div class="{card_class}"><div style="border-left: 5px solid {border_color}; padding-left: 1rem;"><h3 style="margin:0; color: {border_color};">{product["Article_Number"]} - {product["Product_Name"]}</h3>'
        
        if 'Supplier' in available_columns:
            html_content += f'<p style="margin:0; font-weight: bold; color: #6B7280;">Supplier: {product["Supplier"]}</p>'
        
        html_content += '<div style="margin-top: 1rem;"><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">'
        
        # Left column
        left_content = ""
        if 'Category' in available_columns and product['Category']:
            left_content += f'<p style="margin:0;"><strong>Main Category:</strong> {product["Category"]}</p>'
        if 'Sub_Category' in available_columns and product['Sub_Category']:
            left_content += f'<p style="margin:0;"><strong>Sub Category:</strong> {product["Sub_Category"]}</p>'
        if 'Sub_Sub_Category' in available_columns and product['Sub_Sub_Category']:
            left_content += f'<p style="margin:0;"><strong>Sub-Sub Category:</strong> {product["Sub_Sub_Category"]}</p>'
        
        # Right column
        right_content = ""
        if 'UOM' in available_columns and product['UOM']:
            right_content += f'<p style="margin:0;"><strong>UOM:</strong> {product["UOM"]}</p>'
        if 'Unit_Weight' in available_columns and product['Unit_Weight']:
            right_content += f'<p style="margin:0;"><strong>Unit Weight:</strong> {product["Unit_Weight"]}</p>'
        if 'Current_Price' in available_columns and product['Current_Price']:
            right_content += f'<p style="margin:0;"><strong>Current Price:</strong> ${product["Current_Price"]}/kg</p>'
        
        html_content += f'<div>{left_content}</div><div>{right_content}</div></div></div>'
        
        # Additional fields - now as single line strings
        if 'Common_Description' in available_columns and product['Common_Description']:
            html_content += f'<div style="margin-top: 1rem;"><p style="margin:0;"><strong>Description:</strong></p><p style="margin:0; color: #6B7280;">{product["Common_Description"]}</p></div>'
        
        if 'Purpose_Of_Use' in available_columns and product['Purpose_Of_Use']:
            html_content += f'<div style="margin-top: 1rem;"><p style="margin:0;"><strong>Purpose of Use:</strong></p><p style="margin:0; color: #6B7280;">{product["Purpose_Of_Use"]}</p></div>'
        
        if 'Dosage' in available_columns and product['Dosage']:
            html_content += f'<div style="margin-top: 1rem;"><p style="margin:0;"><strong>Dosage:</strong></p><p style="margin:0; color: #6B7280;">{product["Dosage"]}</p></div>'
        
        if 'Ingredients' in available_columns and product['Ingredients']:
            # Escape HTML tags in ingredients
            ingredients = str(product['Ingredients']).replace('<', '&lt;').replace('>', '&gt;')
            html_content += f'<div style="margin-top: 1rem;"><p style="margin:0;"><strong>Ingredients:</strong></p><p style="margin:0; color: #6B7280; white-space: pre-wrap;">{ingredients}</p></div>'
        
        if 'Datasheet_Link' in available_columns and product['Datasheet_Link']:
            html_content += f'<div style="margin-top: 1rem;"><p style="margin:0;"><strong>Datasheet:</strong> <a href="{product["Datasheet_Link"]}" target="_blank" style="color: #0EA5E9;">View Datasheet</a></p></div>'
        
        # Close the main divs
        html_content += "</div></div>"
        
        st.markdown(html_content, unsafe_allow_html=True)

def palletizing_tab():
    """Quick Pallet Calculator for CDC Items"""
    st.markdown("""
    <div class="palletizing-header">
        <h2 style="margin:0;">📦 Quick Pallet Calculator</h2>
        <p style="margin:0; opacity:0.9;">Instant Pallet Calculations • CDC Standard Items • Real-time Results</p>
    </div>
    """, unsafe_allow_html=True)
    
    quick_pallet_calculator()

def quick_pallet_calculator():
    """Quick Pallet Calculator for CDC Items"""
    st.subheader("🧮 Quick Pallet Calculator")
    
    # CDC Common Items Database
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
        selected_item = st.selectbox(
            "Select Item:",
            list(cdc_items.keys()),
            key="item_select"
        )
        
        quantity = st.number_input(
            "Quantity:",
            min_value=1,
            value=100,
            step=1,
            key="quantity"
        )
        
        uom = st.selectbox(
            "Unit of Measure:",
            ["Cartons", "KGs", "Pallets"],
            key="uom"
        )
    
    with col2:
        if selected_item == "Custom Item":
            st.info("🔧 Enter Custom Item Details:")
            packing = st.text_input("Packing (e.g., 5kg, 25kg):", value="5kg", key="custom_packing")
            cartons_per_pallet = st.number_input("Cartons per Pallet:", min_value=1, value=100, step=1, key="custom_cartons")
            weight_per_carton = st.number_input("Weight per Carton (kg):", min_value=0.1, value=5.0, step=0.1, key="custom_weight")
        else:
            item_data = cdc_items[selected_item]
            packing = item_data["packing"]
            cartons_per_pallet = item_data["cartons_per_pallet"]
            weight_per_carton = item_data["weight_per_carton"]
            
            st.info(f"📦 **Standard Packing:** {packing}")
            st.info(f"📊 **Cartons per Pallet:** {cartons_per_pallet}")
            st.info(f"⚖️ **Weight per Carton:** {weight_per_carton} kg")
    
    # REAL-TIME CALCULATIONS
    if quantity > 0:
        st.subheader("🎯 INSTANT PALCALC RESULTS")
        
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
            if full_pallets > 0:
                st.success(f"### 📦 {full_pallets:,.0f} FULL PALLET{'S' if full_pallets > 1 else ''}")
            else:
                st.info("### 📦 0 FULL PALLETS")
                
        with col2:
            if partial_pallet_cartons > 0:
                st.warning(f"### 📦 1 PARTIAL PALLET")
                st.write(f"({partial_pallet_cartons:,.0f} cartons - {partial_pallet_percentage:.1f}% full)")
            else:
                st.success("### ✅ NO PARTIAL PALLETS")
                
        with col3:
            st.info(f"### ⚖️ {total_weight:,.0f} kg")
            st.write(f"({total_cartons:,.0f} cartons total)")
        
        with st.expander("📊 View Detailed Calculation", expanded=False):
            st.write(f"**Item:** {selected_item} ({packing})")
            
            if uom == "Cartons":
                st.write(f"**Input:** {quantity:,.0f} cartons")
            elif uom == "KGs":
                st.write(f"**Input:** {quantity:,.0f} kg = {total_cartons:,.0f} cartons")
            else:
                st.write(f"**Input:** {quantity:,.0f} pallets = {total_cartons:,.0f} cartons")
            
            st.write(f"**Calculation:** {total_cartons:,.0f} cartons ÷ {cartons_per_pallet} cartons/pallet")
            st.write(f"**Result:** {full_pallets:,.0f} full pallets + {partial_pallet_cartons:,.0f} cartons partial")
        
        st.subheader("💡 Quick Examples")
        
        examples_col1, examples_col2 = st.columns(2)
        
        with examples_col1:
            if st.button(f"Example: 100 cartons {selected_item}", key="example_100"):
                st.session_state.quantity = 100
                st.session_state.uom = "Cartons"
                st.rerun()
                
        with examples_col2:
            if st.button(f"Example: 1 pallet {selected_item}", key="example_1"):
                st.session_state.quantity = 1
                st.session_state.uom = "Pallets"
                st.rerun()
        
        st.markdown("---")
        st.subheader("🚢 Container Information")
        st.info("""
        **40ft Container Capacity:**
        - **Max Pallets:** 30 pallets
        - **Max Weight:** 23,000 kg (23 tons)
        - **Your current order:** Will fill approximately **{:.1f}%** of container capacity
        """.format((full_pallets / 30) * 100))
    
    st.markdown("---")
    with st.expander("📊 Bulk Analysis from Google Sheets (Optional)"):
        st.info("For bulk analysis of your existing Palletizing_Data sheet, use the main data import features.")
        st.write("The Quick Calculator above is designed for instant pallet calculations!")

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
