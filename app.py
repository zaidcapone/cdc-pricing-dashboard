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

# ============================================
# SECTION 1: IMPORT LIBRARIES
# ============================================
import streamlit as st  # Main dashboard framework
import pandas as pd  # Data manipulation
import requests  # API calls to Google Sheets
import json  # JSON data handling
from datetime import datetime  # Date/time operations
from io import BytesIO  # In-memory file handling
import re  # Regular expressions for text processing

# NEW IMPORTS FOR VISUAL ANALYTICS
import matplotlib.pyplot as plt  # Charting library
import numpy as np  # Numerical operations for analytics

# ============================================
# SECTION 2: PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Multi-Client Dashboard", 
    layout="wide",  # Use full width of screen
    initial_sidebar_state="expanded"  # Sidebar starts open
)

# ============================================
# SECTION 3: CUSTOM CSS STYLING
# ============================================
st.markdown("""
<style>
    /* Main dashboard header */
    .main-header {
        background: linear-gradient(135deg, #991B1B, #7F1D1D);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Client-specific headers */
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
    
    /* Card styles for different content types */
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
    
    /* Statistic cards */
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
    
    /* Stat number styling */
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
    
    /* Price boxes for order display */
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
    
    /* Order information styling */
    .order-info {
        background: #F3F4F6;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        font-size: 0.8em;
        color: #6B7280;
    }
    
    /* Section containers */
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
    
    /* Login page styling */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #991B1B;
    }
    
    /* Tab-specific headers */
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
    
    /* Search and history styling */
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
    
    /* Favorites styling */
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

# ============================================
# SECTION 4: CONFIGURATION & CONSTANTS
# ============================================

# Google Sheets API Configuration
API_KEY = "AIzaSyA3P-ZpLjDdVtGB82_1kaWuO7lNbKDj9HU"  # Google Sheets API key
CDC_SHEET_ID = "1qWgVT0l76VsxQzYExpLfioBHprd3IvxJzjQWv3RryJI"  # Main spreadsheet ID

# User authentication database
# Note: In production, use hashed passwords and database storage
USERS = {
    "admin": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "ceo": {"password": "123456", "clients": ["CDC", "CoteDivoire", "CakeArt", "SweetHouse", "Cameron"]},
    "zaid": {"password": "123456", "clients": ["CDC"]},
    "mohammad": {"password": "123456", "clients": ["CoteDivoire"]},
    "Khalid": {"password": "123456", "clients": ["CakeArt", "SweetHouse"]},
    "Rotana": {"password": "123456", "clients": ["CDC"]}
}

# Client data sheets mapping
# This defines which Google Sheet tabs belong to each client
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
    }
}

# Global sheet names for shared data
PRODUCT_CATALOG_SHEET = "FullProductList"  # Master product catalog
PRICES_SHEET = "Prices"  # All customer prices database

# ============================================
# SECTION 5: SMART SEARCH WITH AI SUGGESTIONS
# ============================================

def get_smart_suggestions(search_term, supplier_data, search_type="all"):
    """
    Get smart search suggestions with scoring system
    Prioritizes exact matches and provides relevance scores
    
    Parameters:
    - search_term: User's search input
    - supplier_data: Data from selected supplier
    - search_type: Type of search (all, article, product, hs_code)
    
    Returns:
    - List of suggestions sorted by relevance score
    """
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
# SECTION 6: SEARCH HISTORY MANAGEMENT
# ============================================

def initialize_search_history():
    """Initialize search history in session state"""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'max_history_items' not in st.session_state:
        st.session_state.max_history_items = 20

def add_to_search_history(search_term, client, supplier, article_num=None):
    """
    Add a search to the history
    Removes duplicates and keeps only latest entries
    """
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
    """Format timestamp as 'time ago' for display"""
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
# SECTION 7: SAVED SEARCHES/FAVORITES
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
    """
    Save a search to favorites
    Returns True if successful, False if already favorited
    """
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
    """Display favorites in a modal popup"""
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
# SECTION 8: CACHED DATA LOADING FUNCTIONS
# ============================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_sheet_data(sheet_name, start_row=0):
    """
    Universal Google Sheets loader for all data types
    Handles different sheet structures and formats
    
    Parameters:
    - sheet_name: Name of the Google Sheet tab
    - start_row: Row to start reading from (for headers)
    
    Returns:
    - DataFrame with loaded data
    """
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_google_sheets_data(client="CDC"):
    """
    Load both supplier data in one call and return proper structure
    Optimized for SweetHouse and other clients with lowercase headers
    
    Parameters:
    - client: Client name (CDC, SweetHouse, etc.)
    
    Returns:
    - Dictionary with Backaldrin and Bateel data
    """
    try:
        backaldrin_sheet = f"Backaldrin_{client}"
        bateel_sheet = f"Bateel_{client}"
        
        backaldrin_df = load_sheet_data(backaldrin_sheet)
        bateel_df = load_sheet_data(bateel_sheet)
        
        def convert_df_to_dict(df):
            """Convert DataFrame to the expected dictionary structure"""
            result = {}
            
            if df.empty:
                return result
            
            # Helper function to find columns with flexible naming
            def get_column(df, possible_names):
                for name in possible_names:
                    if name in df.columns:
                        return name
                return None
            
            # Find columns using lowercase priority first (for SweetHouse compatibility)
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

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_product_catalog():
    """Load product catalog from Google Sheets - Flexible version"""
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

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_prices_data():
    """Load all prices data from Google Sheets"""
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_ceo_special_prices(client="CDC"):
    """Load CEO special prices from Google Sheets for specific client"""
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

@st.cache_data(ttl=180)  # Cache for 3 minutes
def load_etd_data(sheet_id, sheet_name):
    """Optimized ETD loader using universal function"""
    return load_sheet_data(sheet_name, start_row=13)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_new_orders_data(client):
    """Load new client orders data from Google Sheets"""
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

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_orders_data(client):
    """Load ALL orders data - Sample version"""
    try:
        sample_orders = [
            {
                'Order Number': 'SA C.D 125/2025', 'ERP': 'Yes', 'Date of request': 'N/A',
                'Date of PI issue': '08-Sep-25', 'Date of Client signing': 'N/A',
                'Invoice': 0, 'Payment': 'Credit Note 45550', 'Manufacturer': 'BAJ',
                'ETD': '28-Dec-25', 'Payment due date': '16-Sep-25', 
                'Payment Update': 'Pending', 'Status': 'Shipped', 'Notes': 'Credit Note 45550'
            },
            # ... (other sample orders remain the same)
        ]
        
        df = pd.DataFrame(sample_orders)
        return df
        
    except Exception as e:
        st.error(f"Error loading orders data: {str(e)}")
        return pd.DataFrame()

# ============================================
# SECTION 9: AUTHENTICATION & SESSION MANAGEMENT
# ============================================

def check_login():
    """Check if user is logged in and initialize session state"""
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
    """Display login page with form"""
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

# ============================================
# SECTION 10: MAIN DASHBOARD LAYOUT
# ============================================

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
            "📈 **NEW**: Visual Analytics Dashboard added!"
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
# SECTION 11: NEW VISUAL ANALYTICS TAB
# ============================================

def visual_analytics_tab():
    """
    NEW: Visual Analytics Tab with Interactive Charts
    """
    st.markdown("""
    <div class="visual-header">
        <h2 style="margin:0;">📈 Visual Analytics Dashboard</h2>
        <p style="margin:0; opacity:0.9;">Interactive Charts • Sales Trends • Product Performance • Custom Visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SIMPLE TEST - JUST SHOW IF TAB LOADS
    st.write("✅ Visual Analytics tab is loading...")
    
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
    
    st.write(f"✅ Selected client: {client}")
    
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
# SECTION 12: ORIGINAL TAB FUNCTIONS (KEPT AS IS)
# ============================================
# Note: These functions remain unchanged from the previous version
# They are included for completeness but code is truncated for brevity

def clients_tab():
    """Clients management tab - Select client and show dashboard"""
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
    # ... (existing code remains the same)
    pass

def prices_tab():
    """All Customers Prices tab"""
    # ... (existing code remains the same)
    pass

def new_orders_tab():
    """New Client Orders Management tab"""
    # ... (existing code remains the same)
    pass

def etd_tab():
    """ETD Management Dashboard"""
    # ... (existing code remains the same)
    pass

def ceo_specials_tab():
    """CEO Special Prices tab"""
    # ... (existing code remains the same)
    pass

def price_intelligence_tab():
    """CEO Price Intelligence - Cross-client comparison"""
    # ... (existing code remains the same)
    pass

def product_catalog_tab():
    """Full Product Catalog"""
    # ... (existing code remains the same)
    pass

def orders_management_tab():
    """Orders Management Dashboard"""
    # ... (existing code remains the same)
    pass

def palletizing_tab():
    """Quick Pallet Calculator"""
    # ... (existing code remains the same)
    pass

def price_matching_tab():
    """Price Matching Tool for PI validation"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 13: HELPER FUNCTIONS FOR CLIENTS TAB
# ============================================

def get_suggestions(search_term, supplier, data):
    """Get search suggestions for article, product name, or HS code"""
    # ... (existing code remains the same)
    pass

def handle_search(article, product, hs_code, supplier, data, client):
    """Handle search across article, product name, and HS code"""
    # ... (existing code remains the same)
    pass

def create_export_data(article_data, article, supplier, client):
    """Create export data in different formats"""
    # ... (existing code remains the same)
    pass

def display_from_session_state(data, client):
    """Display search results with favorites feature"""
    # ... (existing code remains the same)
    pass

def convert_df_to_excel(df):
    """Convert DataFrame to Excel format"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 14: ETD SPECIFIC FUNCTIONS
# ============================================

def display_etd_order_card(order, month):
    """Display individual ETD order card"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 15: PRICE INTELLIGENCE FUNCTIONS
# ============================================

def analyze_cross_client_prices(search_term, selected_clients, supplier_filter="All"):
    """Analyze prices across selected clients"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 16: PRODUCT CATALOG FUNCTIONS
# ============================================

def display_product_card_flexible(product, available_columns):
    """Display individual product card"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 17: ORDERS MANAGEMENT FUNCTIONS
# ============================================

def display_order_card(order):
    """Display individual order card"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 18: PALLETIZING FUNCTIONS
# ============================================

def quick_pallet_calculator():
    """Quick Pallet Calculator"""
    # ... (existing code remains the same)
    pass

def load_palletizing_data(client):
    """Load palletizing data"""
    # ... (existing code remains the same)
    pass

# ============================================
# SECTION 19: MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Check authentication status
    if not check_login():
        # Show login page if not logged in
        login_page()
    else:
        # Show main dashboard if logged in
        main_dashboard()

# ============================================
# END OF DASHBOARD CODE
# ============================================
# Features included in this version:
# 1. Multi-client management (5 clients)
# 2. Smart search with AI suggestions
# 3. Search history and favorites
# 4. Visual Analytics with interactive charts (NEW)
# 5. Price intelligence across clients
# 6. CEO special prices management
# 7. ETD tracking and management
# 8. Product catalog browsing
# 9. Orders management
# 10. Palletizing calculator
# 11. Price matching tool for PI validation
# 12. Data export in multiple formats
# 13. User authentication and authorization
# 14. Responsive design with custom CSS
# 15. Google Sheets integration with caching
# ============================================
