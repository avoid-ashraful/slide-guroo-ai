# SlideGuroo - Docker Setup Guide

Complete guide for running SlideGuroo using Docker on MacBook Apple Silicon (M1/M2/M3).

## Prerequisites

### Required Software

1. **Docker Desktop for Mac (Apple Silicon)**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Minimum version: 4.0 or later
   - Ensure "Use Rosetta for x86/amd64 emulation" is enabled in Docker Desktop settings

2. **Docker Compose**
   - Included with Docker Desktop
   - Verify installation: `docker-compose --version`

### System Requirements

- macOS 11.0 or later
- Apple Silicon (M1/M2/M3) chip
- At least 4GB free RAM
- At least 5GB free disk space

## Quick Start (Production Mode)

### Step 1: Clone or Navigate to Project

```bash
cd slide-guroo-ai
```

### Step 2: Configure Environment

Create the `.env` file in the `be/` directory:

```bash
cd be
cp .env.example .env
```

Edit `be/.env` and add your API key:

```env
# Choose ONE provider
LLM_PROVIDER=openai

# Add your API key
OPENAI_API_KEY=sk-your-actual-api-key-here

# Or use Anthropic
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

### Step 3: Start the Application

From the project root directory:

```bash
docker-compose up
```

Or run in detached mode (background):

```bash
docker-compose up -d
```

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Step 5: Stop the Application

```bash
# If running in foreground, press Ctrl+C, then:
docker-compose down

# If running in background:
docker-compose down
```

## Development Mode (with Hot Reload)

For active development with automatic code reloading:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This enables:
- Backend hot reload when Python files change
- Frontend hot reload when React files change
- Source code mounted as volumes

## Docker Commands Cheatsheet

### Starting Services

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Start with rebuild
docker-compose up --build

# Start specific service
docker-compose up backend
docker-compose up frontend
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes uploaded files)
docker-compose down -v

# Stop specific service
docker-compose stop backend
docker-compose stop frontend
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Rebuilding Images

```bash
# Rebuild all images
docker-compose build

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Rebuild without cache
docker-compose build --no-cache
```

### Container Management

```bash
# List running containers
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Cleaning Up

```bash
# Remove stopped containers
docker-compose rm

# Remove all images
docker-compose down --rmi all

# Remove everything (containers, networks, volumes, images)
docker-compose down -v --rmi all

# Clean up Docker system (global)
docker system prune -a
```

## Project Structure

```
slide-guroo-ai/
├── docker-compose.yml          # Production configuration
├── docker-compose.dev.yml      # Development overrides
├── be/
│   ├── Dockerfile             # Backend production image
│   ├── .dockerignore          # Files to exclude
│   ├── .env                   # Environment variables (YOU CREATE THIS)
│   └── .env.example           # Environment template
├── fe/
│   ├── Dockerfile             # Frontend production image
│   ├── Dockerfile.dev         # Frontend development image
│   └── .dockerignore          # Files to exclude
└── DOCKER.md                  # This file
```

## Configuration

### Environment Variables

All configuration is done via `be/.env` file:

```env
# LLM Provider (required)
LLM_PROVIDER=openai              # or anthropic

# API Keys (required - choose one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Models (optional)
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Server (optional)
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000

# Upload (optional)
MAX_UPLOAD_SIZE=10485760         # 10MB
UPLOAD_DIR=./uploads
```

### Port Configuration

Default ports:
- Frontend: `3000`
- Backend: `8000`

To change ports, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # HOST:CONTAINER
  frontend:
    ports:
      - "3001:3000"  # HOST:CONTAINER
```

### Volume Management

Uploaded files are stored in a Docker volume:

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect slide-guroo-ai_backend-uploads

# Backup uploads
docker cp slideguroo-backend:/app/uploads ./backup-uploads

# Restore uploads
docker cp ./backup-uploads slideguroo-backend:/app/uploads
```

## Troubleshooting

### Issue 1: Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Issue 2: Container Fails to Start

**Check logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Common causes:**
- Missing API key in `be/.env`
- Invalid API key
- Port conflicts
- Insufficient memory

**Solution:**
```bash
# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Issue 3: API Key Not Working

**Verify environment variables:**
```bash
docker-compose exec backend env | grep API_KEY
```

**Solution:**
```bash
# Ensure .env file exists and has correct values
cat be/.env

# Restart services
docker-compose restart
```

### Issue 4: Rosetta Issues on Apple Silicon

**Error:** Platform mismatch warnings

**Solution:**
1. Open Docker Desktop
2. Go to Settings → General
3. Enable "Use Rosetta for x86/amd64 emulation on Apple Silicon"
4. Restart Docker Desktop
5. Rebuild containers:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

### Issue 5: Slow Performance

**Causes:**
- Not enough resources allocated to Docker
- Rosetta emulation overhead

**Solution:**
1. Open Docker Desktop → Settings → Resources
2. Increase CPU/Memory allocation:
   - CPUs: 4+
   - Memory: 4GB+
3. Restart Docker Desktop

### Issue 6: Frontend Can't Connect to Backend

**Check network:**
```bash
docker-compose exec frontend ping backend
```

**Solution:**
```bash
# Ensure both services are on same network
docker network ls
docker network inspect slide-guroo-ai_slideguroo-network

# Restart with fresh network
docker-compose down
docker-compose up
```

### Issue 7: Hot Reload Not Working in Dev Mode

**Solution:**
```bash
# Ensure dev override is used
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Check if volumes are mounted correctly
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec backend ls -la /app
```

## Health Checks

Services include health checks:

```bash
# Check service health
docker-compose ps

# Services should show "healthy" status
```

Health check endpoints:
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000 (HTTP 200)

## Performance Optimization

### Build Cache

Speed up builds by using cache:

```bash
# Use cache (default)
docker-compose build

# Clear cache when needed
docker-compose build --no-cache
```

### Multi-stage Builds

Frontend uses multi-stage builds for smaller images:
- Build stage: Compiles React app
- Production stage: Serves static files

### Layer Optimization

Dockerfiles are optimized:
- Dependencies installed before code copy
- Separate layers for better caching
- Minimal base images (alpine, slim)

## Production Deployment

### Security Checklist

Before deploying to production:

- [ ] Change default ports
- [ ] Use environment-specific `.env` files
- [ ] Enable HTTPS/SSL
- [ ] Set proper CORS origins
- [ ] Use secrets management (not plain text API keys)
- [ ] Enable firewall rules
- [ ] Regular updates and patches

### Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build:
      context: ./be
      dockerfile: Dockerfile
    restart: always
    environment:
      - HOST=0.0.0.0
      - PORT=8000
    env_file:
      - .env.production

  frontend:
    build:
      context: ./fe
      dockerfile: Dockerfile
    restart: always
    environment:
      - VITE_API_URL=https://api.yourdomain.com/api
```

### Using Docker Swarm or Kubernetes

For scaling, consider:
- Docker Swarm for simple orchestration
- Kubernetes for complex deployments
- Cloud services (AWS ECS, Google Cloud Run, Azure Container Instances)

## Apple Silicon Specific Notes

### Architecture

All images are built for `linux/arm64` platform:
- Native Apple Silicon support
- No Rosetta emulation needed
- Better performance and battery life

### Base Images Used

- **Backend**: `python:3.11-slim` (ARM64)
- **Frontend**: `node:18-alpine` (ARM64)

### Compatibility

If you need x86_64 compatibility (for deployment on Intel servers):

```yaml
services:
  backend:
    build:
      platform: linux/amd64  # Force x86_64
```

## Monitoring

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats slideguroo-backend
docker stats slideguroo-frontend
```

### Logs

```bash
# All logs with timestamps
docker-compose logs -f -t

# Filter by service
docker-compose logs -f backend | grep ERROR
```

## Backup and Restore

### Backup Uploads

```bash
# Create backup
docker run --rm \
  -v slide-guroo-ai_backend-uploads:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/uploads-backup.tar.gz -C /data .
```

### Restore Uploads

```bash
# Restore backup
docker run --rm \
  -v slide-guroo-ai_backend-uploads:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/uploads-backup.tar.gz -C /data
```

## FAQ

### Q: Do I need to install Python or Node.js?

**A:** No, Docker containers include all dependencies. You only need Docker Desktop.

### Q: How do I update the application?

**A:**
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Q: Can I use this on Intel Mac?

**A:** Yes, change `--platform=linux/arm64` to `--platform=linux/amd64` in Dockerfiles.

### Q: How do I access the database?

**A:** This app doesn't use a database. Lessons are generated on-demand using LLM APIs.

### Q: Can I run backend and frontend separately?

**A:** Yes:
```bash
docker-compose up backend    # Only backend
docker-compose up frontend   # Only frontend
```

### Q: How do I use a different port?

**A:** Edit `docker-compose.yml` ports section:
```yaml
ports:
  - "8080:8000"  # Maps host:8080 to container:8000
```

## Support

For Docker-specific issues:
1. Check logs: `docker-compose logs`
2. Verify environment: `cat be/.env`
3. Rebuild: `docker-compose build --no-cache`
4. Check Docker Desktop for resource issues

For application issues:
- See main README.md
- Check API documentation at http://localhost:8000/docs

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ for Apple Silicon users**
