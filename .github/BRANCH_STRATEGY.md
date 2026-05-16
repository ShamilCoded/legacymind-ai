# Branch Strategy

LegacyMind AI uses a modified Git Flow branching strategy optimized for continuous delivery and frontend/backend separation.

## Branch Types

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Highly protected, requires PR approval
- **Deployment**: Auto-deploys to production
- **Merge From**: `release/*` branches only
- **Direct Commits**: ❌ Never
- **Naming**: `main`

#### `develop`
- **Purpose**: Integration branch for features
- **Protection**: Protected, requires PR approval
- **Deployment**: Auto-deploys to staging
- **Merge From**: `feature/*`, `bugfix/*`, `hotfix/*`
- **Direct Commits**: ❌ Never
- **Naming**: `develop`

### Supporting Branches

#### Feature Branches
- **Purpose**: New features or enhancements
- **Branch From**: `develop`
- **Merge Into**: `develop`
- **Lifetime**: Temporary (delete after merge)
- **Naming Convention**: `feature/<component>/<description>`
  - `feature/frontend/user-authentication`
  - `feature/backend/rag-chatbot`
  - `feature/ui/glassmorphism-components`
  - `feature/api/embeddings-endpoint`

#### Bugfix Branches
- **Purpose**: Non-critical bug fixes
- **Branch From**: `develop`
- **Merge Into**: `develop`
- **Lifetime**: Temporary (delete after merge)
- **Naming Convention**: `bugfix/<component>/<description>`
  - `bugfix/frontend/login-validation`
  - `bugfix/backend/memory-leak`

#### Hotfix Branches
- **Purpose**: Critical production bug fixes
- **Branch From**: `main`
- **Merge Into**: `main` AND `develop`
- **Lifetime**: Temporary (delete after merge)
- **Naming Convention**: `hotfix/<version>/<description>`
  - `hotfix/v1.2.1/security-patch`
  - `hotfix/v1.2.2/api-timeout`

#### Release Branches
- **Purpose**: Prepare for production release
- **Branch From**: `develop`
- **Merge Into**: `main` AND `develop`
- **Lifetime**: Temporary (delete after merge)
- **Naming Convention**: `release/<version>`
  - `release/v1.0.0`
  - `release/v1.1.0`

## Component-Specific Branches

### Frontend Branches
```
feature/frontend/<feature-name>
bugfix/frontend/<bug-name>
```

Examples:
- `feature/frontend/dashboard-ui`
- `feature/frontend/authentication-flow`
- `bugfix/frontend/responsive-layout`

### Backend Branches
```
feature/backend/<feature-name>
bugfix/backend/<bug-name>
```

Examples:
- `feature/backend/embeddings-service`
- `feature/backend/rag-implementation`
- `bugfix/backend/api-validation`

### Full-Stack Branches
```
feature/fullstack/<feature-name>
```

Examples:
- `feature/fullstack/user-management`
- `feature/fullstack/repository-analysis`

## Workflow Diagrams

### Feature Development Flow
```
develop
  ↓ (branch)
feature/frontend/new-feature
  ↓ (develop)
  ↓ (test)
  ↓ (PR)
develop
  ↓ (CI/CD)
staging environment
```

### Release Flow
```
develop
  ↓ (branch)
release/v1.0.0
  ↓ (bug fixes only)
  ↓ (PR to main)
main
  ↓ (CI/CD)
production environment
  ↓ (merge back)
develop
```

### Hotfix Flow
```
main
  ↓ (branch)
hotfix/v1.0.1/critical-bug
  ↓ (fix)
  ↓ (PR to main)
main
  ↓ (CI/CD)
production environment
  ↓ (merge back)
develop
```

## Branch Protection Rules

### `main` Branch
- ✅ Require pull request reviews (2 approvals)
- ✅ Require status checks to pass
  - Frontend CI
  - Backend CI
  - Security scans
- ✅ Require branches to be up to date
- ✅ Require signed commits
- ✅ Include administrators
- ✅ Restrict who can push (Release managers only)
- ✅ Require linear history
- ❌ Allow force pushes
- ❌ Allow deletions

### `develop` Branch
- ✅ Require pull request reviews (1 approval)
- ✅ Require status checks to pass
  - Frontend CI
  - Backend CI
- ✅ Require branches to be up to date
- ✅ Dismiss stale reviews
- ❌ Require signed commits (recommended but not enforced)
- ❌ Allow force pushes
- ❌ Allow deletions

### Feature Branches
- No protection rules
- Can be force-pushed during development
- Should be rebased before merging

## Workflow Steps

### Starting a New Feature

```bash
# 1. Update develop branch
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/frontend/new-dashboard

# 3. Make changes and commit
git add .
git commit -m "feat(frontend/ui): add dashboard layout"

# 4. Push to remote
git push -u origin feature/frontend/new-dashboard

# 5. Create Pull Request on GitHub
```

### Merging a Feature

```bash
# 1. Update your branch with latest develop
git checkout feature/frontend/new-dashboard
git fetch origin
git rebase origin/develop

# 2. Resolve conflicts if any
git add .
git rebase --continue

# 3. Force push (if rebased)
git push --force-with-lease

# 4. Merge via GitHub PR after approval
# 5. Delete branch after merge
git checkout develop
git pull origin develop
git branch -d feature/frontend/new-dashboard
```

### Creating a Release

```bash
# 1. Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. Update version numbers
# - frontend/package.json
# - backend/setup.py or version file
# - CHANGELOG.md

# 3. Commit version bump
git commit -am "chore(release): bump version to v1.0.0"

# 4. Push and create PR to main
git push -u origin release/v1.0.0

# 5. After approval and merge to main
# 6. Tag the release
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 7. Merge back to develop
git checkout develop
git merge main
git push origin develop

# 8. Delete release branch
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### Creating a Hotfix

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/v1.0.1/critical-bug

# 2. Fix the bug
git add .
git commit -m "fix(backend/api): resolve critical security issue"

# 3. Update version
# Update version files
git commit -am "chore(hotfix): bump version to v1.0.1"

# 4. Push and create PR to main
git push -u origin hotfix/v1.0.1/critical-bug

# 5. After merge to main, tag it
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
git push origin v1.0.1

# 6. Merge to develop
git checkout develop
git merge main
git push origin develop

# 7. Delete hotfix branch
git branch -d hotfix/v1.0.1/critical-bug
git push origin --delete hotfix/v1.0.1/critical-bug
```

## Best Practices

### Branch Naming
- Use lowercase with hyphens
- Be descriptive but concise
- Include component prefix (frontend/backend)
- Use issue numbers when applicable: `feature/frontend/user-auth-#123`

### Commit Practices
- Follow commit convention (see COMMIT_CONVENTION.md)
- Make atomic commits (one logical change per commit)
- Write meaningful commit messages
- Reference issues in commits

### Pull Request Practices
- Keep PRs small and focused
- Write clear PR descriptions
- Link related issues
- Request reviews from relevant team members
- Respond to review comments promptly
- Ensure CI passes before requesting review

### Merge Practices
- Use "Squash and merge" for feature branches
- Use "Create a merge commit" for release/hotfix branches
- Delete branches after merging
- Keep commit history clean

### Code Review Practices
- Review within 24 hours
- Be constructive and respectful
- Test the changes locally if needed
- Check for security issues
- Verify tests are included

## Environment Mapping

| Branch | Environment | URL | Auto-Deploy |
|--------|-------------|-----|-------------|
| `main` | Production | https://legacymind.ai | ✅ |
| `develop` | Staging | https://staging.legacymind.ai | ✅ |
| `feature/*` | Development | Local/Preview | ❌ |
| `release/*` | Pre-production | https://preprod.legacymind.ai | ✅ |

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Examples:
- `v1.0.0` - Initial release
- `v1.1.0` - New feature added
- `v1.1.1` - Bug fix
- `v2.0.0` - Breaking changes

## Troubleshooting

### Merge Conflicts
```bash
# Update your branch
git fetch origin
git rebase origin/develop

# Resolve conflicts in files
# Then continue rebase
git add .
git rebase --continue
```

### Accidentally Committed to Wrong Branch
```bash
# Save your changes
git stash

# Switch to correct branch
git checkout correct-branch

# Apply changes
git stash pop
```

### Need to Undo Last Commit
```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes
git reset --hard HEAD~1
```

## Additional Resources

- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)