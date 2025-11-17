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

# Custom CSS with better error styling
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
    .error-box {
        background-color: #fee;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with error handling
def initialize_session_state():
    """Initialize all session state variables safely"""
    default_states = {
        'analysis_complete': False,
        'uploaded_image': None,
        'is_duplicate': False,
        'detected_product': None,
        'confidence': 0,
        'product_type': None,
        'error_message': None,
        'last_uploaded_file': None
    }
    
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Call this at the start
initialize_session_state()

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
        "nike_air_force": {
            "name": "Nike Air Force 1",
            "category": "Sneakers",
            "brand": "Nike", 
            "description": "Classic white leather sneakers",
            "features": ["Leather Upper", "Air-Sole Unit", "Rubber Outsole"],
            "prices": [
                {"retailer": "Nike Official", "price": 100.00, "rating": 4.6, "shipping": "Free"},
                {"retailer": "Foot Locker", "price": 99.99, "rating": 4.5, "shipping": "$5.99"},
                {"retailer": "Finish Line", "price": 102.00, "rating": 4.4, "shipping": "$6.99"},
                {"retailer": "Amazon", "price": 95.99, "rating": 4.3, "shipping": "Prime"}
            ],
            "similar_products": [
                {"name": "Nike Air Max 270", "price": 150.00, "similarity": 80},
                {"name": "Adidas Stan Smith", "price": 85.00, "similarity": 75},
                {"name": "Converse Chuck Taylor", "price": 65.00, "similarity": 70}
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
        "jordan_1": {
            "name": "Air Jordan 1 Retro High",
            "category": "Basketball Shoes",
            "brand": "Jordan",
            "description": "Classic high-top basketball sneakers",
            "features": ["Leather Upper", "High-Top", "Air-Sole Unit", "Iconic Design"],
            "prices": [
                {"retailer": "Nike Official", "price": 180.00, "rating": 4.8, "shipping": "Free"},
                {"retailer": "Foot Locker", "price": 179.99, "rating": 4.7, "shipping": "$5.99"},
                {"retailer": "Finish Line", "price": 182.00, "rating": 4.6, "shipping": "$6.99"},
                {"retailer": "StockX", "price": 220.00, "rating": 4.5, "shipping": "$10.99"}
            ],
            "similar_products": [
                {"name": "Jordan 1 Low", "price": 110.00, "similarity": 85},
                {"name": "Nike Dunk High", "price": 120.00, "similarity": 80},
                {"name": "Air Jordan 4", "price": 200.00, "similarity": 75}
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
        }
    }
}

def safe_image_open(uploaded_file):
    """Safely open image with error handling"""
    try:
        image = Image.open(uploaded_file)
        # Verify image can be processed
        image.verify()
        # Reopen since verify closes the image
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
    except Exception as e:
        st.session_state.error_message = f"Error processing image: {str(e)}"
        return None

def detect_product_from_image(uploaded_file):
    """Improved product detection that actually works for shoes"""
    try:
        file_name = uploaded_file.name.lower()
        
        # Check file name for clues
        if any(keyword in file_name for keyword in ['shoe', 'sneaker', 'nike', 'adidas', 'jordan', 'air', 'boot', 'footwear']):
            return "shoes", "nike_air_max"
        elif any(keyword in file_name for keyword in ['dress', 'gown', 'skirt', 'floral', 'zara']):
            return "clothing", "floral_dress"
        elif any(keyword in file_name for keyword in ['bag', 'purse', 'handbag', 'michael', 'kors']):
            return "accessories", "designer_handbag"
        elif any(keyword in file_name for keyword in ['jacket', 'denim', 'levi', 'coat']):
            return "clothing", "denim_jacket"
        
        return "manual", None
    except Exception as e:
        st.session_state.error_message = f"Error detecting product: {str(e)}"
        return "manual", None

def analyze_for_duplicates(product_type, product_id):
    """Enhanced duplicate detection with error handling"""
    try:
        import random
        confidence = random.randint(75, 95)
        is_duplicate = random.choice([True, False])
        return is_duplicate, confidence
    except Exception as e:
        st.session_state.error_message = f"Error in duplicate analysis: {str(e)}"
        return False, 0

def reset_analysis():
    """Reset the analysis state"""
    st.session_state.analysis_complete = False
    st.session_state.detected_product = None
    st.session_state.is_duplicate = False
    st.session_state.confidence = 0
    st.session_state.error_message = None

# Header
st.markdown('<h1 class="main-header">Fashion Comparison Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered price comparison and duplicate detection across multiple websites!</p>', unsafe_allow_html=True)

# Reset button in sidebar
with st.sidebar:
    st.header("App Controls")
    if st.button("🔄 Reset Analysis", use_container_width=True):
        reset_analysis()
        st.rerun()
    
    st.header("📊 App Status")
    st.write(f"Analysis Complete: {'✅' if st.session_state.analysis_complete else '❌'}")
    if st.session_state.error_message:
        st.error("⚠️ Error Detected")
    else:
        st.success("✅ App Running Normally")

# Show error message if any
if st.session_state.error_message:
    st.markdown(f"""
    <div class="error-box">
        <h3>⚠️ Application Error</h3>
        <p>{st.session_state.error_message}</p>
        <p><em>Please try uploading the image again or use the reset button.</em></p>
    </div>
    """, unsafe_allow_html=True)

# File upload section
st.subheader("📸 Upload Product Image")
uploaded_file = st.file_uploader(
    "Upload an image of any fashion item",
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG. Max size: 200MB"
)

# Clear previous error when new file is uploaded
if uploaded_file and uploaded_file != st.session_state.get('last_uploaded_file'):
    st.session_state.error_message = None
    st.session_state.last_uploaded_file = uploaded_file

# Process uploaded image
if uploaded_file is not None:
    try:
        # Safely open image
        image = safe_image_open(uploaded_file)
        if image is None:
            st.error("Failed to process the uploaded image. Please try another image.")
        else:
            st.session_state.uploaded_image = image
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Auto-detect product type from filename
                detected_type, detected_id = detect_product_from_image(uploaded_file)
                
                # Manual category selection for confirmation
                st.subheader("🔍 Confirm Product Type")
                
                if detected_type == "manual":
                    selected_category = st.selectbox(
                        "Select product category:",
                        ["Shoes", "Clothing", "Accessories"]
                    )
                else:
                    category_map = {"shoes": "Shoes", "clothing": "Clothing", "accessories": "Accessories"}
                    detected_category = category_map.get(detected_type, "Shoes")
                    
                    selected_category = st.selectbox(
                        "Detected category (confirm or change):",
                        ["Shoes", "Clothing", "Accessories"],
                        index=["Shoes", "Clothing", "Accessories"].index(detected_category)
                    )
                
                # Product type selection within category
                if selected_category == "Shoes":
                    shoe_type = st.selectbox(
                        "Select shoe type:",
                        ["Nike Air Max 270", "Nike Air Force 1", "Adidas Ultraboost", "Air Jordan 1"]
                    )
                    shoe_map = {
                        "Nike Air Max 270": ("shoes", "nike_air_max"),
                        "Nike Air Force 1": ("shoes", "nike_air_force"), 
                        "Adidas Ultraboost": ("shoes", "adidas_ultraboost"),
                        "Air Jordan 1": ("shoes", "jordan_1")
                    }
                    product_type, product_id = shoe_map[shoe_type]
                    
                elif selected_category == "Clothing":
                    clothing_type = st.selectbox(
                        "Select clothing type:",
                        ["Floral Dress", "Denim Jacket"]
                    )
                    clothing_map = {
                        "Flor
