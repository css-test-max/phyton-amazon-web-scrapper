import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import csv

class PriceStorage:
    """
    A module for storing and managing product prices organized by categories in text files.
    
    Features:
    - Store prices by product category
    - Add/update product prices
    - Retrieve prices by category or product
    - Export/import data in multiple formats
    - Price history tracking
    """
    
    def __init__(self, storage_file: str = "prices_by_category.txt", 
                 backup_dir: str = "price_backups"):
        """
        Initialize the PriceStorage module.
        
        Args:
            storage_file: Main file to store price data
            backup_dir: Directory for backup files
        """
        self.storage_file = storage_file
        self.backup_dir = backup_dir
        self.data = {}
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Load existing data
        self.load_data()
    
    def load_data(self) -> None:
        """Load existing price data from the storage file."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        self.data = json.loads(content)
                    else:
                        self.data = {}
            else:
                self.data = {}
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Warning: Could not load {self.storage_file}. Starting with empty data.")
            self.data = {}
    
    def save_data(self, create_backup: bool = True) -> None:
        """
        Save current price data to the storage file.
        
        Args:
            create_backup: Whether to create a backup before saving
        """
        if create_backup:
            self.create_backup()
        
        with open(self.storage_file, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)
    
    def create_backup(self) -> None:
        """Create a timestamped backup of current data."""
        if os.path.exists(self.storage_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"prices_backup_{timestamp}.txt")
            
            with open(self.storage_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
    
    def add_product(self, category: str, product_name: str, price: float, 
                   date: str = None, additional_info: Dict = None) -> None:
        """
        Add a new product or update existing product price.
        
        Args:
            category: Product category (e.g., "Electronics", "Home & Garden")
            product_name: Name of the product
            price: Product price
            date: Date of price (defaults to current date)
            additional_info: Additional product information (brand, description, etc.)
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if category not in self.data:
            self.data[category] = {}
        
        if product_name not in self.data[category]:
            self.data[category][product_name] = {
                "current_price": price,
                "price_history": [],
                "first_added": date,
                "last_updated": date,
                "additional_info": additional_info or {}
            }
        
        # Add to price history if price changed
        current_data = self.data[category][product_name]
        if current_data["current_price"] != price:
            current_data["price_history"].append({
                "price": current_data["current_price"],
                "date": current_data["last_updated"]
            })
            current_data["current_price"] = price
        
        current_data["last_updated"] = date
        if additional_info:
            current_data["additional_info"].update(additional_info)
        
        self.save_data()
    
    def get_category_products(self, category: str) -> Dict:
        """
        Get all products in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Dictionary of products in the category
        """
        return self.data.get(category, {})
    
    def get_product_info(self, category: str, product_name: str) -> Optional[Dict]:
        """
        Get information about a specific product.
        
        Args:
            category: Product category
            product_name: Product name
            
        Returns:
            Product information dictionary or None if not found
        """
        return self.data.get(category, {}).get(product_name)
    
    def get_all_categories(self) -> List[str]:
        """Get list of all categories."""
        return list(self.data.keys())
    
    def search_products(self, search_term: str) -> List[Tuple[str, str, Dict]]:
        """
        Search for products by name across all categories.
        
        Args:
            search_term: Term to search for in product names
            
        Returns:
            List of tuples: (category, product_name, product_info)
        """
        results = []
        search_term_lower = search_term.lower()
        
        for category, products in self.data.items():
            for product_name, product_info in products.items():
                if search_term_lower in product_name.lower():
                    results.append((category, product_name, product_info))
        
        return results
    
    def get_price_range_products(self, min_price: float = None, 
                                max_price: float = None) -> List[Tuple[str, str, Dict]]:
        """
        Get products within a specific price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            
        Returns:
            List of tuples: (category, product_name, product_info)
        """
        results = []
        
        for category, products in self.data.items():
            for product_name, product_info in products.items():
                price = product_info["current_price"]
                
                if min_price is not None and price < min_price:
                    continue
                if max_price is not None and price > max_price:
                    continue
                
                results.append((category, product_name, product_info))
        
        return results
    
    def export_to_csv(self, filename: str = "prices_export.csv") -> None:
        """
        Export all price data to CSV format.
        
        Args:
            filename: Output CSV filename
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Category', 'Product', 'Current_Price', 'First_Added', 
                         'Last_Updated', 'Price_History_Count', 'Additional_Info']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for category, products in self.data.items():
                for product_name, product_info in products.items():
                    writer.writerow({
                        'Category': category,
                        'Product': product_name,
                        'Current_Price': product_info['current_price'],
                        'First_Added': product_info['first_added'],
                        'Last_Updated': product_info['last_updated'],
                        'Price_History_Count': len(product_info['price_history']),
                        'Additional_Info': str(product_info['additional_info'])
                    })
    
    def import_from_csv(self, filename: str, category_column: str = 'Category',
                       product_column: str = 'Product', price_column: str = 'Price',
                       date_column: str = 'Date') -> None:
        """
        Import price data from CSV file.
        
        Args:
            filename: CSV file to import
            category_column: Column name for category
            product_column: Column name for product
            price_column: Column name for price
            date_column: Column name for date
        """
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    category = row.get(category_column, 'Unknown')
                    product = row.get(product_column, '')
                    price = float(row.get(price_column, 0))
                    date = row.get(date_column, datetime.now().strftime("%Y-%m-%d"))
                    
                    if product and price > 0:
                        self.add_product(category, product, price, date)
                except (ValueError, TypeError) as e:
                    print(f"Error importing row {row}: {e}")
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive text report of all stored data.
        
        Returns:
            Formatted string report
        """
        report = []
        report.append("=" * 60)
        report.append("PRICE STORAGE REPORT")
        report.append("=" * 60)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Categories: {len(self.data)}")
        
        total_products = sum(len(products) for products in self.data.values())
        report.append(f"Total Products: {total_products}")
        report.append("")
        
        for category, products in self.data.items():
            report.append(f"CATEGORY: {category}")
            report.append("-" * 40)
            report.append(f"Products in category: {len(products)}")
            
            if products:
                prices = [info['current_price'] for info in products.values()]
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                
                report.append(f"Price range: ${min_price:.2f} - ${max_price:.2f}")
                report.append(f"Average price: ${avg_price:.2f}")
            
            report.append("")
            
            for product_name, product_info in products.items():
                report.append(f"  • {product_name}")
                report.append(f"    Current Price: ${product_info['current_price']:.2f}")
                report.append(f"    Last Updated: {product_info['last_updated']}")
                
                if product_info['price_history']:
                    report.append(f"    Price Changes: {len(product_info['price_history'])}")
                
                report.append("")
        
        return "\n".join(report)
    
    def save_report(self, filename: str = "price_report.txt") -> None:
        """
        Save the generated report to a text file.
        
        Args:
            filename: Output filename for the report
        """
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.generate_report())
    
    def remove_product(self, category: str, product_name: str) -> bool:
        """
        Remove a product from the storage.
        
        Args:
            category: Product category
            product_name: Product name
            
        Returns:
            True if product was removed, False if not found
        """
        if category in self.data and product_name in self.data[category]:
            del self.data[category][product_name]
            
            # Remove category if empty
            if not self.data[category]:
                del self.data[category]
            
            self.save_data()
            return True
        return False
    
    def clear_category(self, category: str) -> bool:
        """
        Remove all products from a category.
        
        Args:
            category: Category to clear
            
        Returns:
            True if category was cleared, False if not found
        """
        if category in self.data:
            del self.data[category]
            self.save_data()
            return True
        return False


# Convenience functions for quick usage
def create_price_storage(storage_file: str = "prices_by_category.txt") -> PriceStorage:
    """Create a new PriceStorage instance."""
    return PriceStorage(storage_file)

def quick_add_product(category: str, product_name: str, price: float, 
                     storage_file: str = "prices_by_category.txt") -> None:
    """Quickly add a product without managing PriceStorage instance."""
    storage = PriceStorage(storage_file)
    storage.add_product(category, product_name, price)

def quick_search(search_term: str, storage_file: str = "prices_by_category.txt") -> List:
    """Quickly search for products without managing PriceStorage instance."""
    storage = PriceStorage(storage_file)
    return storage.search_products(search_term)