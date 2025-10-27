# AI Agent Steering Instructions

## Core Principles for AI-Assisted Development

### 1. Think Before Acting
**Always analyze the problem thoroughly before writing code**

- Understand the full context and requirements
- Consider edge cases and potential issues
- Plan the solution architecture
- Identify potential pitfalls
- Choose the right approach for the situation

### 2. Follow Best Practices
**Write production-quality code from the start**

- Apply the rules from rules.md
- Use established patterns and conventions
- Consider security implications
- Think about maintainability
- Plan for scalability

### 3. Be Explicit and Clear
**Avoid ambiguity in code and communication**

- Use descriptive variable and function names
- Add comments for complex logic
- Provide clear error messages
- Document assumptions
- Explain your reasoning

## Code Generation Guidelines

### Before Writing Code

#### Checklist
1. **Understand the requirement completely**
   - What is the exact goal?
   - What are the inputs and outputs?
   - What are the constraints?

2. **Check existing codebase**
   - What patterns are already used?
   - What libraries are available?
   - What conventions should I follow?

3. **Consider the context**
   - Is this a new feature or a fix?
   - Will this affect other parts of the system?
   - Are there performance implications?

4. **Plan the solution**
   - What's the simplest approach?
   - What are alternative approaches?
   - What are the trade-offs?

### While Writing Code

#### Quality Standards
- **Type Safety**: Use type hints/annotations
- **Error Handling**: Handle exceptions appropriately
- **Validation**: Validate all inputs
- **Security**: Never expose secrets, sanitize inputs
- **Readability**: Code should be self-documenting
- **Testing**: Consider testability

#### Code Structure
```python
# Good structure example
def process_user_data(user_id: int, data: dict) -> dict:
    """
    Process user data with validation and error handling.
    
    Args:
        user_id: Unique identifier for the user
        data: Dictionary containing user data to process
    
    Returns:
        Processed data dictionary
    
    Raises:
        ValueError: If user_id is invalid or data is malformed
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("User ID must be positive")
    
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    # Process data
    try:
        processed = {
            'user_id': user_id,
            'name': data.get('name', '').strip(),
            'email': data.get('email', '').lower(),
            'timestamp': datetime.now().isoformat()
        }
        return processed
    except Exception as e:
        logger.error(f"Error processing user {user_id}: {e}")
        raise
```

### After Writing Code

#### Self-Review Checklist
- [ ] Code follows project conventions
- [ ] All edge cases are handled
- [ ] Error messages are helpful
- [ ] No hardcoded values (use config/env vars)
- [ ] Code is DRY (no unnecessary repetition)
- [ ] Functions are focused and single-purpose
- [ ] Type hints are present
- [ ] Docstrings are complete
- [ ] No security vulnerabilities
- [ ] Performance is acceptable

## Problem-Solving Framework

### Step 1: Understand
- Read the requirement carefully
- Ask clarifying questions if needed
- Identify the core problem
- List all constraints

### Step 2: Research
- Check documentation
- Look at similar implementations
- Review best practices
- Consider proven patterns

### Step 3: Design
- Sketch the solution
- Identify components
- Define interfaces
- Plan error handling

### Step 4: Implement
- Start with the simplest working solution
- Add complexity only when needed
- Test as you go
- Commit frequently

### Step 5: Review
- Check against requirements
- Test edge cases
- Review for security issues
- Optimize if necessary

### Step 6: Document
- Add docstrings
- Update README if needed
- Comment complex logic
- Create usage examples

## Common Patterns & Anti-Patterns

### ✅ Good Patterns

#### Configuration Management
```python
# Use environment variables or config files
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

#### Error Handling
```python
# Specific, helpful error handling
try:
    user = get_user(user_id)
except UserNotFoundError:
    logger.warning(f"User {user_id} not found")
    return {"error": "User not found"}, 404
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    return {"error": "Internal server error"}, 500
```

#### Dependency Injection
```python
# Make dependencies explicit
class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache
    
    def get_user(self, user_id: int) -> User:
        # Try cache first
        cached = self.cache.get(f"user:{user_id}")
        if cached:
            return cached
        
        # Fetch from database
        user = self.db.get_user(user_id)
        self.cache.set(f"user:{user_id}", user)
        return user
```

### ❌ Anti-Patterns to Avoid

#### Hardcoded Values
```python
# Bad
def send_email(to: str, subject: str):
    smtp.connect("smtp.gmail.com", 587)  # Hardcoded!
    smtp.login("myemail@gmail.com", "password123")  # Terrible!

# Good
def send_email(to: str, subject: str):
    smtp.connect(config.SMTP_HOST, config.SMTP_PORT)
    smtp.login(config.SMTP_USER, os.getenv('SMTP_PASSWORD'))
```

#### Swallowing Exceptions
```python
# Bad
try:
    result = risky_operation()
except:
    pass  # Silent failure!

# Good
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise  # Re-raise or handle appropriately
```

#### God Objects/Functions
```python
# Bad - function does too much
def handle_user_request(request):
    # Validation
    # Authentication
    # Database operations
    # Business logic
    # Email sending
    # Logging
    # Response formatting
    # ... 200 lines later ...

# Good - single responsibility
def handle_user_request(request):
    validate_request(request)
    user = authenticate(request)
    data = process_data(request.data)
    save_to_database(data)
    send_notification(user, data)
    return format_response(data)
```

## Context-Aware Development

### For New Projects
- Set up project structure following conventions
- Initialize version control
- Configure linters and formatters
- Set up virtual environment/dependency management
- Create README with setup instructions
- Add .gitignore for the language/framework

### For Existing Projects
- Study the existing codebase first
- Follow established patterns
- Match the existing code style
- Don't refactor unless asked
- Respect architectural decisions
- Add to existing documentation

### For Bug Fixes
- Reproduce the bug first
- Understand the root cause
- Write a test that fails
- Fix the bug
- Verify the test passes
- Check for similar bugs elsewhere

### For New Features
- Understand the use case
- Design the API/interface
- Write tests first (TDD)
- Implement incrementally
- Document the feature
- Update relevant documentation

## Communication Guidelines

### When Explaining Code
- Start with the high-level purpose
- Explain the approach
- Highlight important details
- Mention trade-offs or limitations
- Provide usage examples

### When Asking for Clarification
- Be specific about what's unclear
- Provide context
- Suggest possible interpretations
- Ask focused questions

### When Reporting Issues
- Describe expected behavior
- Describe actual behavior
- Provide steps to reproduce
- Include relevant error messages
- Suggest possible causes if known

## Continuous Improvement

### Learning from Code
- Study well-written codebases
- Understand why certain patterns are used
- Note new techniques and approaches
- Question and validate best practices

### Adapting to Context
- Recognize when rules should be bent
- Understand the "why" behind rules
- Apply judgment based on situation
- Balance idealism with pragmatism

### Iterative Refinement
- Start simple, add complexity as needed
- Refactor as understanding improves
- Optimize based on real metrics
- Improve based on feedback

## Decision-Making Framework

### When Choosing Technologies
1. **Project Requirements**: What does the project actually need?
2. **Team Familiarity**: What does the team know?
3. **Community Support**: Is it well-maintained and documented?
4. **Performance**: Does it meet performance requirements?
5. **Long-term Viability**: Will it be maintained in the future?

### When Deciding on Architecture
1. **Current Needs**: Solve today's problems
2. **Known Future Needs**: Plan for clear upcoming requirements
3. **Flexibility**: Allow for unforeseen changes
4. **Simplicity**: Choose the simplest solution that works
5. **Maintainability**: Can others understand and modify it?

### When Optimizing
1. **Measure First**: Don't guess at bottlenecks
2. **Cost-Benefit**: Is the optimization worth the complexity?
3. **User Impact**: Will users notice the improvement?
4. **Maintenance Burden**: Does it make the code harder to maintain?
5. **Alternative Solutions**: Are there simpler ways to achieve the goal?

## Summary

As an AI agent assisting with development:
1. **Understand** the context fully before acting
2. **Follow** established best practices and patterns
3. **Write** clean, secure, maintainable code
4. **Test** your solutions thoroughly
5. **Document** your code and decisions
6. **Learn** from each interaction
7. **Adapt** to the specific project needs
8. **Communicate** clearly and helpfully

Remember: The goal is to write code that is correct, secure, maintainable, and appropriate for the context. Quality over speed, clarity over cleverness, and always think about the humans who will read and maintain your code.
