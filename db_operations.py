import sqlite3
from datetime import datetime, date
from typing import Optional, Dict, Any, Tuple, List
from database import DatabaseManager

class MoneyTransferDB:
    """Handles all database operations for money transfer system."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_sender_account(self, account_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve sender account details."""
        with self.db_manager.transaction() as conn:
            cursor = conn.execute(
                'SELECT * FROM sender_accounts WHERE account_number = ?',
                (account_number,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def verify_authentication(self, account_number: str, credential: str) -> bool:
        """Verify authentication credential for sender account."""
        with self.db_manager.transaction() as conn:
            cursor = conn.execute(
                'SELECT authentication_credential FROM sender_accounts WHERE account_number = ?',
                (account_number,)
            )
            row = cursor.fetchone()
            if row:
                return row['authentication_credential'] == credential
            return False
    
    def get_receiver_account(self, account_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve receiver account details with daily limit reset if needed."""
        with self.db_manager.transaction() as conn:
            cursor = conn.execute(
                'SELECT * FROM receiver_accounts WHERE account_number = ?',
                (account_number,)
            )
            row = cursor.fetchone()
            if row:
                receiver = dict(row)
                
                # Reset daily_received if it's a new day
                last_reset = datetime.strptime(receiver['last_reset_date'], '%Y-%m-%d').date()
                today = date.today()
                
                if last_reset < today:
                    conn.execute(
                        '''UPDATE receiver_accounts 
                           SET daily_received = 0, 
                               last_reset_date = ?,
                               updated_at = CURRENT_TIMESTAMP
                           WHERE account_number = ?''',
                        (today.isoformat(), account_number)
                    )
                    receiver['daily_received'] = 0.0
                    receiver['last_reset_date'] = today.isoformat()
                
                return receiver
            return None
    
    def check_sufficient_balance(self, account_number: str, amount: float) -> bool:
        """Check if sender has sufficient balance."""
        account = self.get_sender_account(account_number)
        if account:
            return account['balance'] >= amount
        return False
    
    def check_receiver_daily_limit(self, receiver_account_number: str, amount: float) -> Tuple[bool, float]:
        """Check if receiver can receive the amount within daily limit."""
        receiver = self.get_receiver_account(receiver_account_number)
        if receiver:
            remaining_limit = receiver['daily_limit'] - receiver['daily_received']
            return amount <= remaining_limit, remaining_limit
        return False, 0.0
    
    def process_transfer(self, sender_account: str, receiver_account: str, amount: float, 
                        currency: str, contact_info: str, transaction_reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Process money transfer with full ACID transaction support.
        Either all operations succeed or all fail (atomic).
        """
        with self.db_manager.transaction() as conn:
            # Step 1: Lock and get current sender balance (FOR UPDATE equivalent)
            cursor = conn.execute(
                'SELECT balance FROM sender_accounts WHERE account_number = ?',
                (sender_account,)
            )
            sender_row = cursor.fetchone()
            if not sender_row:
                raise ValueError(f"Sender account {sender_account} not found")
            
            sender_balance_before = float(sender_row['balance'])
            
            # Check sufficient balance
            if sender_balance_before < amount:
                raise ValueError(f"Insufficient balance. Available: {sender_balance_before}, Required: {amount}")
            
            # Step 2: Lock and get receiver daily received amount
            cursor = conn.execute(
                'SELECT daily_limit, daily_received FROM receiver_accounts WHERE account_number = ?',
                (receiver_account,)
            )
            receiver_row = cursor.fetchone()
            if not receiver_row:
                raise ValueError(f"Receiver account {receiver_account} not found")
            
            receiver_daily_before = float(receiver_row['daily_received'])
            receiver_daily_limit = float(receiver_row['daily_limit'])
            
            # Check daily limit
            if receiver_daily_before + amount > receiver_daily_limit:
                remaining = receiver_daily_limit - receiver_daily_before
                raise ValueError(f"Receiver daily limit exceeded. Remaining limit: {remaining}")
            
            # Step 3: Update sender balance (Debit)
            sender_balance_after = sender_balance_before - amount
            conn.execute(
                '''UPDATE sender_accounts 
                   SET balance = ?, 
                       updated_at = CURRENT_TIMESTAMP
                   WHERE account_number = ?''',
                (sender_balance_after, sender_account)
            )
            
            # Step 4: Update receiver daily received amount (Credit tracking)
            receiver_daily_after = receiver_daily_before + amount
            conn.execute(
                '''UPDATE receiver_accounts 
                   SET daily_received = ?,
                       updated_at = CURRENT_TIMESTAMP
                   WHERE account_number = ?''',
                (receiver_daily_after, receiver_account)
            )
            
            # Step 5: Log transaction
            cursor = conn.execute(
                '''INSERT INTO transactions 
                   (sender_account, receiver_account, amount, currency, transaction_reason, 
                    status, sender_balance_before, sender_balance_after, 
                    receiver_daily_before, receiver_daily_after)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (sender_account, receiver_account, amount, currency, transaction_reason,
                 'SUCCESS', sender_balance_before, sender_balance_after,
                 receiver_daily_before, receiver_daily_after)
            )
            
            transaction_id = cursor.lastrowid
            
            # Return transaction details
            return {
                'transaction_id': transaction_id,
                'sender_balance_before': sender_balance_before,
                'sender_balance_after': sender_balance_after,
                'receiver_daily_before': receiver_daily_before,
                'receiver_daily_after': receiver_daily_after,
                'status': 'SUCCESS'
            }
    
    def log_failed_transaction(self, sender_account: str, receiver_account: str, amount: float, 
                               currency: str, reason: str, error_message: str) -> None:
        """Log failed transaction attempt."""
        try:
            with self.db_manager.transaction() as conn:
                conn.execute(
                    '''INSERT INTO transactions 
                       (sender_account, receiver_account, amount, currency, 
                        transaction_reason, status, sender_balance_before, 
                        sender_balance_after, receiver_daily_before, receiver_daily_after)
                       VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0)''',
                    (sender_account, receiver_account, amount, currency,
                     f"FAILED: {error_message}", 'FAILED')
                )
        except Exception as e:
            print(f"Error logging failed transaction: {e}")
    
    def get_transaction_history(self, account_number: str, account_type: str = 'sender', limit: int = 10) -> List[Dict[str, Any]]:
        """Get transaction history for an account."""
        with self.db_manager.transaction() as conn:
            if account_type == 'sender':
                query = '''
                    SELECT * FROM transactions 
                    WHERE sender_account = ? 
                    ORDER BY transaction_timestamp DESC 
                    LIMIT ?
                '''
            else:
                query = '''
                    SELECT * FROM transactions 
                    WHERE receiver_account = ? 
                    ORDER BY transaction_timestamp DESC 
                    LIMIT ?
                '''
            
            cursor = conn.execute(query, (account_number, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_account_balance(self, account_number: str) -> Optional[float]:
        """Get current balance for sender account."""
        account = self.get_sender_account(account_number)
        if account:
            return float(account['balance'])
        return None
    
    def get_all_sender_accounts(self) -> List[Dict[str, Any]]:
        """Get all sender accounts (for admin purposes)."""
        with self.db_manager.transaction() as conn:
            cursor = conn.execute('SELECT * FROM sender_accounts ORDER BY account_number')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_all_receiver_accounts(self) -> List[Dict[str, Any]]:
        """Get all receiver accounts (for admin purposes)."""
        with self.db_manager.transaction() as conn:
            cursor = conn.execute('SELECT * FROM receiver_accounts ORDER BY account_number')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_daily_transaction_summary(self, date_str: Optional[str] = None) -> Dict[str, Any]:
        """Get transaction summary for a specific date (default: today)."""
        if date_str is None:
            date_str = date.today().isoformat()
        
        with self.db_manager.transaction() as conn:
            # Total successful transactions
            cursor = conn.execute(
                '''SELECT COUNT(*) as count, SUM(amount) as total
                   FROM transactions 
                   WHERE DATE(transaction_timestamp) = ? AND status = 'SUCCESS' ''',
                (date_str,)
            )
            row = cursor.fetchone()
            
            return {
                'date': date_str,
                'total_transactions': row['count'] if row['count'] else 0,
                'total_amount': float(row['total']) if row['total'] else 0.0
            }
    
    def update_sender_balance(self, account_number: str, new_balance: float) -> bool:
        """Update sender account balance (admin function)."""
        try:
            with self.db_manager.transaction() as conn:
                conn.execute(
                    '''UPDATE sender_accounts 
                       SET balance = ?, 
                           updated_at = CURRENT_TIMESTAMP
                       WHERE account_number = ?''',
                    (new_balance, account_number)
                )
                return True
        except Exception as e:
            print(f"Error updating balance: {e}")
            return False
    
    def reset_receiver_daily_limit(self, account_number: str) -> bool:
        """Manually reset receiver daily limit (admin function)."""
        try:
            with self.db_manager.transaction() as conn:
                conn.execute(
                    '''UPDATE receiver_accounts 
                       SET daily_received = 0,
                           last_reset_date = ?,
                           updated_at = CURRENT_TIMESTAMP
                       WHERE account_number = ?''',
                    (date.today().isoformat(), account_number)
                )
                return True
        except Exception as e:
            print(f"Error resetting daily limit: {e}")
            return False
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """Get specific transaction details by ID."""
        with self.db_manager.transaction() as conn:
            cursor = conn.execute(
                'SELECT * FROM transactions WHERE transaction_id = ?',
                (transaction_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def search_transactions(self, 
                          sender_account: Optional[str] = None,
                          receiver_account: Optional[str] = None,
                          status: Optional[str] = None,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None,
                          limit: int = 50) -> List[Dict[str, Any]]:
        """Search transactions with multiple filters."""
        query = 'SELECT * FROM transactions WHERE 1=1'
        params: List[Any] = []
        
        if sender_account:
            query += ' AND sender_account = ?'
            params.append(sender_account)
        
        if receiver_account:
            query += ' AND receiver_account = ?'
            params.append(receiver_account)
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        if start_date:
            query += ' AND DATE(transaction_timestamp) >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND DATE(transaction_timestamp) <= ?'
            params.append(end_date)
        
        query += ' ORDER BY transaction_timestamp DESC LIMIT ?'
        params.append(limit)
        
        with self.db_manager.transaction() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
