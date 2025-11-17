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

## Project Structure

```
slide-guroo-ai/
├── be/                      # Backend (Python/FastAPI)
│   ├── services/           # Business logic
│   │   ├── content_extractor.py    # PPT/PDF parsing
│   │   ├── llm_service.py          # LLM integration (OpenAI/Anthropic)
│   │   ├── diagram_service.py      # Mermaid diagram generation
│   │   └── lesson_generator.py     # Main lesson orchestration
│   ├── routers/            # API endpoints
│   │   ├── slides.py       # Slide upload endpoints
│   │   ├── topics.py       # Topic generation endpoints
│   │   ├── chat.py         # Q&A chat endpoints
│   │   └── diagrams.py     # Diagram generation endpoints
│   ├── models.py           # Pydantic data models
│   ├── main.py            # FastAPI application
│   └── requirements.txt    # Python dependencies
│
├── fe/                     # Frontend (React/Vite)
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Header.jsx
│   │   │   └── MermaidDiagram.jsx
│   │   ├── pages/         # Page components
│   │   │   ├── Home.jsx           # Slide upload page
│   │   │   ├── TopicGenerator.jsx # Topic learning page
│   │   │   └── LessonView.jsx     # Lesson display page
│   │   ├── services/      # API client
│   │   │   └── api.js
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   └── package.json       # Node dependencies
│
└── README.md              # This file
```

## Quick Start

### Prerequisites

- **Python** 3.9+
- **Node.js** 18+
- **OpenAI API Key** or **Anthropic API Key**

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd be
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API key:
   ```env
   # Use OpenAI
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here

   # OR use Anthropic
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. **Run the backend:**
   ```bash
   python main.py
   ```

   Backend will start on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd fe
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the frontend:**
   ```bash
   npm run dev
   ```

   Frontend will start on `http://localhost:3000`

### Access the Application

Open your browser and navigate to `http://localhost:3000`

## Usage Guide

### Upload Slides

1. Go to the home page
2. Drag and drop or click to upload PPT/PPTX/PDF/DOCX files
3. Select difficulty level (Beginner/Intermediate/Advanced)
4. Choose whether to generate diagrams
5. Click "Generate Lesson"
6. View your comprehensive lesson with interactive diagrams

### Learn Any Topic

1. Click "Learn Topic" in the navigation
2. Enter any topic (e.g., "Photosynthesis", "World War 2", "Quantum Physics")
3. Select difficulty level and language
4. Click "Generate Lesson"
5. AI will research and create a comprehensive lesson

### Interactive Q&A

1. While viewing a lesson, click "Ask Questions"
2. Type your question in the chat panel
3. Get instant, detailed explanations
4. Receive related concepts and additional examples

### Language Switching

Use the language selector in the header to switch between English and Bangla at any time.

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Main Endpoints

- **POST /api/slides/upload** - Upload and process slides
- **POST /api/topics/generate** - Generate lesson from topic
- **POST /api/chat/ask** - Ask questions about lessons
- **POST /api/diagrams/generate** - Generate diagrams

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
- **Python-PPTX** - PowerPoint parsing
- **PyPDF2** - PDF extraction
- **OpenAI API** - GPT models for content generation
- **Anthropic API** - Claude models (alternative)
- **Pydantic** - Data validation

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Mermaid.js** - Diagram rendering
- **React Router** - Navigation
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering

## Configuration

### Backend Configuration (.env)

```env
# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai

# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Models
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Server
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads
```

### Frontend Configuration

Create `.env` in `fe/` directory (optional):

```env
VITE_API_URL=http://localhost:8000/api
```

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

### Manual Testing Checklist

1. **Slide Upload**
   - [ ] Upload PPT file
   - [ ] Upload PDF file
   - [ ] Upload DOCX file
   - [ ] Test error handling for invalid files
   - [ ] Verify lesson generation

2. **Topic Generation**
   - [ ] Generate lesson for science topic
   - [ ] Generate lesson for history topic
   - [ ] Generate lesson for math topic
   - [ ] Test language switching
   - [ ] Verify diagrams are generated

3. **Lesson Navigation**
   - [ ] Navigate through sections
   - [ ] View diagrams
   - [ ] Check key points and examples
   - [ ] Read lesson summary

4. **Q&A Chat**
   - [ ] Ask questions in English
   - [ ] Ask questions in Bangla
   - [ ] Verify context-aware responses
   - [ ] Check related concepts

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

### Phase 1 (MVP) - Completed ✓
- [x] Slide upload and processing
- [x] Topic-based lesson generation
- [x] Diagram generation
- [x] Interactive Q&A
- [x] Multilingual support (English/Bangla)

### Phase 2 (Future Enhancements)
- [ ] User authentication and profiles
- [ ] Lesson history and bookmarks
- [ ] Quiz generation
- [ ] Progress tracking
- [ ] Mobile app
- [ ] Collaborative learning features
- [ ] More languages (Hindi, Urdu, etc.)
- [ ] Video content integration
- [ ] Offline mode

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
