# ============================================
# MULTI-CLIENT PRICING DASHBOARD
# ============================================
# Author: Zaid F. Al-Shami
# Version: 3.0 (with Visual Analytics)
# Last Updated: 8 Dec 2025
# ============================================
# IMPORTANT NOTES:
# 1. This dashboard connects to Google Sheets for real-time data
# 2. All data is cached for 5 minutes to improve performance
# 3. Supports multiple clients: CDC, CoteDivoire, CakeArt, SweetHouse, Cameron
# 4. Features: Smart Search, Price Intelligence, Order Management, Visual Analytics
# ============================================

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO
import re

# NEW IMPORTS FOR VISUAL ANALYTICS
import matplotlib.pyplot as plt
import numpy as np

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
    /* NEW: Visual Analytics header */
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
    /* Sidebar tabs styling */
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
    /* Header styling */
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
    /* Favorites modal */
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
    /* Price matching specific */
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
        "backaldrin": "Backaldrin_CDC",
        "bateel": "Bateel_CDC", 
        "ceo_special": "CDC_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "paid_orders": "Paid_Orders",
        "palletizing": "Palletizing_Data"
    },
    "CoteDivoire": {
        "backaldrin": "Backaldrin_CoteDivoire",
        "bateel": "Bateel_CoteDivoire", 
        "ceo_special": "CoteDivoire_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "CakeArt": {
        "backaldrin": "Backaldrin_CakeArt",
        "bateel": "Bateel_CakeArt",
        "ceo_special": "CakeArt_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "SweetHouse": {
        "backaldrin": "Backaldrin_SweetHouse",
        "bateel": "Bateel_SweetHouse",
        "ceo_special": "SweetHouse_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "Cameron": {
        "backaldrin": "Backaldrin_Cameron",
        "bateel": "Bateel_Cameron", 
        "ceo_special": "Cameron_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    # NEW CLIENTS ADDED HERE
    "Qzine": {
        "backaldrin": "Backaldrin_Qzine",
        "bateel": "Bateel_Qzine",  # If you have Bateel sheet for Qzine
        "ceo_special": "Qzine_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    },
    "MEPT": {
        "backaldrin": "Backaldrin_MEPT",
        "bateel": "Bateel_MEPT",  # If you have Bateel sheet for MEPT
        "ceo_special": "MEPT_CEO_Special_Prices",
        "new_orders": "New_client_orders",
        "palletizing": "Palletizing_Data"
    }
}

# Sheet names
PRODUCT_CATALOG_SHEET = "FullProductList"
PRICES_SHEET = "Prices"

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
            <h2 style="margin-top: 0; color: #991B1B;">⭐ Favorite Searches</h2>
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
                headers = values[start_row]
                rows = values[start_row + 1:] if len(values) > start_row + 1 else []
                
                df = pd.DataFrame(rows, columns=headers)
                df = df.replace('', pd.NA)
                return df
                
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_google_sheets_data(client="CDC"):
    """Optimized version - loads both suppliers in one call and returns proper structure - CACHED"""
    try:
        backaldrin_sheet = f"Backaldrin_{client}"
        bateel_sheet = f"Bateel_{client}"
        
        backaldrin_df = load_sheet_data(backaldrin_sheet)
        bateel_df = load_sheet_data(bateel_sheet)
        
        def convert_df_to_dict(df):
            """Simple converter that builds the expected structure"""
            result = {}
            
            if df.empty:
                return result
            
            # Helper function to find columns
            def get_column(df, possible_names):
                for name in possible_names:
                    if name in df.columns:
                        return name
                return None
            
            # Find columns using lowercase priority first
            article_column = get_column(df, ['article_number', 'Article_Number', 'article', 'Article'])
            product_column = get_column(df, ['product_name', 'Product_Name', 'Product', 'product'])
            price_column = get_column(df, ['price_per_', 'price_per_kg', 'Price_per_', 'Price_per_kg', 'Price', 'price'])
            order_column = get_column(df, ['order_number', 'Order_Number', 'Order', 'order'])
            date_column = get_column(df, ['order_date', 'Order_Date', 'Date', 'date'])
            year_column = get_column(df, ['year', 'Year', 'order_year', 'Order_Year'])
            hs_code_column = get_column(df, ['hs_code', 'HS_Code', 'hs code', 'HS Code'])
            packaging_column = get_column(df, ['packaging', 'Packaging', 'packing', 'Packing'])
            quantity_column = get_column(df, ['quantity', 'Quantity', 'qty', 'Qty'])
            weight_column = get_column(df, ['total_weight', 'Total_Weight', 'weight', 'Weight'])
            total_price_column = get_column(df, ['total_price', 'Total_Price', 'total', 'Total'])

            if not article_column:
                st.error(f"❌ Missing article number column! Available columns: {list(df.columns)}")
                return result

            for _, row in df.iterrows():
                article = str(row.get(article_column, '')).strip()
                if not article:
                    continue
                    
                if article not in result:
                    result[article] = {
                        'names': [],
                        'prices': [],
                        'orders': []
                    }
                
                product_name = str(row.get(product_column, '')).strip() if product_column else ''
                if product_name and product_name not in result[article]['names']:
                    result[article]['names'].append(product_name)
                
                price_str = str(row.get(price_column, '')).strip() if price_column else ''
                if price_str:
                    try:
                        price_float = float(price_str)
                        result[article]['prices'].append(price_float)
                    except:
                        pass
                
                order_details = {
                    'order_no': str(row.get(order_column, '')).strip() if order_column else '',
                    'date': str(row.get(date_column, '')).strip() if date_column else '',
                    'year': str(row.get(year_column, '')).strip() if year_column else '',
                    'product_name': product_name,
                    'article': article,
                    'hs_code': str(row.get(hs_code_column, '')).strip() if hs_code_column else '',
                    'packaging': str(row.get(packaging_column, '')).strip() if packaging_column else '',
                    'quantity': str(row.get(quantity_column, '')).strip() if quantity_column else '',
                    'total_weight': str(row.get(weight_column, '')).strip() if weight_column else '',
                    'price': price_str,
                    'total_price': str(row.get(total_price_column, '')).strip() if total_price_column else ''
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
def load_new_orders_data(client):
    """Load new client orders data from Google Sheets - CACHED"""
    try:
        sheet_name = CLIENT_SHEETS[client]["new_orders"]
        orders_url = f"https://sheets.googleapis.com/v4/spreadsheets/{CDC_SHEET_ID}/values/{sheet_name}!A:Z?key={API_KEY}"
        response = requests.get(orders_url)
        
        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            
            if values and len(values) > 1:
                headers = values[0]
                rows = values[1:]
                
                df = pd.DataFrame(rows, columns=headers)
                
                required_cols = ['Order_Number', 'Product_Name', 'Article_No', 'HS_Code', 'Origin', 
                                'Packing', 'Qty', 'Type', 'Total_Weight', 'Price_in_USD_kg', 'Total_Price']
                
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = ''
                
                if 'Status' not in df.columns:
                    df['Status'] = 'Draft'
                
                numeric_cols = ['Qty', 'Total_Weight', 'Price_in_USD_kg', 'Total_Price']
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df
                
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error loading new orders data for {client}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_orders_data(client):
    """Load ALL orders data - SIMPLE VERSION - CACHED"""
    try:
        sample_orders = [
            {
                'Order Number': 'SA C.D 125/2025', 'ERP': 'Yes', 'Date of request': 'N/A',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': 'N/A',
                'Invoice': 0, 'Payment': 'Credit Note 45550', 'Manufacturer': 'BAJ',
                'ETD': '28-Dec-25', 'Payment due date': '16-Sep-25', 
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'Credit Note 45550'
            },
            {
                'Order Number': 'SA C.D 127/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '12-Oct-25',
                'Invoice': 80500.00, 'Payment': '$80,500.00', 'Manufacturer': 'BAJ',
                'ETD': '30-Oct-25', 'Payment due date': '17-Nov-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 140/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 49092.59, 'Payment': '$49,092.59', 'Manufacturer': 'BAJ',
                'ETD': '17-Nov-25', 'Payment due date': '30-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'New ETD 30 Oct'
            },
            {
                'Order Number': 'SA C.D 135/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 58770.00, 'Payment': '$58,770.00', 'Manufacturer': 'BAJ',
                'ETD': '13-Nov-25', 'Payment due date': '26-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 138/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 42900.00, 'Payment': '$42,900.00', 'Manufacturer': 'BAJ',
                'ETD': '8-Nov-25', 'Payment due date': '21-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 128/2025', 'ERP': 'Bated', 'Date of request': '08-Sep-25',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': '10-Sep-25',
                'Invoice': 46711.00, 'Payment': '$46,711.00', 'Manufacturer': 'BT',
                'ETD': '7-Nov-25', 'Payment due date': '20-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'ETD was shared by CEO with Ammar'
            },
            {
                'Order Number': 'SA C.D 115/2025', 'ERP': 'Yes', 'Date of request': '22-Jul-25',
                'Date of PI issue': '05-Aug-25', 'Date of Client signing': '07-Aug-25',
                'Invoice': 36228.00, 'Payment': '$36,228.00', 'Manufacturer': 'BAJ',
                'ETD': '6-Nov-25', 'Payment due date': '19-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'Will follow'
            },
            {
                'Order Number': 'SA C.D 130/2025', 'ERP': 'Yes', 'Date of request': '08-Sep-25',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': '10-Sep-25',
                'Invoice': 38550.30, 'Payment': '$38,550.30', 'Manufacturer': 'BAJ',
                'ETD': '6-Nov-25', 'Payment due date': '19-Oct-25',
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 136/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 27140.00, 'Payment': '$27,140.00', 'Manufacturer': 'BAJ',
                'ETD': '3-Nov-25', 'Payment due date': '16-Oct-25',
                'Payment Update': 'Pending', 'Status': 'In Production', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 137/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '09-Oct-25',
                'Invoice': 32190.00, 'Payment': '$32,190.00', 'Manufacturer': 'BAJ',
                'ETD': '3-Nov-25', 'Payment due date': '16-Oct-25',
                'Payment Update': 'Pending', 'Status': 'In Production', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 133/2025', 'ERP': 'Yes', 'Date of request': '08-Sep-25',
                'Date of PI issue': '14-Sep-25', 'Date of Client signing': '15-Sep-25',
                'Invoice': 48966.10, 'Payment': '$48,966.10', 'Manufacturer': 'BAJ',
                'ETD': '20-Oct-25', 'Payment due date': '2-Oct-25',
                'Payment Update': 'Due', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 129/2025', 'ERP': 'Yes', 'Date of request': '08-Sep-25',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': '10-Sep-25',
                'Invoice': 55668.20, 'Payment': '$55,668.20', 'Manufacturer': 'BAJ',
                'ETD': '19-Oct-25', 'Payment due date': '1-Oct-25',
                'Payment Update': 'Due', 'Status': 'Shipped', 'Notes': ''
            },
            {
                'Order Number': 'SA C.D 144/2025', 'ERP': 'Yes', 'Date of request': '08-Oct-25',
                'Date of PI issue': '09-Oct-25', 'Date of Client signing': '12-Oct-25',
                'Invoice': 69494.00, 'Payment': '$69,494.00', 'Manufacturer': 'BAJ',
                'ETD': '19-Nov-25', 'Payment due date': '18-Jan-00',
                'Payment Update': 'Pending', 'Status': 'Pending', 'Notes': 'add chocolate'
            }
        ]
        
        df = pd.DataFrame(sample_orders)
        return df
        
    except Exception as e:
        st.error(f"Error loading orders data: {str(e)}")
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
                "📋 NEW ORDERS",
                "📅 ETD SHEET",
                "⭐ CEO SPECIAL PRICES",
                "💰 PRICE INTELLIGENCE",
                "📦 PRODUCT CATALOG",
                "📊 ORDERS MANAGEMENT",
                "📦 PALLETIZING",
                "🔴 PRICE MATCHING",
                "📈 VISUAL ANALYTICS"  # NEW TAB ADDED HERE
            ]
        else:
            tabs = [
                "🏢 CLIENTS",
                "💰 PRICES", 
                "📋 NEW ORDERS",
                "📅 ETD SHEET",
                "⭐ CEO SPECIAL PRICES",
                "💰 PRICE INTELLIGENCE",
                "📦 PRODUCT CATALOG",
                "📊 ORDERS MANAGEMENT"
            ]
            if st.session_state.username in ["zaid", "Rotana", "Khalid"]:
                tabs.append("📦 PALLETIZING")
            tabs.append("🔴 PRICE MATCHING")
            tabs.append("📈 VISUAL ANALYTICS")  # NEW TAB ADDED FOR ALL USERS
        
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
            "🔴 **NEW**: Price Matching Tool available for all clients!",
            "📈 **NEW**: Visual Analytics Dashboard added!"  # NEW ANNOUNCEMENT
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
    
    # Main content area based on active tab
    st.markdown(f"""
    <div class="main-header">
        <h1>Backaldrin Arab Jordan Dashboard</h1>
        <h3>{st.session_state.active_tab}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the active tab content
    if st.session_state.active_tab == "🏢 CLIENTS":
        clients_tab()
    elif st.session_state.active_tab == "💰 PRICES":
        prices_tab()
    elif st.session_state.active_tab == "📋 NEW ORDERS":
        new_orders_tab()
    elif st.session_state.active_tab == "📅 ETD SHEET":
        etd_tab()
    elif st.session_state.active_tab == "⭐ CEO SPECIAL PRICES":
        ceo_specials_tab()
    elif st.session_state.active_tab == "💰 PRICE INTELLIGENCE":
        price_intelligence_tab()
    elif st.session_state.active_tab == "📦 PRODUCT CATALOG":
        product_catalog_tab()
    elif st.session_state.active_tab == "📊 ORDERS MANAGEMENT":
        orders_management_tab()
    elif st.session_state.active_tab == "📦 PALLETIZING":
        palletizing_tab()
    elif st.session_state.active_tab == "🔴 PRICE MATCHING":
        price_matching_tab()
    elif st.session_state.active_tab == "📈 VISUAL ANALYTICS":  # NEW TAB HANDLER
        visual_analytics_tab()
    
    # Logout button at bottom
    st.markdown("---")
    logout_button()

# ============================================
# NEW VISUAL ANALYTICS TAB FUNCTION
# ============================================

def visual_analytics_tab():
    """
    NEW: Visual Analytics Tab with Interactive Charts
    This tab provides graphical analysis of sales data, price trends, and product performance
    """
    st.markdown("""
    <div class="visual-header">
        <h2 style="margin:0;">📈 Visual Analytics Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Interactive Charts • Sales Trends • Product Performance • Custom Visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection
    available_clients = st.session_state.user_clients
    if not available_clients:
        st.warning("No clients available for your account")
        return
    
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="visual_client_select"
    )
    
    # Load client data
    with st.spinner(f"📥 Loading data for {client}..."):
        DATA = get_google_sheets_data(client)
    
    if not DATA.get("Backaldrin") and not DATA.get("Bateel"):
        st.error(f"❌ No data found for {client}")
        return
    
    st.success(f"✅ Loaded data for {client}")
    
    # Supplier selection
    supplier = st.radio(
        "Select Supplier:",
        ["Backaldrin", "Bateel"],
        horizontal=True,
        key="visual_supplier"
    )
    
    # ============================================
    # SECTION 1: PRODUCT SELECTION
    # ============================================
    st.subheader("🎯 Select Product for Analysis")
    
    # Get all articles from the selected supplier
    supplier_data = DATA.get(supplier, {})
    articles = list(supplier_data.keys())
    
    if not articles:
        st.info(f"No articles found for {supplier} - {client}")
        return
    
    # Create searchable select box
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_article = st.selectbox(
            "Search and select article:",
            articles,
            format_func=lambda x: f"{x} - {supplier_data[x]['names'][0] if supplier_data[x]['names'] else 'No Name'}",
            key="visual_article_select"
        )
    
    with col2:
        # Time range selection
        time_range = st.selectbox(
            "Time Period:",
            ["All Time", "Last 2 Years", "Last Year", "Last 6 Months", "Custom"],
            key="visual_time_range"
        )
    
    # Get selected article data
    article_data = supplier_data.get(selected_article, {})
    
    if not article_data:
        st.error(f"No data found for article {selected_article}")
        return
    
    # ============================================
    # SECTION 2: PERFORMANCE METRICS
    # ============================================
    st.subheader("📊 Performance Overview")
    
    # Calculate metrics
    orders = article_data.get('orders', [])
    prices = article_data.get('prices', [])
    
    if not orders:
        st.info(f"No order history for article {selected_article}")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(orders)
        st.metric("Total Orders", total_orders)
    
    with col2:
        avg_price = sum(prices) / len(prices) if prices else 0
        st.metric("Avg Price/kg", f"${avg_price:.2f}")
    
    with col3:
        min_price = min(prices) if prices else 0
        st.metric("Min Price", f"${min_price:.2f}")
    
    with col4:
        max_price = max(prices) if prices else 0
        st.metric("Max Price", f"${max_price:.2f}")
    
    # ============================================
    # SECTION 3: PRICE TREND CHART
    # ============================================
    st.subheader("📈 Price Trend Over Time")
    
    # Prepare data for chart
    chart_data = []
    for order in orders:
        try:
            price = float(order.get('price', 0))
            date_str = order.get('date', '')
            if price > 0 and date_str:
                # Try to parse date
                try:
                    # Handle different date formats
                    for fmt in ['%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
                        try:
                            date = datetime.strptime(date_str, fmt)
                            chart_data.append({
                                'Date': date,
                                'Price': price,
                                'Order': order.get('order_no', ''),
                                'Quantity': float(order.get('quantity', 0) or 0),
                                'Total_Weight': float(order.get('total_weight', 0) or 0)
                            })
                            break
                        except:
                            continue
                except:
                    continue
        except:
            continue
    
    if chart_data:
        # Create DataFrame for charting
        df_chart = pd.DataFrame(chart_data)
        df_chart = df_chart.sort_values('Date')
        
        # Chart 1: Price Trend Line
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**Price per kg over time**")
            st.line_chart(df_chart.set_index('Date')['Price'], use_container_width=True)
        
        with col2:
            st.markdown("**Statistics**")
            st.write(f"First order: {df_chart['Date'].min().strftime('%b %Y')}")
            st.write(f"Latest order: {df_chart['Date'].max().strftime('%b %Y')}")
            st.write(f"Total period: {(df_chart['Date'].max() - df_chart['Date'].min()).days} days")
        
        # Chart 2: Quantity vs Price Scatter
        st.subheader("📊 Quantity vs Price Analysis")
        
        if not df_chart.empty and 'Quantity' in df_chart.columns and df_chart['Quantity'].sum() > 0:
            # Scatter plot
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            scatter = ax1.scatter(df_chart['Quantity'], df_chart['Price'], 
                                 c=range(len(df_chart)), cmap='viridis', s=100, alpha=0.6)
            
            # Add labels and trend line
            ax1.set_xlabel('Quantity (units)')
            ax1.set_ylabel('Price ($/kg)')
            ax1.set_title(f'Quantity vs Price - {selected_article}')
            ax1.grid(True, alpha=0.3)
            
            # Add trend line if enough points
            if len(df_chart) > 1:
                z = np.polyfit(df_chart['Quantity'], df_chart['Price'], 1)
                p = np.poly1d(z)
                ax1.plot(df_chart['Quantity'], p(df_chart['Quantity']), "r--", alpha=0.5, 
                        label=f'Trend: y={z[0]:.4f}x + {z[1]:.2f}')
                ax1.legend()
            
            # Add colorbar
            plt.colorbar(scatter, ax=ax1, label='Order Sequence')
            
            st.pyplot(fig1)
            
            # Insights
            correlation = df_chart['Quantity'].corr(df_chart['Price'])
            st.info(f"**Insight:** Quantity-Price correlation: {correlation:.3f}")
            if correlation < -0.3:
                st.success("✅ **Negative correlation:** Higher quantities tend to get better prices")
            elif correlation > 0.3:
                st.warning("⚠️ **Positive correlation:** Higher quantities might be paying more")
            else:
                st.info("ℹ️ **Weak correlation:** Quantity doesn't strongly affect price")
        
        # Chart 3: Monthly Aggregation
        st.subheader("📅 Monthly Performance")
        
        # Group by month
        df_chart['YearMonth'] = df_chart['Date'].dt.to_period('M')
        monthly_data = df_chart.groupby('YearMonth').agg({
            'Price': ['mean', 'count', 'min', 'max'],
            'Quantity': 'sum',
            'Total_Weight': 'sum'
        }).round(2)
        
        monthly_data.columns = ['Avg_Price', 'Order_Count', 'Min_Price', 'Max_Price', 'Total_Quantity', 'Total_Weight']
        monthly_data = monthly_data.reset_index()
        monthly_data['YearMonth'] = monthly_data['YearMonth'].astype(str)
        
        # Display monthly table
        with st.expander("📋 View Monthly Breakdown", expanded=True):
            st.dataframe(
                monthly_data.style
                .background_gradient(subset=['Avg_Price'], cmap='RdYlGn_r')
                .background_gradient(subset=['Total_Quantity'], cmap='Blues')
                .format({'Avg_Price': '${:.2f}', 'Min_Price': '${:.2f}', 'Max_Price': '${:.2f}'}),
                use_container_width=True
            )
        
        # Chart 4: Bar chart for monthly comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Monthly Average Price**")
            st.bar_chart(monthly_data.set_index('YearMonth')['Avg_Price'])
        
        with col2:
            st.markdown("**Monthly Order Count**")
            st.bar_chart(monthly_data.set_index('YearMonth')['Order_Count'])
        
        # ============================================
        # SECTION 4: COMPARATIVE ANALYSIS
        # ============================================
        st.subheader("🔍 Comparative Analysis")
        
        # Compare with other articles
        compare_articles = st.multiselect(
            "Compare with other articles:",
            [a for a in articles if a != selected_article],
            max_selections=3,
            key="compare_articles"
        )
        
        if compare_articles:
            comparison_data = []
            for article in [selected_article] + compare_articles:
                art_data = supplier_data.get(article, {})
                art_prices = art_data.get('prices', [])
                if art_prices:
                    comparison_data.append({
                        'Article': article,
                        'Name': art_data.get('names', [''])[0],
                        'Avg_Price': sum(art_prices) / len(art_prices),
                        'Min_Price': min(art_prices),
                        'Max_Price': max(art_prices),
                        'Order_Count': len(art_data.get('orders', [])),
                        'Price_Range': max(art_prices) - min(art_prices)
                    })
            
            if comparison_data:
                df_comparison = pd.DataFrame(comparison_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Price Comparison**")
                    fig2, ax2 = plt.subplots(figsize=(8, 6))
                    
                    articles_list = df_comparison['Article'].tolist()
                    avg_prices = df_comparison['Avg_Price'].tolist()
                    
                    bars = ax2.bar(range(len(articles_list)), avg_prices, 
                                  color=['#991B1B' if a == selected_article else '#6B7280' for a in articles_list],
                                  alpha=0.7)
                    
                    ax2.set_xlabel('Article')
                    ax2.set_ylabel('Average Price ($/kg)')
                    ax2.set_title('Average Price Comparison')
                    ax2.set_xticks(range(len(articles_list)))
                    ax2.set_xticklabels([f"{a[:15]}..." for a in articles_list], rotation=45, ha='right')
                    
                    # Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        ax2.text(bar.get_x() + bar.get_width()/2., height,
                                f'${height:.2f}', ha='center', va='bottom')
                    
                    st.pyplot(fig2)
                
                with col2:
                    st.markdown("**Comparison Table**")
                    st.dataframe(
                        df_comparison.style
                        .highlight_max(subset=['Avg_Price'], color='#FECACA')
                        .highlight_min(subset=['Avg_Price'], color='#D1FAE5')
                        .format({'Avg_Price': '${:.2f}', 'Min_Price': '${:.2f}', 
                                'Max_Price': '${:.2f}', 'Price_Range': '${:.2f}'}),
                        use_container_width=True
                    )
        
        # ============================================
        # SECTION 5: EXPORT VISUAL REPORT
        # ============================================
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Visual Report")
        
        # Generate summary report
        report_text = f"""
VISUAL ANALYTICS REPORT
=======================

Client: {client}
Supplier: {supplier}
Article: {selected_article}
Product: {article_data.get('names', [''])[0]}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

PERFORMANCE SUMMARY:
• Total Orders: {total_orders}
• Average Price: ${avg_price:.2f}/kg
• Price Range: ${min_price:.2f} - ${max_price:.2f}/kg
• Analysis Period: {df_chart['Date'].min().strftime('%b %d, %Y')} to {df_chart['Date'].max().strftime('%b %d, %Y')}

MONTHLY BREAKDOWN:
{chr(10).join([f"• {row['YearMonth']}: ${row['Avg_Price']:.2f} avg ({row['Order_Count']} orders, {row['Total_Quantity']} units)" 
               for _, row in monthly_data.iterrows()])}

KEY INSIGHTS:
1. Price stability: {'Stable' if (max_price - min_price) < avg_price * 0.2 else 'Volatile'}
2. Order frequency: {'Regular' if len(df_chart) / ((df_chart['Date'].max() - df_chart['Date'].min()).days/30) > 0.5 else 'Irregular'}
3. Best performing month: {monthly_data.loc[monthly_data['Order_Count'].idxmax(), 'YearMonth']}
4. Highest average price: ${monthly_data['Avg_Price'].max():.2f} in {monthly_data.loc[monthly_data['Avg_Price'].idxmax(), 'YearMonth']}

RECOMMENDATIONS:
• Consider price adjustment if volatility > 20%
• Monitor order patterns for seasonal trends
• Compare with market benchmarks regularly
        """
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download CSV
            if not df_chart.empty:
                csv = df_chart.to_csv(index=False)
                st.download_button(
                    label="📥 Download Chart Data (CSV)",
                    data=csv,
                    file_name=f"{client}_{supplier}_{selected_article}_chart_data.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="visual_csv"
                )
        
        with col2:
            # Download Report
            st.download_button(
                label="📄 Download Analysis Report",
                data=report_text,
                file_name=f"{client}_{supplier}_{selected_article}_analysis_report.txt",
                mime="text/plain",
                use_container_width=True,
                key="visual_report"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.warning("No valid date/price data available for charting")
    
    # ============================================
    # SECTION 6: QUICK TIPS
    # ============================================
    with st.expander("💡 How to use this dashboard"):
        st.markdown("""
        **📈 Visual Analytics Guide:**
        
        1. **Select Client & Supplier** - Choose which data to analyze
        2. **Search Article** - Use dropdown to find specific products
        3. **Analyze Trends** - View price changes over time
        4. **Compare Products** - Select multiple articles for comparison
        5. **Export Insights** - Download reports for presentations
        
        **Key Metrics to Watch:**
        - **Price Volatility**: Large price swings may indicate market changes
        - **Order Frequency**: Regular orders suggest stable demand
        - **Quantity-Price Correlation**: Bulk discounts or premium pricing patterns
        - **Monthly Trends**: Seasonal demand patterns
        
        **Pro Tips:**
        - Use monthly breakdown to identify seasonal patterns
        - Compare similar products to spot pricing opportunities
        - Export charts for client presentations
        - Monitor price stability for negotiation strategies
        """)




# ============================================
# ORIGINAL TAB FUNCTIONS (REMAIN UNCHANGED)
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
    """Client pricing dashboard with FOUR NEW FEATURES"""
    
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
    """Display search results with NEW CARD DESIGN AND FAVORITES FEATURE"""
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
    
    # UPDATED: NEW CARD DESIGN
    st.subheader("💵 Historical Prices with Order Details")
    cols = st.columns(2)
    for i, order in enumerate(article_data['orders']):
        with cols[i % 2]:
            order_details = f"""
            <div class="price-box">
                <div style="font-size: 1.4em; font-weight: bold; border-bottom: 2px solid white; padding-bottom: 0.5rem; margin-bottom: 0.5rem;">
                    📦 {order.get('order_no', 'N/A')}
                </div>
                <div style="font-size: 1.1em; margin-bottom: 0.5rem;">
                    <strong>📅 Date:</strong> {order.get('date', 'N/A')}
                </div>
                <div style="font-size: 1.3em; font-weight: bold; color: #FEF3C7; margin-bottom: 0.8rem;">
                    ${order.get('price', 'N/A')}/kg
                </div>
                <div class="order-info">
                    <strong>📦 Product:</strong> {order.get('product_name', 'N/A')}<br>
                    <strong>🔢 Article:</strong> {order.get('article', 'N/A')}<br>
                    {f"<strong>📅 Year:</strong> {order.get('year', 'N/A')}<br>" if order.get('year') else ""}
                    {f"<strong>🏷️ HS Code:</strong> {order.get('hs_code', 'N/A')}<br>" if order.get('hs_code') else ""}
                    {f"<strong>📦 Packaging:</strong> {order.get('packaging', 'N/A')}<br>" if order.get('packaging') else ""}
                    {f"<strong>🔢 Quantity:</strong> {order.get('quantity', 'N/A')}<br>" if order.get('quantity') else ""}
                    {f"<strong>⚖️ Total Weight:</strong> {order.get('total_weight', 'N/A')}<br>" if order.get('total_weight') else ""}
                    {f"<strong>💰 Total Price:</strong> {order.get('total_price', 'N/A')}<br>" if order.get('total_price') else ""}
                </div>
            </div>
            """
            st.markdown(order_details, unsafe_allow_html=True)
    
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
    """NEW: All Customers Prices Tab"""
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
    
    # NEW: Specific search options
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

def new_orders_tab():
    """NEW: Client Orders Management Tab"""
    st.markdown("""
    <div class="new-orders-header">
        <h2 style="margin:0;">📋 New Client Orders Management</h2>
        <p style="margin:0; opacity:0.9;">Order Preparation • PI Generation • Item Allocation • Availability Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="new_orders_client"
    )
    
    if not client:
        st.warning("Please select a client to manage orders")
        return
    
    # Load new orders data
    with st.spinner(f"📥 Loading orders data for {client}..."):
        orders_data = load_new_orders_data(client)
    
    if orders_data.empty:
        st.info(f"""
        ⚠️ **No new orders data found for {client}**
        
        **To get started:**
        1. Go to your Google Sheet for {client}
        2. Add data to the **'New_client_orders'** sheet
        3. Use these headers:
           - Order_Number, Client_Name, Product_Name, Article_No
           - HS_Code, Origin, Packing, Qty, Type
           - Total_Weight, Price_in_USD_kg, Total_Price, Status
        """)
        return
    
    # Orders Overview
    st.subheader("📊 Orders Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = orders_data['Order_Number'].nunique()
        st.metric("Total PIs", total_orders)
    
    with col2:
        total_items = len(orders_data)
        st.metric("Total Items", total_items)
    
    with col3:
        total_value = orders_data['Total_Price'].sum()
        st.metric("Total Value", f"${total_value:,.2f}")
    
    with col4:
        unique_articles = orders_data['Article_No'].nunique()
        st.metric("Unique Articles", unique_articles)
    
    # Search and Filter Section
    st.subheader("🔍 Search & Filter Orders")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_type = st.radio("Search By:", ["Article Number", "Product Name", "PI Number", "HS Code"], 
                              horizontal=True, key="new_orders_search_type")
    
    with col2:
        search_term = st.text_input("Enter search term...", key="new_orders_search")
    
    with col3:
        status_filter = st.selectbox("Order Status", ["All", "Draft", "Confirmed", "In Production", "Shipped"], 
                                    key="new_orders_status")
    
    # Filter data
    filtered_data = orders_data.copy()
    
    if search_term:
        if search_type == "Article Number":
            filtered_data = filtered_data[filtered_data['Article_No'].astype(str).str.contains(search_term, case=False, na=False)]
        elif search_type == "Product Name":
            filtered_data = filtered_data[filtered_data['Product_Name'].str.contains(search_term, case=False, na=False)]
        elif search_type == "PI Number":
            filtered_data = filtered_data[filtered_data['Order_Number'].str.contains(search_term, case=False, na=False)]
        elif search_type == "HS Code":
            filtered_data = filtered_data[filtered_data['HS_Code'].astype(str).str.contains(search_term, case=False, na=False)]
    
    if status_filter != "All":
        filtered_data = filtered_data[filtered_data['Status'] == status_filter]
    
    # Display Results
    st.subheader(f"📋 Order Items ({len(filtered_data)} found)")
    
    if not filtered_data.empty:
        # Group by Order Number
        for order_num, order_group in filtered_data.groupby('Order_Number'):
            with st.expander(f"📦 PI: {order_num} | Items: {len(order_group)} | Status: {order_group['Status'].iloc[0]}", expanded=False):
                
                # Order summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Items", len(order_group))
                with col2:
                    st.metric("Total Qty", order_group['Qty'].sum())
                with col3:
                    st.metric("Total Weight", f"{order_group['Total_Weight'].sum():.1f} kg")
                with col4:
                    st.metric("Total Value", f"${order_group['Total_Price'].sum():,.2f}")
                
                # Display items in this order
                for _, item in order_group.iterrows():
                    st.markdown(f"""
                    <div class="price-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 2;">
                                <h4 style="margin:0; color: #991B1B;">
                                                                {item['Article_No']} - {item['Product_Name']}</h4>
                                <p style="margin:0; color: #6B7280;">
                                    HS Code: {item['HS_Code']} | Origin: {item['Origin']} | Packing: {item['Packing']}
                                </p>
                            </div>
                            <div style="flex: 1; text-align: right;">
                                <p style="margin:0; font-weight: bold;">Qty: {item['Qty']} {item['Type']}</p>
                                <p style="margin:0;">Weight: {item['Total_Weight']} kg</p>
                                <p style="margin:0; color: #059669;">Price: ${item['Price_in_USD_kg']}/kg</p>
                                <p style="margin:0; font-weight: bold;">Total: ${item['Total_Price']:,.2f}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Export Orders Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{client}_new_orders_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="new_orders_csv"
            )
        
        with col2:
            # Create summary report
            summary_text = f"""
{client} New Orders Report
=========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total PIs: {filtered_data['Order_Number'].nunique()}
Total Items: {len(filtered_data)}
Total Value: ${filtered_data['Total_Price'].sum():,.2f}

Orders Summary:
{chr(10).join([f"• {order_num}: {len(group)} items, ${group['Total_Price'].sum():,.2f} ({group['Status'].iloc[0]})" 
               for order_num, group in filtered_data.groupby('Order_Number')])}

Search Criteria: {search_type} = '{search_term}' | Status: {status_filter}
            """
            st.download_button(
                label="📄 Download Summary",
                data=summary_text,
                file_name=f"{client}_orders_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="new_orders_summary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No orders match your search criteria.")

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

def orders_management_tab():
    """Orders Management Dashboard"""
    st.markdown("""
    <div class="orders-header">
        <h2 style="margin:0;">📋 Orders Management Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Order Tracking • Status Monitoring • Payment Updates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection for orders
    available_clients = st.session_state.user_clients
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="orders_client_select"
    )
    
    if not client:
        st.warning("Please select a client to view orders")
        return
    
    # Load orders data
    orders_data = load_orders_data(client)
    
    if orders_data.empty:
        st.info(f"No orders data found for {client}. Orders management will be available when data is added.")
        return
    
    st.success(f"✅ Showing {len(orders_data)} orders from your data")
    
    # Orders Overview
    st.subheader("📊 Orders Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(orders_data)
        st.metric("Total Orders", total_orders)
    
    with col2:
        shipped_orders = len(orders_data[orders_data['Status'] == 'Shipped'])
        st.metric("Shipped", shipped_orders)
    
    with col3:
        production_orders = len(orders_data[orders_data['Status'] == 'In Production'])
        st.metric("In Production", production_orders)
    
    with col4:
        pending_orders = len(orders_data[orders_data['Status'] == 'Pending'])
        st.metric("Pending", pending_orders)
    
    # Filter section
    st.subheader("🔍 Filter Orders")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Shipped", "In Production", "Pending"],
            key="orders_status_filter"
        )
    
    with col2:
        payment_filter = st.selectbox(
            "Payment Status", 
            ["All", "Pending", "Due", "Paid"],
            key="orders_payment_filter"
        )
    
    with col3:
        search_term = st.text_input("Search Order Number...", key="orders_search")
    
    # Apply filters
    filtered_orders = orders_data.copy()
    
    if status_filter != "All":
        filtered_orders = filtered_orders[filtered_orders['Status'] == status_filter]
    
    if payment_filter != "All":
        filtered_orders = filtered_orders[filtered_orders['Payment Update'] == payment_filter]
    
    if search_term:
        filtered_orders = filtered_orders[
            filtered_orders['Order Number'].str.contains(search_term, case=False, na=False)
        ]
    
    # Display orders
    st.subheader(f"📋 Orders ({len(filtered_orders)} found)")
    
    if not filtered_orders.empty:
        for _, order in filtered_orders.iterrows():
            display_order_card(order)
    else:
        st.info("No orders match your filter criteria.")
    
    # Export section
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.subheader("📤 Export Orders Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_orders.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{client}_orders_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="orders_csv"
        )
    
    with col2:
        st.download_button(
            label="📄 Download Summary",
            data=f"""
{client} Orders Summary
======================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Total Orders: {len(filtered_orders)}
Shipped: {shipped_orders}
In Production: {production_orders}
Pending: {pending_orders}

Orders List:
{chr(10).join([f"• {row['Order Number']} - {row['Status']} - Payment: {row['Payment Update']}" for _, row in filtered_orders.iterrows()])}
            """,
            file_name=f"{client}_orders_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="orders_summary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_order_card(order):
    """Display individual order card using Streamlit components only"""
    
    status = order.get('Status', 'Pending')
    payment_status = order.get('Payment Update', 'Pending')
    order_number = order.get('Order Number', 'N/A')
    
    with st.expander(f"📦 {order_number} - {status}", expanded=False):
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(order_number)
            st.write(f"**Status:** {status}")
            
        with col2:
            if payment_status == 'Paid':
                st.success(f"💳 {payment_status}")
            elif payment_status == 'Due':
                st.error(f"⚠️ {payment_status}")
            else:
                st.warning(f"⏳ {payment_status}")
            
            st.write(f"**ERP:** {order.get('ERP', 'N/A')}")
        
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📋 Order Details**")
            st.write(f"Manufacturer: {order.get('Manufacturer', 'N/A')}")
            st.write(f"ETD: {order.get('ETD', 'N/A')}")
            st.write(f"PI Issue: {order.get('Date of PI issue', 'N/A')}")
            
        with col2:
            st.write("**💰 Financial Details**")
            st.write(f"Payment Due: {order.get('Payment due date', 'N/A')}")
            st.write(f"Invoice: {order.get('Invoice', 'N/A')}")
            st.write(f"Client Signed: {order.get('Date of Client signing', 'N/A')}")
        
        notes = order.get('Notes', '')
        if pd.notna(notes) and notes != '':
            st.write("---")
            st.write("**📝 Notes**")
            st.info(notes)

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

# ============================================
# NEW PRICE MATCHING TAB FUNCTION
# ============================================

def price_matching_tab():
    """New Price Matching Tab for all clients"""
    st.markdown("""
    <div class="price-matching-header">
        <h2 style="margin:0;">🔴 PI Price Validation Tool</h2>
        <p style="margin:0; opacity:0.9;">Client-Specific Price Validation • Historical Price Comparison • Smart Matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Client selection
    available_clients = st.session_state.user_clients
    if not available_clients:
        st.warning("No clients available for your account")
        return
    
    client = st.selectbox(
        "Select Client:",
        available_clients,
        key="price_matching_client"
    )
    
    st.markdown(f"""
    <div class="price-matching-section">
        <h3 style="color: #DC2626; margin-top: 0;">📊 {client} PI Price Validation</h3>
        <p><strong>CRITICAL:</strong> Before sending PI to client, validate ALL prices here!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load client data
    with st.spinner(f"📥 Loading historical data for {client}..."):
        DATA = get_google_sheets_data(client)
    
    if not DATA.get("Backaldrin") and not DATA.get("Bateel"):
        st.error(f"❌ No historical data found for {client}. Please ensure the client has data in Google Sheets.")
        return
    
    st.success(f"✅ Connected to {client} historical data")
    
    # ============================================
    # PRICE VALIDATION TOOL
    # ============================================
    st.subheader("📤 Upload Client PI Draft")
    
    # Supplier selection
    supplier = st.radio(
        "Select Supplier:",
        ["Backaldrin", "Bateel"],
        horizontal=True,
        key="price_matching_supplier"
    )
    
    # Upload options
    upload_method = st.radio(
        "Upload Method:",
        ["Upload File", "Paste Data"],
        horizontal=True,
        key="price_matching_upload_method"
    )
    
    pi_data = None
    
    if upload_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Choose client's PI draft file (Excel/CSV)",
            type=['csv', 'xlsx', 'xls'],
            key="price_matching_upload"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    pi_data = pd.read_csv(uploaded_file)
                else:
                    pi_data = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Loaded {len(pi_data)} items from client PI")
                
                # Show file preview
                with st.expander("📊 Preview Client PI Items", expanded=False):
                    st.dataframe(pi_data.head(10), use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("Please ensure file has columns: Article Number, Product Name, Price, Quantity, etc.")
    
    else:  # Paste Data
        st.info("📝 **Instructions:** Copy data from Excel (include headers) and paste below")
        pasted_data = st.text_area(
            "Paste tabular data from Excel (copy-paste):",
            height=200,
            placeholder="Article\tProduct Name\tPrice\tQuantity\n1-366\tChocolate Chips\t25.50\t100\n1-367\tDate Mix\t30.75\t50",
            key="price_matching_paste_data"
        )
        
        if pasted_data:
            try:
                from io import StringIO
                pi_data = pd.read_csv(StringIO(pasted_data), sep='\t')
                st.success(f"✅ Loaded {len(pi_data)} items from pasted data")
            except:
                try:
                    pi_data = pd.read_csv(StringIO(pasted_data), sep=',')
                    st.success(f"✅ Loaded {len(pi_data)} items from pasted data")
                except Exception as e:
                    st.error("❌ Could not parse pasted data. Use Excel copy-paste format (tab or comma separated).")
    
    # ============================================
    # VALIDATION PROCESS
    # ============================================
    if pi_data is not None and not pi_data.empty:
        # Auto-detect columns
        article_column = None
        price_column = None
        product_column = None
        
        # Try to detect article column
        for col in pi_data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['article', 'art', 'item', 'code', 'sku', 'no', 'num', 'number']):
                article_column = col
                break
        
        # Try to detect price column
        for col in pi_data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['price', 'cost', 'rate', 'usd', '$', 'amount', 'value']):
                price_column = col
                break
        
        # Try to detect product name column
        for col in pi_data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['product', 'name', 'description', 'item', 'product_name']):
                product_column = col
                break
        
        if not article_column:
            st.error("❌ Could not detect article number column. Please ensure your data has an 'Article' or similar column.")
            return
        
        if not price_column:
            st.error("❌ Could not detect price column. Please ensure your data has a 'Price' or similar column.")
            return
        
        if not product_column:
            product_column = "Product"
            pi_data[product_column] = "N/A"
        
        st.info(f"📋 **Detected columns:** Article: '{article_column}', Price: '{price_column}', Product: '{product_column}'")
        
        # Validate button
        if st.button("🔍 VALIDATE ALL PRICES (Check vs Latest 2 Historical)", 
                    type="primary", 
                    use_container_width=True,
                    key="validate_all_prices"):
            
            with st.spinner(f"🔄 Validating {len(pi_data)} items..."):
                validation_results = []
                items_not_found = []
                
                progress_bar = st.progress(0)
                
                for idx, row in pi_data.iterrows():
                    article = str(row[article_column]).strip()
                    product_name = str(row[product_column]).strip() if product_column in row else "N/A"
                    
                    # Try to extract client price
                    client_price = None
                    if price_column in row and pd.notna(row[price_column]):
                        try:
                            # Remove any currency symbols and convert to float
                            price_str = str(row[price_column]).replace('$', '').replace(',', '').strip()
                            client_price = float(price_str)
                        except:
                            client_price = None
                    
                    # Search in historical data
                    historical_prices = []
                    
                    supplier_data = DATA.get(supplier, {})
                    
                    if article in supplier_data:
                        article_data = supplier_data[article]
                        
                        # Get orders sorted by date (newest first)
                        orders = article_data.get('orders', [])
                        
                        # Sort by date if available, otherwise use as is
                        try:
                            # Try to parse dates
                            for order in orders:
                                try:
                                    if order.get('date'):
                                        order['parsed_date'] = pd.to_datetime(order['date'], errors='coerce')
                                except:
                                    order['parsed_date'] = pd.NaT
                            
                            # Sort by date (newest first)
                            orders.sort(key=lambda x: x.get('parsed_date', pd.NaT), reverse=True)
                        except:
                            # If date parsing fails, keep original order
                            pass
                        
                        # Take latest 2 orders with prices
                        valid_orders = []
                        for order in orders[:10]:  # Check up to 10 latest
                            try:
                                price_str = order.get('price', '')
                                if price_str:
                                    # Clean price string
                                    price_str_clean = str(price_str).replace('$', '').replace(',', '').strip()
                                    price_val = float(price_str_clean)
                                    valid_orders.append({
                                        'order_no': order.get('order_no', 'N/A'),
                                        'date': order.get('date', 'N/A'),
                                        'price': price_val,
                                        'year': order.get('year', ''),
                                        'product_name': order.get('product_name', 'N/A'),
                                        'hs_code': order.get('hs_code', ''),
                                        'packaging': order.get('packaging', '')
                                    })
                            except:
                                continue
                        
                        # Take latest 2
                        historical_prices = valid_orders[:2]
                    
                    # Prepare result
                    result = {
                        'Article': article,
                        'Product_Name': product_name,
                        'Client_Price': f"${client_price:.2f}" if client_price else "N/A",
                        'Client_Price_Value': client_price,
                        'Status': '',
                        'Decision': '❓ Pending',
                        'Selected_Price': None,
                        'Selected_Order': None,
                        'Selected_Date': None,
                        'Selected_Product_Name': None,
                        'Price_Difference': None,
                        'Price_Difference_Percent': None,
                        'Notes': ''
                    }
                    
                    if historical_prices:
                        # Compare with historical prices
                        if client_price is not None:
                            latest_price = historical_prices[0]['price']
                            price_diff = client_price - latest_price
                            price_diff_percent = (price_diff / latest_price * 100) if latest_price != 0 else 0
                            
                            result['Price_Difference'] = price_diff
                            result['Price_Difference_Percent'] = price_diff_percent
                            
                            if abs(price_diff) < 0.01:  # Less than 1 cent difference
                                result['Status'] = f"✅ MATCH: ${latest_price:.2f}"
                                result['Decision'] = '✅ Use Client Price'
                                result['Selected_Price'] = client_price
                                result['Selected_Order'] = historical_prices[0]['order_no']
                                result['Selected_Date'] = historical_prices[0]['date']
                                result['Selected_Product_Name'] = historical_prices[0]['product_name']
                            elif price_diff > 0:
                                result['Status'] = f"⚠️ HIGHER: +${price_diff:.2f} (+{price_diff_percent:.1f}%)"
                            else:
                                result['Status'] = f"⚠️ LOWER: -${abs(price_diff):.2f} ({price_diff_percent:.1f}%)"
                        else:
                            result['Status'] = "ℹ️ No client price provided"
                        
                        # Add historical price details
                        for i, hist in enumerate(historical_prices, 1):
                            result[f'Hist_Price_{i}'] = f"${hist['price']:.2f}"
                            result[f'Hist_Order_{i}'] = hist['order_no']
                            result[f'Hist_Date_{i}'] = hist['date']
                            result[f'Hist_Product_{i}'] = hist['product_name']
                            result[f'Hist_HS_Code_{i}'] = hist['hs_code']
                            result[f'Hist_Packaging_{i}'] = hist['packaging']
                            
                            if i == 1:  # Latest price
                                result['Latest_Price'] = f"${hist['price']:.2f}"
                                result['Latest_Order'] = hist['order_no']
                                result['Latest_Date'] = hist['date']
                                result['Latest_Product'] = hist['product_name']
                        
                        # Add notes about historical data
                        if len(historical_prices) == 1:
                            result['Notes'] = f"Only 1 historical record found from {historical_prices[0]['date']}"
                        elif len(historical_prices) == 2:
                            result['Notes'] = f"2 historical records found ({historical_prices[0]['date']}, {historical_prices[1]['date']})"
                        else:
                            result['Notes'] = f"{len(historical_prices)} historical records found"
                    
                    else:
                        result['Status'] = "❌ NO HISTORY: Never ordered before"
                        result['Notes'] = "No historical pricing data found for this article"
                        items_not_found.append(article)
                    
                    validation_results.append(result)
                    progress_bar.progress((idx + 1) / len(pi_data))
                
                # Store results in session state
                st.session_state.price_matching_results = {
                    'client': client,
                    'supplier': supplier,
                    'results': validation_results,
                    'items_not_found': items_not_found,
                    'total_items': len(pi_data)
                }
                
                # ============================================
                # DISPLAY VALIDATION RESULTS
                # ============================================
                st.subheader("📊 VALIDATION RESULTS SUMMARY")
                
                # Quick Stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_items = len(validation_results)
                    st.metric("Total Items", total_items)
                
                with col2:
                    matches = len([r for r in validation_results if '✅' in r['Status']])
                    st.metric("✅ Matches", matches)
                
                with col3:
                    mismatches = len([r for r in validation_results if '⚠️' in r['Status']])
                    st.metric("⚠️ Mismatches", mismatches)
                
                with col4:
                    no_history = len([r for r in validation_results if '❌' in r['Status']])
                    st.metric("❌ No History", no_history)
                
                # ============================================
                # INTERACTIVE VALIDATION TABLE
                # ============================================
                st.subheader("🎯 MAKE PRICE DECISIONS")
                st.info("Review each item and make a final decision on which price to use")
                
                # Store decisions in session state if not already
                if 'price_decisions' not in st.session_state:
                    st.session_state.price_decisions = {}
                
                for i, result in enumerate(validation_results):
                    # Create unique key for this item
                    item_key = f"{client}_{supplier}_{result['Article']}_{i}"
                    
                    # Initialize decision if not exists
                    if item_key not in st.session_state.price_decisions:
                        st.session_state.price_decisions[item_key] = result['Decision']
                    
                    # Display each item in an expander
                    with st.expander(f"{result['Article']} - {result['Product_Name']} | {result['Status']}", expanded=True):
                        
                        # Badge for status
                        if '✅' in result['Status']:
                            st.markdown('<span class="match-badge">Match Found</span>', unsafe_allow_html=True)
                        elif '⚠️' in result['Status']:
                            st.markdown('<span class="mismatch-badge">Price Mismatch</span>', unsafe_allow_html=True)
                        elif '❌' in result['Status']:
                            st.markdown('<span class="no-history-badge">No History</span>', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.write("**📋 Client PI Details**")
                            st.write(f"**Article:** {result['Article']}")
                            st.write(f"**Product:** {result['Product_Name']}")
                            st.write(f"**Client Price:** {result['Client_Price']}")
                            
                            if result.get('Price_Difference') is not None:
                                diff_color = "red" if result['Price_Difference'] > 0 else "green"
                                diff_symbol = "+" if result['Price_Difference'] > 0 else ""
                                st.write(f"**Price Difference:** <span style='color:{diff_color}'>{diff_symbol}${abs(result['Price_Difference']):.2f} ({result['Price_Difference_Percent']:.1f}%)</span>", unsafe_allow_html=True)
                        
                        with col2:
                            if 'Latest_Price' in result:
                                st.write("**📊 Historical Data**")
                                st.write(f"**Latest Price:** {result['Latest_Price']}")
                                st.write(f"**Latest Order:** {result['Latest_Order']}")
                                st.write(f"**Latest Date:** {result['Latest_Date']}")
                                st.write(f"**Latest Product:** {result['Latest_Product']}")
                            
                            if 'Hist_Price_1' in result:
                                st.write("**📈 All Historical Prices:**")
                                for hist_num in [1, 2]:
                                    if f'Hist_Price_{hist_num}' in result:
                                        st.write(f"{hist_num}. **{result[f'Hist_Price_{hist_num}']}**")
                                        st.caption(f"Order: {result[f'Hist_Order_{hist_num}']}")
                                        st.caption(f"Date: {result[f'Hist_Date_{hist_num}']}")
                                        if result[f'Hist_HS_Code_{hist_num}']:
                                            st.caption(f"HS Code: {result[f'Hist_HS_Code_{hist_num}']}")
                        
                        # Decision Section
                        st.markdown("---")
                        st.write("**🤔 FINAL DECISION**")
                        
                        # Create decision options
                        decision_options = [
                            "❓ Pending",
                            "✅ Use Client Price",
                            "✅ Use Latest Historical",
                            "✅ Use Historical #2",
                            "✏️ Set Custom Price",
                            "❌ Flag for Review",
                            "⏸️ Skip for Now"
                        ]
                        
                        # Create columns for decision
                        dec_col1, dec_col2 = st.columns([2, 1])
                        
                        with dec_col1:
                            selected_decision = st.selectbox(
                                "Select your decision:",
                                decision_options,
                                index=decision_options.index(st.session_state.price_decisions.get(item_key, "❓ Pending")),
                                key=f"decision_select_{item_key}"
                            )
                            
                            # Update session state
                            st.session_state.price_decisions[item_key] = selected_decision
                            
                            # If custom price selected
                            if selected_decision == "✏️ Set Custom Price":
                                custom_price = st.number_input(
                                    "Enter custom price ($/kg):",
                                    min_value=0.0,
                                    value=float(result['Client_Price'].replace('$', '')) if result['Client_Price'] != 'N/A' else 0.0,
                                    step=0.01,
                                    key=f"custom_price_{item_key}"
                                )
                                # Store custom price
                                validation_results[i]['Selected_Price'] = custom_price
                                validation_results[i]['Selected_Order'] = "Custom"
                                validation_results[i]['Selected_Date'] = datetime.now().strftime("%Y-%m-%d")
                                validation_results[i]['Selected_Product_Name'] = result['Product_Name']
                            
                            elif selected_decision == "✅ Use Client Price" and result['Client_Price_Value']:
                                validation_results[i]['Selected_Price'] = result['Client_Price_Value']
                                validation_results[i]['Selected_Order'] = "Client PI"
                                validation_results[i]['Selected_Date'] = datetime.now().strftime("%Y-%m-%d")
                                validation_results[i]['Selected_Product_Name'] = result['Product_Name']
                            
                            elif selected_decision == "✅ Use Latest Historical" and 'Hist_Price_1' in result:
                                hist_price = float(result['Hist_Price_1'].replace('$', ''))
                                validation_results[i]['Selected_Price'] = hist_price
                                validation_results[i]['Selected_Order'] = result['Hist_Order_1']
                                validation_results[i]['Selected_Date'] = result['Hist_Date_1']
                                validation_results[i]['Selected_Product_Name'] = result['Hist_Product_1']
                            
                            elif selected_decision == "✅ Use Historical #2" and 'Hist_Price_2' in result:
                                hist_price = float(result['Hist_Price_2'].replace('$', ''))
                                validation_results[i]['Selected_Price'] = hist_price
                                validation_results[i]['Selected_Order'] = result['Hist_Order_2']
                                validation_results[i]['Selected_Date'] = result['Hist_Date_2']
                                validation_results[i]['Selected_Product_Name'] = result['Hist_Product_2']
                        
                        with dec_col2:
                            if validation_results[i]['Selected_Price']:
                                st.success(f"**Selected Price:**")
                                st.markdown(f"# **${validation_results[i]['Selected_Price']:.2f}**")
                                st.caption(f"Reference: {validation_results[i]['Selected_Order']}")
                                st.caption(f"Date: {validation_results[i]['Selected_Date']}")
                
                # ============================================
                # FINAL PI GENERATION
                # ============================================
                st.subheader("📄 GENERATE VALIDATED PI")
                
                # Create final PI DataFrame
                final_pi_data = []
                for result in validation_results:
                    final_item = {
                        'Article': result['Article'],
                        'Product_Name': result['Product_Name'],
                        'Original_Client_Price': result['Client_Price'],
                        'Validation_Status': result['Status'],
                        'Final_Decision': st.session_state.price_decisions.get(f"{client}_{supplier}_{result['Article']}_{validation_results.index(result)}", "❓ Pending"),
                        'Final_Price': f"${result.get('Selected_Price', ''):.2f}" if result.get('Selected_Price') else '',
                        'Reference_Order': result.get('Selected_Order', ''),
                        'Reference_Date': result.get('Selected_Date', ''),
                        'Price_Difference': f"${result.get('Price_Difference', ''):.2f}" if result.get('Price_Difference') is not None else '',
                        'Price_Difference_Percent': f"{result.get('Price_Difference_Percent', ''):.1f}%" if result.get('Price_Difference_Percent') is not None else '',
                        'Notes': result.get('Notes', '')
                    }
                    final_pi_data.append(final_item)
                
                final_pi_df = pd.DataFrame(final_pi_data)
                
                # Export Section
                st.markdown('<div class="export-section">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Download Validation Report (CSV)
                    csv = final_pi_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Validation Report (CSV)",
                        data=csv,
                        file_name=f"{client}_PI_Validation_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="validation_csv"
                    )
                
                with col2:
                    # Generate Excel Report
                    try:
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            final_pi_df.to_excel(writer, index=False, sheet_name='Validated_PI')
                        excel_data = output.getvalue()
                        
                        st.download_button(
                            label="📊 Download Excel Report",
                            data=excel_data,
                            file_name=f"{client}_PI_Validation_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                            mime="application/vnd.ms-excel",
                            use_container_width=True,
                            key="validation_excel"
                        )
                    except:
                        st.info("📊 Excel export requires openpyxl package")
                
                with col3:
                    # Generate PI Summary
                    summary_text = f"""
{client} PI PRICE VALIDATION REPORT
====================================

Client: {client}
Supplier: {supplier}
Validated By: {st.session_state.username}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SUMMARY:
• Total Items: {total_items}
• ✅ Matched Prices: {matches}
• ⚠️ Price Mismatches: {mismatches}
• ❌ No History: {no_history}

ITEMS REQUIRING ATTENTION ({mismatches + no_history}):
{chr(10).join([f"• {r['Article']} - {r['Status']}" for r in validation_results if '⚠️' in r['Status'] or '❌' in r['Status']])}

VALIDATED PRICES:
{chr(10).join([f"• {r['Article']}: ${r.get('Selected_Price', 'N/A')} ({st.session_state.price_decisions.get(f'{client}_{supplier}_{r['Article']}_{validation_results.index(r)}', 'Pending')})" for r in validation_results if r.get('Selected_Price')])}

GENERAL NOTES:
1. This validation compares client PI prices with the latest 2 historical prices
2. Green check (✅) indicates price matches historical data within $0.01
3. Warning (⚠️) indicates price differs from historical by more than $0.01
4. Red cross (❌) indicates no historical pricing data found
                    """
                    
                    st.download_button(
                        label="📋 Download Summary Report",
                        data=summary_text,
                        file_name=f"{client}_PI_Validation_Summary_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key="validation_summary"
                    )
                
                # Items not found warning
                if items_not_found:
                    st.warning(f"⚠️ **{len(items_not_found)} items not found in historical data**")
                    with st.expander("View items with no history"):
                        st.write(", ".join(items_not_found[:20]))
                        if len(items_not_found) > 20:
                            st.write(f"... and {len(items_not_found) - 20} more")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Quick Actions
                st.subheader("⚡ Quick Actions")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Validate Another PI", use_container_width=True):
                        # Clear previous results
                        if 'price_matching_results' in st.session_state:
                            del st.session_state.price_matching_results
                        if 'price_decisions' in st.session_state:
                            del st.session_state.price_decisions
                        st.rerun()
                
                with col2:
                    if st.button("📊 View Raw Results", use_container_width=True):
                        with st.expander("Raw Validation Results", expanded=True):
                            st.dataframe(final_pi_df, use_container_width=True)

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    if not check_login():
        login_page()
    else:
        main_dashboard()
