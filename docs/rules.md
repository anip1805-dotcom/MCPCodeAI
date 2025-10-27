# Professional Development Rules

## Code Quality Standards

### 1. Code Organization
- **Single Responsibility Principle**: Each function/class should have one clear purpose
- **DRY (Don't Repeat Yourself)**: Extract common logic into reusable functions
- **Clear Naming**: Use descriptive, meaningful names for variables, functions, and classes
- **Consistent Structure**: Follow language-specific conventions and patterns

### 2. Error Handling
- **Never Fail Silently**: Always handle errors appropriately
- **Specific Exceptions**: Catch specific exceptions, not broad try-except blocks
- **Meaningful Error Messages**: Provide context about what went wrong and how to fix it
- **Graceful Degradation**: Handle errors without crashing the entire application

### 3. Security Best Practices
- **Never Hardcode Secrets**: Use environment variables or secure vaults
- **Input Validation**: Always validate and sanitize user input
- **SQL Injection Prevention**: Use parameterized queries or ORMs
- **Authentication & Authorization**: Implement proper access controls
- **HTTPS/TLS**: Use secure connections for data transmission

### 4. Performance Optimization
- **Avoid Premature Optimization**: Write clear code first, optimize when needed
- **Database Query Efficiency**: Use indexes, avoid N+1 queries
- **Caching Strategy**: Cache expensive operations appropriately
- **Async Operations**: Use async/await for I/O-bound operations
- **Resource Management**: Properly close files, connections, and streams

### 5. Code Documentation
- **Docstrings**: Document all public functions, classes, and modules
- **Type Hints**: Use type annotations in Python (or equivalent in other languages)
- **Comments for Complex Logic**: Explain "why" not "what"
- **README Files**: Provide clear setup and usage instructions
- **API Documentation**: Document endpoints, parameters, and responses

### 6. Testing Requirements
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **Edge Cases**: Test boundary conditions and error scenarios
- **Test Coverage**: Aim for >80% code coverage for critical paths
- **Mock External Dependencies**: Isolate tests from external services

### 7. Version Control
- **Atomic Commits**: Each commit should represent one logical change
- **Descriptive Messages**: Write clear commit messages explaining the change
- **Branch Strategy**: Use feature branches, keep main/master stable
- **Code Reviews**: All code should be reviewed before merging
- **Semantic Versioning**: Follow semver for releases (MAJOR.MINOR.PATCH)

### 8. Code Style & Formatting
- **Consistent Formatting**: Use linters and formatters (black, prettier, etc.)
- **Line Length**: Keep lines under 88-120 characters
- **Indentation**: Use consistent indentation (4 spaces for Python)
- **Import Organization**: Group and sort imports logically
- **Remove Dead Code**: Delete commented-out code and unused imports

### 9. API Design
- **RESTful Principles**: Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- **Versioning**: Version your APIs (/v1/, /v2/)
- **Consistent Responses**: Standardize response formats
- **Rate Limiting**: Implement rate limiting for public APIs
- **Pagination**: Paginate large result sets

### 10. Database Best Practices
- **Normalization**: Normalize data to reduce redundancy
- **Indexing**: Create indexes on frequently queried columns
- **Migrations**: Use migration tools for schema changes
- **Backups**: Regular automated backups
- **Connection Pooling**: Reuse database connections

## Python-Specific Rules

### Code Style
- Follow PEP 8 style guide
- Use `snake_case` for variables and functions
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants

### Best Practices
- Use list comprehensions for simple transformations
- Leverage context managers (`with` statements)
- Use `pathlib` for file path operations
- Prefer f-strings for string formatting
- Use dataclasses or pydantic for data structures

### Common Patterns
```python
# Use type hints
def process_data(items: list[dict]) -> list[str]:
    return [item['name'] for item in items]

# Use context managers
with open('file.txt', 'r') as f:
    content = f.read()

# Use dataclasses
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
```

## JavaScript/TypeScript-Specific Rules

### Code Style
- Use `camelCase` for variables and functions
- Use `PascalCase` for classes and components
- Use `UPPER_CASE` for constants
- Prefer `const` over `let`, never use `var`

### Best Practices
- Use async/await over callbacks
- Leverage destructuring for objects and arrays
- Use arrow functions appropriately
- Implement proper error boundaries in React
- Use TypeScript for type safety

## Git Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(auth): add OAuth2 authentication

- Implement OAuth2 flow with Google provider
- Add user session management
- Create protected route middleware

Closes #123
```

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is comprehensive
- [ ] Documentation is updated
- [ ] No TODO or FIXME comments left unresolved
- [ ] Performance implications considered
- [ ] Security vulnerabilities addressed
- [ ] Backward compatibility maintained
