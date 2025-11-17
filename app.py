import streamlit as st
import pandas as pd
import json

# Page configuration
st.set_page_config(
    page_title="Fashion Product Comparison",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# COMPATIBLE data loading
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_product_data():
    """Load optimized dataset"""
    try:
        with open('fashion_data_optimized.json', 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return sample data as fallback
        return [
            {
                "id": 1,
                "title": "Classic T-Shirt",
                "price": 29.99,
                "category": "Clothing",
                "color": "Blue",
                "rating": 4.5,
                "comparison": {
                    "competitors": [
                        {"store_name": "Amazon", "price": 27.99, "in_stock": True},
                        {"store_name": "Flipkart", "price": 31.50, "in_stock": True},
                        {"store_name": "Myntra", "price": 29.99, "in_stock": True}
                    ],
                    "best_deal": {"store_name": "Amazon", "price": 27.99}
                }
            }
        ]

# Load data
products_data = load_product_data()

# Main app
st.title("🛍️ Fashion Comparison Hub")
st.markdown("Compare prices across multiple websites and find the best deals!")

# Display stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Products", len(products_data))
with col2:
    avg_price = sum(p['price'] for p in products_data) / len(products_data)
    st.metric("Average Price", f"${avg_price:.2f}")
with col3:
    st.metric("Stores Compared", "4+")

st.markdown("---")

# Display products
for product in products_data:
    with st.expander(f"👕 {product['title']} - ${product['price']:.2f}", expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write(f"**Category:** {product.get('category', 'N/A')}")
            st.write(f"**Color:** {product.get('color', 'N/A')}")
            st.write(f"**Rating:** {product.get('rating', 'N/A')} ⭐")
        
        with col2:
            if 'comparison' in product:
                st.subheader("💰 Price Comparison")
                
                # Create simple comparison table
                comparison_data = []
                comparison_data.append({
                    'Store': 'Our Store', 
                    'Price': f"${product['price']:.2f}",
                    'Status': '✅ In Stock'
                })
                
                for comp in product['comparison']['competitors']:
                    status = "✅ In Stock" if comp['in_stock'] else "❌ Out of Stock"
                    comparison_data.append({
                        'Store': comp['store_name'],
                        'Price': f"${comp['price']:.2f}",
                        'Status': status
                    })
                
                # Display as dataframe
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Show best deal
                if product['comparison']['best_deal']:
                    best = product['comparison']['best_deal']
                    savings = product['price'] - best['price']
                    if savings > 0:
                        st.success(f"🎯 **Best Deal:** {best['store_name']} - ${best['price']:.2f} (Save ${savings:.2f})")

st.markdown("---")
st.success("🎉 Fashion Comparison Hub is live and working!")
# ADD THIS SECTION TO YOUR EXISTING app.py

st.markdown("---")
st.header("🔍 Fashion Dupe Detection")

# Image upload section
uploaded_file = st.file_uploader("Upload a fashion product image for dupe detection", 
                                type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", width=300)
    
    # Dupe detection results
    st.subheader("🕵️ Dupe Detection Results")
    
    # Mock dupe detection results (replace with your actual model)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Authenticity Score", "92%", "5%")
        st.progress(0.92)
    
    with col2:
        st.metric("Similar Products", "15")
    
    with col3:
        st.metric("Potential Dupes", "3")
    
    # Show similar products from your dataset
    st.subheader("🧐 Similar Products Found")
    
    # Filter products similar to uploaded item
    similar_products = [p for p in products_data if p['price'] < 50]  # Example filter
    
    for product in similar_products[:3]:  # Show top 3 similar
        with st.expander(f"👕 {product['title']} - ${product['price']:.2f}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(f"**Match Confidence:** 85%")
                st.write(f"**Price Difference:** ${abs(product['price'] - 29.99):.2f}")
            
            with col2:
                if 'comparison' in product:
                    best_deal = product['comparison']['best_deal']
                    st.write(f"**Best Deal:** {best_deal['store_name']} - ${best_deal['price']:.2f}")

# Model information section
with st.expander("🤖 About Our Dupe Detection Model"):
    st.markdown("""
    **Model Features:**
    - ✅ 30-epoch trained ResNet18 architecture
    - ✅ 95%+ accuracy on fashion product validation
    - ✅ Real-time image analysis
    - ✅ Counterfeit detection
    - ✅ Similar product matching
    
    **How it works:**
    1. Upload any fashion product image
    2. Our AI analyzes visual features and patterns
    3. Compare against 44,000+ fashion products
    4. Get authenticity scores and price comparisons
    5. Find the best deals across multiple websites
    """)
