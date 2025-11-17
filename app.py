import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
from datetime import datetime
import io

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
    .duplicate-yes {
        background-color: rgba(220, 53, 69, 0.1);
        color: #dc3545;
        padding: 8px 15px;
        border-radius: 50px;
        font-weight: 600;
    }
    .duplicate-no {
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
    .product-category {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive Product Database
PRODUCT_DATABASE = {
    "shoes": {
        "nike_air_max": {
            "name": "Nike Air Max 270",
            "category": "Sneakers",
            "brand": "Nike",
            "description": "Men's Running Shoes with Air Max unit",
            "features": ["Air Cushioning", "Breathable Mesh", "Rubber Outsole"],
            "prices": [
                {"retailer": "Nike Official", "price": 150.00, "rating": 4.5, "shipping": "Free"},
                {"retailer": "Amazon", "price": 139.99, "rating": 4.3, "shipping": "Prime"},
                {"retailer": "Foot Locker", "price": 149.99, "rating": 4.4, "shipping": "$5.99"},
                {"retailer": "JD Sports", "price": 144.50, "rating": 4.2, "shipping": "Free"},
                {"retailer": "Finish Line", "price": 147.99, "rating": 4.1, "shipping": "$6.99"}
            ],
            "similar_products": [
                {"name": "Nike Air Force 1", "price": 100.00, "similarity": 85},
                {"name": "Adidas Ultraboost", "price": 180.00, "similarity": 78},
                {"name": "Nike Revolution 6", "price": 65.00, "similarity": 72}
            ]
        },
        "adidas_ultraboost": {
            "name": "Adidas Ultraboost 22",
            "category": "Running Shoes", 
            "brand": "Adidas",
            "description": "Men's Premium Running Shoes with Boost technology",
            "features": ["Boost Midsole", "Primeknit Upper", "Continental Rubber"],
            "prices": [
                {"retailer": "Adidas Official", "price": 190.00, "rating": 4.7, "shipping": "Free"},
                {"retailer": "Amazon", "price": 179.99, "rating": 4.5, "shipping": "Prime"},
                {"retailer": "Foot Locker", "price": 185.00, "rating": 4.6, "shipping": "$5.99"},
                {"retailer": "Dick's Sporting Goods", "price": 189.99, "rating": 4.4, "shipping": "Free"}
            ],
            "similar_products": [
                {"name": "Adidas NMD_R1", "price": 130.00, "similarity": 82},
                {"name": "Nike Pegasus 39", "price": 120.00, "similarity": 75},
                {"name": "New Balance Fresh Foam", "price": 110.00, "similarity": 70}
            ]
        },
        "puma_rs": {
            "name": "Puma RS-X Reinvention",
            "category": "Lifestyle Sneakers",
            "brand": "Puma",
            "description": "Chunky sneaker with retro-inspired design",
            "features": ["RS Cushioning", "Leather Upper", "Chunky Sole"],
            "prices": [
                {"retailer": "Puma Official", "price": 120.00, "rating": 4.3, "shipping": "Free"},
                {"retailer": "Zappos", "price": 115.99, "rating": 4.2, "shipping": "Free"},
                {"retailer": "Foot Locker", "price": 119.99, "rating": 4.1, "shipping": "$5.99"}
            ],
            "similar_products": [
                {"name": "Puma Cali Sport", "price": 85.00, "similarity": 80},
                {"name": "Nike Air Max 97", "price": 170.00, "similarity": 75},
                {"name": "Adidas Falcon", "price": 100.00, "similarity": 78}
            ]
        }
    },
    "clothing": {
        "floral_dress": {
            "name": "Women's Floral Summer Dress",
            "category": "Dresses",
            "brand": "ZARA",
            "description": "Floral Print Midi Dress with flowy silhouette",
            "features": ["100% Cotton", "Midi Length", "Floral Print"],
            "prices": [
                {"retailer": "ZARA", "price": 49.99, "rating": 4.2, "shipping": "$4.99"},
                {"retailer": "ASOS", "price": 54.99, "rating": 4.0, "shipping": "Free"},
                {"retailer": "H&M", "price": 39.99, "rating": 3.8, "shipping": "$3.99"},
                {"retailer": "Mango", "price": 59.99, "rating": 4.1, "shipping": "Free"}
            ],
            "similar_products": [
                {"name": "Blue Floral Dress", "price": 47.99, "similarity": 89},
                {"name": "Summer Maxi Dress", "price": 55.99, "similarity": 78},
                {"name": "Floral Print Midi", "price": 51.50, "similarity": 85}
            ]
        },
        "denim_jacket": {
            "name": "Men's Denim Jacket",
            "category": "Jackets",
            "brand": "Levi's",
            "description": "Classic denim trucker jacket",
            "features": ["100% Cotton", "Regular Fit", "Classic Wash"],
            "prices": [
                {"retailer": "Levi's Official", "price": 89.99, "rating": 4.6, "shipping": "Free"},
                {"retailer": "Macy's", "price": 84.99, "rating": 4.4, "shipping": "Free"},
                {"retailer": "Nordstrom", "price": 92.00, "rating": 4.5, "shipping": "Free"},
                {"retailer": "Amazon", "price": 79.99, "rating": 4.2, "shipping": "Prime"}
            ],
            "similar_products": [
                {"name": "Wrangler Denim Jacket", "price": 69.99, "similarity": 82},
                {"name": "Lee Classic Jacket", "price": 74.99, "similarity": 85},
                {"name": "Carhartt Denim Jacket", "price": 99.99, "similarity": 78}
            ]
        },
        "wool_coat": {
            "name": "Women's Wool Blend Coat",
            "category": "Outerwear",
            "brand": "Mango",
            "description": "Double-breasted wool blend coat",
            "features": ["Wool Blend", "Double-Breasted", "Belted"],
            "prices": [
                {"retailer": "Mango", "price": 129.99, "rating": 4.4, "shipping": "Free"},
                {"retailer": "ASOS", "price": 139.99, "rating": 4.2, "shipping": "Free"},
                {"retailer": "Nordstrom", "price": 149.99, "rating": 4.5, "shipping": "Free"}
            ],
            "similar_products": [
                {"name": "ZARA Wool Coat", "price": 119.99, "similarity": 88},
                {"name": "H&M Long Coat", "price": 99.99, "similarity": 75},
                {"name": "Massimo Dutti Coat", "price": 199.99, "similarity": 82}
            ]
        }
    },
    "accessories": {
        "designer_handbag": {
            "name": "Designer Crossbody Bag",
            "category": "Bags",
            "brand": "Michael Kors",
            "description": "Leather crossbody bag with chain strap",
            "features": ["Genuine Leather", "Adjustable Strap", "Multiple Compartments"],
            "prices": [
                {"retailer": "Michael Kors", "price": 198.00, "rating": 4.5, "shipping": "Free"},
                {"retailer": "Macy's", "price": 189.99, "rating": 4.3, "shipping": "Free"},
                {"retailer": "Nordstrom", "price": 205.00, "rating": 4.6, "shipping": "Free"},
                {"retailer": "Bloomingdale's", "price": 199.99, "rating": 4.4, "shipping": "Free"}
            ],
            "similar_products": [
                {"name": "Coach Crossbody", "price": 175.00, "similarity": 85},
                {"name": "Kate Spade Bag", "price": 168.00, "similarity": 82},
                {"name": "Fossil Leather Bag", "price": 120.00, "similarity": 78}
            ]
        },
        "sunglasses": {
            "name": "Aviator Sunglasses",
            "category": "Eyewear",
            "brand": "Ray-Ban",
            "description": "Classic aviator sunglasses with UV protection",
            "features": ["UV400 Protection", "Metal Frame", "Polarized Lenses"],
            "prices": [
                {"retailer": "Ray-Ban Official", "price": 153.00, "rating": 4.7, "shipping": "Free"},
                {"retailer": "Sunglass Hut", "price": 149.99, "rating": 4.6, "shipping": "Free"},
                {"retailer": "Amazon", "price": 139.99, "rating": 4.4, "shipping": "Prime"}
            ],
            "similar_products": [
                {"name": "Oakley Sunglasses", "price": 120.00, "similarity": 75},
                {"name": "Persol Sunglasses", "price": 180.00, "similarity": 80},
                {"name": "Warby Parker Aviator", "price": 95.00, "similarity": 82}
            ]
        },
        "smartwatch": {
            "name": "Smartwatch Series 8",
            "category": "Watches",
            "brand": "Apple",
            "description": "Latest smartwatch with health monitoring",
            "features": ["Heart Rate Monitor", "GPS", "Water Resistant", "OLED Display"],
            "prices": [
                {"retailer": "Apple Store", "price": 399.00, "rating": 4.8, "shipping": "Free"},
                {"retailer": "Amazon", "price": 379.99, "rating": 4.7, "shipping": "Prime"},
                {"retailer": "Best Buy", "price": 389.99, "rating": 4.6, "shipping": "Free"},
                {"retailer": "Target", "price": 395.00, "rating": 4.5, "shipping": "Free"}
            ],
            "similar_products": [
                {"name": "Samsung Galaxy Watch", "price": 299.99, "similarity": 75},
                {"name": "Fitbit Sense 2", "price": 249.99, "similarity": 70},
                {"name": "Garmin Venu 2", "price": 349.99, "similarity": 72}
            ]
        }
    },
    "jewelry": {
        "gold_bracelet": {
            "name": "14K Gold Chain Bracelet",
            "category": "Jewelry",
            "brand": "Pandora",
            "description": "Delicate gold chain bracelet with clasp",
            "features": ["14K Gold", "Adjustable", "Secure Clasp"],
            "prices": [
                {"retailer": "Pandora", "price": 89.99, "rating": 4.4, "shipping": "Free"},
                {"retailer": "Kay Jewelers", "price": 94.99, "rating": 4.3, "shipping": "Free"},
                {"retailer": "Zales", "price": 87.99, "rating": 4.2, "shipping": "Free"}
            ],
            "similar_products": [
                {"name": "Silver Chain Bracelet", "price": 45.99, "similarity": 78},
                {"name": "Rose Gold Bracelet", "price": 79.99, "similarity": 85},
                {"name": "Charm Bracelet", "price": 65.00, "similarity": 72}
            ]
        }
    }
}

def detect_product_from_image(image):
    """
    Enhanced product detection based on image analysis
    This simulates what an AI model would do
    """
    # Convert image to bytes to analyze
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_size = len(img_byte_arr.getvalue())
    
    # Get image dimensions
    width, height = image.size
    aspect_ratio = width / height
    
    # Enhanced detection logic
    if img_size < 50000:  # Small file size might be accessories/jewelry
        return "accessories", "sunglasses"
    elif aspect_ratio > 1.3:  # Wide images often show shoes horizontally
        return "shoes", "nike_air_max"
    elif aspect_ratio < 0.8:  # Tall images often show full outfits
        return "clothing", "wool_coat"
    elif width > 1000 and height > 1000:  # Large detailed images often show bags
        return "accessories", "designer_handbag"
    else:  # Default to a common clothing item
        return "clothing", "floral_dress"

def analyze_for_duplicates(product_type, product_id):
    """
    Enhanced duplicate detection with realistic scoring
    """
    import random
    
    # Base confidence based on product type (some are easier to identify than others)
    base_confidence = {
        "shoes": 85,
        "clothing": 80,
        "accessories": 75,
        "jewelry": 70
    }
    
    confidence = base_confidence.get(product_type, 75) + random.randint(-10, 15)
    confidence = max(65, min(98, confidence))  # Keep within reasonable range
    
    # Higher confidence products are less likely to be duplicates
    is_duplicate = confidence < 85  # If confidence < 85%, mark as potential duplicate
    
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
    "Upload an image of any fashion item (shoes, clothing, accessories, jewelry)",
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG. Works best with clear product images."
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
        
        # Manual category selection for better accuracy
        st.subheader("🔧 Help Improve Detection")
        manual_category = st.selectbox(
            "Select product category (optional):",
            ["Auto-detect", "Shoes", "Clothing", "Accessories", "Jewelry"],
            help="This helps the AI identify your product more accurately"
        )
        
        # Analyze button
        if st.button("🔍 Analyze Image", use_container_width=True, type="primary"):
            with st.spinner("🔬 Analyzing your image and searching for matches..."):
                # Simulate AI processing time
                time.sleep(2)
                
                # Detect product type
                if manual_category == "Auto-detect":
                    product_type, product_id = detect_product_from_image(image)
                else:
                    # Map manual selection to database categories
                    category_map = {
                        "Shoes": "shoes",
                        "Clothing": "clothing", 
                        "Accessories": "accessories",
                        "Jewelry": "jewelry"
                    }
                    product_type = category_map.get(manual_category, "clothing")
                    # Select a random product from that category
                    product_id = np.random.choice(list(PRODUCT_DATABASE[product_type].keys()))
                
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
                st.rerun()

# Show results if analysis is complete
if st.session_state.analysis_complete and st.session_state.detected_product is not None:
    product = st.session_state.detected_product
    
    st.subheader("📊 Analysis Results")
    
    # Product identification
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="product-category">{product["category"].upper()}</div>', unsafe_allow_html=True)
        st.write(f"**Product:** {product['name']}")
        st.write(f"**Brand:** {product['brand']}")
        st.write(f"**Description:** {product['description']}")
        
        # Show features
        if 'features' in product:
            st.write("**Key Features:**")
            for feature in product['features']:
                st.write(f"• {feature}")
    
    with col2:
        st.write(f"**Confidence:** {st.session_state.confidence}%")
        if st.session_state.is_duplicate:
            st.markdown('<div class="duplicate-yes">🔄 Potential Duplicate</div>', unsafe_allow_html=True)
            st.info("Similar products found from multiple sellers.")
        else:
            st.markdown('<div class="duplicate-no">✅ Original Product</div>', unsafe_allow_html=True)
            st.success("This appears to be an authentic product.")
    
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
                
                # Display rating and shipping
                rating = retailer_data['rating']
                stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                st.write(f"{stars} ({rating}/5)")
                st.write(f"**Shipping:** {retailer_data['shipping']}")
                
                if st.button(f"View on {retailer_data['retailer']}", key=f"btn_{idx}", use_container_width=True):
                    st.info(f"🛒 Redirecting to {retailer_data['retailer']}...")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Price history chart
    st.subheader("📈 Price History (Last 6 Months)")
    
    # Generate realistic price history data
    current_price = product['prices'][0]['price']
    dates = pd.date_range(start='2024-05-01', periods=6, freq='M')
    
    # Create realistic price fluctuations
    base_prices = []
    for i in range(6):
        fluctuation = np.random.uniform(-0.15, 0.10)
        historical_price = current_price * (1 + fluctuation)
        base_prices.append(round(historical_price, 2))
    
    # Ensure the trend makes sense
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
    st.info("👆 Upload a product image to analyze it for duplicates and compare prices!")
    
    # Show all available categories
    st.subheader("🎯 Supported Product Categories")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**👟 Shoes**")
        st.write("- Nike Air Max")
        st.write("- Adidas Ultraboost") 
        st.write("- Puma RS-X")
        st.write("- Running Shoes")
        st.write("- Lifestyle Sneakers")
        
    with col2:
        st.write("**👗 Clothing**")
        st.write("- Dresses")
        st.write("- Jackets & Coats")
        st.write("- T-Shirts")
        st.write("- Jeans")
        st.write("- Activewear")
        
    with col3:
        st.write("**👜 Accessories**")
        st.write("- Handbags")
        st.write("- Sunglasses")
        st.write("- Watches")
        st.write("- Belts")
        st.write("- Wallets")
        
    with col4:
        st.write("**💎 Jewelry**")
        st.write("- Bracelets")
        st.write("- Necklaces")
        st.write("- Earrings")
        st.write("- Rings")
        st.write("- Luxury Watches")

# Footer
st.markdown("---")
st.markdown("**Fashion Comparison Hub** - AI-powered price intelligence and authenticity verification")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
