# Price Storage Module Usage Guide

This module provides a comprehensive solution for storing and managing product prices organized by categories in text files.

## Quick Start

```python
from price_storage import PriceStorage

# Create a storage instance
storage = PriceStorage("my_prices.txt")

# Add a product
storage.add_product("Electronics", "iPhone 15", 999.99)

# Search for products
results = storage.search_products("iPhone")
print(results)
```

## Core Features

### 1. Adding Products

```python
# Basic product addition
storage.add_product("Electronics", "MacBook Pro", 1999.99)

# With additional information
storage.add_product("Electronics", "iPad Air", 599.99, 
                   additional_info={
                       "brand": "Apple",
                       "storage": "256GB",
                       "color": "Space Gray"
                   })

# With specific date
storage.add_product("Books", "Python Programming", 39.99, 
                   date="2024-01-15")
```

### 2. Retrieving Data

```python
# Get all categories
categories = storage.get_all_categories()

# Get products in a category
electronics = storage.get_category_products("Electronics")

# Get specific product info
product_info = storage.get_product_info("Electronics", "iPhone 15")

# Search across all categories
iphone_results = storage.search_products("iPhone")

# Filter by price range
expensive_items = storage.get_price_range_products(min_price=1000)
affordable_items = storage.get_price_range_products(max_price=100)
mid_range = storage.get_price_range_products(min_price=100, max_price=500)
```

### 3. Price History Tracking

The module automatically tracks price changes:

```python
# First time adding a product
storage.add_product("Electronics", "Laptop", 1200.00)

# Later, update the price - creates price history
storage.add_product("Electronics", "Laptop", 1100.00)

# Check price history
laptop_info = storage.get_product_info("Electronics", "Laptop")
print(f"Current price: ${laptop_info['current_price']}")
print(f"Price changes: {len(laptop_info['price_history'])}")
```

### 4. Data Export and Import

```python
# Export to CSV
storage.export_to_csv("my_prices.csv")

# Import from CSV
storage.import_from_csv("imported_prices.csv")

# Generate and save detailed report
storage.save_report("price_report.txt")
```

### 5. Management Operations

```python
# Remove a specific product
storage.remove_product("Electronics", "Old Product")

# Clear entire category
storage.clear_category("Discontinued Items")

# Create manual backup
storage.create_backup()
```

## Convenience Functions

For quick operations without managing storage instances:

```python
from price_storage import quick_add_product, quick_search

# Quick add
quick_add_product("Sports", "Running Shoes", 120.00)

# Quick search
results = quick_search("Nike")
```

## File Structure

The module creates these files:

- `prices_by_category.txt` - Main storage file (JSON format)
- `price_backups/` - Directory for automatic backups
- `prices_export.csv` - When exporting to CSV
- `price_report.txt` - When generating reports

## Data Structure

Products are stored in this structure:

```json
{
  "Electronics": {
    "iPhone 15": {
      "current_price": 999.99,
      "price_history": [
        {"price": 1099.99, "date": "2024-01-01"}
      ],
      "first_added": "2024-01-01",
      "last_updated": "2024-01-15",
      "additional_info": {
        "brand": "Apple",
        "storage": "128GB"
      }
    }
  }
}
```

## Integration with Web Scraping

Perfect for price monitoring from web scraping:

```python
# After scraping Amazon/other sites
def update_scraped_prices(scraped_data):
    storage = PriceStorage("scraped_prices.txt")
    
    for item in scraped_data:
        storage.add_product(
            category=item['category'],
            product_name=item['title'],
            price=float(item['price']),
            additional_info={
                'url': item['url'],
                'seller': item['seller'],
                'rating': item.get('rating', 'N/A')
            }
        )
```

## Best Practices

1. **Use meaningful categories**: "Electronics", "Books", "Home & Garden"
2. **Include additional info**: Brand, model, specifications
3. **Regular backups**: The module auto-creates backups before saves
4. **Consistent naming**: Use consistent product names for price tracking
5. **Date format**: Use YYYY-MM-DD format for dates

## Error Handling

The module handles common errors gracefully:

- Missing files are created automatically
- Invalid data is skipped during imports
- Corrupted files trigger warnings and restart with empty data
- Automatic backups protect against data loss

## Example: Complete Price Monitoring Setup

```python
from price_storage import PriceStorage
from datetime import datetime

class PriceMonitor:
    def __init__(self, storage_file="monitored_prices.txt"):
        self.storage = PriceStorage(storage_file)
    
    def add_monitored_product(self, category, name, price, target_price=None):
        """Add a product with optional target price for alerts."""
        additional_info = {}
        if target_price:
            additional_info['target_price'] = target_price
        
        self.storage.add_product(category, name, price, 
                               additional_info=additional_info)
    
    def check_price_alerts(self):
        """Check for products that hit target prices."""
        alerts = []
        
        for category in self.storage.get_all_categories():
            products = self.storage.get_category_products(category)
            
            for name, info in products.items():
                target = info['additional_info'].get('target_price')
                current = info['current_price']
                
                if target and current <= target:
                    alerts.append(f"{name}: ${current} (Target: ${target})")
        
        return alerts
    
    def generate_weekly_report(self):
        """Generate a weekly price monitoring report."""
        self.storage.save_report(f"weekly_report_{datetime.now().strftime('%Y%m%d')}.txt")

# Usage
monitor = PriceMonitor()
monitor.add_monitored_product("Electronics", "Gaming Laptop", 1500.00, target_price=1200.00)
alerts = monitor.check_price_alerts()
```

This module provides a robust foundation for any price tracking and monitoring application!