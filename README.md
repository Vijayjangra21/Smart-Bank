# SmartBank – Banking Backend System

**A secure, scalable banking backend system implementing core banking operations with modern technologies.**

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)
5. [System Actors](#system-actors)
6. [Project Structure](#project-structure)
7. [Implementation Strategy](#implementation-strategy)
8. [3-Hour Development Plan](#3-hour-development-plan)
9. [Setup Instructions](#setup-instructions)
10. [GitHub Deployment](#github-deployment)
11. [Demo Scenarios](#demo-scenarios)
12. [Success Metrics](#success-metrics)

---

## Project Overview

**SmartBank** is a comprehensive banking backend system developed for the **HCLTech Hackathon 2025**. The project implements two core banking operations: **Money Transfer (Task 3)** and **Loan Application with EMI Calculation (Task 4)**.

### Project Goals
- Build a secure, functional banking system in 3 hours
- Implement robust business logic for financial operations
- Create a scalable architecture for future enhancements
- Deploy to GitHub with professional documentation

### Key Differentiators
- **Fast Development**: Template-based frontend + custom backend
- **Complete Features**: Two full banking operations working end-to-end
- **Professional Code**: Clean architecture following industry standards
- **Demo-Ready**: Easy to demonstrate to judges

---

## Features

### Task 3: Money Transfer

**Functionality:**
- Transfer funds between customer accounts
- Real-time balance validation
- Daily transaction limit enforcement
- Transaction history tracking
- Error handling for edge cases

**Business Logic:**
- Verify sender has sufficient balance
- Prevent exceeding daily transfer limits
- Atomic transaction processing (both accounts update or neither)
- Log all transactions for audit trail

**User Experience:**
- Simple transfer form with recipient selection
- Real-time balance display
- Transaction confirmation
- Success/error notifications

---

### Task 4: Loan Application & EMI Calculation

**Functionality:**
- Submit loan applications with loan details
- Automatic EMI (Equated Monthly Installment) calculation
- Support multiple loan types (Personal, Home, Car, Education)
- Admin approval/rejection workflow
- Loan status tracking

**Business Logic:**
- EMI Calculation Formula: **EMI = [P × r × (1 + r)^n] / [(1 + r)^n - 1]**
  - P = Principal amount
  - r = Monthly interest rate
  - n = Number of months
- Validate loan amount based on customer eligibility
- Generate repayment schedule
- Track loan status (Pending → Approved/Rejected → Active → Closed)

**User Experience:**
- Loan application form with dynamic EMI preview
- Loan status dashboard
- Repayment schedule visualization
- Admin panel for loan approvals

---

## System Architecture

### High-Level Design

```
┌─────────────────────────────────┐
│   React Frontend                │
│   (react-banking-app-template)  │
└──────────────┬──────────────────┘
               │ REST API (Axios)
               │ JSON over HTTP
               ▼
┌─────────────────────────────────┐
│   FastAPI Backend               │
│   (Python 3.9+)                 │
└──────────────┬──────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
   ┌─────────┐   ┌──────────┐
   │ SQLite  │   │ JWT Auth │
   │ DB      │   │ Module   │
   └─────────┘   └──────────┘
```

### Data Flow

**Money Transfer Flow:**
```
1. Customer logs in → JWT token generated
2. Customer selects recipient and amount
3. Frontend validates input → Backend API call
4. Backend validates balance and daily limits
5. Backend executes transfer (update both accounts)
6. Transaction logged in database
7. Response sent to frontend
8. Transaction history updated
```

**Loan Application Flow:**
```
1. Customer fills loan application form
2. Frontend calculates EMI → displays preview
3. Customer submits application
4. Backend stores loan as "PENDING"
5. Admin reviews application
6. Admin approves/rejects
7. Customer notified of status
8. If approved, loan becomes "ACTIVE"
```

---

## Technology Stack

### Backend Components
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI | High-performance async API |
| Database | SQLite | Lightweight, instant setup |
| ORM | SQLAlchemy | Database abstraction |
| Authentication | JWT | Secure token-based auth |
| Password Hashing | bcrypt | Secure password storage |
| Validation | Pydantic | Request/response validation |
| Server | Uvicorn | ASGI application server |

### Frontend Components
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React 18+ | UI library |
| HTTP Client | Axios | API communication |
| Styling | Tailwind CSS | CSS utility framework |
| Routing | React Router | Page navigation |
| UI Components | Pre-built | From template |

### Tools & Services
| Tool | Purpose |
|------|---------|
| Git | Version control |
| GitHub | Repository hosting |
| Docker | Containerization (optional) |
| VSCode | Code editor |

---

## System Actors

### 1. Customer
**Responsibilities:**
- Register and login to system
- View account balance
- Initiate money transfers
- Apply for loans
- Track transaction history
- View loan status

**Access Level:** Customer role

### 2. Bank Admin
**Responsibilities:**
- Review loan applications
- Approve or reject loans
- Manage customer accounts
- Monitor transactions
- Generate reports

**Access Level:** Admin role

### 3. System (Backend)
**Responsibilities:**
- Process transactions
- Calculate EMI
- Validate business rules
- Store data persistently
- Generate responses

---

## Project Structure

```
smartbank/
│
├── frontend/                          # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── TransferForm.jsx      # Task 3 form
│   │   │   ├── LoanForm.jsx          # Task 4 form
│   │   │   ├── Dashboard.jsx         # User dashboard
│   │   │   └── AdminPanel.jsx        # Admin interface
│   │   ├── services/
│   │   │   └── api.js               # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── .env
│
├── backend/                           # FastAPI application
│   ├── app/
│   │   ├── main.py                  # Entry point
│   │   ├── database.py              # Database connection
│   │   ├── models.py                # SQLAlchemy models
│   │   ├── schemas.py               # Pydantic schemas
│   │   ├── auth.py                  # Authentication logic
│   │   ├── transactions.py          # Task 3: Transfer logic
│   │   └── loans.py                 # Task 4: Loan logic
│   ├── requirements.txt
│   └── .env
│
├── .gitignore
├── README.md
└── docker-compose.yml (optional)
```

---

## Implementation Strategy

### Development Approach: Template + Custom Backend

**Why This Strategy?**
- Saves 40-50% development time using existing frontend template
- Allows focus on core business logic in backend
- Leverages best practices in UI/UX from template
- Enables rapid deployment

### Frontend Strategy
- **Use**: react-banking-app-template by cenksari
- **Customize**: Adapt components for Task 3 & 4
- **Connect**: Point to FastAPI backend
- **Time**: 30-40 minutes

### Backend Strategy
- **Build**: Custom FastAPI implementation
- **Focus**: Business logic for Tasks 3 & 4
- **Database**: SQLite for instant setup
- **Time**: 90-100 minutes

### Integration Strategy
- **Connect**: Frontend API calls to backend
- **Test**: Manual testing of full user flows
- **Deploy**: Push to GitHub
- **Time**: 30-40 minutes

---

## 3-Hour Development Plan

### Timeline Overview

| Phase | Time | Deliverable |
|-------|------|-------------|
| Setup | 30 min | Frontend + Backend foundation |
| Task 3 | 45 min | Money transfer working |
| Task 4 | 45 min | Loan application working |
| Integration | 20 min | Frontend-backend connected |
| Testing | 15 min | End-to-end validation |
| GitHub | 15 min | Code pushed and documented |

### Phase-by-Phase Breakdown

#### Phase 1: Environment Setup (0-30 min)

**Frontend (15 min)**
```
1. Clone: git clone https://github.com/cenksari/react-banking-app-template.git frontend
2. Setup: cd frontend && npm install
3. Verify: npm run dev (check if it runs)
4. Add .env: VITE_API_URL=http://localhost:8000
```

**Backend (15 min)**
```
1. Create: mkdir backend && cd backend
2. Venv: python -m venv venv && source venv/bin/activate
3. Install: pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib bcrypt
4. Create: app/main.py with basic FastAPI app structure
```

---

#### Phase 2: Backend Foundation (30-75 min)

**Database Models (15 min)**
- User model (id, email, password_hash, name, role)
- Account model (id, user_id, balance, account_type)
- Transaction model (id, from_account_id, to_account_id, amount, timestamp)
- Loan model (id, user_id, amount, tenure, status, emi_amount)

**API Endpoints (25 min)**
- Authentication:
  - POST /auth/register
  - POST /auth/login
  - GET /auth/me
- Accounts:
  - GET /accounts/{id}
  - POST /accounts

**Database (10 min)**
- Create SQLite database
- Initialize tables
- Add seed data (test customers with accounts)

---

#### Phase 3: Task 3 - Money Transfer (75-120 min)

**Backend Implementation (30 min)**
```
Endpoint: POST /transactions/transfer
Input: {
  from_account_id: int,
  to_account_id: int,
  amount: float,
  description: string
}
Logic:
  1. Verify JWT token
  2. Check sender balance >= amount
  3. Check daily transfer limit not exceeded
  4. Deduct from sender account
  5. Add to receiver account
  6. Create transaction record
  7. Return success/error
```

**Frontend Implementation (15 min)**
- Add Transfer page with form
- Input validation (amount, recipient)
- API call to backend
- Display response (success/error)

---

#### Phase 4: Task 4 - Loan Application (120-165 min)

**Backend Implementation (30 min)**
```
Endpoints:
  POST /loans/apply
    Input: {
      user_id: int,
      loan_type: string,
      amount: float,
      tenure_months: int,
      interest_rate: float
    }
    Calculate EMI using formula
    Store in database
    Return loan details

  PUT /loans/{id}/approve
    Input: { status: "APPROVED"|"REJECTED" }
    Update loan status
    (Admin only)

  GET /loans/{id}
    Return loan details and EMI schedule
```

**Frontend Implementation (15 min)**
- Add Loan Application page
- Form with loan details
- Real-time EMI calculation display
- Show loan status after submission

---

#### Phase 5: Integration & Testing (165-185 min)

**Frontend-Backend Integration (15 min)**
- Update API endpoints in frontend
- Test authentication flow
- Test transfer flow
- Test loan flow

**Manual Testing (10 min)**
- Login test
- Transfer test
- Loan application test
- Admin approval test

---

#### Phase 6: GitHub Deployment (185-195 min)

**Repository Setup (10 min)**
```
git init
git add .
git commit -m "SmartBank: Tasks 3 & 4 Implementation"
git remote add origin https://github.com/yourusername/smartbank.git
git push -u origin main
```

**Documentation (10 min)**
- Add README.md
- Add quick start instructions
- Add test credentials

---

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Git
- Text editor (VSCode recommended)

### Installation Steps

#### 1. Clone & Setup Frontend

```bash
# Clone template
git clone https://github.com/cenksari/react-banking-app-template.git frontend
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000" > .env

# Verify setup
npm run dev
# Visit http://localhost:5173
```

#### 2. Setup Backend

```bash
# Create backend directory
mkdir backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-jose passlib bcrypt

# Create requirements file
pip freeze > requirements.txt

# Create environment file
echo "DATABASE_URL=sqlite:///./smartbank.db
SECRET_KEY=your-secret-key-here" > .env

# Run server
uvicorn app.main:app --reload
# API available at http://localhost:8000
```

#### 3. Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Customer 1 | customer1@smartbank.com | password123 |
| Customer 2 | customer2@smartbank.com | password123 |
| Admin | admin@smartbank.com | admin123 |

---

## GitHub Deployment

### Step 1: Create Repository

1. Go to https://github.com/new
2. Repository name: `smartbank`
3. Description: "Banking backend system - Tasks 3 & 4"
4. Choose: Public
5. Create repository

### Step 2: Push Code

```bash
cd smartbank
git init
git add .
git commit -m "Initial commit: SmartBank - Tasks 3 & 4 Implementation"
git remote add origin https://github.com/yourusername/smartbank.git
git branch -M main
git push -u origin main
```

### Step 3: Repository Structure on GitHub

```
smartbank/
├── frontend/
├── backend/
├── .gitignore
└── README.md
```

### .gitignore Content

```
# Python
__pycache__/
*.py[cod]
*.so
venv/
env/

# Node
node_modules/
npm-debug.log
yarn-error.log

# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Demo Scenarios

### Scenario 1: Customer Registration & Login

**Steps:**
1. Open application
2. Click "Register"
3. Enter email and password
4. Submit registration
5. Login with credentials
6. Dashboard displays

**Expected Result:** ✅ User logged in, can see account balance

---

### Scenario 2: Money Transfer (Task 3)

**Steps:**
1. Login as Customer 1
2. Click "Transfer Money"
3. Select recipient (Customer 2)
4. Enter amount: ₹2,000
5. Submit transfer
6. View confirmation

**Expected Result:** ✅ Transfer successful, balance updated

**Verification:**
- Customer 1 balance decreased by ₹2,000
- Customer 2 balance increased by ₹2,000
- Transaction appears in history

---

### Scenario 3: Loan Application (Task 4)

**Steps:**
1. Login as Customer
2. Click "Apply for Loan"
3. Fill loan details:
   - Loan Type: Personal
   - Amount: ₹50,000
   - Tenure: 24 months
   - Interest: 12% p.a.
4. View EMI calculation (should show ₹2,357/month)
5. Submit application

**Expected Result:** ✅ Loan application submitted

---

### Scenario 4: Admin Loan Approval

**Steps:**
1. Login as Admin
2. View pending loans
3. Click loan application
4. Review details
5. Click "Approve" or "Reject"
6. Submit decision

**Expected Result:** ✅ Loan status updated

**Verification:**
- Customer sees "APPROVED" status
- Loan appears in active loans

---

### Scenario 5: Edge Cases

**Test Insufficient Balance:**
1. Try to transfer more than balance
2. System shows error: "Insufficient balance"

**Test Daily Limit:**
1. Try to transfer exceeding daily limit
2. System shows error: "Daily limit exceeded"

**Test Invalid Loan Amount:**
1. Apply with negative amount
2. System shows validation error

---

## Success Metrics

### Functional Requirements

| Requirement | Status | Evidence |
|-------------|--------|----------|
| User registration | ✅ | User can create account |
| User authentication | ✅ | JWT token generated |
| Account balance view | ✅ | Balance displays correctly |
| Money transfer | ✅ | Transfer executed, balances updated |
| Balance validation | ✅ | Insufficient funds blocked |
| Loan application | ✅ | Application submitted to database |
| EMI calculation | ✅ | Correct formula applied |
| Loan status tracking | ✅ | Status changes: Pending → Approved |
| Admin approval | ✅ | Admin can approve/reject loans |
| Transaction history | ✅ | Transfers appear in history |

### Non-Functional Requirements

| Requirement | Target | Status |
|-------------|--------|--------|
| API response time | < 200ms | ✅ |
| Database transactions | Atomic | ✅ |
| Security | JWT auth | ✅ |
| Code quality | Clean | ✅ |
| Documentation | Complete | ✅ |

### Deliverables

| Deliverable | Description | Status |
|-------------|-------------|--------|
| Frontend | React template customized | ✅ |
| Backend | FastAPI implementation | ✅ |
| Database | SQLite with models | ✅ |
| API | 10+ endpoints | ✅ |
| GitHub | Code repository | ✅ |
| README | This documentation | ✅ |

---

## Project Statistics

### Code Metrics
- **Backend**: ~400-500 lines of Python
- **Frontend**: Template-based (pre-built)
- **Database**: 4 core tables
- **API Endpoints**: 10+ RESTful endpoints

### Development Time
- **Setup**: 30 minutes
- **Backend**: 60 minutes
- **Frontend**: 30 minutes
- **Integration & Testing**: 30 minutes
- **Deployment**: 10 minutes
- **Total**: ~3 hours

### Technical Coverage
- **Authentication**: ✅ JWT
- **Database**: ✅ SQLite + SQLAlchemy
- **Business Logic**: ✅ Transfer + Loan
- **Validation**: ✅ Pydantic
- **Error Handling**: ✅ Comprehensive

---

## About This Project

**Project**: SmartBank Banking Backend System  
**Hackathon**: HCLTech 2025  
**Duration**: 3 hours  
**Tasks Completed**: Task 3 (Money Transfer) + Task 4 (Loan Application)  
**Technology**: Python, FastAPI, React, SQLite  

---

## Author

**Vijay**  
AI/ML Engineer  
HCLTech Hackathon 2025

---

## License

This project is developed for educational purposes as part of HCLTech Hackathon 2025.

---

**Built with precision for HCLTech Hackathon 2025** ✨
