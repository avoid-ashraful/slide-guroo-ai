# SlideGuroo Backend

FastAPI-based backend for the SlideGuroo AI Learning Assistant.

## Features

- **Content Extraction**: Parse PPT, PDF, DOCX files
- **LLM Integration**: OpenAI and Anthropic support
- **Lesson Generation**: AI-powered comprehensive lessons
- **Diagram Generation**: Intelligent Mermaid diagram creation
- **Q&A System**: Context-aware question answering
- **RESTful API**: Well-documented endpoints

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Edit `.env` file:

```env
# Choose LLM provider
LLM_PROVIDER=openai  # or anthropic

# Add API key for chosen provider
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Server settings
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000

# File upload
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads
```

## Running

```bash
# Development (with auto-reload)
python main.py

# Production (with uvicorn)
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Slides
- `POST /api/slides/upload` - Upload and process slides
  - Form data: `file`, `language`, `difficulty_level`, `include_diagrams`
  - Returns: Generated lesson

### Topics
- `POST /api/topics/generate` - Generate lesson from topic
  - JSON: `{topic, language, difficulty_level, include_diagrams}`
  - Returns: Generated lesson

### Chat
- `POST /api/chat/ask` - Ask question about lesson
  - JSON: `{lesson_id, question, language, context, conversation_history}`
  - Returns: Answer with related concepts

- `POST /api/chat/store-lesson` - Store lesson for Q&A
  - JSON: Lesson object
  - Returns: Success message

### Diagrams
- `POST /api/diagrams/generate` - Generate diagram
  - JSON: `{concept, diagram_type, context}`
  - Returns: Mermaid diagram code

## Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
be/
├── services/
│   ├── content_extractor.py  # File parsing
│   ├── llm_service.py         # LLM integration
│   ├── diagram_service.py     # Diagram generation
│   └── lesson_generator.py    # Main orchestrator
├── routers/
│   ├── slides.py              # Slide endpoints
│   ├── topics.py              # Topic endpoints
│   ├── chat.py                # Chat endpoints
│   └── diagrams.py            # Diagram endpoints
├── models.py                  # Pydantic models
├── main.py                    # FastAPI app
└── requirements.txt           # Dependencies
```

## Development

### Adding New Features

1. **New Service**: Add to `services/` directory
2. **New Endpoint**: Add to appropriate router in `routers/`
3. **New Model**: Add to `models.py`
4. **Register Router**: Include in `main.py`

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Use async/await for I/O operations

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when implemented)
pytest
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **API Key Errors**: Check `.env` file configuration
3. **File Upload Errors**: Verify `uploads/` directory exists
4. **Port Already in Use**: Change PORT in `.env`

### Logs

Application logs are printed to stdout. Check for:
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Failures and exceptions

## Performance

- Upload size limited to 10MB by default
- LLM requests timeout after 60 seconds
- Diagram generation cached per session
- Async operations for concurrent requests

## Security

- CORS configured for allowed origins
- File type validation on upload
- Size limits on uploads
- Input validation with Pydantic
- No sensitive data logging

## License

MIT License
