# Money Transfer System

**Version:** 1.0.0  
**Status:** Development/Educational  
**Author:** Vijay  
**Date:** October 25, 2025  

---

## Executive Summary

This project presents a secure, ACID-compliant money transfer system built with Python and SQLite, designed as a hackathon submission. The application features a robust command-line interface for peer-to-peer account transfers, comprehensive validation mechanisms, detailed transaction logging, and full transactional database support using only the Python standard library. All system operations, including error handling and rollback, are implemented in a production-inspired manner for educational demonstration.

---

## Table of Contents

- [Money Transfer System](#money-transfer-system)
  - [Executive Summary](#executive-summary)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Technology Stack](#technology-stack)
  - [System Architecture](#system-architecture)
  - [Feature Overview](#feature-overview)
  - [Database Schema](#database-schema)
    - [Table: sender\_accounts](#table-sender_accounts)
    - [Table: receiver\_accounts](#table-receiver_accounts)
    - [Table: transactions](#table-transactions)
  - [Installation Guide](#installation-guide)
    - [Prerequisites](#prerequisites)
    - [Step-by-step Installation](#step-by-step-installation)
  - [Sample Data](#sample-data)
    - [Sender Accounts](#sender-accounts)
    - [Receiver Accounts](#receiver-accounts)
  - [Usage Instructions](#usage-instructions)
    - [Starting the Application](#starting-the-application)
    - [Viewing Transactions](#viewing-transactions)
  - [Error Handling](#error-handling)
  - [Transactional Operations](#transactional-operations)
  - [Testing Suite](#testing-suite)
  - [Security Features](#security-features)
  - [Troubleshooting](#troubleshooting)
  - [Future Enhancements](#future-enhancements)
  - [Contributing](#contributing)
  - [License and Acknowledgments](#license-and-acknowledgments)

---

## Project Overview

The Money Transfer System is a self-contained Python CLI application for secure money transfers between user accounts, fully backed by a local SQLite3 database. Major functionalities include account and transaction validation, daily receiver limits, security and authentication controls, comprehensive audit trails, and guaranteed ACID transactions. All operations and data flows adhere to best practices for financial software design.

---

## Technology Stack

- **Language:** Python 3.6+  
- **Database:** SQLite3 (bundled via standard library)  
- **Interface:** Command Line (CLI)  
- **Dependencies:** None (Python Standard Library Only)  
- **Key Libraries:** `sqlite3`, `datetime`, `typing`, `hashlib`  

---

## System Architecture

The project follows a layered architecture for clarity and maintainability:

| Layer         | Module          | Responsibility                                    |
|---------------|-----------------|-------------------------------------------------|
| Presentation  | main_db.py      | Handles CLI, user prompts, messaging             |
| Business Logic| db_operations.py| Core transaction logic, validation, operations   |
| Data Access   | database.py     | Manages SQLite connections, context managers     |
| Initialization| init_db.py      | Database schema setup, sample data seeding       |
| Testing       | test_db.py      | Automated verification of major operations       |

All database transactions utilize context managers to enforce atomicity and guarantee resource clean-up, while modular separation ensures future feature expansion and clear auditing.

---

## Feature Overview

- **Account & Currency Validation:** Ensures both sender and receiver accounts exist, are active, and use matching currencies  
- **Authentication:** Password-based verification with three attempts maximum  
- **Amount & Balance Checks:** Validates transfer amounts and ensures sufficient funds  
- **Daily Limits:** Receiver daily transaction limit with automatic reset  
- **Contact Verification:** Confirms sender's registered phone for security  
- **Transaction Reason (Optional):** Transfer notes  
- **Transactional Safety:** All transfers executed via ACID-compliant SQLite transaction; rollback guaranteed if any step fails  
- **Full Audit Trail:** Logs all transactions, including failures, with balance before/after and reason  
- **CLI Guidance:** Clear, interactive CLI with step-by-step prompts  
- **Database Integrity:** All failures recorded for audit compliance  

---

## Database Schema

### Table: sender_accounts

| Column           | Type  | Description                 |
|------------------|-------|-----------------------------|
| account_number   | TEXT  | Primary Key. Unique Sender ID|
| account_holder_name | TEXT | Sender name                  |
| password         | TEXT  | Sender password             |
| balance          | REAL  | Current balance             |
| currency         | TEXT  | Currency code (INR, USD, EUR, etc.) |
| contact_number   | TEXT  | Registered contact number   |
| is_active        | INTEGER | Active flag (1=active, 0=inactive) |

### Table: receiver_accounts

| Column           | Type  | Description                   |
|------------------|-------|-------------------------------|
| account_number   | TEXT  | Primary Key. Unique Receiver ID|
| account_holder_name | TEXT | Receiver name                 |
| daily_limit      | REAL  | Daily maximum receipt amount  |
| daily_received   | REAL  | Total received today          |
| last_reset_date  | TEXT  | Date daily_received last reset|
| currency         | TEXT  | Currency code                 |
| is_active        | INTEGER | Active flag                  |

### Table: transactions

| Column                | Type  | Description                          |
|-----------------------|-------|------------------------------------|
| transaction_id        | TEXT  | Transaction Unique ID (Primary Key) |
| sender_account        | TEXT  | Sender account number               |
| receiver_account      | TEXT  | Receiver account number             |
| amount                | REAL  | Money transferred                  |
| currency              | TEXT  | Currency code                     |
| transaction_timestamp | TEXT  | ISO 8601 timestamp                |
| status                | TEXT  | SUCCESS or FAILED                 |
| reason                | TEXT  | Transaction purpose (optional)    |
| sender_balance_before | REAL  | Balance before transfer            |
| sender_balance_after  | REAL  | Balance after transfer             |
| failure_reason        | TEXT  | Populated if transaction failed   |

---

## Installation Guide

### Prerequisites

- Python 3.6 or newer  
- No external dependencies—Python standard library only  
- SQLite3 is bundled with Python standard library  

To verify Python & SQLite installation:

python --version
python -c "import sqlite3"

### Step-by-step Installation

1. Clone/download project source to your system  
2. Navigate to project directory

cd money-transfer-system
3. Initialize the database and load sample data
python init_db.py

Expected output:

Database initialized successfully!
Sample data inserted.

---

## Sample Data

### Sender Accounts

| Account Number | Password | Balance  | Currency | Contact    | Status |
|----------------|----------|----------|----------|------------|--------|
| ACC001         | pass123  | 10000.00 | INR      | 9876543210 | Active |
| ACC002         | pass456  | 5000.00  | USD      | 9876543211 | Active |
| ACC003         | pass789  | 15000.00 | EUR      | 9876543212 | Active |

### Receiver Accounts

| Account Number | Holder      | Daily Limit | Currency | Status |
|----------------|-------------|-------------|----------|--------|
| REC001         | John Doe    | 50000.00    | INR      | Active |
| REC002         | Jane Smith  | 10000.00    | USD      | Active |
| REC003         | Bob Johnson | 20000.00    | EUR      | Active |

---

## Usage Instructions

### Starting the Application

python main_db.py

Follow interactive CLI steps to:  

- Enter sender account number  
- Authenticate (max 3 attempts)  
- Enter receiver account number  
- Specify transfer amount  
- Verify contact number  
- Optionally enter transaction reason  
- Confirm and execute transfer  

Example:
Enter sender account number: ACC001
Enter password: pass123
✓ Authentication successful!
...
✓ Transfer successful!
Transaction ID: TXN20251025170830001
New Balance: 9000.00 INR

### Viewing Transactions

Inspect transactions via SQLite CLI or GUI tool:

sqlite3 money_transfer.db
SELECT * FROM transactions ORDER BY transaction_timestamp DESC LIMIT 10;

---

## Error Handling

All validation errors and exceptions are gracefully managed and logged:

| Error Type          | System Response                              |
|---------------------|---------------------------------------------|
| Invalid credentials  | Max 3 attempts, then abort                   |
| Insufficient funds   | Transaction blocked, details shown          |
| Currency mismatch    | Rejected, instruct user on valid options    |
| Exceeding daily limit| Transaction denied, daily limit reported    |
| Inactive account    | Blocked, status message returned             |
| Invalid amount       | Input re-prompted                            |
| Contact mismatch     | Authentication failed                        |
| Database error       | Transaction rolled back, error logged       |

All errors are captured in the transactions log for compliance and analysis.

---

## Transactional Operations

The entire money transfer workflow is performed inside a single SQLite transaction, guaranteeing:

- **Atomicity:** Either all changes succeed, or none are made  
- **Consistency:** All business logic is strictly enforced  
- **Isolation:** No interference between concurrent transactions  
- **Durability:** Changes are persisted reliably  

A failed transaction results in immediate rollback and log entry with root-cause details.

---

## Testing Suite

Run automated tests for all business logic and edge cases:

python test_db.py

Tests include authentication, balance checking, daily limits, rollback scenarios, and audit log validation.

Expected output:

All tests passed! System is functioning correctly.

---

## Security Features

- Password authentication plus contact verification  
- Account activation status validation  
- Input sanitization at every step  
- Maximum attempt limits for login  
- Complete transaction logging (including failures)  
- Full rollback on errors  

**Note:**  
This is an educational demonstration. For real-world systems, implement hashed passwords (e.g., bcrypt), encrypted connections, multi-factor authentication, and periodic security audits.

---

## Troubleshooting

| Issue                     | Solution                                      |
|---------------------------|-----------------------------------------------|
| "Database is locked" error | Ensure no other applications are using the DB |
| Authentication fails      | Reset database with `python init_db.py`        |
| Daily limits not resetting | Manually update `last_reset_date` and reset amount |

---

## Future Enhancements

Planned features for future versions:

- Web interface (Flask/Django)  
- REST API for integrations  
- Multi-currency support with exchange rates  
- SMS/email notifications  
- Scheduled/recurring transfers  
- Sender transaction limits  
- Admin dashboard for analytics  
- Mobile app support  
- Blockchain integration (immutable logs)  
- ML-powered fraud detection  
- Role management (user/admin/auditor)  
- Data export (PDF/CSV)  

---

## Contributing

- Fork and clone the repo  
- Create a feature branch  
- Follow PEP8/Python best practices  
- Add and document tests for features  
- Submit pull requests with clear descriptions  

---

## License and Acknowledgments

- **License:** MIT (See LICENSE file if included)  
- **Author:** Vijay  
- **Acknowledgments:**  
Open-source Python and SQLite community, hackathon mentors and organizers, and all contributors.
