import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
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
        margin: 5px;
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
        margin: 5px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Product database for different categories
PRODUCT_DATABASE = {
    "shoes": {
        "nike": {
            "name": "Nike Air Max 270",
            "category": "Sneakers",
            "brand": "Nike",
            "description": "Men's Running Shoes",
            "prices": [
                {"retailer": "Nike Official", "price": 150.00, "rating": 4.5},
                {"retailer": "Amazon", "price": 139.99, "rating": 4.3},
                {"retailer": "Foot Locker", "price": 149.99, "rating": 4.4},
                {"retailer": "JD Sports", "price": 144.50, "rating": 4.2},
                {"retailer": "Finish Line", "price": 147.99, "rating": 4.1}
            ],
            "similar_products": [
                {"name": "Nike Air Force 1", "price": 100.00, "similarity": 85},
                {"name": "Adidas Ultraboost", "price": 180.00, "similarity": 78},
                {"name": "Nike Revolution 6", "price": 65.00, "similarity": 72}
            ]
        },
        "adidas": {
            "name": "Adidas Ultraboost 22",
            "category": "Running Shoes", 
            "brand": "Adidas",
            "description": "Men's Premium Running Shoes",
            "prices": [
                {"retailer": "Adidas Official", "price": 190.00, "rating": 4.7},
                {"retailer": "Amazon", "price": 179.99, "rating": 4.5},
                {"retailer": "Foot Locker", "price": 185.00, "rating": 4.6},
                {"retailer": "Dick's Sporting Goods", "price": 189.99, "rating": 4.4}
            ],
            "similar_products": [
                {"name": "Adidas NMD_R1", "price": 130.00, "similarity": 82},
                {"name": "Nike Pegasus 39", "price": 120.00, "similarity": 75},
                {"name": "New Balance Fresh Foam", "price": 110.00, "similarity": 70}
            ]
        }
    },
    "dresses": {
        "floral_dress": {
            "name": "Women's Floral Summer Dress",
            "category": "Dresses",
            "brand": "ZARA",
            "description": "Floral Print Midi Dress",
            "prices": [
                {"retailer": "ZARA", "price": 49.99, "rating": 4.2},
                {"retailer": "ASOS", "price": 54.99, "rating": 4.0},
                {"retailer": "H&M", "price": 39.99, "rating": 3.8},
                {"retailer": "Mango", "price": 59.99, "rating": 4.1}
            ],
            "similar_products": [
                {"name": "Blue Floral Dress", "price": 47.99, "similarity": 89},
                {"name": "Summer Maxi Dress", "price": 55.99, "similarity": 78},
                {"name": "Floral Print Midi", "price": 51.50, "similarity": 85}
            ]
        }
    }
}

def detect_product_type(image):
    """
    Simulate AI product detection based on image analysis
    In a real app, this would use computer vision models
    """
    # For demo purposes, we'll use a simple detection based on image characteristics
    # In reality, you would use a trained model here
    
    # Get image size to make a "guess" about the product type
    width, height = image.size
    aspect_ratio = width / height
    
    # Simple heuristic (this is just for demo)
    if aspect_ratio > 1.2:  # Wider images might be shoes
        return "shoes", "nike"
    else:  # More square/tall images might be clothing
        return "dresses", "floral_dress"

def analyze_for_duplicates(product_type, product_id):
    """
    Simulate duplicate detection analysis
    """
    # In a real app, this would compare against a database of known products
    # For demo, we'll return random but realistic results
    
    import random
    confidence = random.randint(75, 95)
    is_duplicate = confidence > 80  # If confidence > 80%, mark as potential duplicate
    
    return is_duplicate, confidence

# Header
st.markdown('<h1 class="main-header">Fashion Comparison Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered price comparison and duplicate detection across multiple websites!</p>', unsafe_allow_html=True)

# Mode selection
col1, col2 = st.columns(2)
with col1:
    price_comparison = st.button("💰 Price Comparison", use_container_width=True, type="primary")
with col2:
    duplicate_detection = st.button("🔍 Duplicate Detection", use_container_width=True)

# Default mode
current_mode = "Price Comparison"
if duplicate_detection:
    current_mode = "Duplicate Detection"

st.write(f"**Current Mode:** {current_mode}")

# File upload section
st.subheader("📸 Upload Product Image")
uploaded_file = st.file_uploader(
    "Upload an image of a fashion item to check for duplicates and compare prices",
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG"
)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'is_duplicate' not in st.session_state:
    st.session_state.is_duplicate = False
if 'detected_product' not in st.session_state:
    st.session_state.detected_product = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0

# Process uploaded image
if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Analyze button
        if st.button("🔍 Analyze Image", use_container_width=True, type="primary"):
            with st.spinner("🔬 Analyzing your image and searching for matches..."):
                # Simulate AI processing time
                time.sleep(3)
                
                # Detect product type (simulated AI)
                product_type, product_id = detect_product_type(image)
                detected_product = PRODUCT_DATABASE[product_type][product_id]
                
                # Analyze for duplicates
                is_duplicate, confidence = analyze_for_duplicates(product_type, product_id)
                
                # Store results in session state
                st.session_state.is_duplicate = is_duplicate
                st.session_state.detected_product = detected_product
                st.session_state.confidence = confidence
                st.session_state.analysis_complete = True
                st.session_state.product_type = product_type
                
                st.success("✅ Analysis complete!")

# Show results if analysis is complete
if st.session_state.analysis_complete and st.session_state.detected_product is not None:
    product = st.session_state.detected_product
    
    st.subheader("📊 Analysis Results")
    
    # Product identification and duplicate detection result
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**Product:** {product['name']}")
        st.write(f"**Brand:** {product['brand']}")
        st.write(f"**Category:** {product['category']}")
        st.write(f"**Description:** {product['description']}")
    
    with col2:
        st.write(f"**Confidence:** {st.session_state.confidence}%")
    
    with col3:
        if st.session_state.is_duplicate:
            st.markdown('<div class="dupe-yes">🔄 Potential Duplicate</div>', unsafe_allow_html=True)
            st.info("This product may have identical or very similar versions from other sellers.")
        else:
            st.markdown('<div class="dupe-no">✅ Original Product</div>', unsafe_allow_html=True)
            st.success("This appears to be an authentic/original product.")
    
    # Price comparison section
    st.subheader("💰 Price Comparison Across Retailers")
    
    if product['prices']:
        # Find best price
        best_price = min(product['prices'], key=lambda x: x['price'])
        
        # Display price comparison cards
        cols = st.columns(len(product['prices']))
        
        for idx, (col, retailer_data) in enumerate(zip(cols, product['prices'])):
            with col:
                is_best = retailer_data == best_price
                
                if is_best:
                    st.markdown('<div class="best-price">', unsafe_allow_html=True)
                    st.markdown('<div class="best-price-tag">Best Price</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="website-card">', unsafe_allow_html=True)
                
                st.write(f"**{retailer_data['retailer']}**")
                st.write(f"## ${retailer_data['price']}")
                
                # Display rating stars
                rating = retailer_data['rating']
                stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                st.write(f"{stars} ({rating}/5)")
                
                if st.button(f"View on {retailer_data['retailer']}", key=f"btn_{idx}", use_container_width=True):
                    st.info(f"🛒 Redirecting to {retailer_data['retailer']}...")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Price history chart
    st.subheader("📈 Price History (Last 6 Months)")
    
    # Generate realistic price history data
    current_price = product['prices'][0]['price']  # Use first price as reference
    dates = pd.date_range(start='2024-05-01', end='2024-11-16', freq='M')
    
    # Create realistic price fluctuations
    base_prices = []
    for i in range(len(dates)):
        # Simulate price changes (slight variations around current price)
        fluctuation = np.random.uniform(-0.15, 0.10)  # -15% to +10% fluctuation
        historical_price = current_price * (1 + fluctuation)
        base_prices.append(round(historical_price, 2))
    
    # Ensure the trend makes sense (latest price should be close to current)
    base_prices[-1] = current_price
    
    price_history_df = pd.DataFrame({
        'Date': dates,
        'Price ($)': base_prices
    })
    
    st.line_chart(price_history_df.set_index('Date'))
    
    # Similar products section
    st.subheader("🛍️ Similar Products")
    
    if product['similar_products']:
        for similar in product['similar_products']:
            with st.expander(f"{similar['name']} - ${similar['price']} ({similar['similarity']}% similar)"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Price:** ${similar['price']}")
                    st.write(f"**Similarity Score:** {similar['similarity']}%")
                with col2:
                    if st.button("Compare", key=f"compare_{similar['name']}"):
                        st.info(f"🔍 Comparing with {similar['name']}...")

# Instructions when no image is uploaded
else:
    st.info("👆 Please upload an image to get started!")
    
    # Show sample products for demonstration
    st.subheader("🎯 Sample Products You Can Analyze")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**👟 Nike Shoes**")
        st.write("- Nike Air Max 270")
        st.write("- Nike Air Force 1")
        st.write("- Nike Revolution 6")
        
    with col2:
        st.write("**👟 Adidas Shoes**")
        st.write("- Adidas Ultraboost")
        st.write("- Adidas NMD_R1")
        st.write("- Adidas Stan Smith")
        
    with col3:
        st.write("**👗 Clothing**")
        st.write("- ZARA Floral Dress")
        st.write("- H&M Summer Dress")
        st.write("- Mango Midi Dress")

# Footer
st.markdown("---")
st.markdown("**Fashion Comparison Hub** - AI-powered price intelligence and authenticity verification")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
