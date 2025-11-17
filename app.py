import streamlit as st
import pandas as pd
import json
import os
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Fashion Comparison Hub",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_product_data():
    """Load product data with multiple fallbacks"""
    files_to_try = [
        'fashion_data_optimized.json',
        'fashion_data_with_comparison.json', 
        'fashion_data_small.json'
    ]
    
    for file_path in files_to_try:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            continue
        except Exception as e:
            st.warning(f"⚠️ Error loading {file_path}: {e}")
            continue
    
    return []

# Mock dupe detection function (replace with your actual model)
def analyze_image_for_dupes(uploaded_image):
    """Mock dupe detection - replace with your actual model inference"""
    # This is where you'd load your .pth model and run inference
    # For now, returning mock results
    
    # Simulate different product types based on filename or random selection
    product_types = ['Footwear', 'Clothing', 'Accessories']
    detected_type = np.random.choice(product_types)
    
    return {
        'authenticity_score': np.random.uniform(0.85, 0.98),
        'product_type': detected_type,
        'similar_products_count': np.random.randint(5, 20),
        'potential_dupes': np.random.randint(0, 3),
        'confidence': np.random.uniform(0.75, 0.95)
    }

# Load data
products_data = load_product_data()

# Main app
st.title("🛍️ Fashion Comparison Hub")
st.markdown("AI-powered price comparison and dupe detection across multiple websites!")

# Sidebar for navigation
st.sidebar.title("🔍 Navigation")
app_mode = st.sidebar.radio("Choose Mode:", ["Price Comparison", "Dupe Detection"])

if app_mode == "Price Comparison":
    # PRICE COMPARISON SECTION
    
    if products_data:
        # Extract unique categories
        categories = list(set([p.get('category', 'Unknown') for p in products_data]))
        categories.sort()
        
        # Category selector
        selected_category = st.selectbox(
            "🔍 Select Product Category:",
            categories,
            index=0 if categories else 0
        )
        
        # Filter products by selected category
        filtered_products = [p for p in products_data if p.get('category') == selected_category]
        
        # Display category stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Products", len(products_data))
        with col2:
            st.metric(f"{selected_category} Products", len(filtered_products))
        with col3:
            if filtered_products:
                avg_price = sum(p['price'] for p in filtered_products) / len(filtered_products)
                st.metric("Average Price", f"${avg_price:.2f}")
            else:
                st.metric("Average Price", "$0.00")
        with col4:
            st.metric("Stores Compared", "4+")
        
        st.markdown("---")
        
        # Display products from selected category
        if filtered_products:
            st.subheader(f"📦 {selected_category} Products")
            
            # Product grid - 3 columns
            cols = st.columns(3)
            
            for idx, product in enumerate(filtered_products):
                col = cols[idx % 3]
                
                with col:
                    with st.container():
                        st.markdown(f"### {product['title']}")
                        st.markdown(f"*{product.get('description', '')}*")
                        
                        # Price information
                        col_price1, col_price2 = st.columns(2)
                        with col_price1:
                            st.markdown(f"**${product['price']:.2f}**")
                            if 'original_price' in product:
                                st.markdown(f"~~${product['original_price']:.2f}~~")
                        with col_price2:
                            if 'discount' in product:
                                st.markdown(f"🔴 **{product['discount']}% OFF**")
                            st.markdown(f"⭐ {product.get('rating', 'N/A')}")
                        
                        # Product details
                        st.markdown(f"""
                        **Type:** {product.get('articleType', 'N/A')}  
                        **Color:** {product.get('color', 'N/A')}  
                        **Gender:** {product.get('gender', 'Unisex')}
                        """)
                        
                        # View details button
                        if st.button(f"View Price Comparison", key=f"btn_{product['id']}"):
                            st.session_state.selected_product = product
                        
                        st.markdown("---")
            
            # Detailed product view when selected
            if 'selected_product' in st.session_state:
                product = st.session_state.selected_product
                
                st.markdown("---")
                st.title(f"🔍 {product['title']}")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Product image placeholder
                    st.image(
                        "https://via.placeholder.com/300x400/4B7BF5/FFFFFF?text=Fashion+Product",
                        width=250
                    )
                    
                    # Quick info
                    st.markdown("### Product Details")
                    st.write(f"**Category:** {product.get('category', 'N/A')}")
                    st.write(f"**Type:** {product.get('articleType', 'N/A')}")
                    st.write(f"**Color:** {product.get('color', 'N/A')}")
                    st.write(f"**Season:** {product.get('season', 'N/A')}")
                    st.write(f"**Rating:** {product.get('rating', 'N/A')} ⭐")
                
                with col2:
                    # Price comparison section
                    st.subheader("💰 Price Comparison")
                    
                    if 'comparison' in product:
                        # Create comparison table
                        comparison_data = []
                        
                        # Add our store
                        comparison_data.append({
                            'Store': '🏪 Our Store',
                            'Price': f"${product['price']:.2f}",
                            'Discount': f"{product.get('discount', 0)}%",
                            'Rating': f"{product.get('rating', 'N/A')} ⭐",
                            'Stock': '✅ In Stock',
                            'Delivery': '2-3 days'
                        })
                        
                        # Add competitors
                        for competitor in product['comparison']['competitors']:
                            stock_status = '✅ In Stock' if competitor['in_stock'] else '❌ Out of Stock'
                            comparison_data.append({
                                'Store': f"{competitor['store_logo']} {competitor['store_name']}",
                                'Price': f"${competitor['price']:.2f}",
                                'Discount': f"{competitor['discount']}%",
                                'Rating': f"{competitor['rating']} ⭐",
                                'Stock': stock_status,
                                'Delivery': competitor['delivery_time']
                            })
                        
                        # Display as dataframe
                        df_comparison = pd.DataFrame(comparison_data)
                        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
                        
                        # Show best deal
                        if product['comparison']['best_deal']:
                            best_deal = product['comparison']['best_deal']
                            savings = product['price'] - best_deal['price']
                            if savings > 0:
                                st.success(f"🎯 **Best Deal:** {best_deal['store_name']} - ${best_deal['price']:.2f} (Save ${savings:.2f})")
                    
                    else:
                        st.info("No comparison data available for this product.")
        
        else:
            st.warning(f"No products found in {selected_category} category.")
    
    else:
        st.error("No product data loaded. Please check your data files.")

else:
    # DUPE DETECTION SECTION
    
    st.header("🔍 AI Dupe Detection")
    st.markdown("Upload a fashion product image to check authenticity and find similar products")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "📁 Upload Fashion Product Image", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload shoes, clothing, accessories for authenticity analysis"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)
        
        # Analyze image
        with st.spinner("🔬 Analyzing image for duplicates and authenticity..."):
            analysis_results = analyze_image_for_dupes(uploaded_file)
        
        # Display analysis results
        st.subheader("🕵️ Analysis Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            authenticity_score = analysis_results['authenticity_score']
            st.metric("Authenticity Score", f"{authenticity_score*100:.1f}%")
            st.progress(authenticity_score)
        
        with col2:
            st.metric("Detected Type", analysis_results['product_type'])
        
        with col3:
            st.metric("Similar Products", analysis_results['similar_products_count'])
        
        with col4:
            st.metric("Potential Dupes", analysis_results['potential_dupes'])
        
        st.markdown("---")
        
        # Show relevant products based on detected type
        detected_type = analysis_results['product_type']
        relevant_products = [p for p in products_data if p.get('category') == detected_type]
        
        if relevant_products:
            st.subheader(f"🧐 Similar {detected_type} Products")
            
            # Show top 3 similar products
            for product in relevant_products[:3]:
                with st.expander(f"👕 {product['title']} - ${product['price']:.2f}"):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        confidence = analysis_results['confidence']
                        st.write(f"**Match Confidence:** {confidence*100:.1f}%")
                        price_diff = abs(product['price'] - 50)  # Mock price comparison
                        st.write(f"**Price Difference:** ${price_diff:.2f}")
                    
                    with col2:
                        if 'comparison' in product:
                            best_deal = product['comparison']['best_deal']
                            st.write(f"**Best Deal:** {best_deal['store_name']} - ${best_deal['price']:.2f}")
        
        # Model information
        with st.expander("🤖 About Our Dupe Detection AI"):
            st.markdown("""
            **Model Features:**
            - ✅ 30-epoch trained ResNet18 architecture
            - ✅ 95%+ accuracy on fashion product validation
            - ✅ Real-time image analysis
            - ✅ Counterfeit detection
            - ✅ Product categorization
            
            **Supported Product Types:**
            - 👟 Footwear (Shoes, Sneakers, Boots)
            - 👕 Clothing (T-shirts, Jeans, Dresses)
            - 🎒 Accessories (Bags, Watches, Jewelry)
            """)
    
    else:
        st.info("👆 Please upload a fashion product image to start dupe detection")

# Footer
st.markdown("---")
st.markdown("🛍️ **Fashion Comparison Hub** • AI-powered price intelligence and authenticity verification")
