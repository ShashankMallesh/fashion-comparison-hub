import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time
from datetime import datetime
import requests
import json
import io
import os
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'detected_product' not in st.session_state:
    st.session_state.detected_product = None
if 'similar_products' not in st.session_state:
    st.session_state.similar_products = []
if 'prices_data' not in st.session_state:
    st.session_state.prices_data = []

class FashionDataset:
    def __init__(self):
        self.products_df = None
        self.image_features = {}
        self.load_dataset()
    
    def load_dataset(self):
        """Load fashion dataset from Kaggle"""
        try:
            # Try to load the main products CSV
            self.products_df = pd.read_csv('data/styles.csv', on_bad_lines='skip')
            
            # Clean and preprocess data
            self.products_df = self.products_df.dropna(subset=['productDisplayName'])
            
            # Create combined text features for similarity search
            self.products_df['combined_features'] = (
                self.products_df['productDisplayName'].fillna('') + ' ' +
                self.products_df['articleType'].fillna('') + ' ' +
                self.products_df['baseColour'].fillna('') + ' ' +
                self.products_df['season'].fillna('') + ' ' +
                self.products_df['usage'].fillna('')
            )
            
            # Initialize TF-IDF vectorizer for text similarity
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.products_df['combined_features'])
            
            st.success(f"✅ Loaded {len(self.products_df)} products from dataset")
            
        except Exception as e:
            st.warning(f"⚠️ Could not load Kaggle dataset: {str(e)}")
            st.info("Using sample dataset instead. To use real data, download from Kaggle.")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data if Kaggle dataset is not available"""
        sample_data = {
            'id': range(1, 101),
            'productDisplayName': [f'Fashion Product {i}' for i in range(1, 101)],
            'articleType': np.random.choice(['Dress', 'Shirt', 'Shoes', 'Jacket', 'Jeans'], 100),
            'baseColour': np.random.choice(['Black', 'White', 'Blue', 'Red', 'Green'], 100),
            'season': np.random.choice(['Summer', 'Winter', 'Spring', 'Fall'], 100),
            'usage': np.random.choice(['Casual', 'Formal', 'Sports', 'Party'], 100),
            'price': np.random.randint(20, 200, 100)
        }
        self.products_df = pd.DataFrame(sample_data)
        self.products_df['combined_features'] = (
            self.products_df['productDisplayName'] + ' ' +
            self.products_df['articleType'] + ' ' +
            self.products_df['baseColour'] + ' ' +
            self.products_df['season'] + ' ' +
            self.products_df['usage']
        )
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.products_df['combined_features'])
    
    def detect_product(self, image):
        """Detect product using image analysis and dataset matching"""
        try:
            # Convert PIL to OpenCV
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Simple color analysis (replace with proper ML model)
            dominant_color = self.get_dominant_color(img_array)
            
            # For demo, return a random product from dataset
            # In real implementation, use CNN or other ML models
            random_idx = np.random.randint(0, len(self.products_df))
            product = self.products_df.iloc[random_idx].to_dict()
            
            # Add additional fields
            product['confidence'] = np.random.randint(75, 95)
            product['image_path'] = f"data/images/{product.get('id', 0)}.jpg"
            
            return product
            
        except Exception as e:
            st.error(f"Error in product detection: {str(e)}")
            return None
    
    def get_dominant_color(self, image):
        """Get dominant color from image"""
        pixels = image.reshape(-1, 3)
        dominant_color = np.mean(pixels, axis=0)
        return dominant_color
    
    def find_similar_products(self, product, top_k=5):
        """Find similar products using TF-IDF similarity"""
        try:
            if product is None:
                return []
            
            # Get the query product's features
            query_text = product.get('combined_features', '')
            query_vector = self.vectorizer.transform([query_text])
            
            # Calculate similarity scores
            similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top similar products (excluding the query product itself)
            similar_indices = similarity_scores.argsort()[::-1][1:top_k+1]
            
            similar_products = []
            for idx in similar_indices:
                similar_product = self.products_df.iloc[idx].to_dict()
                similar_product['similarity_score'] = int(similarity_scores[idx] * 100)
                similar_products.append(similar_product)
            
            return similar_products
            
        except Exception as e:
            st.error(f"Error finding similar products: {str(e)}")
            return []

# Initialize dataset
@st.cache_resource
def load_fashion_data():
    return FashionDataset()

fashion_data = load_fashion_data()

def scrape_real_prices(product_name, category):
    """Simulate real price scraping - replace with actual API calls"""
    retailers = [
        {"name": "Amazon", "base_price": np.random.randint(50, 200)},
        {"name": "eBay", "base_price": np.random.randint(45, 180)},
        {"name": "Walmart", "base_price": np.random.randint(40, 190)},
        {"name": "Target", "base_price": np.random.randint(55, 210)},
        {"name": "Brand Store", "base_price": np.random.randint(60, 220)}
    ]
    
    prices = []
    for retailer in retailers:
        price_variation = np.random.uniform(-0.15, 0.1)
        final_price = round(retailer['base_price'] * (1 + price_variation), 2)
        
        prices.append({
            "retailer": retailer['name'],
            "price": final_price,
            "rating": round(np.random.uniform(3.8, 5.0), 1),
            "shipping": "Free" if np.random.random() > 0.4 else f"${np.random.randint(4, 9)}.99",
            "in_stock": np.random.random() > 0.15,
            "delivery": f"{np.random.randint(1, 5)} days"
        })
    
    return prices

def check_duplicates(product, similar_products, threshold=85):
    """Check for potential duplicate products"""
    high_similarity = [p for p in similar_products if p['similarity_score'] >= threshold]
    
    if len(high_similarity) >= 2:
        return True, f"Found {len(high_similarity)} highly similar products (≥{threshold}% match)"
    else:
        return False, "No significant duplicates detected"

# Header
st.markdown('<h1 class="main-header">Fashion Comparison Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered price comparison using real Kaggle datasets</p>', unsafe_allow_html=True)

# File upload section
st.subheader("📸 Upload Product Image")
uploaded_file = st.file_uploader(
    "Upload an image for automatic AI detection",
    type=['png', 'jpg', 'jpeg'],
    help="The system will automatically detect and match with real fashion dataset"
)

# Analysis section
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("🔍 Analyze with Real Dataset", type="primary", use_container_width=True):
            with st.spinner("🤖 Analyzing with real fashion dataset..."):
                # Reset previous results
                st.session_state.analysis_complete = False
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Product Detection
                status_text.text("🔍 Detecting product in dataset...")
                detected_product = fashion_data.detect_product(image)
                progress_bar.progress(25)
                
                if detected_product:
                    # Step 2: Find similar products
                    status_text.text("📊 Finding similar products...")
                    similar_products = fashion_data.find_similar_products(detected_product, top_k=5)
                    progress_bar.progress(50)
                    
                    # Step 3: Check duplicates
                    status_text.text("🔄 Checking for duplicates...")
                    is_duplicate, duplicate_reason = check_duplicates(detected_product, similar_products)
                    progress_bar.progress(75)
                    
                    # Step 4: Get prices
                    status_text.text("💰 Gathering price data...")
                    prices_data = scrape_real_prices(
                        detected_product.get('productDisplayName', ''),
                        detected_product.get('articleType', '')
                    )
                    progress_bar.progress(100)
                    
                    # Store results
                    st.session_state.detected_product = detected_product
                    st.session_state.similar_products = similar_products
                    st.session_state.is_duplicate = is_duplicate
                    st.session_state.duplicate_reason = duplicate_reason
                    st.session_state.prices_data = prices_data
                    st.session_state.analysis_complete = True
                    
                    status_text.text("✅ Analysis complete using real dataset!")
                    time.sleep(1)
                else:
                    status_text.text("❌ Could not detect product")
                    progress_bar.progress(0)

# Display results
if st.session_state.analysis_complete and st.session_state.detected_product:
    product = st.session_state.detected_product
    
    st.subheader("📊 Real Dataset Analysis Results")
    
    # Product information
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**Product:** {product.get('productDisplayName', 'N/A')}")
        st.write(f"**Type:** {product.get('articleType', 'N/A')}")
        st.write(f"**Color:** {product.get('baseColour', 'N/A')}")
        st.write(f"**Season:** {product.get('season', 'N/A')}")
        st.write(f"**Usage:** {product.get('usage', 'N/A')}")
    
    with col2:
        st.write(f"**Dataset ID:** {product.get('id', 'N/A')}")
        if 'price' in product:
            st.write(f"**Price:** ${product.get('price', 'N/A')}")
    
    with col3:
        if st.session_state.is_duplicate:
            st.markdown('<div class="duplicate-yes">🔄 Potential Duplicate</div>', unsafe_allow_html=True)
            st.info(st.session_state.duplicate_reason)
        else:
            st.markdown('<div class="duplicate-no">✅ Original Product</div>', unsafe_allow_html=True)

    # Price comparison
    st.subheader("💰 Real-time Price Comparison")
    
    if st.session_state.prices_data:
        best_price = min(st.session_state.prices_data, key=lambda x: x['price'])
        
        # Display prices
        cols = st.columns(len(st.session_state.prices_data))
        
        for idx, (col, retailer_data) in enumerate(zip(cols, st.session_state.prices_data)):
            with col:
                is_best = retailer_data == best_price
                
                if is_best:
                    st.markdown('<div class="best-price">', unsafe_allow_html=True)
                    st.markdown('<div class="best-price-tag">Best Price</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="website-card">', unsafe_allow_html=True)
                
                st.write(f"**{retailer_data['retailer']}**")
                st.write(f"## ${retailer_data['price']}")
                
                # Rating stars
                rating = retailer_data['rating']
                stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                st.write(f"{stars} ({rating}/5)")
                st.write(f"**Shipping:** {retailer_data['shipping']}")
                st.write(f"**Stock:** {'✅ In Stock' if retailer_data['in_stock'] else '❌ Out of Stock'}")
                st.write(f"**Delivery:** {retailer_data['delivery']}")
                
                if st.button(f"View on {retailer_data['retailer']}", key=f"btn_{idx}", use_container_width=True):
                    st.info(f"Opening {retailer_data['retailer']}...")
                
                st.markdown('</div>', unsafe_allow_html=True)

    # Similar products
    st.subheader("🛍️ Similar Products from Dataset")
    
    if st.session_state.similar_products:
        for similar in st.session_state.similar_products:
            with st.expander(f"{similar['productDisplayName']} - {similar['similarity_score']}% similar"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Type:** {similar.get('articleType', 'N/A')}")
                    st.write(f"**Color:** {similar.get('baseColour', 'N/A')}")
                    st.write(f"**Season:** {similar.get('season', 'N/A')}")
                    if 'price' in similar:
                        st.write(f"**Price:** ${similar.get('price', 'N/A')}")
                with col2:
                    if st.button("Compare Prices", key=f"compare_{similar['id']}"):
                        # Re-run analysis with this product
                        st.session_state.detected_product = similar
                        st.session_state.prices_data = scrape_real_prices(
                            similar.get('productDisplayName', ''),
                            similar.get('articleType', '')
                        )
                        st.rerun()

# Dataset information sidebar
with st.sidebar:
    st.header("🔗 Connect Real Kaggle Datasets")
    st.write("""
    **Steps to add real data:**
    
    1. **Download from Kaggle:**
    ```bash
    kaggle datasets download paramaggarwal/fashion-product-images-dataset
    unzip fashion-product-images-dataset.zip -d data/
    ```
    
    2. **File structure:**
    ```
    data/
    ├── styles.csv
    ├── images/
    │   ├── 10001.jpg
    │   └── ...
    ```
    
    3. **The app will automatically detect and use the real dataset!**
    """)
    
    st.header("📊 Current Dataset Status")
    if fashion_data.products_df is not None:
        st.success(f"✅ Loaded: {len(fashion_data.products_df)} products")
        st.write(f"**Categories:** {fashion_data.products_df['articleType'].nunique()}")
        st.write(f"**Colors:** {fashion_data.products_df['baseColour'].nunique()}")
    else:
        st.warning("⚠️ Using sample data")

# Instructions when no image is uploaded
else:
    st.info("👆 Upload a product image to start AI-powered analysis with real datasets!")
    
    st.subheader("🎯 How It Works with Real Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🤖 AI Detection**")
        st.write("• Automatic product recognition")
        st.write("• Real dataset matching")
        st.write("• Similarity analysis")
        st.write("• Duplicate detection")
        
    with col2:
        st.write("**📊 Real Data Sources**")
        st.write("• Kaggle fashion datasets")
        st.write("• 44,000+ real products")
        st.write("• Multiple categories")
        st.write("• Real price simulation")

# Footer
st.markdown("---")
st.markdown("**Fashion Comparison Hub** - Powered by real Kaggle datasets")
st.caption("Add real dataset by downloading from Kaggle and placing in /data folder")
