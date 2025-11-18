# Backend Setup Guide

This guide will help you set up the SlideGuroo backend API locally.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 15 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd slide-guroo-ai/be
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

**Option A: Using Docker (Recommended)**

```bash
# From the root directory
docker-compose up -d postgres
```

**Option B: Local PostgreSQL**

```bash
# Create database
createdb slideguroo_db

# Or using psql
psql -U postgres
CREATE DATABASE slideguroo_db;
```

### 5. Configure Environment Variables

Create a `.env` file in the `be/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://slideguroo:slideguroo123@localhost:5432/slideguroo_db

# API Keys (get from respective providers)
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars

# Email Configuration (for production)
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_FROM=noreply@slideguroo.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_TLS=True
MAIL_SSL=False

# Frontend URL
FRONTEND_URL=http://localhost:3000

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# File Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 6. Generate Secret Key

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use it as your `SECRET_KEY` in `.env`.

### 7. Set Up LLM API Keys

You need at least one LLM provider API key. Get them from:

- **Google Gemini**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

**Recommended**: Use Google Gemini as it's used as the primary LLM in the codebase.

### 8. Initialize Database

The database tables will be created automatically when you start the server for the first time.

Alternatively, you can use Alembic migrations:

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 9. Start the Server

**Development Mode:**

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production Mode:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 10. Verify Installation

Open your browser and navigate to:

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

You should see the interactive API documentation.

## Email Configuration

### Development Mode

By default, emails are printed to the console in development. No SMTP configuration needed.

### Production Mode

For production, configure a real SMTP server:

**Gmail Example:**

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:

```env
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_TLS=True
```

**Other Providers:**

- **SendGrid**: Use SendGrid SMTP relay
- **AWS SES**: Configure SES SMTP credentials
- **Mailgun**: Use Mailgun SMTP settings

## Running Tests

### Install Test Dependencies

Test dependencies are already in `requirements.txt`.

### Create Test Database

```bash
# Using psql
psql -U postgres
CREATE DATABASE slideguroo_test_db;
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Configuration

Tests use a separate database (`slideguroo_test_db`) to avoid affecting your development data.

## Project Structure

```
be/
├── main.py                 # Application entry point
├── database.py            # Database configuration
├── db_models.py           # SQLAlchemy models
├── auth_utils.py          # Authentication utilities
├── email_service.py       # Email sending service
├── models.py              # Pydantic models
├── routers/               # API route handlers
│   ├── auth.py           # Authentication endpoints
│   ├── slides.py         # Slide upload endpoints
│   ├── topics.py         # Topic generation endpoints
│   ├── chat.py           # Chat/Q&A endpoints
│   ├── diagrams.py       # Diagram generation
│   └── dashboard.py      # User dashboard endpoints
├── services/              # Business logic
│   ├── lesson_service.py
│   ├── chat_history_service.py
│   └── lesson_generator.py
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_auth.py
├── docs/                  # Documentation
│   ├── API.md
│   ├── SETUP.md
│   └── AUTH_IMPLEMENTATION_STATUS.md
├── uploads/               # File uploads (gitignored)
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── .env.example          # Environment template
└── .env                  # Your environment (gitignored)
```

## Common Issues

### Database Connection Error

**Error**: `could not connect to server`

**Solution**:
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env`
- Verify database exists: `psql -l`

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### LLM API Errors

**Error**: `Invalid API key`

**Solution**:
- Verify your API key in `.env`
- Check API key has proper permissions
- Ensure API key is active and not expired

### File Upload Errors

**Error**: `Permission denied` when uploading files

**Solution**:
```bash
# Create uploads directory with proper permissions
mkdir -p uploads
chmod 755 uploads
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `GOOGLE_API_KEY` | Recommended | - | Google Gemini API key |
| `SECRET_KEY` | Yes | - | JWT signing key (min 32 chars) |
| `FRONTEND_URL` | No | http://localhost:3000 | Frontend URL for CORS |
| `CORS_ORIGINS` | No | localhost:3000,5173 | Allowed CORS origins |
| `MAIL_USERNAME` | No | - | SMTP username |
| `MAIL_PASSWORD` | No | - | SMTP password |
| `UPLOAD_DIR` | No | ./uploads | Upload directory path |
| `HOST` | No | 0.0.0.0 | Server host |
| `PORT` | No | 8000 | Server port |

## Next Steps

- Read the [API Documentation](API.md)
- Check [Authentication Implementation Status](AUTH_IMPLEMENTATION_STATUS.md)
- Set up the [Frontend](../../fe/docs/SETUP.md)
- Review [Docker Setup](../../docs/DOCKER.md) for containerized deployment

## Support

For issues or questions:
- Check existing documentation in `be/docs/`
- Open an issue on GitHub
- Review the code comments in source files
