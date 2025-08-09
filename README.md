# 📚 Library Management & Borrowing System

A comprehensive Library Management System built with Django REST Framework featuring user authentication, book borrowing/returning, inventory management, and penalty tracking system.

## Features

- 🔐 **User Authentication**
  - JWT-based login/register using **Simple-JWT**
  - Custom user model with penalty points tracking
  
- 📖 **Book Management**
  - Admins ➝ Full CRUD operations for books, authors, and categories
  - Users ➝ Browse books with advanced filtering (author, category)
  - Real-time inventory tracking with atomic updates
  
- 📋 **Borrowing System**
  - Smart borrowing limits (max 3 books per user)
  - Automated due date calculation (14 days)
  - Early return support
  - Late return penalty system (1 point per day late)
  
- 📊 **Inventory Management**
  - Multiple copies per book tracking
  - Atomic inventory updates during borrow/return
  - Real-time availability checking
  
- 📘 **API Documentation**
  - Swagger & ReDoc support for live testing via **drf_yasg**

## Tech Stack

- Django, Django REST Framework
- SimpleJWT for JWT authentication
- drf_yasg for Swagger API Documentation

## 📄 API Documentation (Swagger)

Access the interactive API documentation:

```bash
http://localhost:8000/api/docs/   # Swagger UI
http://localhost:8000/api/redoc/  # ReDoc UI 
```

## 🪪 Authorization

Click "Authorize" in Swagger UI and paste your JWT token:

```
Bearer <your_access_token>
```

## 🗄️ Database Models

### Core Models
- **User**: Extended with `penalty_points` field
- **Author**: `name`, `bio`
- **Category**: `name`
- **Book**: `title`, `description`, `author` (FK), `category` (FK), `total_copies`, `available_copies`
- **Borrow**: `user` (FK), `book` (FK), `borrow_date`, `due_date`, `return_date` (nullable)

## 📁 Project Structure

The project follows a modular and scalable architecture:
```
backend/
├── core/               # Project-level configuration
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL routing
│   └── wsgi.py         # WSGI configuration
├── apps/               # Modular app structure
│   ├── borrow/         # Borrowing and returning related APIs
│   ├── catalog/        # Books, authors, categories related APIs  
│   └── users/          # Authentication, registration, and penalty APIs
└── manage.py
```

App Responsibilities:
- `core/`: Project-level settings, URL routing, and configuration
- `apps/borrow/`: Borrowing and returning logic
- `apps/catalog/`: Book, author, and category management  
- `apps/users/`: Authentication, user registration, and penalty tracking

## 🔐 API Endpoints & Usage

### 👤 Authentication

#### Register
`POST /api/register/`
```json
{
  "username": "johndoe",
  "email": "john@example.com", 
  "password": "securepass123"
}
```

#### Login (JWT)
`POST /api/login/`
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

### 📚 Books & Metadata

#### Browse Books
`GET /api/books/`
- Query params: `?author=<author_id>&category=<category_id>`

#### Book Details
`GET /api/books/{id}/`

#### Admin-Only Book Management
```bash
POST /api/books/          # Create book (admin only)
PUT /api/books/{id}/      # Update book (admin only)
DELETE /api/books/{id}/   # Delete book (admin only)
```
*Note: Admin permissions required. Create superuser via `python manage.py createsuperuser`*

#### Authors & Categories
```bash
GET /api/authors/         # List authors
POST /api/authors/        # Create author (admin only)
GET /api/categories/      # List categories  
POST /api/categories/     # Create category (admin only)
```
*Note: Admin permissions required for POST operations*

### 📋 Borrowing Operations

#### Borrow a Book
`POST /api/borrow/`
```json
{
  "book_id": 1
}
```

**Validation Logic:**
- ✅ User has < 3 active borrows
- ✅ Book has available copies (available_copies > 0)
- ✅ Atomically decrements available_copies
- ✅ Sets due_date = borrow_date + 14 days

#### View Active Borrows
`GET /api/borrow/`

#### Return a Book
`POST /api/return/`
```json
{
  "borrow_id": 1
}
```

**Return Logic:**
- ✅ Updates return_date to current timestamp
- ✅ Atomically increments available_copies
- ✅ Calculates late days if past due_date
- ✅ Adds penalty points (1 point per day late)

#### Check Penalty Points
`GET /api/users/{id}/penalties/`
- Accessible by admin and the user themselves

## 🧮 Business Logic

### Borrowing System
1. **Limit Enforcement**: Users cannot borrow more than 3 books simultaneously
2. **Inventory Validation**: Only books with `available_copies > 0` can be borrowed
3. **Atomic Updates**: All inventory changes use database transactions to prevent race conditions
4. **Due Date Calculation**: Automatically set to 14 days from borrow date

### Penalty System
- **Late Return Detection**: Compares return_date with due_date
- **Penalty Calculation**: 1 penalty point per day late
- **Accumulative**: Penalty points accumulate across multiple late returns
- **Admin Oversight**: Admins can view all user penalties

### Inventory Management
- **Real-time Tracking**: `available_copies` updated instantly on borrow/return
- **Data Integrity**: Uses Django's `select_for_update()` for atomic operations
- **Validation**: Prevents borrowing when no copies available

## 🚀 Setup & Installation

### ✅ Clone the repository
```bash
git clone https://github.com/shemanto27/Django-Library-Management-Borrowing-System.git
cd Django-Library-Management-Borrowing-System
```

### ✅ Navigate to backend directory
```bash
cd backend
```

### ✅ Install dependencies using uv || **NO NEED FOR requirements.txt FILE, USE `uv sync` COMMAND**
```bash
uv sync
```

### ✅ Activate Virtual Environment
```bash
source .venv/bin/activate  
```

### ✅ Apply migrations
```bash
python manage.py migrate
```

### ✅ Create superuser for admin operations
```bash
python manage.py createsuperuser
```

### ✅ Run the development server
```bash
python manage.py runserver
```

### ✅ Access API Documentation
```bash
http://localhost:8000/api/docs/
```

## 🔄 Testing Workflow

### For Regular Users:
1. **Create User** ➝ `POST /api/register/`
2. **Login** ➝ `POST /api/login/` (get JWT token)
3. **Authorize** ➝ Use token in Swagger UI
4. **Browse Books** ➝ `GET /api/books/`
5. **Borrow Book** ➝ `POST /api/borrow/`
6. **Check Borrows** ➝ `GET /api/borrow/`
7. **Return Book** ➝ `POST /api/return/`

### For Admin Operations:
1. **Create Superuser** ➝ `python manage.py createsuperuser` (in terminal)
2. **Login with Admin** ➝ `POST /api/login/` (use superuser credentials)
3. **Authorize** ➝ Use admin JWT token in Swagger UI
4. **Admin Operations** ➝ Create/Update/Delete books, authors, categories


## ℹ️ Notes

- This project uses **uv** for modern Python package management, **NO NEED FOR requirements.txt FILE, USE `uv sync` COMMAND**
- Authentication uses **Simple-JWT** for stateless JWT tokens
- API documentation generated with **drf_yasg**
- Database operations use atomic transactions for data integrity
- Admin interface available at `/admin/` for manual data management
- Project follows Django best practices with modular app structure