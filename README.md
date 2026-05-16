# 🚀 LegacyMind AI

> AI-Powered Repository Analysis for Legacy Codebases

LegacyMind AI is a production-quality application that analyzes GitHub repositories using artificial intelligence to provide architecture insights, dependency analysis, risk assessment, and modernization recommendations.

![LegacyMind AI](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)

## ✨ Features

- 📊 **Repository Summary** - AI-generated summaries of codebase structure and purpose
- 🏗️ **Architecture Analysis** - Interactive visualization of component relationships
- 📦 **Dependency Analysis** - Identify outdated packages and security vulnerabilities
- ⚠️ **Risk Assessment** - Evaluate technical debt and maintenance complexity
- 🔄 **Modernization Suggestions** - Actionable recommendations for upgrades
- 💬 **AI Chat with Codebase** - Ask questions about your code using RAG

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Flow** - Interactive architecture graphs

### Backend
- **FastAPI** - High-performance Python web framework
- **LangGraph** - AI workflow orchestration
- **LangChain** - LLM integration and RAG
- **FAISS** - Vector similarity search
- **sentence-transformers** - Code embeddings

## 📋 Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.11+
- **Git**
- **OpenAI API Key** (for AI features)
- **GitHub Token** (optional, for private repos)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/legacymind-ai.git
cd legacymind-ai
```

### 2. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local and add your configuration
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your_key_here

# Start development server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

## 📁 Project Structure

```
legacymind-ai/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   │   ├── ui/         # Base UI components
│   │   │   └── features/   # Feature components
│   │   ├── lib/            # Utilities and API client
│   │   └── styles/         # Global styles
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── api/            # API routes
│   │   ├── services/       # Business logic
│   │   │   ├── github/    # GitHub integration
│   │   │   ├── analysis/  # Code analysis
│   │   │   ├── embeddings/# Vector embeddings
│   │   │   ├── ai/        # AI services
│   │   │   └── vector_store/ # FAISS operations
│   │   ├── models/        # Data models
│   │   ├── core/          # Configuration
│   │   └── utils/         # Utilities
│   └── requirements.txt
│
└── docs/                   # Documentation
```

## 🔧 Configuration

### Frontend Environment Variables

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend Environment Variables

```env
# .env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4

# GitHub (optional)
GITHUB_TOKEN=ghp_...

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
```

## 🎯 Usage

### Analyze a Repository

1. Open the application at `http://localhost:3000`
2. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Click "Analyze Repository"
4. Wait for the analysis to complete (typically 1-2 minutes)
5. Explore the results:
   - **Summary**: Overview of the repository
   - **Architecture**: Interactive component graph
   - **Dependencies**: Package analysis
   - **Risks**: Technical debt assessment
   - **Chat**: Ask questions about the code

### API Endpoints

```bash
# Health check
GET /health

# Clone repository
POST /api/v1/repositories/clone
{
  "url": "https://github.com/username/repo"
}

# Get repository details
GET /api/v1/repositories/{id}

# Generate summary
POST /api/v1/analysis/summarize
{
  "repository_id": "repo_id"
}

# Analyze architecture
POST /api/v1/analysis/architecture
{
  "repository_id": "repo_id"
}

# Chat with codebase
POST /api/v1/chat
{
  "repository_id": "repo_id",
  "message": "What does this repository do?"
}
```

## 🚢 Deployment

### Deploy Frontend to Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

### Deploy Backend to Render

1. Create `render.yaml` in backend directory
2. Push to GitHub
3. Connect repository to Render
4. Set environment variables
5. Deploy!

## 🧪 Testing

### Frontend Tests

```bash
cd frontend
npm run test
```

### Backend Tests

```bash
cd backend
pytest
```

## 📚 Documentation

- [Frontend Structure](./FRONTEND_STRUCTURE.md)
- [Backend Structure](./BACKEND_STRUCTURE.md)
- [Implementation Plan](./IMPLEMENTATION_PLAN.md)
- [Architecture Diagrams](./ARCHITECTURE_DIAGRAM.md)
- [Quick Start Guide](./QUICK_START_GUIDE.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain for LLM integration
- FAISS for vector search
- Next.js team for the amazing framework
- FastAPI for the high-performance backend

## 📧 Contact

- **Project Link**: [https://github.com/yourusername/legacymind-ai](https://github.com/yourusername/legacymind-ai)
- **Demo**: [https://legacymind.vercel.app](https://legacymind.vercel.app)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for hackathons and beyond**