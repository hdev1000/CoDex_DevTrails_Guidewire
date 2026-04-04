# CoDex Parametric Insurance Platform

A multi-agent, AI-driven parametric insurance engine with geospatial verification, device authenticity checks, behavioral biometrics, fraud pattern modeling, and real-time consensus decisioning.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Flutter Frontend                        │
│  - OTP Authentication                                       │
│  - Claim Submission with Sensors                            │
│  - Device Fingerprinting                                    │
│  - Image Capture                                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│  - RESTful API                                              │
│  - JWT Authentication                                       │
│  - Rate Limiting                                            │
│  - Multi-Agent Consensus Engine                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent Ensemble                        │
│  - Geo Agent (Location Verification)                        │
│  - Device Agent (Device Integrity)                          │
│  - Image Agent (Visual Evidence Analysis)                   │
│  - LLM Agent (Contextual Reasoning)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  - MongoDB (Claims Storage)                                 │
│  - Redis (Caching & Fraud Patterns)                         │
└─────────────────────────────────────────────────────────────┘
```

## Features

### Backend
- JWT-based authentication with OTP verification
- Multi-agent consensus engine (deterministic + LLM + ensemble)
- Fraud detection modules:
  - Behavior clustering
  - Signature pattern matching
  - Heuristic anomaly detection
- Device fingerprinting and IMEI tracking
- Rate limiting and abuse detection
- Redis caching and episodic memory
- MongoDB persistence

### AI Agent Ensemble
- **Geo Agent**: Validates location data, detects GPS spoofing
- **Device Agent**: Checks device integrity, VPN/TOR detection
- **Image Agent**: Analyzes visual evidence for fraud patterns
- **LLM Agent**: Contextual reasoning with OpenAI integration

### Flutter Frontend
- OTP-based authentication
- Device fingerprinting
- Sensor data collection (accelerometer, gyroscope, GPS)
- Image capture and upload
- Claim submission with auto-sensor capture
- Claims history and status display
- Multi-language support (English, Hindi, Malayalam)

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ (for Flutter)
- Docker & Docker Compose
- MongoDB 6+
- Redis 7+

### Backend Setup

1. Clone the repository:
```bash
cd "GITHUB/Agent"
```

2. Create `.env` file from template:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration:
```env
MONGO_URI=mongodb://localhost:27017/codex
REDIS_HOST=localhost
JWT_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-key
```

4. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

5. Run the backend:
```bash
uvicorn main:app --reload --port 8080
```

### Flutter Frontend Setup

1. Navigate to the Flutter directory:
```bash
cd Frontend/gig_protect
```

2. Install dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
flutter run
```

### Docker Deployment

1. Build and run all services:
```bash
docker-compose up --build
```

2. Access the backend at `http://localhost:8080`
3. Access the Flutter app on your device/emulator

## API Endpoints

### Authentication
- `POST /auth/request_otp` - Request OTP
- `POST /auth/verify_otp` - Verify OTP and get tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout user

### Claims
- `POST /claims/submit` - Submit a new claim
- `GET /claims/list?user_id={id}` - List user claims
- `GET /claims/{claim_id}` - Get claim details
- `GET /claims/status/{claim_id}` - Get claim status

### Fraud Detection
- `POST /fraud/risk-check` - Check fraud risk
- `POST /fraud/cluster` - Analyze behavior cluster

### System
- `GET /system/health` - Health check
- `GET /system/config` - Get configuration

## Project Structure

```
GITHUB/Agent/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── claim_routes.py
│   │   ├── device_routes.py
│   │   ├── fraud_routes.py
│   │   ├── health_routes.py
│   │   ├── identity_routes.py
│   │   ├── payout_routes.py
│   │   └── system_routes.py
│   ├── models/
│   │   └── claim.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── claim_service.py
│   │   ├── multi_agent_orchestrator.py
│   │   ├── consensus_v3.py
│   │   ├── consensus_engine.py
│   │   ├── deterministic_rules.py
│   │   ├── llm_reasoner.py
│   │   ├── redis_client.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── geo_agent.py
│   │   │   ├── device_agent.py
│   │   │   ├── image_agent.py
│   │   │   └── llm_agent.py
│   │   ├── fraud/
│   │   │   ├── __init__.py
│   │   │   ├── signature_engine.py
│   │   │   ├── behavior_cluster.py
│   │   │   └── heuristics.py
│   │   └── security/
│   │       ├── __init__.py
│   │       ├── jwt_manager.py
│   │       ├── identity_guard.py
│   │       ├── device_fingerprint.py
│   │       ├── rate_limit.py
│   │       └── abuse_detector.py
│   └── utils/
│       └── response.py
├── Frontend/
│   └── gig_protect/
│       ├── lib/
│       │   ├── main.dart
│       │   ├── models/
│       │   │   ├── claim_model.dart
│       │   │   └── response_model.dart
│       │   ├── services/
│       │   │   ├── auth_service.dart
│       │   │   ├── sensor_service.dart
│       │   │   ├── location_service.dart
│       │   │   └── image_service.dart
│       │   ├── core/
│       │   │   ├── api/
│       │   │   │   ├── api_client.dart
│       │   │   │   ├── api_endpoints.dart
│       │   │   │   └── claim_repository.dart
│       │   │   └── utils/
│       │   │       ├── auth_utils.dart
│       │   │       ├── device_info.dart
│       │   │       ├── sensor_utils.dart
│       │   │       ├── validation_utils.dart
│       │   │       └── exception_handler.dart
│       │   ├── screens/
│       │   │   ├── language_selection_screen.dart
│       │   │   ├── login_screen.dart
│       │   │   ├── otp_screen.dart
│       │   │   ├── profile_setup_screen.dart
│       │   │   ├── dashboard_screen.dart
│       │   │   └── subscription_plans.dart
│       │   ├── theme/
│       │   │   └── app_theme.dart
│       │   └── l10n/
│       │       ├── app_en.arb
│       │       ├── app_hi.arb
│       │       └── app_ml.arb
│       └── pubspec.yaml
└── docker-compose.yml
```

## Deployment

### Render Deployment

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your repository
4. Set the build command: `cd backend && pip install -r requirements.txt`
5. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env`
7. Deploy!

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ENV` | Environment (development/production) | Yes |
| `MONGO_URI` | MongoDB connection string | Yes |
| `REDIS_HOST` | Redis host | Yes |
| `REDIS_PORT` | Redis port | Yes |
| `JWT_SECRET` | JWT signing secret | Yes |
| `LLM_PROVIDER` | LLM provider (openai) | Yes |
| `LLM_MODEL` | LLM model name | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |

## Security Features

- JWT-based authentication with refresh tokens
- Rate limiting (user, IP, claim-level)
- Device fingerprinting
- IMEI tracking and rotation detection
- OTP abuse detection
- VPN/TOR detection
- GPS spoofing detection
- Fraud signature pattern matching

## AI Agent Scoring

Each agent returns a score (0.0-1.0) and confidence level:
- **Geo Agent**: Location validity, timestamp sanity
- **Device Agent**: VPN/TOR detection, emulator detection
- **Image Agent**: Image count, fraud pattern matching
- **LLM Agent**: Contextual reasoning with OpenAI

Final decision uses weighted consensus:
- 60% Multi-agent score
- 25% Fraud score
- 15% Identity risk

## License

MIT License - See LICENSE file for details.
