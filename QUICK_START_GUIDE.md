# LegacyMind AI - Quick Start Guide

## 🚀 Getting Started

This guide will help you quickly set up and run LegacyMind AI locally.

## 📋 Prerequisites

### Required Software
- **Node.js** 18+ (for Next.js)
- **Python** 3.11+ (for FastAPI)
- **Git** (for repository cloning)
- **npm** or **yarn** (package manager)
- **pip** (Python package manager)

### Required API Keys
- **OpenAI API Key** (for AI features)
- **GitHub Token** (optional, for private repos)

## 🏗️ Project Setup

### Step 1: Clone the Project

```bash
# Create project directory
mkdir legacymind-ai
cd legacymind-ai
```

### Step 2: Set Up Frontend

```bash
# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir

cd frontend

# Install dependencies
npm install framer-motion reactflow @tanstack/react-query axios clsx tailwind-merge lucide-react

# Install dev dependencies
npm install -D @types/node @types/react @types/react-dom

cd ..
```

### Step 3: Set Up Backend

```bash
# Create backend directory
mkdir backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0
langchain==0.1.0
langgraph==0.0.20
openai==1.10.0
sentence-transformers==2.3.1
faiss-cpu==1.7.4
gitpython==3.1.41
PyGithub==2.1.1
python-dotenv==1.0.0
httpx==0.26.0
aiofiles==23.2.1
python-multipart==0.0.6
EOF

# Install dependencies
pip install -r requirements.txt

cd ..
```

### Step 4: Configure Environment Variables

#### Frontend (.env.local)
```bash
cd frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
EOF
cd ..
```

#### Backend (.env)
```bash
cd backend
cat > .env << EOF
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# GitHub (optional)
GITHUB_TOKEN=your_github_token_here

# Storage
STORAGE_PATH=./app/storage
MAX_REPO_SIZE_MB=500

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# CORS
CORS_ORIGINS=http://localhost:3000

# Logging
LOG_LEVEL=INFO
EOF
cd ..
```

## 🎯 Running the Application

### Terminal 1: Start Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 📁 Project Structure Overview

```
legacymind-ai/
├── frontend/                 # Next.js application
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and API client
│   └── package.json
│
└── backend/                 # FastAPI application
    ├── app/
    │   ├── main.py         # FastAPI entry point
    │   ├── api/            # API routes
    │   ├── services/       # Business logic
    │   ├── models/         # Data models
    │   └── core/           # Configuration
    └── requirements.txt
```

## 🧪 Testing the Application

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Test Repository Analysis

1. Open `http://localhost:3000` in your browser
2. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Click "Analyze Repository"
4. Wait for analysis to complete
5. Explore the results!

## 🔧 Common Issues & Solutions

### Issue 1: Port Already in Use

**Backend (Port 8000)**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Kill the process or use a different port
uvicorn app.main:app --reload --port 8001
```

**Frontend (Port 3000)**
```bash
# Next.js will automatically try port 3001 if 3000 is busy
# Or specify a different port:
npm run dev -- -p 3001
```

### Issue 2: OpenAI API Key Not Working

1. Verify your API key is correct
2. Check if you have credits in your OpenAI account
3. Ensure the key is properly set in `.env` file
4. Restart the backend server after updating `.env`

### Issue 3: Module Not Found

**Frontend**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Backend**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### Issue 4: CORS Errors

1. Check that `CORS_ORIGINS` in backend `.env` includes your frontend URL
2. Restart the backend server
3. Clear browser cache

### Issue 5: Git Clone Fails

1. Ensure Git is installed: `git --version`
2. Check repository URL is valid
3. For private repos, add GitHub token to `.env`
4. Check disk space for cloning

## 📊 Development Workflow

### 1. Frontend Development

```bash
cd frontend

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### 2. Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/
```

## 🎨 Customization

### Change Theme Colors

Edit `frontend/tailwind.config.ts`:
```typescript
theme: {
  extend: {
    colors: {
      primary: '#667eea',
      secondary: '#764ba2',
      // Add your colors
    }
  }
}
```

### Change AI Model

Edit `backend/.env`:
```env
# Use GPT-3.5 for faster/cheaper responses
OPENAI_MODEL=gpt-3.5-turbo

# Use GPT-4 for better quality
OPENAI_MODEL=gpt-4
```

### Change Embedding Model

Edit `backend/.env`:
```env
# Smaller, faster model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Larger, more accurate model
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

```
POST   /api/v1/repositories/clone          # Clone repository
GET    /api/v1/repositories/{id}           # Get repository details
POST   /api/v1/analysis/summarize          # Generate summary
POST   /api/v1/analysis/architecture       # Analyze architecture
POST   /api/v1/analysis/dependencies       # Analyze dependencies
POST   /api/v1/analysis/risks              # Analyze risks
POST   /api/v1/chat                        # Chat with codebase
```

## 🚀 Deployment

### Deploy Frontend to Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Deploy Backend to Render

1. Create `render.yaml` in backend directory
2. Push to GitHub
3. Connect repository to Render
4. Set environment variables in Render dashboard
5. Deploy!

## 🎓 Learning Resources

### Next.js
- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js 15 App Router](https://nextjs.org/docs/app)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### LangChain
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

### FAISS
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [FAISS Tutorial](https://www.pinecone.io/learn/faiss/)

## 💡 Tips for Hackathons

1. **Start with MVP**: Get basic features working first
2. **Use Mock Data**: Test UI without waiting for AI
3. **Parallel Development**: Frontend and backend can be built simultaneously
4. **Focus on Demo**: Make the demo flow smooth
5. **Add Polish**: Animations and loading states make a big difference
6. **Test Early**: Don't wait until the end to test integration
7. **Document**: Good README helps judges understand your project

## 🆘 Getting Help

### Check Logs

**Frontend**
- Browser console (F12)
- Terminal output

**Backend**
- Terminal output
- Check `LOG_LEVEL=DEBUG` in `.env` for more details

### Debug Mode

**Frontend**
```bash
npm run dev -- --debug
```

**Backend**
```bash
uvicorn app.main:app --reload --log-level debug
```

## ✅ Checklist Before Demo

- [ ] Both servers running without errors
- [ ] Environment variables configured
- [ ] OpenAI API key working
- [ ] Can clone a public repository
- [ ] Analysis completes successfully
- [ ] Chat responds to questions
- [ ] UI looks good (no broken styles)
- [ ] Loading states work
- [ ] Error handling works
- [ ] Demo repository prepared
- [ ] Presentation ready

## 🎉 You're Ready!

You now have everything you need to build and run LegacyMind AI. Start with the basic setup, then gradually add features following the implementation plan.

Good luck with your hackathon! 🚀