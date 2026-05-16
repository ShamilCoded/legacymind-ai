# Environment Setup Guide

## Table of Contents
1. [Overview](#overview)
2. [Environment Variables](#environment-variables)
3. [Frontend Setup](#frontend-setup)
4. [Backend Setup](#backend-setup)
5. [Environment Hierarchy](#environment-hierarchy)
6. [Security Best Practices](#security-best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

LegacyMind AI uses environment-specific configurations to manage different deployment stages. This guide covers setting up and managing environment variables for development, staging, and production environments.

### Environment Types

- **Development**: Local development environment
- **Staging**: Pre-production testing environment
- **Production**: Live production environment

---

## Environment Variables

### Frontend Environment Variables

#### Required Variables

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# Environment
NEXT_PUBLIC_ENV=development
```

#### Optional Variables

```bash
# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=true
NEXT_PUBLIC_ENABLE_MOCK_DATA=true

# Analytics (if enabled)
NEXT_PUBLIC_GA_TRACKING_ID=
NEXT_PUBLIC_MIXPANEL_TOKEN=

# Error Tracking
NEXT_PUBLIC_SENTRY_DSN=
```

### Backend Environment Variables

#### Required Variables

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# AI Services
OPENAI_API_KEY=your_openai_key_here
WATSONX_API_KEY=your_watsonx_key_here
WATSONX_PROJECT_ID=your_project_id_here

# Environment
ENVIRONMENT=development
```

#### Optional Variables

```bash
# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost:5432/legacymind

# Vector Store
VECTOR_STORE_PATH=./vector_stores
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# Cache
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=.py,.js,.ts,.java,.cpp,.c,.h

# Error Tracking
SENTRY_DSN=
```

---

## Frontend Setup

### 1. Create Environment File

```bash
cd frontend
cp .env.example .env.local
```

### 2. Configure Variables

Edit `.env.local` with your settings:

```bash
# Development
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_ENABLE_DEBUG=true
```

### 3. Environment-Specific Files

Create separate files for different environments:

#### `.env.development`
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_ENABLE_DEBUG=true
NEXT_PUBLIC_ENABLE_MOCK_DATA=true
```

#### `.env.staging`
```bash
NEXT_PUBLIC_API_URL=https://api-staging.legacymind.ai
NEXT_PUBLIC_ENV=staging
NEXT_PUBLIC_ENABLE_DEBUG=false
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

#### `.env.production`
```bash
NEXT_PUBLIC_API_URL=https://api.legacymind.ai
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_ENABLE_DEBUG=false
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_GA_TRACKING_ID=UA-XXXXXXXXX-X
```

### 4. Verify Setup

```bash
npm run dev
```

Check console for environment variables:
```javascript
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);
console.log('Environment:', process.env.NEXT_PUBLIC_ENV);
```

---

## Backend Setup

### 1. Create Environment File

```bash
cd backend
cp .env.example .env
```

### 2. Configure Variables

Edit `.env` with your settings:

```bash
# Development
HOST=0.0.0.0
PORT=8000
DEBUG=True
ENVIRONMENT=development

# AI Services (REQUIRED)
OPENAI_API_KEY=sk-...
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id

# Security
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Environment-Specific Files

#### `.env.development`
```bash
HOST=0.0.0.0
PORT=8000
DEBUG=True
ENVIRONMENT=development

OPENAI_API_KEY=sk-...
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id

SECRET_KEY=dev-secret-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

LOG_LEVEL=DEBUG
VECTOR_STORE_PATH=./vector_stores
```

#### `.env.staging`
```bash
HOST=0.0.0.0
PORT=8000
DEBUG=False
ENVIRONMENT=staging

OPENAI_API_KEY=sk-...
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id

DATABASE_URL=postgresql://user:pass@staging-db:5432/legacymind
SECRET_KEY=staging-secret-key-from-secrets-manager
ALLOWED_ORIGINS=https://staging.legacymind.ai

LOG_LEVEL=INFO
SENTRY_DSN=https://...
RATE_LIMIT_ENABLED=True
```

#### `.env.production`
```bash
HOST=0.0.0.0
PORT=8000
DEBUG=False
ENVIRONMENT=production

OPENAI_API_KEY=sk-...
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id

DATABASE_URL=postgresql://user:pass@prod-db:5432/legacymind
SECRET_KEY=production-secret-key-from-secrets-manager
ALLOWED_ORIGINS=https://legacymind.ai

LOG_LEVEL=WARNING
SENTRY_DSN=https://...
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=30
```

### 4. Verify Setup

```bash
python start_server.py
```

Check logs for configuration:
```
INFO: Environment: development
INFO: Debug mode: True
INFO: Allowed origins: ['http://localhost:3000']
```

---

## Environment Hierarchy

### Loading Order

1. **System Environment Variables** (highest priority)
2. **`.env.local`** (local overrides, not committed)
3. **`.env.[environment]`** (environment-specific)
4. **`.env`** (default values)

### Frontend Loading

Next.js loads environment variables in this order:
1. `.env.production.local` (production only)
2. `.env.local` (all environments except test)
3. `.env.production` / `.env.development` / `.env.test`
4. `.env`

### Backend Loading

Python loads environment variables in this order:
1. System environment variables
2. `.env` file (using python-dotenv)

---

## Security Best Practices

### 1. Never Commit Secrets

```bash
# ❌ NEVER DO THIS
git add .env
git commit -m "Add environment variables"

# ✅ DO THIS
# Ensure .env is in .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.*.local" >> .gitignore
```

### 2. Use Secrets Management

#### Development
- Use `.env.local` for local secrets
- Share `.env.example` with team

#### Staging/Production
- Use cloud secrets manager (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- Use GitHub Secrets for CI/CD
- Rotate keys regularly

### 3. Validate Environment Variables

#### Frontend
```typescript
// src/lib/config.ts
const requiredEnvVars = [
  'NEXT_PUBLIC_API_URL',
  'NEXT_PUBLIC_ENV',
];

requiredEnvVars.forEach((envVar) => {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
});

export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  environment: process.env.NEXT_PUBLIC_ENV!,
  enableDebug: process.env.NEXT_PUBLIC_ENABLE_DEBUG === 'true',
};
```

#### Backend
```python
# backend/config.py
import os
from typing import Optional

class Config:
    # Required
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    WATSONX_API_KEY: str = os.getenv('WATSONX_API_KEY', '')
    WATSONX_PROJECT_ID: str = os.getenv('WATSONX_PROJECT_ID', '')
    
    # Optional with defaults
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    @classmethod
    def validate(cls):
        required = ['OPENAI_API_KEY', 'WATSONX_API_KEY', 'WATSONX_PROJECT_ID']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Validate on import
Config.validate()
```

### 4. Separate Public and Private Variables

#### Frontend
- **Public** (NEXT_PUBLIC_*): Exposed to browser
- **Private**: Server-side only

```bash
# ✅ Safe to expose
NEXT_PUBLIC_API_URL=https://api.example.com

# ❌ NEVER expose
API_SECRET_KEY=secret123
```

### 5. Use Different Keys per Environment

```bash
# Development
OPENAI_API_KEY=sk-dev-...

# Staging
OPENAI_API_KEY=sk-staging-...

# Production
OPENAI_API_KEY=sk-prod-...
```

---

## Troubleshooting

### Frontend Issues

#### Environment Variables Not Loading

**Problem**: Variables are undefined in the browser

**Solution**:
1. Ensure variables start with `NEXT_PUBLIC_`
2. Restart dev server after changing `.env` files
3. Clear `.next` cache: `rm -rf .next`

```bash
rm -rf .next
npm run dev
```

#### CORS Errors

**Problem**: API requests blocked by CORS

**Solution**:
1. Check `NEXT_PUBLIC_API_URL` is correct
2. Verify backend `ALLOWED_ORIGINS` includes frontend URL
3. Check browser console for exact error

### Backend Issues

#### Missing Environment Variables

**Problem**: `KeyError` or `None` values

**Solution**:
1. Verify `.env` file exists
2. Check variable names (case-sensitive)
3. Ensure `python-dotenv` is installed

```bash
pip install python-dotenv
```

#### API Key Errors

**Problem**: 401/403 errors from AI services

**Solution**:
1. Verify API keys are correct
2. Check key permissions
3. Ensure keys are not expired
4. Test keys with curl:

```bash
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### Port Already in Use

**Problem**: `Address already in use` error

**Solution**:
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
PORT=8001 python start_server.py
```

### General Issues

#### Environment Not Detected

**Problem**: Wrong environment loaded

**Solution**:
1. Check `ENVIRONMENT` variable
2. Verify correct `.env` file is loaded
3. Check environment variable precedence

```bash
# Print all environment variables
printenv | grep ENVIRONMENT  # macOS/Linux
set | findstr ENVIRONMENT  # Windows
```

#### Secrets Not Working in CI/CD

**Problem**: GitHub Actions failing due to missing secrets

**Solution**:
1. Add secrets in GitHub repository settings
2. Reference secrets in workflow:

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

---

## Quick Reference

### Frontend Commands

```bash
# Development
npm run dev

# Staging
npm run build && npm run start

# Production
npm run build && npm run start
```

### Backend Commands

```bash
# Development
python start_server.py

# With specific environment
ENVIRONMENT=staging python start_server.py

# Production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.app:app
```

### Environment File Locations

```
project-root/
├── .env                          # Root defaults (not committed)
├── .env.example                  # Template (committed)
├── frontend/
│   ├── .env.local               # Local overrides (not committed)
│   ├── .env.development         # Development (committed)
│   ├── .env.staging             # Staging (committed)
│   ├── .env.production          # Production (committed)
│   └── .env.example             # Template (committed)
└── backend/
    ├── .env                     # Local config (not committed)
    ├── .env.development         # Development (committed)
    ├── .env.staging             # Staging (committed)
    ├── .env.production          # Production (committed)
    └── .env.example             # Template (committed)
```

---

## Support

For environment setup issues:
- Check this documentation
- Review `.env.example` files
- Create an issue with label `environment`
- Contact the development team

**Last Updated**: 2026-05-16
**Version**: 1.0.0