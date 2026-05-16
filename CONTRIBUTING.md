# Contributing to LegacyMind AI

Thank you for your interest in contributing to LegacyMind AI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Submitting Changes](#submitting-changes)
8. [Review Process](#review-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Trolling or insulting comments
- Publishing others' private information
- Any conduct that could be considered inappropriate

---

## Getting Started

### Prerequisites

**Frontend:**
- Node.js 18+ and npm
- Basic knowledge of React, Next.js, and TypeScript

**Backend:**
- Python 3.11+
- Basic knowledge of FastAPI and Python

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/legacymind-ai.git
   cd legacymind-ai
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/legacymind-ai.git
   ```

4. **Set up frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your settings
   npm run dev
   ```

5. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your settings
   python start_server.py
   ```

---

## Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
# Update your local develop branch
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/LM-123-your-feature-name

# Or bugfix branch
git checkout -b bugfix/LM-456-fix-description
```

### 2. Make Changes

- Write clean, readable code
- Follow coding standards
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Changes

Follow our commit message conventions:

```bash
# Stage changes
git add .

# Commit with proper message
git commit -m "feat(scope): add new feature"
```

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for detailed commit conventions.

### 4. Keep Branch Updated

Regularly sync with upstream:

```bash
git fetch upstream
git rebase upstream/develop
```

### 5. Push Changes

```bash
git push origin feature/LM-123-your-feature-name
```

### 6. Create Pull Request

1. Go to GitHub and create a Pull Request
2. Fill out the PR template completely
3. Link related issues
4. Request reviewers
5. Wait for CI/CD checks to pass

---

## Coding Standards

### Frontend Standards

#### TypeScript

```typescript
// ✅ Good
interface UserProps {
  name: string;
  email: string;
  role: 'admin' | 'user';
}

export const UserCard: React.FC<UserProps> = ({ name, email, role }) => {
  return (
    <div className="user-card">
      <h3>{name}</h3>
      <p>{email}</p>
      <span>{role}</span>
    </div>
  );
};

// ❌ Bad
export const UserCard = (props: any) => {
  return <div>{props.name}</div>;
};
```

#### Component Structure

```typescript
// 1. Imports
import React from 'react';
import { Button } from '@/components/ui/button';

// 2. Types/Interfaces
interface ComponentProps {
  title: string;
}

// 3. Component
export const Component: React.FC<ComponentProps> = ({ title }) => {
  // 4. Hooks
  const [state, setState] = React.useState('');

  // 5. Handlers
  const handleClick = () => {
    setState('clicked');
  };

  // 6. Render
  return (
    <div>
      <h1>{title}</h1>
      <Button onClick={handleClick}>Click</Button>
    </div>
  );
};
```

#### Naming Conventions

- **Components**: PascalCase (`UserCard`, `RiskDashboard`)
- **Files**: kebab-case (`user-card.tsx`, `risk-dashboard.tsx`)
- **Functions**: camelCase (`handleClick`, `fetchData`)
- **Constants**: UPPER_SNAKE_CASE (`API_URL`, `MAX_RETRIES`)

### Backend Standards

#### Python

```python
# ✅ Good
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    """User model with validation."""
    name: str
    email: str
    role: str

def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Retrieve user by ID.
    
    Args:
        user_id: The user's unique identifier
        
    Returns:
        User object if found, None otherwise
    """
    # Implementation
    pass

# ❌ Bad
def get_user(id):
    # No type hints, no docstring
    pass
```

#### Code Organization

```python
# 1. Standard library imports
import os
from typing import List, Optional

# 2. Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 3. Local imports
from src.services.user_service import UserService
from src.utils.logger import logger

# 4. Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 5. Classes and functions
class UserAPI:
    """User API endpoints."""
    
    def __init__(self):
        self.service = UserService()
    
    async def get_user(self, user_id: int) -> dict:
        """Get user by ID."""
        return await self.service.get_user(user_id)
```

#### Naming Conventions

- **Classes**: PascalCase (`UserService`, `RiskAnalyzer`)
- **Files**: snake_case (`user_service.py`, `risk_analyzer.py`)
- **Functions**: snake_case (`get_user`, `analyze_risk`)
- **Constants**: UPPER_SNAKE_CASE (`API_KEY`, `MAX_SIZE`)

### General Standards

#### Code Quality

- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It
- **SOLID**: Follow SOLID principles

#### Comments

```typescript
// ✅ Good - Explain WHY, not WHAT
// Use debounce to prevent excessive API calls during typing
const debouncedSearch = debounce(searchFunction, 300);

// ❌ Bad - Obvious comment
// Set the value to 5
const value = 5;
```

#### Error Handling

```typescript
// ✅ Good
try {
  const data = await fetchData();
  return data;
} catch (error) {
  logger.error('Failed to fetch data:', error);
  throw new Error('Data fetch failed');
}

// ❌ Bad
try {
  const data = await fetchData();
  return data;
} catch (error) {
  console.log(error);
}
```

---

## Testing Guidelines

### Frontend Testing

#### Unit Tests

```typescript
// component.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

#### Integration Tests

```typescript
// api.test.ts
import { fetchUserData } from './api';

describe('API Integration', () => {
  it('fetches user data successfully', async () => {
    const data = await fetchUserData(1);
    expect(data).toHaveProperty('name');
    expect(data).toHaveProperty('email');
  });
});
```

### Backend Testing

#### Unit Tests

```python
# test_user_service.py
import pytest
from src.services.user_service import UserService

@pytest.fixture
def user_service():
    return UserService()

def test_get_user_by_id(user_service):
    """Test retrieving user by ID."""
    user = user_service.get_user_by_id(1)
    assert user is not None
    assert user.id == 1

def test_get_nonexistent_user(user_service):
    """Test retrieving non-existent user."""
    user = user_service.get_user_by_id(9999)
    assert user is None
```

#### Integration Tests

```python
# test_api.py
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_get_user_endpoint():
    """Test user endpoint."""
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert "name" in response.json()
```

### Test Coverage

- Aim for **80%+ code coverage**
- All new features must include tests
- Bug fixes should include regression tests

---

## Documentation

### Code Documentation

#### Frontend

```typescript
/**
 * Fetches user data from the API.
 * 
 * @param userId - The unique identifier of the user
 * @param options - Optional fetch configuration
 * @returns Promise resolving to user data
 * @throws {Error} If the API request fails
 * 
 * @example
 * ```typescript
 * const user = await fetchUserData(123);
 * console.log(user.name);
 * ```
 */
export async function fetchUserData(
  userId: number,
  options?: RequestOptions
): Promise<User> {
  // Implementation
}
```

#### Backend

```python
def analyze_risk(code: str, language: str) -> RiskAnalysis:
    """
    Analyze code for potential risks.
    
    Args:
        code: The source code to analyze
        language: Programming language of the code
        
    Returns:
        RiskAnalysis object containing detected risks
        
    Raises:
        ValueError: If language is not supported
        
    Example:
        >>> analysis = analyze_risk("print('hello')", "python")
        >>> print(analysis.risk_score)
        0.2
    """
    # Implementation
```

### README Updates

Update relevant README files when:
- Adding new features
- Changing APIs
- Modifying setup procedures
- Adding dependencies

---

## Submitting Changes

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with develop
- [ ] PR template is filled out completely
- [ ] No merge conflicts
- [ ] CI/CD checks pass

### PR Title Format

```
[TYPE] Scope: Brief description

Examples:
[FEAT] Frontend: Add risk analysis dashboard
[FIX] Backend: Resolve API timeout issue
[DOCS] Update Git workflow documentation
```

### PR Description

Use the provided template and include:
- Clear description of changes
- Related issue numbers
- Testing performed
- Screenshots (for UI changes)
- Breaking changes (if any)

---

## Review Process

### For Contributors

1. **Respond to feedback promptly**
2. **Make requested changes**
3. **Ask questions if unclear**
4. **Be patient and respectful**
5. **Learn from feedback**

### For Reviewers

1. **Review within 48 hours**
2. **Provide constructive feedback**
3. **Test changes locally if needed**
4. **Approve when satisfied**
5. **Be respectful and helpful**

### Review Criteria

Reviewers check for:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security concerns
- Breaking changes

---

## Additional Resources

- [Git Workflow Guide](GIT_WORKFLOW.md)
- [Environment Setup](ENVIRONMENT_SETUP.md)
- [Architecture Documentation](ARCHITECTURE_DIAGRAM.md)
- [Frontend Structure](FRONTEND_STRUCTURE.md)
- [Backend Structure](BACKEND_STRUCTURE.md)

---

## Getting Help

- **Questions**: Create an issue with label `question`
- **Bugs**: Use bug report template
- **Features**: Use feature request template
- **Discussion**: Start a GitHub Discussion

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to LegacyMind AI! 🚀

**Last Updated**: 2026-05-16
**Version**: 1.0.0