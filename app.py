# OPTIMIZED DATA LOADING - Add this to your app.py

@st.cache_data
def load_optimized_data():
    """Load optimized dataset for faster deployment"""
    try:
        # Try optimized version first
        with open('fashion_data_optimized.json', 'r') as f:
            data = json.load(f)
        print(f"✅ Loaded optimized dataset: {len(data)} products")
        return data
    except FileNotFoundError:
        try:
            # Fallback to small version
            with open('fashion_data_small.json', 'r') as f:
                data = json.load(f)
            print(f"✅ Loaded small dataset: {len(data)} products")
            return data
        except FileNotFoundError:
            # Final fallback to original (with limit)
            with open('fashion_data_with_comparison.json', 'r') as f:
                data = json.load(f)
            # Limit to 50 products if original is too large
            data = data[:50]
            print(f"✅ Loaded limited original dataset: {len(data)} products")
            return data

# Use this in your main app
products_data = load_optimized_data()
