from database import DatabaseManager

def initialize_database():
    """Initialize database and seed with sample data."""
    print("Initializing Money Transfer Database...")
    
    db_manager = DatabaseManager()
    db_manager.seed_sample_data()
    
    print("✅ Database initialized successfully!")
    print("📊 Sample data loaded:")
    print("   - 2 Sender Accounts (ACC1001, ACC1002)")
    print("   - 2 Receiver Accounts (ACC2001, ACC2002)")
    print("\nYou can now run main_db.py to start the application.")

if __name__ == "__main__":
    initialize_database()
