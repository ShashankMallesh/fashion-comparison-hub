# Create the optimized dataset
import json
import os

# Check if we have the comparison data
if os.path.exists('fashion_data_with_comparison.json'):
    with open('fashion_data_with_comparison.json', 'r') as f:
        data = json.load(f)
    
    # Create very small optimized version
    optimized_data = data[:10]  # Only 10 products!
    
    with open('fashion_data_optimized.json', 'w') as f:
        json.dump(optimized_data, f)
    
    print(f"✅ Created fashion_data_optimized.json with {len(optimized_data)} products")
else:
    # Create sample data if no file exists
    sample_data = [
        {
            "id": 1,
            "title": "Sample T-Shirt",
            "price": 29.99,
            "category": "Clothing",
            "color": "Blue",
            "comparison": {
                "competitors": [
                    {"store_name": "Amazon", "price": 27.99, "in_stock": True},
                    {"store_name": "Flipkart", "price": 31.50, "in_stock": True}
                ]
            }
        }
    ]
    with open('fashion_data_optimized.json', 'w') as f:
        json.dump(sample_data, f)
    print("✅ Created sample fashion_data_optimized.json")
