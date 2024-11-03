import csv
import random
import os
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# Get the directory where the script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

# Helper data for generating realistic orders
PRODUCT_CATEGORIES = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones'],
    'Fashion': ['T-shirt', 'Jeans', 'Sneakers', 'Dress'],
    'Home': ['Coffee Maker', 'Bedding Set', 'Vacuum Cleaner'],
    'Books': ['Fiction Paperback', 'Technical Manual', 'Cookbook']
}

WAREHOUSES = {
    'WEST': ['CA', 'OR', 'WA', 'NV'],
    'EAST': ['NY', 'MA', 'FL', 'GA'],
    'CENTRAL': ['TX', 'IL', 'OH', 'MI']
}

ORDER_TYPES = ['B2B', 'B2C']

def clear_directory(directory_path):
    """Remove all files from the specified directory"""
    if directory_path.exists():
        shutil.rmtree(directory_path)
    directory_path.mkdir(exist_ok=True)

def format_warehouse_distribution(warehouse_counts, total_orders):
    """Format the warehouse distribution string"""
    parts = []
    for warehouse, count in warehouse_counts.items():
        parts.append(f"  * {count} {'is' if count == 1 else 'are'} for the {warehouse} warehouse region")
    
    if len(parts) > 1:
        return f"\n{'\n'.join(parts)}"
    return parts[0] if parts else ""

def generate_individual_orders(num_orders):
    """Generate individual CSV files for each order"""
    # Create output directory and clear existing files
    # Use script directory as base path
    output_dir = SCRIPT_DIR / 'sample_orders'
    clear_directory(output_dir)
    
    print(f"Output directory: {output_dir}")  # Print the full path for verification
    
    # Headers for our CSV files
    headers = [
        'order_id', 
        'timestamp',
        'order_type',
        'customer_id',
        'shipping_state',
        'product_name',
        'product_category',
        'quantity',
        'unit_price',
        'total_amount',
        'assigned_warehouse',
        'shipping_priority'
    ]
    
    generated_files = []
    warehouse_distribution = Counter()
    
    # Generate individual order files
    for i in range(num_orders):
        # Select random category and product
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        product = random.choice(PRODUCT_CATEGORIES[category])
        
        # Select random warehouse region and state
        warehouse_region = random.choice(list(WAREHOUSES.keys()))
        shipping_state = random.choice(WAREHOUSES[warehouse_region])
        
        # Track warehouse distribution
        warehouse_distribution[warehouse_region] += 1
        
        # Generate order timestamp
        order_timestamp = datetime.now() - timedelta(hours=random.randint(0, 72))
        
        # Generate order ID using timestamp
        order_id = f'ORD-{order_timestamp.strftime("%Y%m")}-{i+1:04d}'
        
        # Generate order data
        order = {
            'order_id': order_id,
            'timestamp': order_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'order_type': random.choice(ORDER_TYPES),
            'customer_id': f'CUST-{random.randint(1000, 9999)}',
            'shipping_state': shipping_state,
            'product_name': product,
            'product_category': category,
            'quantity': random.randint(1, 10),
            'unit_price': round(random.uniform(10.0, 1000.0), 2),
            'total_amount': 0,  # Will be calculated
            'assigned_warehouse': warehouse_region,
            'shipping_priority': random.choice(['Standard', 'Express', 'Next Day'])
        }
        
        # Calculate total amount
        order['total_amount'] = round(order['quantity'] * order['unit_price'], 2)
        
        # Create filename using order ID and timestamp
        filename = f"{order_id}_{order_timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = output_dir / filename
        
        # Write individual order to CSV file
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerow(order)
            
        generated_files.append(filename)
    
    # Print summary of generated files
    print(f"\nCleared existing files and generated {num_orders} new order files in '{output_dir}' directory")
    print(f"\n{num_orders} orders were created. {format_warehouse_distribution(warehouse_distribution, num_orders)}")
    
    print("\nSample of generated files:")
    for filename in generated_files[:3]:  # Show first 3 files
        print(f"\nContents of {filename}:")
        with open(output_dir / filename, 'r') as file:
            print(file.read().strip())

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate individual CSV files for sample orders'
    )
    
    parser.add_argument(
        '-n', '--number',
        type=int,
        default=10,
        help='Number of order files to generate (default: 10)'
    )
    
    args = parser.parse_args()
    
    if args.number < 1:
        parser.error("Number of orders must be at least 1")
    
    generate_individual_orders(args.number)

if __name__ == "__main__":
    main()