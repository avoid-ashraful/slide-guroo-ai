#!/bin/bash

# SlideGuroo Quick Start Script for Docker
# Works on MacBook Apple Silicon (M1/M2/M3)

set -e

echo "🚀 SlideGuroo - Starting Application with Docker"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Check if .env file exists
if [ ! -f "be/.env" ]; then
    echo "⚠️  Environment file not found!"
    echo "Creating .env file from template..."
    cp be/.env.example be/.env
    echo ""
    echo "⚠️  IMPORTANT: You need to add your API key to be/.env"
    echo ""
    echo "Please edit be/.env and add your OpenAI or Anthropic API key:"
    echo "  - For OpenAI: Set LLM_PROVIDER=openai and add OPENAI_API_KEY"
    echo "  - For Anthropic: Set LLM_PROVIDER=anthropic and add ANTHROPIC_API_KEY"
    echo ""
    echo "Get your API key from:"
    echo "  - OpenAI: https://platform.openai.com/api-keys"
    echo "  - Anthropic: https://console.anthropic.com/settings/keys"
    echo ""
    read -p "Press Enter after you've added your API key to be/.env..."
fi

# Check if API key is set
if ! grep -q "OPENAI_API_KEY=sk-" be/.env && ! grep -q "ANTHROPIC_API_KEY=sk-ant-" be/.env; then
    echo ""
    echo "⚠️  WARNING: No valid API key found in be/.env"
    echo "The application will not work without an API key!"
    echo ""
    read -p "Do you want to continue anyway? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting. Please add your API key to be/.env and run this script again."
        exit 1
    fi
fi

echo ""
echo "🐳 Starting Docker containers..."
echo ""

# Start services
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Services started successfully!"
    echo ""
    echo "📱 Access your application:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo ""
    echo "📋 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop app: docker-compose down"
    echo "   - Restart app: docker-compose restart"
    echo ""
    echo "🎉 Happy learning with SlideGuroo!"
    echo ""

    # Ask if user wants to view logs
    read -p "Do you want to view the logs? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose logs -f
    fi
else
    echo ""
    echo "❌ Failed to start services!"
    echo "Check the logs with: docker-compose logs"
    exit 1
fi
