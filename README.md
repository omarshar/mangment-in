# Inventory System Backend - Final Delivery

## Overview
This package contains the upgraded inventory management system with the following key features:

1. **Centralized Data Storage**
   - All data stored in SQLite database
   - Proper data relationships and cascading updates
   - Consistent data access through backend models

2. **Simple Login System**
   - Secure user authentication
   - User-friendly login and registration interfaces
   - Session management for secure access

3. **Automatic Backup Feature**
   - Scheduled daily backups
   - Manual backup and restore functionality
   - 30-day backup retention policy

4. **Data Migration Utilities**
   - Tools to import data from old localStorage-based system
   - Data export functionality for backup purposes

## Installation and Setup

1. Clone the repository to your server
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```
   flask init-db
   ```
4. Run the application:
   ```
   flask run --host=0.0.0.0
   ```

## Usage Instructions

### Login System
- Access the system at http://your-server-address:5000/
- Register a new account or log in with existing credentials

### Data Migration
- Use the migration page to import data from your old system
- Upload JSON or HTML files containing localStorage data

### Backup Management
- Access backup management at http://your-server-address:5000/backup/
- Create manual backups or restore from previous backups
- Automatic backups run daily at 3:00 AM

## System Architecture
The system follows a modular architecture with:
- Database models for each entity (products, branches, inventory, etc.)
- Authentication and authorization middleware
- Backup and migration utilities
- Web interface for all operations

## Contact
For support or questions, please contact the system administrator.
