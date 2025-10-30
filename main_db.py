from db_operations import MoneyTransferDB
from datetime import datetime
from typing import Optional, Dict, Any

db = MoneyTransferDB()

def get_valid_account() -> str:
    """Prompt for account number until valid."""
    while True:
        account_number = input("Enter Account Number: ").strip()
        account = db.get_sender_account(account_number)
        if account:
            print("✅ Account found!")
            return account_number
        else:
            print("❌ Sender account not found or inactive. Please try again.\n")


def get_valid_authentication(account_number: str) -> Optional[str]:
    """Prompt for authentication credential until valid."""
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        authentication_credential = input("Enter Authentication Credential: ").strip()
        if db.verify_authentication(account_number, authentication_credential):
            print("✅ Authentication successful!")
            return authentication_credential
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"❌ Invalid authentication credentials. {remaining} attempt(s) remaining.\n")
            else:
                print("❌ Maximum authentication attempts reached. Transaction cancelled.")
                return None
    return None


def get_valid_receiver_account() -> str:
    """Prompt for receiver account until valid."""
    while True:
        receiver_account_number = input("Enter Receiver Account Number: ").strip()
        receiver = db.get_receiver_account(receiver_account_number)
        if receiver:
            print("✅ Receiver account found!")
            return receiver_account_number
        else:
            print("❌ Receiver account not found. Please try again.\n")


def get_valid_currency(account_number: str, receiver_account_number: str) -> Optional[str]:
    """Prompt for currency until valid."""
    sender = db.get_sender_account(account_number)
    receiver = db.get_receiver_account(receiver_account_number)
    
    # Handle None cases
    if not sender or not receiver:
        print("❌ Error retrieving account information.")
        return None
    
    sender_currency = sender['currency']
    receiver_currency = receiver['currency']

    print(f"ℹ️  Your account currency: {sender_currency}")
    print(f"ℹ️  Receiver account currency: {receiver_currency}")

    if sender_currency != receiver_currency:
        print(f"❌ Cross-currency transfers not supported. Both accounts must use {sender_currency}.")
        return None

    while True:
        currency = input(f"Enter Currency (ISO 4217 Code, must be {sender_currency}): ").strip()
        if currency.upper() == sender_currency:
            print("✅ Currency validated!")
            return currency.upper()
        else:
            print(f"❌ Currency mismatch. You must enter {sender_currency}. Please try again.\n")


def get_valid_amount(account_number: str) -> float:
    """Prompt for transfer amount until valid."""
    balance = db.get_account_balance(account_number)
    sender = db.get_sender_account(account_number)
    
    # Handle None cases
    if balance is None or sender is None:
        print("❌ Error retrieving account information.")
        return 0.0
    
    currency = sender['currency']

    print(f"ℹ️  Available balance: {balance} {currency}")

    while True:
        transfer_amount = input("Enter Transfer Amount: ").strip()

        try:
            amount = float(transfer_amount)

            if amount <= 0:
                print("❌ Transfer amount must be greater than 0. Please try again.\n")
                continue

            if amount > balance:
                print(f"❌ Insufficient balance. Your balance is {balance} {currency}. Please try again.\n")
                continue

            print(f"✅ Amount validated: {amount} {currency}")
            return amount

        except ValueError:
            print("❌ Invalid amount format. Please enter a numeric value.\n")


def get_valid_contact(account_number: str) -> str:
    """Prompt for contact information until valid."""
    sender = db.get_sender_account(account_number)
    
    # Handle None case
    if sender is None:
        print("❌ Error retrieving account information.")
        return ""
    
    stored_contact = sender['contact_information']

    while True:
        contact_information = input("Enter Contact Information (Phone or Email): ").strip()

        if contact_information == stored_contact:
            print("✅ Contact information verified!")
            return contact_information
        else:
            print(f"❌ Contact information does not match registered record. Please try again.\n")


def get_transaction_reason() -> Optional[str]:
    """Get optional transaction reason."""
    transaction_reason = input("Enter Transaction Reason (optional, press Enter to skip): ").strip()
    if transaction_reason:
        print(f"✅ Reason recorded: {transaction_reason}")
        return transaction_reason
    return None


def check_receiver_daily_limit(receiver_account_number: str, amount: float) -> bool:
    """Check if receiver can receive the given amount within their daily limit."""
    can_receive, remaining_limit = db.check_receiver_daily_limit(receiver_account_number, amount)
    
    receiver = db.get_receiver_account(receiver_account_number)
    
    # Handle None case
    if receiver is None:
        print("❌ Error retrieving receiver information.")
        return False
    
    daily_limit = receiver['daily_limit']
    daily_received = receiver['daily_received']

    print(f"ℹ️  Receiver's Daily Limit: {daily_limit}")
    print(f"ℹ️  Receiver's Already Received Today: {daily_received}")

    if not can_receive:
        print("❌ Receiver has reached or will exceed their daily transfer limit.")
        print(f"Receiver can only receive {remaining_limit} more today.")
        return False
    else:
        print(f"✅ Receiver can receive this amount. Remaining limit after transfer: {remaining_limit - amount}")
        return True


def process_transaction(sender_account: str, receiver_account: str, amount: float, 
                       currency: str, contact_info: str, transaction_reason: Optional[str]) -> bool:
    """Process transaction using database with full ACID support."""
    try:
        result = db.process_transfer(
            sender_account, 
            receiver_account, 
            amount, 
            currency,
            contact_info,
            transaction_reason
        )
        
        print("\n💰 Transaction processed successfully!")
        print(f"Transaction ID: {result['transaction_id']}")
        print(f"Sender's new balance: {result['sender_balance_after']}")
        print(f"Receiver's total received today: {result['receiver_daily_after']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Transaction failed: {str(e)}")
        db.log_failed_transaction(
            sender_account, 
            receiver_account, 
            amount, 
            currency,
            transaction_reason or "",
            str(e)
        )
        return False


def main() -> None:
    print("=== Money Transfer System (Database Version) ===\n")

    # Step 1: Validate account existence
    print("--- Step 1: Account Validation ---")
    account_number = get_valid_account()
    print()

    # Step 2: Validate authentication
    print("--- Step 2: Authentication ---")
    authentication_credential = get_valid_authentication(account_number)
    if authentication_credential is None:
        return
    print()

    # Step 3: Validate receiver existence
    print("--- Step 3: Receiver Account Validation ---")
    receiver_account_number = get_valid_receiver_account()
    print()

    # Step 4: Validate currency
    print("--- Step 4: Currency Validation ---")
    currency = get_valid_currency(account_number, receiver_account_number)
    if currency is None:
        return
    print()

    # Step 5: Validate transfer amount
    print("--- Step 5: Amount Validation ---")
    amount = get_valid_amount(account_number)
    if amount <= 0:
        return
    print()

    # Step 6: Validate receiver daily limit
    print("--- Step 6: Receiver Daily Limit Check ---")
    if not check_receiver_daily_limit(receiver_account_number, amount):
        print("🚫 Transaction blocked due to receiver's daily limit.\n")
        return
    print()

    # Step 7: Validate contact information
    print("--- Step 7: Contact Verification ---")
    contact_information = get_valid_contact(account_number)
    if not contact_information:
        return
    print()

    # Step 8: Transaction reason (optional)
    print("--- Step 8: Transaction Details ---")
    transaction_reason = get_transaction_reason()
    print()

    # Step 9: Process transaction
    success = process_transaction(
        account_number, 
        receiver_account_number, 
        amount, 
        currency,
        contact_information,
        transaction_reason
    )

    if success:
        # Step 10: Final confirmation
        print("\n" + "=" * 50)
        print("✅ TRANSACTION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"\n📋 Transaction Summary:")
        print(f"   From Account: {account_number}")
        print(f"   To Account: {receiver_account_number}")
        print(f"   Amount: {amount} {currency}")
        if transaction_reason:
            print(f"   Reason: {transaction_reason}")
        print(f"   Contact: {contact_information}")


if __name__ == "__main__":
    # Initialize database and seed data
    print("Initializing database...")
    db.db_manager.seed_sample_data()
    print("Database ready!\n")
    
    main()
