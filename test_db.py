from db_operations import MoneyTransferDB
from database import DatabaseManager

def test_database_operations():
    """Test all database operations."""
    
    # Initialize database
    print("=" * 60)
    print("TESTING DATABASE OPERATIONS")
    print("=" * 60)
    
    db = MoneyTransferDB()
    
    # Seed data
    print("\n1. Seeding database with sample data...")
    db.db_manager.seed_sample_data()
    print("✅ Data seeded successfully!")
    
    # Test get sender account
    print("\n2. Testing get_sender_account...")
    sender = db.get_sender_account('ACC1001')
    if sender:
        print(f"✅ Found: {sender['account_number']}, Balance: {sender['balance']}")
    
    # Test authentication
    print("\n3. Testing authentication...")
    auth_result = db.verify_authentication('ACC1001', 'pass123')
    print(f"✅ Authentication: {'Success' if auth_result else 'Failed'}")
    
    # Test get receiver account
    print("\n4. Testing get_receiver_account...")
    receiver = db.get_receiver_account('ACC2001')
    if receiver:
        print(f"✅ Found: {receiver['account_number']}, Daily Limit: {receiver['daily_limit']}")
    
    # Test check balance
    print("\n5. Testing check_sufficient_balance...")
    has_balance = db.check_sufficient_balance('ACC1001', 1000)
    print(f"✅ Has sufficient balance for 1000: {has_balance}")
    
    # Test check daily limit
    print("\n6. Testing check_receiver_daily_limit...")
    can_receive, remaining = db.check_receiver_daily_limit('ACC2001', 5000)
    print(f"✅ Can receive 5000: {can_receive}, Remaining limit: {remaining}")
    
    # Test successful transaction
    print("\n7. Testing successful transaction...")
    try:
        result = db.process_transfer(
            'ACC1001',
            'ACC2001',
            1000.0,
            'INR',
            'vijay@example.com',
            'Test transaction'
        )
        print(f"✅ Transaction successful! ID: {result['transaction_id']}")
        print(f"   Sender balance: {result['sender_balance_before']} → {result['sender_balance_after']}")
        print(f"   Receiver daily: {result['receiver_daily_before']} → {result['receiver_daily_after']}")
    except Exception as e:
        print(f"❌ Transaction failed: {e}")
    
    # Test failed transaction (insufficient balance)
    print("\n8. Testing failed transaction (insufficient balance)...")
    try:
        result = db.process_transfer(
            'ACC1001',
            'ACC2001',
            10000.0,  # More than balance
            'INR',
            'vijay@example.com',
            'Test failed transaction'
        )
        print(f"❌ Should have failed!")
    except ValueError as e:
        print(f"✅ Transaction correctly rejected: {e}")
    
    # Test transaction history
    print("\n9. Testing get_transaction_history...")
    history = db.get_transaction_history('ACC1001', 'sender', 5)
    print(f"✅ Found {len(history)} transaction(s)")
    for txn in history:
        print(f"   - ID: {txn['transaction_id']}, Amount: {txn['amount']}, Status: {txn['status']}")
    
    # Test daily summary
    print("\n10. Testing get_daily_transaction_summary...")
    summary = db.get_daily_transaction_summary()
    print(f"✅ Today's summary: {summary['total_transactions']} transactions, Total: {summary['total_amount']}")
    
    # Test get all accounts
    print("\n11. Testing get_all_sender_accounts...")
    all_senders = db.get_all_sender_accounts()
    print(f"✅ Found {len(all_senders)} sender account(s)")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    test_database_operations()
