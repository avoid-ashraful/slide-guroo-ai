#!/bin/bash

# SlideGuroo Stop Script
# Stops all Docker containers

echo "🛑 Stopping SlideGuroo..."
echo ""

docker-compose down

echo ""
echo "✅ SlideGuroo has been stopped"
echo ""
echo "To start again, run: ./start.sh"
echo "or: docker-compose up"
