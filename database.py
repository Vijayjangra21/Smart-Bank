import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

class DatabaseManager:
    """Manages database connection and operations with transaction support."""
    
    def __init__(self, db_path='money_transfer.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create a new database connection with proper settings."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA journal_mode = WAL')  # Write-Ahead Logging for better concurrency
        conn.execute('PRAGMA foreign_keys = ON')   # Enable foreign key constraints
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions with automatic rollback on error."""
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database schema if not exists."""
        with self.transaction() as conn:
            # Sender accounts table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sender_accounts (
                    account_number TEXT PRIMARY KEY,
                    authentication_credential TEXT NOT NULL,
                    balance REAL NOT NULL CHECK(balance >= 0),
                    contact_information TEXT NOT NULL,
                    currency TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Receiver accounts table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS receiver_accounts (
                    account_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact_information TEXT NOT NULL,
                    currency TEXT NOT NULL,
                    daily_limit REAL NOT NULL CHECK(daily_limit > 0),
                    daily_received REAL DEFAULT 0 CHECK(daily_received >= 0),
                    last_reset_date DATE DEFAULT CURRENT_DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Transactions log table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_account TEXT NOT NULL,
                    receiver_account TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    currency TEXT NOT NULL,
                    transaction_reason TEXT,
                    status TEXT NOT NULL,
                    sender_balance_before REAL NOT NULL,
                    sender_balance_after REAL NOT NULL,
                    receiver_daily_before REAL NOT NULL,
                    receiver_daily_after REAL NOT NULL,
                    transaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_account) REFERENCES sender_accounts(account_number),
                    FOREIGN KEY (receiver_account) REFERENCES receiver_accounts(account_number)
                )
            ''')
            
            # Create indexes for better performance
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_transactions_sender 
                ON transactions(sender_account)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_transactions_receiver 
                ON transactions(receiver_account)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_transactions_timestamp 
                ON transactions(transaction_timestamp)
            ''')
    
    def seed_sample_data(self):
        """Seed database with sample data."""
        with self.transaction() as conn:
            # Insert sender accounts
            sender_data = [
                ('ACC1001', 'pass123', 90000.0, 'vijay@example.com', 'INR'),
                ('ACC1002', 'secure456', 50000.5, 'rahul@example.com', 'INR')
            ]
            
            conn.executemany('''
                INSERT OR REPLACE INTO sender_accounts 
                (account_number, authentication_credential, balance, contact_information, currency)
                VALUES (?, ?, ?, ?, ?)
            ''', sender_data)
            
            # Insert receiver accounts
            receiver_data = [
                ('ACC2001', 'Amit Sharma', 'amitsharma@gmail.com', 'INR', 100000.0, 9000.0),
                ('ACC2002', 'Priya Singh', 'priya.singh@example.com', 'INR', 50000.0, 10000.0)
            ]
            
            conn.executemany('''
                INSERT OR REPLACE INTO receiver_accounts 
                (account_number, name, contact_information, currency, daily_limit, daily_received)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', receiver_data)
