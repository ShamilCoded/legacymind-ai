# Commit Message Convention

LegacyMind AI follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

## Scope

The scope should specify the place of the commit change. Examples:

### Frontend Scopes
- `ui`: UI components
- `pages`: Page components
- `api`: API integration
- `styles`: Styling changes
- `config`: Configuration files
- `hooks`: React hooks
- `utils`: Utility functions
- `types`: TypeScript types

### Backend Scopes
- `api`: API endpoints
- `services`: Service layer
- `models`: Data models
- `db`: Database related
- `auth`: Authentication
- `embeddings`: Embeddings service
- `rag`: RAG chatbot
- `modernization`: Modernization engine
- `risk`: Risk analysis
- `architecture`: Architecture visualization
- `utils`: Utility functions

### General Scopes
- `deps`: Dependencies
- `config`: Configuration
- `docs`: Documentation
- `ci`: CI/CD
- `tests`: Testing

## Subject

The subject contains a succinct description of the change:

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No dot (.) at the end
- Maximum 72 characters

## Body (Optional)

The body should include the motivation for the change and contrast this with previous behavior.

- Use the imperative, present tense
- Wrap at 72 characters
- Explain what and why vs. how

## Footer (Optional)

The footer should contain any information about Breaking Changes and reference GitHub issues that this commit closes.

### Breaking Changes

Breaking changes should start with `BREAKING CHANGE:` followed by a description.

### Issue References

Closed issues should be listed on a separate line prefixed with "Closes" keyword:

```
Closes #123
Closes #456, #789
```

## Examples

### Feature Addition

```
feat(frontend/ui): add glassmorphism button component

Implement a new button component with glassmorphism design
- Add hover and active states
- Support multiple variants (primary, secondary, outline)
- Include loading state with spinner

Closes #45
```

### Bug Fix

```
fix(backend/rag): resolve memory leak in chat service

Fix memory leak caused by unclosed database connections
in the RAG chatbot service. Implement proper connection
pooling and cleanup.

Closes #123
```

### Breaking Change

```
feat(backend/api): update authentication endpoint structure

BREAKING CHANGE: The authentication endpoint now returns
a different response structure. Update your API clients
to handle the new format.

Before:
{
  "token": "...",
  "user": {...}
}

After:
{
  "data": {
    "accessToken": "...",
    "refreshToken": "...",
    "user": {...}
  }
}

Closes #234
```

### Documentation

```
docs(readme): update installation instructions

Add detailed steps for setting up the development environment
including prerequisites and troubleshooting tips.
```

### Refactoring

```
refactor(backend/services): extract common validation logic

Move duplicate validation code into a shared utility module
to improve maintainability and reduce code duplication.
```

### Performance Improvement

```
perf(frontend/api): implement request caching

Add caching layer for API requests to reduce server load
and improve response times. Cache expires after 5 minutes.
```

### Testing

```
test(backend/embeddings): add unit tests for pipeline

Add comprehensive unit tests for the embeddings pipeline
covering edge cases and error scenarios.
```

### CI/CD

```
ci: add automated security scanning

Integrate Snyk security scanning into the CI pipeline
to detect vulnerabilities in dependencies.
```

### Dependency Updates

```
chore(deps): upgrade Next.js to v14.0.0

Update Next.js and related dependencies to latest stable version.
No breaking changes affecting our codebase.
```

### Multiple Scopes

```
feat(frontend/ui,backend/api): implement user profile feature

Add user profile management functionality:
- Frontend: Profile page with edit capabilities
- Backend: Profile API endpoints with validation

Closes #567
```

## Commit Message Validation

Commits are validated using [commitlint](https://commitlint.js.io/) in the CI pipeline. Invalid commit messages will cause the build to fail.

## Tips

1. **Keep commits atomic**: Each commit should represent a single logical change
2. **Write clear subjects**: Make it easy to understand what changed at a glance
3. **Use the body for context**: Explain why the change was made, not just what changed
4. **Reference issues**: Always link to related issues or tickets
5. **Test before committing**: Ensure your changes work and don't break existing functionality

## Tools

### Commitizen

Use [Commitizen](https://github.com/commitizen/cz-cli) for interactive commit message creation:

```bash
npm install -g commitizen
git cz
```

### Git Hooks

Pre-commit hooks are configured to validate commit messages. Install them with:

```bash
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install pre-commit && pre-commit install
```

## Revert Commits

When reverting a commit, use the `revert` type:

```
revert: feat(frontend/ui): add glassmorphism button component

This reverts commit abc123def456.

Reason: The feature caused performance issues in production.
```

## Merge Commits

Merge commits should follow the same convention:

```
merge: feature/user-authentication into develop

Merge user authentication feature including:
- Login/logout functionality
- JWT token management
- Protected routes

Closes #789