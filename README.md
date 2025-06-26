# 📊 Analytics API

A powerful FastAPI-based analytics platform for tracking sales, expenses, and generating comprehensive financial insights with chart-ready data formats.

## 🚀 Features

- **User Authentication & Authorization** - Secure JWT-based authentication
- **Sales Management** - Track and manage sales transactions
- **Expense Tracking** - Monitor business expenses by category
- **Financial Analytics** - Comprehensive financial summaries and insights
- **Chart-Ready Data** - All analytics endpoints return data optimized for frontend charting libraries
- **Time-Based Analysis** - Monthly, weekly, and custom date range analytics
- **Top Selling Items** - Track best-performing products
- **Expense Breakdown** - Categorized expense analysis

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Database**: SQLAlchemy ORM with Alembic migrations
- **Authentication**: JWT tokens with bcrypt password hashing
- **Testing**: Pytest with comprehensive test coverage
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL (or your preferred SQL database)
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd analytics-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/analytics_db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

### Sales
- `GET /api/v1/sales/` - List all sales
- `POST /api/v1/sales/` - Create new sale
- `GET /api/v1/sales/{id}` - Get sale by ID
- `PUT /api/v1/sales/{id}` - Update sale
- `DELETE /api/v1/sales/{id}` - Delete sale

### Expenses
- `GET /api/v1/expenses/` - List all expenses
- `POST /api/v1/expenses/` - Create new expense
- `GET /api/v1/expenses/{id}` - Get expense by ID
- `PUT /api/v1/expenses/{id}` - Update expense
- `DELETE /api/v1/expenses/{id}` - Delete expense

### Analytics
- `GET /api/v1/analytics/summary/` - Financial summary (chart-ready)
- `GET /api/v1/analytics/monthly-summary` - Monthly analytics
- `GET /api/v1/analytics/weekly-summary` - Weekly analytics
- `GET /api/v1/analytics/top-selling-items` - Top performing products
- `GET /api/v1/analytics/expense-breakdown` - Expense analysis by category

## 📊 Chart-Ready Data Format

All analytics endpoints return data in a standardized format optimized for charting libraries like Chart.js, D3.js, etc.:

```json
{
  "labels": ["Jan", "Feb", "Mar"],
  "datasets": [
    {
      "label": "Income",
      "data": [1200, 1500, 1800]
    },
    {
      "label": "Expenses", 
      "data": [800, 900, 1000]
    }
  ]
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_analytics.py

# Run tests with verbose output
pytest -v
```

## 🗄️ Database Schema

The application uses the following main models:

- **User** - User authentication and profile information
- **Sale** - Sales transactions with items, quantities, and amounts
- **Expense** - Business expenses with categories and amounts

Database migrations are managed with Alembic. To create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- User-specific data isolation
- Input validation and sanitization
- SQL injection prevention through ORM

## 🚀 Deployment

### Using Docker (Recommended)

```dockerfile
# Dockerfile example
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Traditional Hosting

1. Set up a production database
2. Configure environment variables
3. Run migrations: `alembic upgrade head`
4. Start with a production ASGI server: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request




