#!/usr/bin/env python3
"""
Integration script showing how to use PriceStorage with Amazon web scraping.
This demonstrates practical usage for price monitoring and tracking.
"""

import csv
from datetime import datetime
from price_storage import PriceStorage

class AmazonPriceTracker:
    """
    A class that integrates with Amazon web scraping for price tracking.
    """
    
    def __init__(self, storage_file="amazon_prices.txt"):
        self.storage = PriceStorage(storage_file)
        self.category_keywords = {
            "Electronics": ["phone", "laptop", "computer", "tablet", "headphones", "speaker"],
            "Home & Garden": ["vacuum", "cleaner", "pot", "kitchen", "garden", "tool"],
            "Sports & Outdoors": ["bike", "fitness", "sports", "outdoor", "exercise"],
            "Books": ["book", "novel", "guide", "manual"],
            "Clothing": ["shirt", "shoes", "dress", "pants", "jacket"],
            "Health & Beauty": ["vitamins", "skincare", "makeup", "health", "beauty"],
            "Toys & Games": ["toy", "game", "puzzle", "kids", "children"]
        }
    
    def categorize_product(self, product_title):
        """
        Automatically categorize a product based on its title.
        
        Args:
            product_title: The product title/name
            
        Returns:
            str: Category name
        """
        title_lower = product_title.lower()
        
        for category, keywords in self.category_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return "Other"  # Default category
    
    def process_scraped_data(self, csv_file, title_col="Title", price_col="Price", date_col="Date"):
        """
        Process scraped Amazon data and add to price storage.
        
        Args:
            csv_file: Path to CSV file with scraped data
            title_col: Column name for product title
            price_col: Column name for price
            date_col: Column name for date
        """
        processed_count = 0
        error_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                # Try different delimiters
                sample = file.read(1024)
                file.seek(0)
                
                delimiter = ';' if ';' in sample else ','
                reader = csv.DictReader(file, delimiter=delimiter)
                
                for row in reader:
                    try:
                        title = row.get(title_col, '').strip()
                        price_str = row.get(price_col, '0').strip()
                        date = row.get(date_col, datetime.now().strftime("%Y-%m-%d"))
                        
                        # Clean price string (remove currency symbols, etc.)
                        price_str = price_str.replace('$', '').replace(',', '').strip()
                        price = float(price_str)
                        
                        if title and price > 0:
                            category = self.categorize_product(title)
                            
                            # Add additional info
                            additional_info = {
                                "source": "Amazon",
                                "scraped_date": datetime.now().strftime("%Y-%m-%d"),
                                "original_category": "Auto-categorized"
                            }
                            
                            self.storage.add_product(category, title, price, date, additional_info)
                            processed_count += 1
                        
                    except (ValueError, TypeError) as e:
                        error_count += 1
                        print(f"Error processing row: {e}")
                        continue
        
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found")
            return
        
        print(f"Processing complete:")
        print(f"  ✓ Successfully processed: {processed_count} products")
        if error_count > 0:
            print(f"  ⚠ Errors encountered: {error_count} rows")
    
    def add_price_alert(self, category, product_name, target_price):
        """
        Add a price alert for a specific product.
        
        Args:
            category: Product category
            product_name: Product name
            target_price: Price to alert when reached
        """
        product_info = self.storage.get_product_info(category, product_name)
        if product_info:
            product_info['additional_info']['price_alert'] = target_price
            self.storage.save_data()
            print(f"✓ Price alert set for {product_name}: ${target_price}")
        else:
            print(f"⚠ Product not found: {product_name}")
    
    def check_price_alerts(self):
        """
        Check all products for price alerts and return triggered alerts.
        
        Returns:
            List of alert messages
        """
        alerts = []
        
        for category in self.storage.get_all_categories():
            products = self.storage.get_category_products(category)
            
            for product_name, info in products.items():
                alert_price = info['additional_info'].get('price_alert')
                current_price = info['current_price']
                
                if alert_price and current_price <= alert_price:
                    alerts.append({
                        'product': product_name,
                        'category': category,
                        'current_price': current_price,
                        'target_price': alert_price,
                        'savings': alert_price - current_price
                    })
        
        return alerts
    
    def get_price_trends(self, category=None):
        """
        Analyze price trends for products.
        
        Args:
            category: Optional category to filter by
            
        Returns:
            Dictionary with trend analysis
        """
        trends = {
            'price_drops': [],
            'price_increases': [],
            'stable_prices': []
        }
        
        categories = [category] if category else self.storage.get_all_categories()
        
        for cat in categories:
            products = self.storage.get_category_products(cat)
            
            for product_name, info in products.items():
                if info['price_history']:
                    # Get the last price change
                    last_price = info['price_history'][-1]['price']
                    current_price = info['current_price']
                    
                    change = current_price - last_price
                    change_percent = (change / last_price) * 100
                    
                    trend_info = {
                        'product': product_name,
                        'category': cat,
                        'old_price': last_price,
                        'new_price': current_price,
                        'change': change,
                        'change_percent': change_percent
                    }
                    
                    if change < -0.01:  # Price dropped
                        trends['price_drops'].append(trend_info)
                    elif change > 0.01:  # Price increased
                        trends['price_increases'].append(trend_info)
                    else:  # Stable
                        trends['stable_prices'].append(trend_info)
        
        return trends
    
    def generate_daily_report(self):
        """Generate a daily price monitoring report."""
        report_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"daily_price_report_{report_date}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"AMAZON PRICE TRACKING REPORT - {report_date}\n")
            f.write("=" * 60 + "\n\n")
            
            # Price alerts
            alerts = self.check_price_alerts()
            if alerts:
                f.write("🚨 PRICE ALERTS TRIGGERED:\n")
                f.write("-" * 30 + "\n")
                for alert in alerts:
                    f.write(f"• {alert['product']}\n")
                    f.write(f"  Current: ${alert['current_price']:.2f} | ")
                    f.write(f"Target: ${alert['target_price']:.2f} | ")
                    f.write(f"Savings: ${alert['savings']:.2f}\n\n")
            else:
                f.write("No price alerts triggered today.\n\n")
            
            # Price trends
            trends = self.get_price_trends()
            
            if trends['price_drops']:
                f.write("📉 PRICE DROPS:\n")
                f.write("-" * 15 + "\n")
                for drop in trends['price_drops']:
                    f.write(f"• {drop['product']}\n")
                    f.write(f"  ${drop['old_price']:.2f} → ${drop['new_price']:.2f} ")
                    f.write(f"({drop['change_percent']:.1f}%)\n\n")
            
            if trends['price_increases']:
                f.write("📈 PRICE INCREASES:\n")
                f.write("-" * 20 + "\n")
                for increase in trends['price_increases']:
                    f.write(f"• {increase['product']}\n")
                    f.write(f"  ${increase['old_price']:.2f} → ${increase['new_price']:.2f} ")
                    f.write(f"({increase['change_percent']:.1f}%)\n\n")
            
            # Summary statistics
            f.write("📊 SUMMARY:\n")
            f.write("-" * 10 + "\n")
            total_products = sum(len(self.storage.get_category_products(cat)) 
                               for cat in self.storage.get_all_categories())
            f.write(f"Total products tracked: {total_products}\n")
            f.write(f"Categories: {len(self.storage.get_all_categories())}\n")
            f.write(f"Price drops today: {len(trends['price_drops'])}\n")
            f.write(f"Price increases today: {len(trends['price_increases'])}\n")
            f.write(f"Active price alerts: {len(alerts)}\n")
        
        print(f"✓ Daily report saved: {filename}")
        return filename

def main():
    """Demonstration of the Amazon price tracker."""
    print("=" * 60)
    print("AMAZON PRICE TRACKER DEMONSTRATION")
    print("=" * 60)
    
    # Create tracker instance
    tracker = AmazonPriceTracker("amazon_demo_prices.txt")
    
    # Process existing Amazon data
    print("\n1. Processing existing Amazon scraping data...")
    tracker.process_scraped_data("Result Amazon Web Scrapping.csv")
    
    # Add some sample price alerts
    print("\n2. Setting up price alerts...")
    # First, let's see what products we have
    categories = tracker.storage.get_all_categories()
    for category in categories:
        products = tracker.storage.get_category_products(category)
        for product_name, info in products.items():
            # Set alert for 10% below current price
            alert_price = info['current_price'] * 0.9
            tracker.add_price_alert(category, product_name, alert_price)
            break  # Just set one alert as example
    
    # Check for alerts
    print("\n3. Checking price alerts...")
    alerts = tracker.check_price_alerts()
    if alerts:
        print("Active alerts found:")
        for alert in alerts:
            print(f"  • {alert['product']}: ${alert['current_price']:.2f} "
                  f"(Target: ${alert['target_price']:.2f})")
    else:
        print("No active alerts at this time.")
    
    # Analyze trends
    print("\n4. Analyzing price trends...")
    trends = tracker.get_price_trends()
    print(f"Price drops: {len(trends['price_drops'])}")
    print(f"Price increases: {len(trends['price_increases'])}")
    print(f"Stable prices: {len(trends['stable_prices'])}")
    
    # Generate report
    print("\n5. Generating daily report...")
    report_file = tracker.generate_daily_report()
    
    # Show summary
    print("\n6. Summary:")
    total_products = sum(len(tracker.storage.get_category_products(cat)) 
                        for cat in tracker.storage.get_all_categories())
    print(f"  Total products tracked: {total_products}")
    print(f"  Categories: {', '.join(tracker.storage.get_all_categories())}")
    
    print(f"\nFiles created:")
    print(f"  • amazon_demo_prices.txt (price data)")
    print(f"  • {report_file} (daily report)")

if __name__ == "__main__":
    main()