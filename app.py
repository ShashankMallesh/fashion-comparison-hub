import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import time
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fashion Comparison Hub",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #6a11cb;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #2575fc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .dupe-yes {
        background-color: rgba(220, 53, 69, 0.1);
        color: #dc3545;
        padding: 8px 15px;
        border-radius: 50px;
        font-weight: 600;
    }
    .dupe-no {
        background-color: rgba(40, 167, 69, 0.1);
        color: #28a745;
        padding: 8px 15px;
        border-radius: 50px;
        font-weight: 600;
    }
    .best-price {
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        position: relative;
    }
    .best-price-tag {
        position: absolute;
        top: -10px;
        right: 10px;
        background-color: #28a745;
        color: white;
        padding: 3px 10px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .website-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Fashion Comparison Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered price comparison and dupe detection across multiple websites!</p>', unsafe_allow_html=True)

# Mode selection
col1, col2 = st.columns(2)
with col1:
    price_comparison = st.button("💰 Price Comparison", use_container_width=True)
with col2:
    dups_detection = st.button("🔍 Dups Detection", use_container_width=True)

# Default mode
current_mode = "Price Comparison"

if dups_detection:
    current_mode = "Dups Detection"

st.write(f"**Current Mode:** {current_mode}")

# File upload section
st.subheader("Upload Product Image")
uploaded_file = st.file_uploader(
    "Upload an image of a fashion item to check for duplicates and compare prices",
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG"
)

# Initialize session state for results
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'is_dupe' not in st.session_state:
    st.session_state.is_dupe = False

# Process uploaded image
if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Analyze button
        if st.button("🔍 Analyze Image", use_container_width=True):
            with st.spinner("Analyzing your image and searching for matches..."):
                # Simulate API processing time
                time.sleep(3)
                
                # Simulate dupe detection (random for demo)
                st.session_state.is_dupe = np.random.choice([True, False], p=[0.6, 0.4])
                st.session_state.analysis_complete = True
                
                st.success("Analysis complete!")
                
                # Rerun to show results
                st.rerun()

# Show results if analysis is complete
if st.session_state.analysis_complete and st.session_state.uploaded_image is not None:
    st.subheader("Analysis Results")
    
    # Dupe detection result
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Product Identified:** Women's Floral Summer Dress")
        st.write(f"**Similarity Confidence:** {np.random.randint(85, 98)}%")
    with col2:
        if st.session_state.is_dupe:
            st.markdown('<div class="dupe-yes">Potential Duplicate Detected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="dupe-no">Original Product</div>', unsafe_allow_html=True)
    
    # Price comparison section
    st.subheader("💰 Price Comparison Across Websites")
    
    # Sample price data
    websites = [
        {"name": "FashionOutlet", "price": 49.99, "rating": 4.2, "is_best": True},
        {"name": "StyleHub", "price": 54.99, "rating": 4.0, "is_best": False},
        {"name": "DressCode", "price": 59.99, "rating": 4.7, "is_best": False},
        {"name": "TrendyBoutique", "price": 62.50, "rating": 3.8, "is_best": False},
        {"name": "ChicBazaar", "price": 52.99, "rating": 4.3, "is_best": False},
    ]
    
    # Display price comparison
    cols = st.columns(len(websites))
    
    for idx, (col, website) in enumerate(zip(cols, websites)):
        with col:
            if website["is_best"]:
                st.markdown('<div class="best-price">', unsafe_allow_html=True)
                st.markdown('<div class="best-price-tag">Best Price</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="website-card">', unsafe_allow_html=True)
            
            st.write(f"**{website['name']}**")
            st.write(f"**${website['price']}**")
            st.write(f"⭐ {website['rating']}/5")
            
            if st.button(f"View on {website['name']}", key=f"btn_{idx}", use_container_width=True):
                st.info(f"Redirecting to {website['name']}...")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional features
    st.subheader("📊 Price History")
    
    # Sample price history data
    dates = pd.date_range(start='2024-01-01', end='2024-11-16', freq='M')
    prices = [65, 62, 58, 55, 52, 50, 53, 55, 52, 49, 50]
    
    price_history_df = pd.DataFrame({
        'Date': dates,
        'Price ($)': prices
    })
    
    st.line_chart(price_history_df.set_index('Date')['Price ($)'])
    
    # Similar products
    st.subheader("🛍️ Similar Products")
    
    similar_products = [
        {"name": "Blue Floral Dress", "price": 47.99, "similarity": 89},
        {"name": "Summer Maxi Dress", "price": 55.99, "similarity": 78},
        {"name": "Floral Print Midi", "price": 51.50, "similarity": 85},
    ]
    
    for product in similar_products:
        with st.expander(f"{product['name']} - ${product['price']} ({product['similarity']}% similar)"):
            st.write(f"**Price:** ${product['price']}")
            st.write(f"**Similarity Score:** {product['similarity']}%")
            if st.button("Compare", key=f"compare_{product['name']}"):
                st.info(f"Comparing with {product['name']}...")

# Footer
st.markdown("---")
st.markdown("**Fashion Comparison Hub** - AI-powered price intelligence and authenticity verification")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
