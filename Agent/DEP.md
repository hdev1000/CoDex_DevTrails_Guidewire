# CoDex Platform - Deployment Guide

This document provides step-by-step instructions for deploying the CoDex Parametric Insurance Platform.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Flutter Frontend Deployment](#flutter-frontend-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Render Deployment](#render-deployment)
7. [Post-Deployment Verification](#post-deployment-verification)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Flutter tooling |
| Flutter | 3.11+ | Frontend framework |
| Docker | 24+ | Containerization |
| Docker Compose | 2.20+ | Multi-container orchestration |
| MongoDB | 6+ | Database |
| Redis | 7+ | Caching |

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 10GB free
- **Network**: Stable internet connection

---

## Environment Setup

### 1. Clone the Repository

```bash
cd "GITHUB/Agent"
```

### 2. Create Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` with your values:

```env
# Environment Configuration
ENV=production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/codex
MONGO_DB=codex
CLAIMS_COLLECTION=claims

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGO=HS256
JWT_ACCESS_EXP=3600
JWT_REFRESH_EXP=86400
OTP_EXPIRY_SEC=180

# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-openai-api-key-here

# Security
ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,http://10.0.2.2,https://your-render-url

# Rate Limiting
RATE_LIMIT_MAX_REQ=10
RATE_LIMIT_WINDOW_SEC=60

# H3 Geo Settings
H3_RESOLUTION=9
```

### 4. Generate JWT Secret

```bash
# Generate a secure random secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the output as your `JWT_SECRET`.

---

## Backend Deployment

### Option A: Direct Deployment (Development)

#### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 2. Start MongoDB

```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:6

# Or use your local MongoDB installation
mongod --dbpath /path/to/data
```

#### 3. Start Redis

```bash
# Using Docker
docker run -d -p 6379:6379 --name redis redis:7

# Or use your local Redis installation
redis-server
```

#### 4. Run the Backend

```bash
# Development mode with auto-reload
uvicorn main:app --reload --port 8080

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8080
```

#### 5. Verify Backend is Running

```bash
curl http://localhost:8080/
# Expected response: {"status": "backend running", "env": "production"}
```

### Option B: Docker Deployment (Recommended)

#### 1. Build Backend Image

```bash
cd backend
docker build -t codex-backend .
```

#### 2. Run Backend Container

```bash
docker run -d \
  --name codex-backend \
  --env-file ../.env \
  -p 8080:8080 \
  --link mongodb:mongodb \
  --link redis:redis \
  codex-backend
```

---

## Flutter Frontend Deployment

### Prerequisites

1. Install Flutter SDK: https://docs.flutter.dev/get-started/install
2. Configure Android/iOS development environment

### Deployment Steps

#### 1. Install Dependencies

```bash
cd Frontend/gig_protect
flutter pub get
```

#### 2. Configure API Endpoint

Update `lib/core/api/api_endpoints.dart` with your backend URL:

```dart
class ApiEndpoints {
  // For local development
  static const String baseUrl = "http://10.0.2.2:8080";  // Android emulator
  
  // For iOS simulator
  // static const String baseUrl = "http://localhost:8080";
  
  // For production
  // static const String baseUrl = "https://your-backend-url.com";
}
```

#### 3. Build for Android

```bash
# Debug build
flutter build apk --debug

# Release build
flutter build apk --release

# App bundle
flutter build appbundle --release
```

#### 4. Build for iOS

```bash
# Debug build
flutter build ios --debug

# Release build
flutter build ios --release --no-codesign
```

#### 5. Run on Device

```bash
# List connected devices
flutter devices

# Run on device
flutter run
```

---

## Docker Deployment

### 1. Update docker-compose.yml

Ensure your `docker-compose.yml` has the correct configuration:

```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    container_name: codex-backend
    restart: always
    env_file:
      - .env
    ports:
      - "8080:8080"
    depends_on:
      - mongo
      - redis
    environment:
      - PYTHONUNBUFFERED=1

  mongo:
    image: mongo:6
    container_name: codex-mongo
    restart: always
    volumes:
      - mongo_data:/data/db
    ports:
      - "27017:27017"

  redis:
    image: redis:7
    container_name: codex-redis
    restart: always
    ports:
      - "6379:6379"

volumes:
  mongo_data:
```

### 2. Build and Start Services

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 3. Verify Services

```bash
# Check backend health
curl http://localhost:8080/

# Check MongoDB
docker exec -it codex-mongo mongosh --eval "db.adminCommand('ping')"

# Check Redis
docker exec -it codex-redis redis-cli ping
```

### 4. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Render Deployment

### 1. Prepare Repository

```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Create Render Account

1. Go to https://render.com
2. Sign up or log in
3. Verify your email

### 3. Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the `GITHUB/Agent` repository

### 4. Configure Service

**Basic Settings:**
- Name: `codex-backend`
- Region: Choose closest region
- Branch: `main`
- Root Directory: `backend`

**Build Settings:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment:**
Add the following environment variables:

| Variable | Value |
|----------|-------|
| `ENV` | `production` |
| `MONGO_URI` | Your MongoDB connection string |
| `REDIS_HOST` | Your Redis host |
| `REDIS_PORT` | `6379` |
| `JWT_SECRET` | Your generated JWT secret |
| `LLM_PROVIDER` | `openai` |
| `LLM_MODEL` | `gpt-4o-mini` |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `ALLOWED_ORIGINS` | Your Flutter app URL |

### 5. Create MongoDB Service

1. Click "New +" → "PostgreSQL"
2. Name: `codex-mongo`
3. Select "MongoDB" database type
4. Copy the connection string

### 6. Create Redis Service

1. Click "New +" → "Redis"
2. Name: `codex-redis`
3. Copy the connection details

### 7. Update Environment Variables

Update the backend service with MongoDB and Redis connection strings:

```bash
# Update MongoDB URI
MONGO_URI=mongodb://<username>:<password>@<host>:<port>/codex

# Update Redis connection
REDIS_HOST=<redis-host>
REDIS_PORT=6379
```

### 8. Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Access your backend at `https://your-service.onrender.com`

### 9. Update Flutter API Endpoint

Update `lib/core/api/api_endpoints.dart`:

```dart
class ApiEndpoints {
  static const String baseUrl = "https://your-backend-url.onrender.com";
}
```

---

## Post-Deployment Verification

### Backend Verification

#### 1. Health Check

```bash
curl https://your-backend-url.onrender.com/
```

Expected response:
```json
{
  "status": "backend running",
  "env": "production"
}
```

#### 2. Test Authentication

```bash
# Request OTP
curl -X POST https://your-backend-url.onrender.com/auth/request_otp \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919876543210"}'

# Verify OTP (after receiving it)
curl -X POST https://your-backend-url.onrender.com/auth/verify_otp \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "otp": "123456"
  }'
```

#### 3. Test Claim Submission

```bash
curl -X POST https://your-backend-url.onrender.com/claims/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "phone_number": "+919876543210",
    "incident_type": "Waterlogging",
    "timestamp": 1712200000,
    "location": {"lat": 12.9716, "lng": 77.5946},
    "images": [],
    "device_info": {
      "model": "Test Device",
      "emulator": false
    },
    "network_info": {
      "ip": "127.0.0.1"
    }
  }'
```

### Frontend Verification

#### 1. Test Login Flow

1. Open the Flutter app
2. Enter phone number
3. Verify OTP
4. Complete profile setup
5. Navigate to dashboard

#### 2. Test Claim Submission

1. Click "Trigger Instant AI Claim"
2. Verify sensor data collection
3. Check claim submission success
4. Verify AI decision is displayed

#### 3. Test Claims History

1. Navigate to claims history
2. Verify past claims are displayed
3. Check claim status and payout amounts

---

## Troubleshooting

### Backend Issues

#### 1. Connection Refused

**Problem**: `ConnectionRefusedError: [Errno 111] Connection refused`

**Solution**:
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# Check if Redis is running
docker ps | grep redis

# Restart services
docker-compose restart
```

#### 2. JWT Token Errors

**Problem**: `Invalid token` or `Token has expired`

**Solution**:
```bash
# Verify JWT_SECRET is set correctly
echo $JWT_SECRET

# Regenerate if needed
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 3. LLM API Errors

**Problem**: `OpenAI API key not found`

**Solution**:
```bash
# Verify OPENAI_API_KEY is set
echo $OPENAI_API_KEY

# Add to .env if missing
echo "OPENAI_API_KEY=your-key-here" >> .env
```

### Frontend Issues

#### 1. API Connection Failed

**Problem**: `Cannot connect to server`

**Solution**:
```dart
// Update API endpoint in api_endpoints.dart
// For Android emulator: http://10.0.2.2:8080
// For iOS simulator: http://localhost:8080
// For production: https://your-backend-url.com
```

#### 2. Permission Denied

**Problem**: Location or sensor permissions denied

**Solution**:
```bash
# Android: Check AndroidManifest.xml
# iOS: Check Info.plist for permission keys
```

#### 3. Build Errors

**Problem**: `Flutter build failed`

**Solution**:
```bash
# Clean build
flutter clean
flutter pub get
flutter build apk --release
```

### Docker Issues

#### 1. Container Won't Start

**Problem**: `Container exited with code 1`

**Solution**:
```bash
# Check logs
docker-compose logs backend

# Check environment variables
docker-compose exec backend env
```

#### 2. Volume Permission Issues

**Problem**: `Permission denied` for data volumes

**Solution**:
```bash
# Fix permissions
docker-compose down -v
docker-compose up -d
```

### Render Issues

#### 1. Build Failed

**Problem**: `Build failed` on Render

**Solution**:
- Check build logs in Render dashboard
- Ensure `requirements.txt` is in `backend/` directory
- Verify all dependencies are listed

#### 2. Service Unavailable

**Problem**: `503 Service Unavailable`

**Solution**:
- Check if MongoDB/Redis services are connected
- Verify environment variables are set
- Check service logs in Render dashboard

---

## Maintenance

### Backup Database

```bash
# MongoDB backup
docker exec -it codex-mongo mongodump --out /data/backup

# Copy backup
docker cp codex-mongo:/data/backup ./backup
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build
```

### View Logs

```bash
# Backend logs
docker-compose logs -f backend

# MongoDB logs
docker-compose logs -f mongo

# Redis logs
docker-compose logs -f redis
```

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify environment variables are set correctly
4. Ensure all services are running

---

**Last Updated**: April 4, 2026
**Version**: 1.0.0
