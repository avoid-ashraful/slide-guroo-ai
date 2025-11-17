# SlideGuroo Setup Guide

Complete step-by-step guide to set up and run SlideGuroo locally.

## System Requirements

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- 4GB RAM minimum
- Internet connection for API calls

## Installation Steps

### Step 1: Clone or Download

If you haven't already, ensure you have the project files.

### Step 2: Backend Setup

#### 2.1 Navigate to Backend

```bash
cd be
```

#### 2.2 Create Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 2.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- Python-PPTX
- PyPDF2
- OpenAI SDK
- Anthropic SDK
- And other dependencies

#### 2.4 Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file with your preferred editor:

```env
# IMPORTANT: Choose ONE LLM provider and add its API key

# Option 1: OpenAI (Recommended for GPT-4)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Option 2: Anthropic (Recommended for Claude)
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-api-key-here
# ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Server Configuration (defaults are fine)
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Upload Configuration
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads
```

**Getting API Keys:**

- **OpenAI**: Sign up at https://platform.openai.com/ and create an API key
- **Anthropic**: Sign up at https://console.anthropic.com/ and create an API key

#### 2.5 Create Upload Directory

```bash
mkdir -p uploads
```

#### 2.6 Test Backend

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit http://localhost:8000/docs to see the API documentation.

Press `Ctrl+C` to stop the server.

### Step 3: Frontend Setup

Open a **NEW terminal** (keep backend running) and navigate to frontend:

```bash
cd fe  # From project root
```

#### 3.1 Install Dependencies

```bash
npm install
```

This will install:
- React
- Vite
- Tailwind CSS
- Mermaid.js
- React Router
- Axios
- And other dependencies

#### 3.2 Configure Environment (Optional)

Create `.env` file if you want to customize API URL:

```env
VITE_API_URL=http://localhost:8000/api
```

Default is already configured, so this step is optional.

#### 3.3 Start Frontend

```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Step 4: Access Application

Open your browser and go to:

```
http://localhost:3000
```

You should see the SlideGuroo homepage!

## Quick Test

### Test 1: Topic Generation

1. Click "Learn Topic" in navigation
2. Enter "Photosynthesis"
3. Select "Intermediate" difficulty
4. Click "Generate Lesson"
5. Wait 20-30 seconds for AI to generate the lesson
6. You should see a comprehensive lesson with diagrams

### Test 2: Slide Upload

1. Go to home page
2. Create a simple test PowerPoint or PDF
3. Upload the file
4. Wait for processing
5. View the generated lesson

### Test 3: Q&A

1. While viewing a lesson, click "Ask Questions"
2. Type "Explain this in simpler terms"
3. Click Send
4. You should get an AI response

## Troubleshooting

### Backend Issues

**Issue 1: Port already in use**
```bash
# Change port in .env
PORT=8001
```

**Issue 2: Module not found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue 3: API key errors**
```bash
# Verify .env file
cat .env

# Make sure API key is correct and has no extra spaces
```

**Issue 4: Upload errors**
```bash
# Create uploads directory
mkdir -p uploads
chmod 755 uploads
```

### Frontend Issues

**Issue 1: Module not found**
```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue 2: Port already in use**
```bash
# Vite will automatically try port 3001, 3002, etc.
# Or specify port:
npm run dev -- --port 3001
```

**Issue 3: API connection failed**
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check browser console for CORS errors
```

**Issue 4: Diagrams not rendering**
```bash
# Clear browser cache
# Check browser console for Mermaid errors
# Ensure mermaid package is installed
npm list mermaid
```

### Common Errors

**Error: "No API key found"**
- Solution: Add your OpenAI or Anthropic API key to `.env`

**Error: "CORS policy blocked"**
- Solution: Ensure CORS_ORIGINS in backend `.env` includes your frontend URL

**Error: "File too large"**
- Solution: File must be under 10MB. Increase MAX_UPLOAD_SIZE in `.env` if needed

**Error: "Failed to generate lesson"**
- Solution: Check backend logs for detailed error
- Ensure API key is valid and has credits

## Production Deployment

### Backend (Production)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Frontend (Production)

```bash
# Build for production
npm run build

# Serve built files
npm install -g serve
serve -s dist -l 3000
```

### Environment Variables

Set these in your production environment:

```env
# Backend
LLM_PROVIDER=openai
OPENAI_API_KEY=your-production-key
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://api.yourdomain.com/api
```

## Development Tips

### Backend Development

```bash
# Watch mode with auto-reload
python main.py

# Check logs
tail -f logs/app.log  # if logging to file

# Test API endpoints
curl -X POST http://localhost:8000/api/topics/generate \
  -H "Content-Type: application/json" \
  -d '{"topic":"Test Topic","language":"en"}'
```

### Frontend Development

```bash
# Development with HMR
npm run dev

# Check for linting errors
npm run lint

# Build and test production build
npm run build
npm run preview
```

## Architecture Overview

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │ ◄─────► │   React     │ ◄─────► │   FastAPI   │
│  (Client)   │         │  Frontend   │         │   Backend   │
└─────────────┘         └─────────────┘         └─────────────┘
                              │                        │
                              │                        ├──► OpenAI/Anthropic
                              │                        ├──► File Parser
                              │                        └──► Diagram Generator
                              │
                        Mermaid.js
                     (Diagram Rendering)
```

## Next Steps

1. **Customize**: Modify prompts in `be/services/llm_service.py` to adjust AI behavior
2. **Extend**: Add new diagram types in `be/services/diagram_service.py`
3. **Enhance UI**: Customize colors and styling in `fe/src/index.css`
4. **Add Features**: Implement quiz generation, user profiles, etc.

## Support

For issues:
1. Check logs in backend terminal
2. Check browser console (F12) for frontend errors
3. Review this guide
4. Check README.md for detailed documentation

## License

MIT License - See LICENSE file for details
