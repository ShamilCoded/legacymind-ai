# LegacyMind AI - Git Workflow Guide

## Table of Contents
1. [Branch Strategy](#branch-strategy)
2. [Commit Conventions](#commit-conventions)
3. [Pull Request Process](#pull-request-process)
4. [Environment Management](#environment-management)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Best Practices](#best-practices)

---

## Branch Strategy

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Protected, requires PR reviews
- **Deployment**: Auto-deploys to production
- **Merge From**: `develop` only (via release PRs)

#### `develop`
- **Purpose**: Integration branch for features
- **Protection**: Protected, requires PR reviews
- **Deployment**: Auto-deploys to staging
- **Merge From**: `feature/*`, `bugfix/*`, `hotfix/*`

### Supporting Branches

#### Feature Branches: `feature/<ticket-id>-<short-description>`
```bash
# Examples:
feature/LM-123-user-authentication
feature/LM-456-risk-analysis-dashboard
```
- **Created From**: `develop`
- **Merged Into**: `develop`
- **Naming**: Use ticket ID + kebab-case description
- **Lifetime**: Delete after merge

#### Bugfix Branches: `bugfix/<ticket-id>-<short-description>`
```bash
# Examples:
bugfix/LM-789-fix-api-timeout
bugfix/LM-101-correct-chart-rendering
```
- **Created From**: `develop`
- **Merged Into**: `develop`
- **Naming**: Use ticket ID + kebab-case description
- **Lifetime**: Delete after merge

#### Hotfix Branches: `hotfix/<version>-<short-description>`
```bash
# Examples:
hotfix/1.2.1-critical-security-patch
hotfix/1.2.2-fix-production-crash
```
- **Created From**: `main`
- **Merged Into**: `main` AND `develop`
- **Naming**: Version number + description
- **Lifetime**: Delete after merge

#### Release Branches: `release/<version>`
```bash
# Examples:
release/1.0.0
release/1.1.0
```
- **Created From**: `develop`
- **Merged Into**: `main` AND `develop`
- **Purpose**: Final testing and version bumping
- **Lifetime**: Delete after merge

### Frontend/Backend Separation

#### Frontend-Specific Branches
```bash
feature/frontend-LM-123-component-library
bugfix/frontend-LM-456-styling-issue
```

#### Backend-Specific Branches
```bash
feature/backend-LM-789-api-endpoint
bugfix/backend-LM-101-database-query
```

#### Full-Stack Branches
```bash
feature/fullstack-LM-202-user-dashboard
```

---

## Commit Conventions

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies
- **ci**: CI/CD configuration changes
- **build**: Build system changes

### Scopes

#### Frontend Scopes
- `ui`: UI components
- `pages`: Page components
- `api-client`: API client code
- `styles`: Styling changes
- `config`: Configuration files

#### Backend Scopes
- `api`: API endpoints
- `services`: Service layer
- `models`: Data models
- `utils`: Utility functions
- `config`: Configuration files
- `db`: Database related

#### Shared Scopes
- `deps`: Dependencies
- `docs`: Documentation
- `tests`: Testing

### Examples

```bash
# Feature commits
feat(ui): add risk analysis dashboard component
feat(api): implement repository summarization endpoint
feat(services): add embeddings pipeline service

# Bug fix commits
fix(api-client): correct timeout handling in architecture API
fix(services): resolve memory leak in RAG chatbot
fix(ui): fix responsive layout on mobile devices

# Documentation commits
docs(readme): update installation instructions
docs(api): add API endpoint documentation

# Refactoring commits
refactor(services): extract common logic to utility functions
refactor(ui): simplify component hierarchy

# Performance commits
perf(services): optimize vector store retrieval
perf(ui): implement lazy loading for charts

# Chore commits
chore(deps): update dependencies to latest versions
chore(config): update environment variables

# CI/CD commits
ci(github-actions): add frontend build workflow
ci(github-actions): configure automated testing
```

### Commit Message Rules

1. **Subject Line**
   - Use imperative mood ("add" not "added")
   - Don't capitalize first letter
   - No period at the end
   - Max 72 characters

2. **Body** (optional)
   - Explain what and why, not how
   - Wrap at 72 characters
   - Separate from subject with blank line

3. **Footer** (optional)
   - Reference issues: `Closes #123`
   - Breaking changes: `BREAKING CHANGE: description`

### Full Example
```
feat(api): add repository analysis endpoint

Implement new endpoint for analyzing repository structure
and generating dependency graphs. Includes support for
multiple programming languages and framework detection.

- Add dependency parser service
- Implement graph generation logic
- Add comprehensive error handling

Closes #123
```

---

## Pull Request Process

### PR Title Format
```
[<type>] <scope>: <description>
```

Examples:
```
[FEAT] Frontend: Add risk analysis dashboard
[FIX] Backend: Resolve API timeout issue
[DOCS] Update Git workflow documentation
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #123

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

### PR Review Process

1. **Create PR**
   - Fill out PR template completely
   - Link related issues
   - Add appropriate labels
   - Request reviewers

2. **Code Review**
   - Minimum 1 approval required
   - Address all comments
   - Keep discussions focused

3. **CI/CD Checks**
   - All tests must pass
   - Linting must pass
   - Build must succeed

4. **Merge**
   - Use "Squash and merge" for feature branches
   - Use "Create a merge commit" for release branches
   - Delete branch after merge

---

## Environment Management

### Environment Files

#### Frontend (.env.local)
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=true

# Environment
NEXT_PUBLIC_ENV=development
```

#### Backend (.env)
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/legacymind

# AI Services
OPENAI_API_KEY=your_key_here
WATSONX_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id

# Vector Store
VECTOR_STORE_PATH=./vector_stores
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

### Environment Hierarchy

```
development → staging → production
```

#### Development
- Local development
- Debug mode enabled
- Mock data allowed
- Relaxed CORS

#### Staging
- Pre-production testing
- Production-like configuration
- Real integrations
- Limited access

#### Production
- Live environment
- Debug mode disabled
- Strict security
- Monitoring enabled

### Environment Variables Management

1. **Never commit .env files**
2. **Use .env.example as template**
3. **Document all variables**
4. **Use secrets management for production**
5. **Rotate keys regularly**

---

## CI/CD Pipeline

### GitHub Actions Workflows

#### Frontend CI/CD
```yaml
# .github/workflows/frontend-ci.yml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main, develop]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run test
      - run: cd frontend && npm run build
```

#### Backend CI/CD
```yaml
# .github/workflows/backend-ci.yml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main, develop]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest
      - run: cd backend && pylint src/
```

### Deployment Strategy

#### Staging Deployment
- **Trigger**: Push to `develop`
- **Environment**: Staging
- **Auto-deploy**: Yes
- **Approval**: Not required

#### Production Deployment
- **Trigger**: Push to `main`
- **Environment**: Production
- **Auto-deploy**: Yes (with approval)
- **Approval**: Required from maintainers

---

## Best Practices

### General Guidelines

1. **Commit Often**
   - Make small, focused commits
   - Each commit should be a logical unit
   - Easier to review and revert

2. **Write Clear Messages**
   - Follow commit conventions
   - Explain the "why" not just "what"
   - Reference issues when applicable

3. **Keep Branches Updated**
   - Regularly sync with develop
   - Resolve conflicts early
   - Rebase when appropriate

4. **Review Your Own Code**
   - Self-review before requesting reviews
   - Check for console.logs, TODOs
   - Verify tests pass locally

5. **Respect Code Reviews**
   - Respond to all comments
   - Don't take feedback personally
   - Learn from suggestions

### Frontend-Specific

1. **Component Development**
   - Create feature branches for new components
   - Include Storybook stories
   - Add unit tests

2. **Styling Changes**
   - Test across browsers
   - Verify responsive design
   - Check accessibility

3. **API Integration**
   - Mock API responses for testing
   - Handle loading and error states
   - Document API contracts

### Backend-Specific

1. **API Development**
   - Follow RESTful conventions
   - Version APIs appropriately
   - Document endpoints

2. **Database Changes**
   - Create migration scripts
   - Test rollback procedures
   - Backup before major changes

3. **Service Development**
   - Write unit tests
   - Handle errors gracefully
   - Log appropriately

### Security

1. **Never Commit Secrets**
   - Use environment variables
   - Rotate keys regularly
   - Use secrets management tools

2. **Code Review Security**
   - Check for SQL injection
   - Verify input validation
   - Review authentication logic

3. **Dependency Management**
   - Keep dependencies updated
   - Review security advisories
   - Use lock files

---

## Quick Reference

### Common Commands

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/LM-123-new-feature

# Commit changes
git add .
git commit -m "feat(scope): description"

# Push branch
git push origin feature/LM-123-new-feature

# Update branch with develop
git checkout develop
git pull origin develop
git checkout feature/LM-123-new-feature
git rebase develop

# Squash commits before PR
git rebase -i HEAD~3

# Delete merged branch
git branch -d feature/LM-123-new-feature
git push origin --delete feature/LM-123-new-feature
```

### Workflow Diagram

```
main (production)
  ↑
  └── release/1.0.0
        ↑
        └── develop (staging)
              ↑
              ├── feature/LM-123-feature-a
              ├── feature/LM-456-feature-b
              ├── bugfix/LM-789-fix-bug
              └── hotfix/1.0.1-critical-fix → main
```

---

## Support

For questions or issues with the Git workflow:
- Create an issue with label `workflow`
- Contact the development team
- Refer to this documentation

**Last Updated**: 2026-05-16
**Version**: 1.0.0