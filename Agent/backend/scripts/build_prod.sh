#!/bin/bash

echo "🚀 Building CoDex Backend (Production Mode)"

# Load environment variables
export $(grep -v '^#' .env | xargs)

echo "📦 Building Docker image..."
docker build -t codex-backend-prod .

echo "🔧 Starting containers..."
docker compose -f docker-compose.yml up -d

echo "⏳ Waiting for backend to boot..."
sleep 5

echo "🔍 Checking backend health..."
curl -s http://localhost:8080/health | jq

echo "✅ Production build complete!"