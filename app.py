import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Fashion Product Comparison",
    page_icon="👕",
    layout="wide"
)

# COMPATIBLE data loading (works with all Streamlit versions)
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_product_data():
    """Load optimized dataset"""
    try:
        # Try optimized version first
        with open('fashion_data_optimized.json', 'r') as f:
            data = json.load(f)
        st.success(f"✅ Loaded {len(data)} products")
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
                        {"store_name": "Flipkart", "price": 31.50, "in_stock": True}
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

# Display products
for product in products_data:
    with st.expander(f"👕 {product['title']} - ${product['price']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Category:** {product.get('category', 'N/A')}")
            st.write(f"**Color:** {product.get('color', 'N/A')}")
            st.write(f"**Rating:** {product.get('rating', 'N/A')} ⭐")
        
        with col2:
            if 'comparison' in product:
                st.write("**Price Comparison:**")
                for comp in product['comparison']['competitors'][:3]:  # Show top 3
                    status = "✅" if comp['in_stock'] else "❌"
                    st.write(f"{status} {comp['store_name']}: ${comp['price']}")

st.markdown("---")
st.success("🎉 Fashion Comparison Hub is live!")

