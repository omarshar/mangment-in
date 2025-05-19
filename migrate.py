"""
Data migration script for the inventory system.
"""
import os
import json
import argparse
from flask import Flask
from src.utils.migration import migrate_from_json, extract_localstorage_from_html
from src.utils.db import init_db

def create_app():
    """Create a minimal Flask app for migration."""
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'instance', 'inventory.db')
    
    # Ensure instance directory exists
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    
    return app

def migrate_from_file(file_path):
    """Migrate data from a JSON or HTML file."""
    app = create_app()
    
    with app.app_context():
        # Initialize database
        init_db()
        
        # Check file type
        if file_path.endswith('.json'):
            # Read JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = f.read()
            
            # Migrate data
            result = migrate_from_json(json_data)
        elif file_path.endswith('.html'):
            # Read HTML file
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Extract localStorage data
            data = extract_localstorage_from_html(html_content)
            
            # Migrate data
            result = migrate_from_json(data)
        else:
            return {"success": False, "error": "Unsupported file type. Use .json or .html"}
        
        return result

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Migrate data from localStorage to database')
    parser.add_argument('file', help='Path to JSON or HTML file containing localStorage data')
    args = parser.parse_args()
    
    result = migrate_from_file(args.file)
    
    if result['success']:
        print("Migration completed successfully!")
        print(f"Products: {result['products']}")
        print(f"Branches: {result['branches']}")
        print(f"Inventory: {result['inventory']}")
        print(f"Waste: {result['waste']}")
        print(f"Purchases: {result['purchases']}")
        print(f"Invoices: {result['invoices']}")
        
        if result['errors']:
            print("\nWarnings/Errors:")
            for error in result['errors']:
                print(f"- {error}")
    else:
        print("Migration failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        
        if result.get('errors'):
            print("\nErrors:")
            for error in result['errors']:
                print(f"- {error}")

if __name__ == '__main__':
    main()
