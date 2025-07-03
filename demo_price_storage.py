#!/usr/bin/env python3
"""
Demonstration script for the PriceStorage module.
This script shows how to use all the main features of the price storage system.
"""

from price_storage import PriceStorage, quick_add_product, quick_search
from datetime import datetime, timedelta

def demo_basic_usage():
    """Demonstrate basic usage of the PriceStorage module."""
    print("=" * 60)
    print("PRICE STORAGE MODULE DEMONSTRATION")
    print("=" * 60)
    
    # Create a new price storage instance
    storage = PriceStorage("demo_prices.txt")
    
    print("1. Adding products to different categories:")
    print("-" * 40)
    
    # Add products to Electronics category
    storage.add_product("Electronics", "iPhone 15 Pro", 999.99, additional_info={
        "brand": "Apple",
        "model": "A3108",
        "storage": "128GB"
    })
    storage.add_product("Electronics", "Samsung Galaxy S24", 899.99, additional_info={
        "brand": "Samsung",
        "model": "SM-S921",
        "storage": "256GB"
    })
    storage.add_product("Electronics", "MacBook Air M3", 1199.99, additional_info={
        "brand": "Apple",
        "screen": "13.6 inch",
        "processor": "M3"
    })
    
    # Add products to Home & Garden category
    storage.add_product("Home & Garden", "Dyson V15 Detect", 749.99, additional_info={
        "brand": "Dyson",
        "type": "Cordless Vacuum",
        "battery_life": "60 minutes"
    })
    storage.add_product("Home & Garden", "Instant Pot Duo 7-in-1", 79.99, additional_info={
        "brand": "Instant Pot",
        "capacity": "6 quart",
        "functions": 7
    })
    
    # Add products to Books category
    storage.add_product("Books", "The Psychology of Money", 14.99, additional_info={
        "author": "Morgan Housel",
        "pages": 256,
        "publisher": "Harriman House"
    })
    storage.add_product("Books", "Atomic Habits", 13.49, additional_info={
        "author": "James Clear",
        "pages": 320,
        "publisher": "Avery"
    })
    
    print("✓ Added 7 products across 3 categories")
    
    return storage

def demo_price_updates():
    """Demonstrate price update functionality."""
    print("\n2. Updating product prices (with price history):")
    print("-" * 40)
    
    storage = PriceStorage("demo_prices.txt")
    
    # Update iPhone price (price drop)
    old_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    storage.add_product("Electronics", "iPhone 15 Pro", 949.99, date=old_date)
    print("✓ Updated iPhone 15 Pro price: $999.99 → $949.99")
    
    # Update MacBook price
    storage.add_product("Electronics", "MacBook Air M3", 1099.99)
    print("✓ Updated MacBook Air M3 price: $1199.99 → $1099.99")
    
    return storage

def demo_search_and_filter():
    """Demonstrate search and filtering capabilities."""
    print("\n3. Searching and filtering products:")
    print("-" * 40)
    
    storage = PriceStorage("demo_prices.txt")
    
    # Search for products by name
    print("Search results for 'iPhone':")
    results = storage.search_products("iPhone")
    for category, product, info in results:
        print(f"  - {product} ({category}): ${info['current_price']:.2f}")
    
    # Filter by price range
    print("\nProducts under $100:")
    cheap_products = storage.get_price_range_products(max_price=100)
    for category, product, info in cheap_products:
        print(f"  - {product} ({category}): ${info['current_price']:.2f}")
    
    print("\nProducts between $500-$1000:")
    mid_range = storage.get_price_range_products(min_price=500, max_price=1000)
    for category, product, info in mid_range:
        print(f"  - {product} ({category}): ${info['current_price']:.2f}")

def demo_category_management():
    """Demonstrate category management features."""
    print("\n4. Category management:")
    print("-" * 40)
    
    storage = PriceStorage("demo_prices.txt")
    
    # List all categories
    categories = storage.get_all_categories()
    print(f"Available categories: {', '.join(categories)}")
    
    # Get products in specific category
    print("\nElectronics category products:")
    electronics = storage.get_category_products("Electronics")
    for product, info in electronics.items():
        print(f"  - {product}: ${info['current_price']:.2f}")
        if info['price_history']:
            print(f"    (Price changed {len(info['price_history'])} times)")

def demo_data_export():
    """Demonstrate data export functionality."""
    print("\n5. Data export and reporting:")
    print("-" * 40)
    
    storage = PriceStorage("demo_prices.txt")
    
    # Export to CSV
    storage.export_to_csv("demo_export.csv")
    print("✓ Exported data to demo_export.csv")
    
    # Generate and save report
    storage.save_report("demo_report.txt")
    print("✓ Generated detailed report: demo_report.txt")
    
    # Show sample report content
    print("\nSample report preview:")
    report = storage.generate_report()
    print(report[:300] + "...")

def demo_quick_functions():
    """Demonstrate quick convenience functions."""
    print("\n6. Quick convenience functions:")
    print("-" * 40)
    
    # Quick add without managing storage instance
    quick_add_product("Sports", "Nike Air Max 270", 150.00)
    print("✓ Quickly added Nike Air Max 270")
    
    # Quick search
    results = quick_search("Nike")
    print(f"✓ Quick search found {len(results)} results for 'Nike'")
    for category, product, info in results:
        print(f"  - {product}: ${info['current_price']:.2f}")

def demo_import_existing_data():
    """Demonstrate importing existing CSV data."""
    print("\n7. Importing existing Amazon scraping data:")
    print("-" * 40)
    
    storage = PriceStorage("demo_prices.txt")
    
    # Import from the existing Amazon CSV file
    try:
        # First, let's create a properly formatted version of the existing data
        import csv
        
        # Read the existing Amazon data and reformat it
        with open("Result Amazon Web Scrapping.csv", 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            
            # Create a new properly formatted CSV
            with open("formatted_amazon_data.csv", 'w', newline='', encoding='utf-8') as outfile:
                fieldnames = ['Category', 'Product', 'Price', 'Date']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in reader:
                    if 'Title' in row and 'Price' in row:
                        # Categorize the product (simple example)
                        title = row['Title']
                        category = "Home & Garden"  # Default category
                        if any(word in title.lower() for word in ['vacuum', 'cleaner']):
                            category = "Home & Garden"
                        elif any(word in title.lower() for word in ['phone', 'laptop', 'computer']):
                            category = "Electronics"
                        
                        writer.writerow({
                            'Category': category,
                            'Product': title,
                            'Price': row['Price'],
                            'Date': row.get('Date', datetime.now().strftime("%Y-%m-%d"))
                        })
        
        # Now import the formatted data
        storage.import_from_csv("formatted_amazon_data.csv")
        print("✓ Successfully imported Amazon scraping data")
        
        # Show what was imported
        vacuum_products = storage.search_products("vacuum")
        if vacuum_products:
            category, product, info = vacuum_products[0]
            print(f"  - Imported: {product} (${info['current_price']:.2f})")
        
    except FileNotFoundError:
        print("⚠ Amazon CSV file not found, skipping import demo")
    except Exception as e:
        print(f"⚠ Error importing data: {e}")

def show_final_summary():
    """Show final summary of all stored data."""
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    storage = PriceStorage("demo_prices.txt")
    
    categories = storage.get_all_categories()
    total_products = sum(len(storage.get_category_products(cat)) for cat in categories)
    
    print(f"Total categories: {len(categories)}")
    print(f"Total products: {total_products}")
    print(f"Categories: {', '.join(categories)}")
    
    # Show cheapest and most expensive products
    all_products = []
    for category in categories:
        products = storage.get_category_products(category)
        for product, info in products.items():
            all_products.append((category, product, info['current_price']))
    
    if all_products:
        cheapest = min(all_products, key=lambda x: x[2])
        most_expensive = max(all_products, key=lambda x: x[2])
        
        print(f"\nCheapest product: {cheapest[1]} (${cheapest[2]:.2f})")
        print(f"Most expensive product: {most_expensive[1]} (${most_expensive[2]:.2f})")

if __name__ == "__main__":
    """Run the complete demonstration."""
    try:
        demo_basic_usage()
        demo_price_updates()
        demo_search_and_filter()
        demo_category_management()
        demo_data_export()
        demo_quick_functions()
        demo_import_existing_data()
        show_final_summary()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("Files created:")
        print("- demo_prices.txt (main price storage file)")
        print("- demo_export.csv (exported data)")
        print("- demo_report.txt (detailed report)")
        print("- formatted_amazon_data.csv (reformatted import file)")
        print("- price_backups/ (backup directory)")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()