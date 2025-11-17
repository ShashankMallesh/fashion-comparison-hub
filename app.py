import streamlit as st
import pandas as pd
import json
import os
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Fashion Dupe Detector & Price Comparison",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_product_data():
    """Load product data with multiple fallbacks"""
    try:
        with open('fashion_data_optimized.json', 'r') as f:
            data = json.load(f)
        return data
    except:
        return []

# Enhanced product detection function
def analyze_fashion_product(uploaded_image):
    """Detect product type and return relevant comparisons"""
    # Mock detection - replace with your actual model
    # For demo, we'll detect based on some logic or random selection
    
    product_categories = {
        'shoes': ['Running Shoes', 'Sneakers', 'Boots', 'Sandals'],
        'clothing': ['T-Shirts', 'Jeans', 'Dresses', 'Jackets'], 
        'accessories': ['Bags', 'Watches', 'Sunglasses', 'Jewelry']
    }
    
    # Simple detection logic (replace with your model)
    filename = uploaded_image.name.lower() if hasattr(uploaded_image, 'name') else ""
    
    if any(word in filename for word in ['shoe', 'sneaker', 'boot', 'footwear']):
        detected_type = 'shoes'
        product_name = "Running Sneakers"
    elif any(word in filename for word in ['shirt', 'tshirt', 'top', 'clothing']):
        detected_type = 'clothing' 
        product_name = "Cotton T-Shirt"
    elif any(word in filename for word in ['bag', 'watch', 'accessory']):
        detected_type = 'accessories'
        product_name = "Leather Bag"
    else:
        # Random fallback
        detected_type = np.random.choice(['shoes', 'clothing', 'accessories'])
        product_names = {
            'shoes': "Sports Shoes",
            'clothing': "Casual T-Shirt", 
            'accessories': "Fashion Bag"
        }
        product_name = product_names[detected_type]
    
    return {
        'product_type': detected_type,
        'product_name': product_name,
        'authenticity_score': np.random.uniform(0.85, 0.98),
        'similar_matches': np.random.randint(8, 25),
        'potential_dupes': np.random.randint(0, 4),
        'confidence': np.random.uniform(0.80, 0.95)
    }

# Load product data
products_data = load_product_data()

# Main App
st.title("🔍 Fashion Dupe Detector & Price Comparison")
st.markdown("Upload any fashion product image to check authenticity and compare prices across websites")

# File upload section
uploaded_file = st.file_uploader(
    "📸 Upload Fashion Product Image", 
    type=['jpg', 'jpeg', 'png'],
    help="Upload shoes, clothing, accessories for instant price comparison and dupe detection"
)

if uploaded_file is not None:
    # Display uploaded image
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(uploaded_file, caption="Your Product", use_column_width=True)
        
        # Analyze button
        if st.button("🔬 Analyze Product", type="primary"):
            with st.spinner("Analyzing product and finding best prices..."):
                analysis = analyze_fashion_product(uploaded_file)
                st.session_state.analysis_results = analysis
    
    with col2:
        if 'analysis_results' in st.session_state:
            analysis = st.session_state.analysis_results
            
            # Display analysis results
            st.subheader("🕵️ Dupe Detection Results")
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Authenticity", f"{analysis['authenticity_score']*100:.1f}%")
                st.progress(analysis['authenticity_score'])
            with col2:
                st.metric("Product Type", analysis['product_type'].title())
            with col3:
                st.metric("Similar Matches", analysis['similar_matches'])
            with col4:
                st.metric("Potential Dupes", analysis['potential_dupes'])
            
            st.markdown("---")
            
            # PRICE COMPARISON SECTION
            st.subheader("💰 Price Comparison Across Websites")
            
            # Filter relevant products based on detected type
            relevant_products = [
                p for p in products_data 
                if p.get('category', '').lower() == analysis['product_type']
            ]
            
            if relevant_products:
                # Show all relevant products with comparisons
                for product in relevant_products[:3]:  # Show top 3 matches
                    with st.expander(f"🛍️ {product['title']} - ${product['price']:.2f}", expanded=True):
                        
                        # Product details
                        col_a, col_b = st.columns([1, 2])
                        
                        with col_a:
                            st.write(f"**Match Confidence:** {analysis['confidence']*100:.1f}%")
                            st.write(f"**Category:** {product.get('category', 'N/A')}")
                            st.write(f"**Rating:** {product.get('rating', 'N/A')} ⭐")
                            st.write(f"**Color:** {product.get('color', 'N/A')}")
                        
                        with col_b:
                            if 'comparison' in product:
                                # Create comparison table
                                comparison_data = []
                                
                                # Our store
                                comparison_data.append({
                                    'Store': '🏪 Our Store',
                                    'Price': f"${product['price']:.2f}",
                                    'Discount': f"{product.get('discount', 0)}% OFF",
                                    'Rating': f"{product.get('rating', 'N/A')} ⭐",
                                    'Delivery': '2-3 days',
                                    'Trust': '98%'
                                })
                                
                                # Competitors
                                for comp in product['comparison']['competitors']:
                                    stock_icon = '✅' if comp['in_stock'] else '❌'
                                    comparison_data.append({
                                        'Store': f"{comp['store_logo']} {comp['store_name']}",
                                        'Price': f"${comp['price']:.2f}",
                                        'Discount': f"{comp['discount']}% OFF",
                                        'Rating': f"{comp['rating']} ⭐",
                                        'Delivery': comp['delivery_time'],
                                        'Trust': f"{comp['trust_score']}%"
                                    })
                                
                                # Display comparison
                                df = pd.DataFrame(comparison_data)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                # Best deal highlight
                                if product['comparison']['best_deal']:
                                    best = product['comparison']['best_deal']
                                    savings = product['price'] - best['price']
                                    if savings > 0:
                                        st.success(f"🎯 **BEST DEAL:** {best['store_name']} at ${best['price']:.2f} (Save ${savings:.2f})")
                                    else:
                                        st.info(f"💡 **Competitive Price:** Our store offers the best value")
            else:
                st.warning(f"No {analysis['product_type']} products found in database")
                
            # Dupe detection details
            st.markdown("---")
            st.subheader("🔍 Dupe Detection Analysis")
            
            if analysis['potential_dupes'] > 0:
                st.error(f"⚠️ **Warning:** {analysis['potential_dupes']} potential counterfeit products detected")
                st.write("""
                **Recommendations:**
                - Purchase from trusted stores with high trust scores
                - Check product reviews and ratings
                - Verify seller authenticity
                - Use secure payment methods
                """)
            else:
                st.success("✅ **Excellent:** No significant counterfeit risks detected")
                
else:
    # Default view when no image uploaded
    st.info("👆 **Upload a fashion product image to get started**")
    
    # Show sample of what's available
    if products_data:
        st.subheader("📦 Available Product Categories")
        
        categories = {}
        for product in products_data:
            cat = product.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)
        
        for category, products in categories.items():
            with st.expander(f"🔹 {category.title()} ({len(products)} products)"):
                for product in products[:2]:  # Show 2 samples per category
                    st.write(f"**{product['title']}** - ${product['price']:.2f}")
                    if 'comparison' in product and product['comparison']['best_deal']:
                        best = product['comparison']['best_deal']
                        st.write(f"   Best deal: {best['store_name']} - ${best['price']:.2f}")

# Footer
st.markdown("---")
st.markdown("""
**🛍️ Fashion Dupe Detector & Price Comparison**  
*AI-powered authenticity checking and multi-website price intelligence*
""")
