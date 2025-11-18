# SlideGuroo - AI-Powered Student Learning Assistant

Transform your slides and topics into comprehensive, interactive lessons with AI-generated diagrams and multilingual explanations.

## Overview

SlideGuroo is an AI-powered educational platform designed for students (Class 6-12 & University) that transforms static slides and topic queries into comprehensive, interactive learning experiences.

### Key Features

- **Slide Enhancement**: Upload PowerPoint, PDF, or Word documents and get detailed AI-generated lessons
- **Topic-Based Learning**: Ask about any topic and receive comprehensive, structured lessons
- **Intelligent Diagrams**: Automatic generation of Mermaid diagrams (flowcharts, mind maps, timelines, etc.)
- **Interactive Q&A**: Chat with AI tutor for instant explanations and clarifications
- **Multilingual Support**: Seamless switching between English and Bangla (Bengali)
- **Progressive Learning**: Step-by-step lesson structure with prerequisites and summaries
- **User Authentication**: Secure JWT-based authentication with email verification
- **Personal Dashboard**: Track your learning progress, lessons, and chat history
- **Chat History**: All conversations saved and accessible anytime

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directories:

### General Documentation
- **[Docker Setup Guide](docs/DOCKER.md)** - Complete Docker setup instructions for macOS (Apple Silicon) and Linux
- **[Docker Quick Start](docs/DOCKER-QUICKSTART.md)** - Quick reference for Docker commands

### Backend Documentation
- **[API Documentation](be/docs/API.md)** - Complete REST API reference with examples
- **[Backend Setup Guide](be/docs/SETUP.md)** - Local development setup for backend
- **[Authentication Status](be/docs/AUTH_IMPLEMENTATION_STATUS.md)** - Authentication implementation details

### Frontend Documentation
- **[Frontend Setup Guide](fe/docs/SETUP.md)** - Local development setup for frontend
- **[User Guide](fe/docs/USER_GUIDE.md)** - Complete user manual for SlideGuroo

## Project Structure

```
slide-guroo-ai/
├── docs/                    # General documentation
│   ├── DOCKER.md           # Docker setup guide
│   └── DOCKER-QUICKSTART.md # Docker quick reference
│
├── be/                      # Backend (Python/FastAPI)
│   ├── docs/               # Backend documentation
│   │   ├── API.md          # Complete API documentation
│   │   ├── SETUP.md        # Setup guide
│   │   └── AUTH_IMPLEMENTATION_STATUS.md
│   ├── services/           # Business logic
│   │   ├── lesson_service.py       # Lesson CRUD
│   │   ├── chat_history_service.py # Chat management
│   │   ├── lesson_generator.py     # AI lesson generation
│   │   └── content_extractor.py    # PPT/PDF parsing
│   ├── routers/            # API endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── slides.py       # Slide upload endpoints
│   │   ├── topics.py       # Topic generation endpoints
│   │   ├── chat.py         # Q&A chat endpoints
│   │   ├── diagrams.py     # Diagram generation endpoints
│   │   └── dashboard.py    # User dashboard endpoints
│   ├── tests/              # Backend tests
│   │   └── test_auth.py    # Authentication tests
│   ├── database.py         # Database configuration
│   ├── db_models.py        # SQLAlchemy models
│   ├── auth_utils.py       # JWT utilities
│   ├── email_service.py    # Email service
│   ├── models.py           # Pydantic data models
│   ├── main.py            # FastAPI application
│   └── requirements.txt    # Python dependencies
│
├── fe/                     # Frontend (React/Vite)
│   ├── docs/              # Frontend documentation
│   │   ├── SETUP.md       # Setup guide
│   │   └── USER_GUIDE.md  # User manual
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Header.jsx
│   │   │   ├── MermaidDiagram.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── context/       # React Context providers
│   │   │   └── AuthContext.jsx
│   │   ├── pages/         # Page components
│   │   │   ├── Home.jsx            # Slide upload page
│   │   │   ├── TopicGenerator.jsx  # Topic learning page
│   │   │   ├── LessonView.jsx      # Lesson display page
│   │   │   ├── Login.jsx           # Login page
│   │   │   ├── Signup.jsx          # Registration page
│   │   │   ├── Dashboard.jsx       # User dashboard
│   │   │   ├── VerifyEmail.jsx     # Email verification
│   │   │   ├── ForgotPassword.jsx  # Password reset request
│   │   │   └── ResetPassword.jsx   # Password reset form
│   │   ├── services/      # API client
│   │   │   ├── api.js            # Main API client
│   │   │   └── authService.js    # Authentication service
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   └── package.json       # Node dependencies
│
├── docker-compose.yml      # Docker orchestration
└── README.md              # This file
```

## Quick Start

> **🐳 Recommended:** Use Docker for the easiest setup! See [Docker Setup Guide](docs/DOCKER.md) for complete instructions.

### Option 1: Docker Setup (Recommended)

**Perfect for MacBook Apple Silicon (M1/M2/M3) and Linux**

1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Ensure Docker is running

2. **Configure Environment**
   ```bash
   # Backend configuration
   cd be
   cp .env.example .env
   # Edit .env and add your API keys:
   # - GOOGLE_API_KEY (recommended) or OPENAI_API_KEY
   # - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
   # - Email credentials (optional for development)

   # Frontend configuration
   cd ../fe
   cp .env.example .env
   ```

3. **Start the Application**
   ```bash
   # From project root
   docker-compose up
   ```

4. **Access the App**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs (Swagger): http://localhost:8000/docs
   - Database: localhost:5432

5. **Create Your Account**
   - Visit http://localhost:3000/signup
   - Register with your email
   - Check console for verification email (dev mode)
   - Start creating lessons!

**For detailed Docker instructions, see [docs/DOCKER.md](docs/DOCKER.md)**

### Option 2: Manual Setup

#### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **PostgreSQL** 15+
- **Google Gemini API Key** (recommended) or **OpenAI API Key**

#### Backend Setup

1. **Set up PostgreSQL database:**
   ```bash
   # Using psql
   createdb slideguroo_db
   ```

2. **Navigate to backend directory:**
   ```bash
   cd be
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and configure:
   ```env
   DATABASE_URL=postgresql+asyncpg://slideguroo:slideguroo123@localhost:5432/slideguroo_db
   GOOGLE_API_KEY=your_google_api_key_here
   SECRET_KEY=your-super-secret-key-min-32-chars
   FRONTEND_URL=http://localhost:3000
   ```

6. **Run the backend:**
   ```bash
   python main.py
   ```

   Backend will start on `http://localhost:8000`

**For detailed setup instructions, see [be/docs/SETUP.md](be/docs/SETUP.md)**

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd fe
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   ```

4. **Run the frontend:**
   ```bash
   npm run dev
   ```

   Frontend will start on `http://localhost:5173`

**For detailed setup instructions, see [fe/docs/SETUP.md](fe/docs/SETUP.md)**

#### Access the Application

1. Open browser at `http://localhost:5173`
2. Sign up for an account
3. Verify your email (check console in dev mode)
4. Start creating lessons!

## Usage Guide

**For complete user guide, see [fe/docs/USER_GUIDE.md](fe/docs/USER_GUIDE.md)**

### Getting Started

1. **Create Account**
   - Visit `/signup` and register
   - Verify your email
   - Login at `/login`

2. **Upload Slides**
   - Go to home page
   - Upload PPT/PPTX/PDF files
   - Select difficulty level and language
   - Generate AI lesson

3. **Learn Topics**
   - Click "Learn Topic"
   - Enter any subject
   - Get comprehensive AI-generated lesson

4. **Interactive Q&A**
   - Ask questions in any lesson
   - Get detailed explanations
   - View conversation history

5. **Dashboard**
   - Track all your lessons
   - View statistics
   - Manage content

### Authentication Features

- **Secure Login**: JWT-based authentication
- **Email Verification**: Verify your email to access all features
- **Password Reset**: Secure password recovery via email
- **Profile Management**: View and manage your account
- **Privacy**: All lessons and chats are private to your account

## API Documentation

**Complete API documentation is available at [be/docs/API.md](be/docs/API.md)**

### Interactive API Docs

Once the backend is running, visit `http://localhost:8000/docs` for Swagger UI.

### Main Endpoint Categories

- **Authentication** (`/api/auth/*`) - User registration, login, verification
- **Slides** (`/api/slides/*`) - Upload and process presentations
- **Topics** (`/api/topics/*`) - Generate lessons from topics
- **Chat** (`/api/chat/*`) - Q&A and conversation history
- **Diagrams** (`/api/diagrams/*`) - Generate visual diagrams
- **Dashboard** (`/api/dashboard/*`) - User statistics and management

## Features in Detail

### 1. Slide Enhancement Engine

- Extracts text, images, and structure from uploaded files
- Identifies key concepts and knowledge gaps
- Generates detailed explanations for each slide
- Adds real-world examples and context
- Creates logical lesson flow

### 2. Topic-Based Lesson Generator

- AI-powered content research and synthesis
- Curriculum-aligned lesson structure
- Progressive difficulty levels
- Cultural context for Bangladeshi students
- Multiple explanation approaches

### 3. Intelligent Diagram Generation

- AI decides when diagrams are needed
- Supports multiple diagram types:
  - Flowcharts for processes
  - Mind maps for concept relationships
  - Timelines for chronological events
  - Tree diagrams for classifications
  - Network diagrams for connections
  - Sequence diagrams for interactions

### 4. Interactive Learning Experience

- Progressive navigation through lesson sections
- Section-by-section content breakdown
- Visual representations for complex concepts
- Key points and examples for each section
- Comprehensive summaries

### 5. AI Learning Assistant

- Context-aware question answering
- Personalized explanations
- Related concepts suggestions
- Additional examples on demand
- Conversation history tracking

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM with async support
- **Alembic** - Database migrations
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing
- **FastAPI-Mail** - Email service
- **Python-PPTX** - PowerPoint parsing
- **PyPDF2** - PDF extraction
- **Google Gemini API** - Primary LLM provider
- **OpenAI API** - GPT models (alternative)
- **Anthropic API** - Claude models (alternative)
- **Pydantic** - Data validation
- **Pytest** - Testing framework

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **React Context** - State management
- **Tailwind CSS** - Utility-first CSS framework
- **Mermaid.js** - Diagram rendering
- **Axios** - HTTP client with interceptors
- **Lucide React** - Icon library

## Configuration

### Backend Configuration (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://slideguroo:slideguroo123@localhost:5432/slideguroo_db

# LLM API Keys
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Authentication
SECRET_KEY=your-super-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

# Email Configuration
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_FROM=noreply@slideguroo.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_TLS=True

# Application
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Server
HOST=0.0.0.0
PORT=8000

# Upload
MAX_UPLOAD_SIZE=52428800  # 50 MB
UPLOAD_DIR=./uploads
```

### Frontend Configuration

Create `.env` in `fe/` directory:

```env
VITE_API_URL=http://localhost:8000/api
```

**Note**: Environment variable documentation is available in:
- [be/docs/SETUP.md](be/docs/SETUP.md) - Backend configuration details
- [fe/docs/SETUP.md](fe/docs/SETUP.md) - Frontend configuration details

## Development

### Backend Development

```bash
cd be
source venv/bin/activate
python main.py  # Auto-reloads on code changes
```

### Frontend Development

```bash
cd fe
npm run dev  # Hot module replacement enabled
```

### Code Structure

- Backend follows clean architecture with service layer separation
- Frontend uses component-based architecture
- API client abstraction for easy endpoint management
- Reusable UI components

## Testing

### Running Backend Tests

```bash
cd be

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Manual Testing Checklist

1. **Authentication**
   - [ ] User registration
   - [ ] Email verification
   - [ ] Login/logout
   - [ ] Password reset
   - [ ] Protected routes

2. **Slide Upload**
   - [ ] Upload PPT file
   - [ ] Upload PDF file
   - [ ] Test error handling for invalid files
   - [ ] Verify lesson generation
   - [ ] Check lesson appears in dashboard

3. **Topic Generation**
   - [ ] Generate lesson for science topic
   - [ ] Generate lesson for history topic
   - [ ] Test language switching
   - [ ] Verify diagrams are generated
   - [ ] Save to dashboard

4. **Lesson Navigation**
   - [ ] Navigate through sections
   - [ ] View diagrams
   - [ ] Check key points and examples

5. **Q&A Chat**
   - [ ] Ask questions in English
   - [ ] Ask questions in Bangla
   - [ ] Verify context-aware responses
   - [ ] Check chat history saves

6. **Dashboard**
   - [ ] View lesson statistics
   - [ ] Delete lessons
   - [ ] View recent activity

## Troubleshooting

### Backend Issues

**Issue: Module not found errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue: API key errors**
```bash
# Verify .env file exists and has correct API key
cat .env
```

**Issue: File upload errors**
```bash
# Ensure uploads directory exists
mkdir -p uploads
```

### Frontend Issues

**Issue: Module not found**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Issue: API connection errors**
```bash
# Verify backend is running on port 8000
curl http://localhost:8000/health
```

**Issue: Mermaid diagrams not rendering**
```bash
# Check browser console for errors
# Ensure mermaid package is installed
npm list mermaid
```

## Roadmap

### Phase 1 - Core Features ✅ COMPLETED
- [x] Slide upload and processing
- [x] Topic-based lesson generation
- [x] Diagram generation
- [x] Interactive Q&A
- [x] Multilingual support (English/Bangla)

### Phase 2 - Authentication & User Management ✅ COMPLETED
- [x] User authentication (JWT)
- [x] Email verification
- [x] Password reset
- [x] User dashboard
- [x] Lesson history and management
- [x] Chat history persistence
- [x] User statistics

### Phase 3 - Future Enhancements 🚀
- [ ] Quiz generation from lessons
- [ ] Progress tracking and analytics
- [ ] Lesson bookmarking and favorites
- [ ] Export lessons to PDF
- [ ] Mobile responsive improvements
- [ ] Collaborative learning features
- [ ] More languages (Hindi, Urdu, Spanish, etc.)
- [ ] Video content integration
- [ ] Offline mode
- [ ] Teacher dashboard
- [ ] Classroom management
- [ ] Student performance analytics

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@slideguroo.com (placeholder)

## Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- Mermaid.js for diagram rendering
- FastAPI and React communities

---

**Built with ❤️ for students by the SlideGuroo team**
