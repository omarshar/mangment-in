"""
Update validation script to fix unpacking errors and simplify tests.
"""
import os
import sys
import time
import random
import sqlite3
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, g

def create_app():
    """Create a minimal Flask app for validation."""
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'instance', 'inventory.db')
    
    # Ensure instance directory exists
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    
    return app

def initialize_database(app):
    """Initialize the database with schema."""
    with app.app_context():
        from src.utils.db import init_db
        init_db()
        print("Database initialized with schema.")

def test_product_operations():
    """Test CRUD operations for products."""
    from src.models.product import (
        create_product, get_product_by_id, update_product, 
        delete_product, get_all_products, search_products
    )
    
    print("Testing product operations...")
    
    # Create a test product
    product_id = create_product(
        name="Test Product",
        category="Test Category",
        price=100.0,
        cost=50.0,
        measurement_unit="حبة",
        barcode="TEST123456"
    )
    
    if not product_id:
        print("❌ Failed to create product")
        return False
    
    print(f"✅ Created product with ID: {product_id}")
    
    # Get the product
    product = get_product_by_id(product_id)
    if not product or product['name'] != "Test Product":
        print("❌ Failed to get product")
        return False
    
    print(f"✅ Retrieved product: {product['name']}")
    
    # Update the product
    success = update_product(
        product_id=product_id,
        name="Updated Test Product",
        price=120.0
    )
    
    if not success:
        print("❌ Failed to update product")
        return False
    
    # Verify update
    updated_product = get_product_by_id(product_id)
    if not updated_product or updated_product['name'] != "Updated Test Product" or updated_product['price'] != 120.0:
        print("❌ Failed to verify product update")
        return False
    
    print(f"✅ Updated product: {updated_product['name']}, Price: {updated_product['price']}")
    
    # Test search
    search_results = search_products("Updated")
    if not search_results or search_results[0]['id'] != product_id:
        print("❌ Failed to search products")
        return False
    
    print(f"✅ Search found {len(search_results)} products")
    
    # Delete the product
    success = delete_product(product_id)
    if not success:
        print("❌ Failed to delete product")
        return False
    
    # Verify deletion
    deleted_product = get_product_by_id(product_id)
    if deleted_product:
        print("❌ Product was not deleted")
        return False
    
    print("✅ Product deleted successfully")
    
    return True

def test_branch_operations():
    """Test CRUD operations for branches."""
    from src.models.branch import (
        create_branch, get_branch_by_id, update_branch, 
        delete_branch, get_all_branches
    )
    
    print("\nTesting branch operations...")
    
    # Create a test branch
    branch_id = create_branch(
        name="Test Branch",
        location="Test Location",
        manager="Test Manager",
        phone="123456789"
    )
    
    if not branch_id:
        print("❌ Failed to create branch")
        return False
    
    print(f"✅ Created branch with ID: {branch_id}")
    
    # Get the branch
    branch = get_branch_by_id(branch_id)
    if not branch or branch['name'] != "Test Branch":
        print("❌ Failed to get branch")
        return False
    
    print(f"✅ Retrieved branch: {branch['name']}")
    
    # Update the branch
    success = update_branch(
        branch_id=branch_id,
        name="Updated Test Branch",
        manager="Updated Manager"
    )
    
    if not success:
        print("❌ Failed to update branch")
        return False
    
    # Verify update
    updated_branch = get_branch_by_id(branch_id)
    if not updated_branch or updated_branch['name'] != "Updated Test Branch":
        print("❌ Failed to verify branch update")
        return False
    
    print(f"✅ Updated branch: {updated_branch['name']}")
    
    # Delete the branch
    success = delete_branch(branch_id)
    if not success:
        print("❌ Failed to delete branch")
        return False
    
    # Verify deletion
    deleted_branch = get_branch_by_id(branch_id)
    if deleted_branch:
        print("❌ Branch was not deleted")
        return False
    
    print("✅ Branch deleted successfully")
    
    return True

def test_inventory_operations():
    """Test CRUD operations for inventory."""
    from src.models.product import create_product
    from src.models.branch import create_branch
    from src.models.inventory import (
        create_or_update_inventory, get_inventory_by_id,
        delete_inventory, get_inventory_by_product_branch_month,
        get_inventory_with_details
    )
    
    print("\nTesting inventory operations...")
    
    # Create test product and branch
    product_id = create_product(
        name="Inventory Test Product",
        category="Test Category",
        price=100.0,
        cost=50.0,
        measurement_unit="حبة"
    )
    
    branch_id = create_branch(
        name="Inventory Test Branch",
        location="Test Location"
    )
    
    if not product_id or not branch_id:
        print("❌ Failed to create test product or branch")
        return False
    
    # Get current month and year
    now = datetime.now()
    month = now.month
    year = now.year
    
    # Create inventory record
    inventory_id = create_or_update_inventory(
        product_id=product_id,
        branch_id=branch_id,
        quantity=100,
        month=month,
        year=year
    )
    
    if not inventory_id:
        print("❌ Failed to create inventory record")
        return False
    
    print(f"✅ Created inventory record with ID: {inventory_id}")
    
    # Get the inventory record
    inventory = get_inventory_by_id(inventory_id)
    if not inventory or inventory['quantity'] != 100:
        print("❌ Failed to get inventory record")
        return False
    
    print(f"✅ Retrieved inventory record with quantity: {inventory['quantity']}")
    
    # Update inventory record
    updated_id = create_or_update_inventory(
        product_id=product_id,
        branch_id=branch_id,
        quantity=150,
        month=month,
        year=year
    )
    
    if not updated_id or updated_id != inventory_id:
        print("❌ Failed to update inventory record")
        return False
    
    # Verify update
    updated_inventory = get_inventory_by_id(inventory_id)
    if not updated_inventory or updated_inventory['quantity'] != 150:
        print("❌ Failed to verify inventory update")
        return False
    
    print(f"✅ Updated inventory record with quantity: {updated_inventory['quantity']}")
    
    # Get inventory with details
    inventory_details = get_inventory_with_details(inventory_id)
    if not inventory_details or 'product_name' not in inventory_details:
        print("❌ Failed to get inventory details")
        return False
    
    print(f"✅ Retrieved inventory details with product: {inventory_details['product_name']}")
    
    # Delete the inventory record
    success = delete_inventory(inventory_id)
    if not success:
        print("❌ Failed to delete inventory record")
        return False
    
    # Verify deletion
    deleted_inventory = get_inventory_by_id(inventory_id)
    if deleted_inventory:
        print("❌ Inventory record was not deleted")
        return False
    
    print("✅ Inventory record deleted successfully")
    
    # Clean up
    from src.models.product import delete_product
    from src.models.branch import delete_branch
    
    delete_product(product_id)
    delete_branch(branch_id)
    
    return True

def test_load_performance():
    """Test system performance under load."""
    from src.models.product import create_product, get_all_products, delete_product
    
    print("\nTesting load performance...")
    
    # Number of products to create for load test
    num_products = 100
    
    # Create multiple products
    start_time = time.time()
    product_ids = []
    
    for i in range(num_products):
        product_id = create_product(
            name=f"Load Test Product {i}",
            category="Load Test",
            price=random.uniform(10, 1000),
            cost=random.uniform(5, 500),
            measurement_unit="حبة",
            barcode=f"LOAD{i:06d}"
        )
        if product_id:
            product_ids.append(product_id)
    
    creation_time = time.time() - start_time
    print(f"✅ Created {len(product_ids)} products in {creation_time:.2f} seconds")
    
    # Test retrieval performance
    start_time = time.time()
    products = get_all_products()
    retrieval_time = time.time() - start_time
    
    print(f"✅ Retrieved {len(products)} products in {retrieval_time:.2f} seconds")
    
    # Clean up
    start_time = time.time()
    for product_id in product_ids:
        delete_product(product_id)
    
    cleanup_time = time.time() - start_time
    print(f"✅ Deleted {len(product_ids)} products in {cleanup_time:.2f} seconds")
    
    # Performance is acceptable if operations complete in reasonable time
    return creation_time < 5 and retrieval_time < 2 and cleanup_time < 5

def run_validation_tests():
    """Run all validation tests."""
    app = create_app()
    
    # Initialize the database first
    initialize_database(app)
    
    with app.app_context():
        print("=== INVENTORY SYSTEM VALIDATION TESTS ===")
        print("Starting validation at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        tests = [
            ("Product Operations", test_product_operations),
            ("Branch Operations", test_branch_operations),
            ("Inventory Operations", test_inventory_operations),
            ("Load Performance", test_load_performance)
        ]
        
        results = {}
        all_passed = True
        
        for name, test_func in tests:
            print(f"\n=== Testing {name} ===")
            try:
                result = test_func()
                results[name] = result
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"❌ Test failed with error: {str(e)}")
                results[name] = False
                all_passed = False
        
        print("\n=== VALIDATION TEST RESULTS ===")
        for name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{name}: {status}")
        
        if all_passed:
            print("\n✅ ALL TESTS PASSED! The system is ready for deployment.")
        else:
            print("\n❌ SOME TESTS FAILED! Please fix the issues before deployment.")
        
        return all_passed

if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1)
