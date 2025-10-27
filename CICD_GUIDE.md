# CI/CD Pipeline Guide

This document explains the CI/CD pipeline for the AI Development Guidelines MCP Server.

## Overview

The project uses **GitLab CI/CD** with automated testing, caching, feedback collection, and token optimization.

## Pipeline Stages

### 1. Test Stage
- **Unit Tests**: Runs pytest with coverage reporting
- **Integration Tests**: Tests the MCP server with test_client.py
- **Linting**: Runs ruff for code quality checks
- **Type Checking**: Runs mypy for static type checking

### 2. Build Stage
- **Cache Building**: Creates compressed cache files for efficient delivery
  - JSON format: ~25KB
  - Gzipped JSON: ~9.7KB (61.6% compression)
  - Pickle + Gzip: ~9.7KB (59.7% overall compression)

### 3. Deploy Stage
- **Staging**: Auto-deploys to staging on `develop` branch
- **Production**: Manual deployment from `main` branch

### 4. Analyze Stage
- **Feedback Analysis**: Analyzes usage patterns and metrics
- **Token Optimization**: Reports on token usage and optimization opportunities

## Features

### Token Optimization

The token optimizer tracks and reduces token usage:

```python
from src.token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(max_tokens=4000)
stats = optimizer.get_stats(content)
optimized = optimizer.optimize_content(content, target_tokens=2000)
```

**Current Stats:**
- Total tokens: ~6,012
- Rules: 1,378 tokens
- Skills: 2,144 tokens
- Steering: 2,490 tokens
- Compression potential: 59.7%

### Feedback Collection

Automatically tracks every MCP call:

```python
{
  "timestamp": "2025-10-27T18:00:47.123456",
  "tool_name": "get_coding_rules",
  "arguments": {},
  "response_size": 5513,
  "tokens_used": 1378,
  "response_time_ms": 45.2,
  "success": true
}
```

Stored in `feedback/` directory for analysis.

### Compressed Cache System

**Benefits:**
- 60% reduction in transfer size
- Faster delivery to clients
- Reduced bandwidth usage
- Multiple format support (JSON, Pickle)

**Usage:**
```python
from src.cache_manager import CacheManager

cache = CacheManager()
doc = cache.get_document("rules", format="json_gz")
```

**Available Formats:**
- `json`: Uncompressed JSON
- `json_gz`: Gzipped JSON (recommended)
- `pickle`: Python pickle
- `pickle_gz`: Gzipped pickle (smallest)

## GitLab CI/CD Configuration

### Required Variables

Set these in GitLab CI/CD settings:

```bash
ANTHROPIC_API_KEY=your-api-key-here  # Optional, for AI features
```

### Pipeline Triggers

- **Merge Requests**: Runs tests and linting
- **Main Branch**: Full pipeline + production deployment (manual)
- **Develop Branch**: Full pipeline + staging deployment
- **Scheduled**: Runs analytics and feedback analysis

### Artifacts

The pipeline produces:

1. **Coverage Reports** (`.coverage`, `coverage.xml`)
2. **Cache Files** (`cache/`)
3. **Analytics** (`analytics/feedback_analysis_*.json`)
4. **Token Reports** (`reports/token_usage_*.json`)

## Local Development

### Running Tests

```bash
# Unit tests with coverage
pytest tests/ -v --cov=src --cov-report=term

# Integration test
python test_client.py
```

### Building Cache

```bash
PYTHONPATH=/path/to/workspace python scripts/build_compressed_cache.py
```

### Generating Reports

```bash
# Token optimization report
PYTHONPATH=/path/to/workspace python scripts/token_optimizer_report.py

# Feedback analysis
PYTHONPATH=/path/to/workspace python scripts/analyze_feedback.py
```

## Continuous Improvement

### Feedback Loop

1. **Collect**: Every MCP call is logged with timing and token metrics
2. **Analyze**: Scheduled jobs analyze patterns weekly
3. **Optimize**: Token optimizer suggests improvements
4. **Iterate**: Update documentation based on insights

### Metrics Tracked

- Tool usage frequency
- Token consumption per tool
- Response times
- Success rates
- User feedback (when provided)

### Evolution Process

1. **Weekly**: Automated feedback analysis
2. **Monthly**: Review optimization reports
3. **Quarterly**: Update documentation based on patterns
4. **Continuous**: CI/CD ensures quality

## Deployment

### Staging

Automatically deploys on merge to `develop`:

```yaml
deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.mcp-server.example.com
  only:
    - develop
```

### Production

Manual deployment from `main`:

```yaml
deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://mcp-server.example.com
  only:
    - main
  when: manual
```

## Monitoring

### Key Metrics

- **Success Rate**: % of successful tool calls
- **Avg Response Time**: Milliseconds per tool
- **Token Usage**: Tokens consumed per call
- **Cache Hit Rate**: % of requests served from cache

### Analytics Files

Check `analytics/` directory for:
- Feedback analysis reports
- Usage pattern insights
- Performance trends
- Optimization recommendations

## Best Practices

1. **Always run tests** before committing
2. **Review token reports** to identify optimization opportunities
3. **Monitor feedback** to understand usage patterns
4. **Keep cache updated** by rebuilding after documentation changes
5. **Use compressed formats** for production delivery

## Troubleshooting

### Pipeline Failures

**Test Stage Fails:**
- Check test logs in GitLab artifacts
- Run tests locally: `pytest tests/ -v`

**Build Stage Fails:**
- Verify documentation files exist
- Check cache directory permissions

**Deploy Stage Fails:**
- Verify environment variables are set
- Check deployment logs

### Performance Issues

**High Token Usage:**
- Review token optimization report
- Consider splitting large documents
- Use compressed cache delivery

**Slow Response Times:**
- Enable cache in production
- Pre-build cache files in CI
- Consider CDN for static files

## Future Enhancements

- [ ] Automated A/B testing for documentation updates
- [ ] Machine learning-based content recommendations
- [ ] Real-time analytics dashboard
- [ ] Automated documentation improvement suggestions
- [ ] Client-side caching strategies
