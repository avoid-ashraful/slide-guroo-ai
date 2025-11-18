# SlideGuroo Docker Quick Start

**For MacBook Apple Silicon (M1/M2/M3)**

## 60-Second Setup

### 1. Install Docker Desktop

Download and install from: https://www.docker.com/products/docker-desktop/

### 2. Get API Key

Choose one:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys

### 3. Configure

```bash
cd slide-guroo-ai
cd be
cp .env.example .env
nano .env  # or use any text editor
```

Add your API key:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

### 4. Start

```bash
cd ..  # back to project root
./start.sh
```

Or manually:
```bash
docker-compose up
```

### 5. Open

http://localhost:3000

## Stop

```bash
./stop.sh
```

Or:
```bash
docker-compose down
```

## View Logs

```bash
docker-compose logs -f
```

## Restart

```bash
docker-compose restart
```

## Rebuild

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process
lsof -i :3000
lsof -i :8000
kill -9 <PID>
```

### API Key Not Working

```bash
# Verify .env file
cat be/.env

# Should contain your actual API key
# Restart containers
docker-compose restart
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Enable Rosetta (if needed)

1. Open Docker Desktop
2. Settings → General
3. Check "Use Rosetta for x86/amd64 emulation on Apple Silicon"
4. Restart Docker Desktop
5. Rebuild: `docker-compose build --no-cache`

## That's It! 🎉

For detailed documentation, see [DOCKER.md](DOCKER.md)
