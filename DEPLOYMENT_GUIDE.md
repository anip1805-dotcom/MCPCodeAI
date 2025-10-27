# Deployment Guide

This guide explains how to deploy the AI Development Guidelines MCP Server to different environments.

## Environment Requirements

### All Environments

**Python Requirements:**
- Python 3.11 or higher
- pip or uv package manager

**Required Packages:**
```
mcp>=1.19.0
pyyaml>=6.0
```

**Optional Packages (for AI features):**
```
anthropic>=0.23.0
```

### Staging Environment

**Environment Variables:**
```bash
# Required
ENVIRONMENT=staging

# Optional (enables AI-powered custom guidance)
ANTHROPIC_API_KEY=sk-ant-...

# Server Configuration
SERVER_NAME="AI Dev Guidelines (Staging)"
```

**Deployment Steps:**
1. Merge to `develop` branch
2. CI/CD automatically deploys to staging
3. Verify at staging URL
4. Run smoke tests

### Production Environment

**Environment Variables:**
```bash
# Required
ENVIRONMENT=production

# Optional (enables AI-powered custom guidance)
ANTHROPIC_API_KEY=sk-ant-...

# Server Configuration
SERVER_NAME="AI Development Guidelines Server"
```

**Deployment Steps:**
1. Merge to `main` branch
2. Trigger manual deployment in GitLab
3. Cache is built automatically
4. Verify all 4 tools are available
5. Monitor feedback collection

## GitLab CI/CD Setup

### Required Variables

Configure in GitLab Project Settings > CI/CD > Variables:

| Variable Name | Protected | Masked | Example Value |
|--------------|-----------|--------|---------------|
| `ANTHROPIC_API_KEY` | ✅ | ✅ | `sk-ant-...` |

### Pipeline Schedules

Set up scheduled pipelines in GitLab Project Settings > CI/CD > Schedules:

**Weekly Analytics:**
- Description: Weekly feedback and token analysis
- Interval pattern: `0 2 * * 0` (Sunday 2 AM)
- Target branch: `main`
- Active: ✅

**Daily Cache Rebuild:**
- Description: Rebuild compressed cache daily
- Interval pattern: `0 3 * * *` (Daily 3 AM)
- Target branch: `main`
- Active: ✅

## Deployment Checklist

### Pre-Deployment

- [ ] All tests pass locally
- [ ] Documentation is updated
- [ ] Cache builds successfully
- [ ] Token usage is optimized
- [ ] No LSP errors

### Staging Deployment

- [ ] Code merged to `develop`
- [ ] CI/CD pipeline passes
- [ ] Staging environment accessible
- [ ] All 4 tools working
- [ ] Feedback collection enabled
- [ ] Cache serving correctly

### Production Deployment

- [ ] Staging validated
- [ ] Code merged to `main`
- [ ] Manual deployment triggered
- [ ] Production health check passes
- [ ] Monitoring enabled
- [ ] Analytics configured

### Post-Deployment

- [ ] Verify all endpoints
- [ ] Check feedback collection
- [ ] Monitor token usage
- [ ] Review error rates
- [ ] Update documentation

## Monitoring

### Key Metrics

**Health Metrics:**
- Tool success rate: Should be >99%
- Average response time: <100ms for cached
- Cache hit rate: >80% after warmup

**Token Metrics:**
- Total tokens per call: ~1,378-2,490
- Compression ratio: ~60%
- Cache size: <10KB compressed

**Feedback Metrics:**
- Calls per day: Track trend
- Most used tool: Identify patterns
- Error rate: Should be <1%

### Log Locations

**Feedback Logs:**
```
feedback/call_*.json       # Individual call logs
```

**Analytics:**
```
analytics/feedback_analysis_*.json  # Weekly summaries
```

**Reports:**
```
reports/token_usage_*.json  # Token optimization reports
```

### Troubleshooting

**Cache Not Loading:**
```bash
# Rebuild cache manually
PYTHONPATH=/path/to/project python scripts/build_compressed_cache.py

# Verify cache files exist
ls -la cache/
```

**Feedback Not Collecting:**
```bash
# Check feedback directory permissions
chmod 755 feedback/

# Verify FeedbackCollector is enabled
# Check server initialization logs
```

**High Token Usage:**
```bash
# Generate token report
PYTHONPATH=/path/to/project python scripts/token_optimizer_report.py

# Review recommendations in reports/
```

## Rollback Procedure

### If Deployment Fails

1. **Stop the deployment:**
   ```bash
   # In GitLab, cancel the deployment job
   ```

2. **Identify the issue:**
   - Check pipeline logs
   - Review error messages
   - Verify environment variables

3. **Rollback to previous version:**
   ```bash
   # Revert the merge commit
   git revert <commit-hash>
   git push
   ```

4. **Verify rollback:**
   - Pipeline passes
   - Service is healthy
   - All tools working

### Emergency Hotfix

For critical issues in production:

1. Create hotfix branch from `main`
2. Apply minimal fix
3. Test thoroughly
4. Deploy via manual trigger
5. Merge back to `develop` and `main`

## Performance Optimization

### Cache Optimization

**Preload Cache:**
```bash
# Build cache before deployment
python scripts/build_compressed_cache.py
```

**Verify Compression:**
```bash
# Check cache sizes
ls -lh cache/
# Should show ~60% reduction
```

### Token Optimization

**Review Reports:**
```bash
# Generate latest report
python scripts/token_optimizer_report.py

# Check for optimization suggestions
cat reports/token_usage_*.json | jq '.documents[].optimization_suggestions'
```

**Implement Recommendations:**
- Split large documents if needed
- Use compressed cache for delivery
- Enable client-side caching

## Security

### API Key Management

**Best Practices:**
- Store in GitLab CI/CD variables (masked + protected)
- Never commit to repository
- Rotate keys regularly
- Use different keys per environment

**Key Rotation:**
1. Generate new Anthropic API key
2. Update GitLab CI/CD variable
3. Redeploy to staging
4. Verify functionality
5. Deploy to production
6. Revoke old key

### Access Control

**GitLab Permissions:**
- Maintainer: Can deploy to production
- Developer: Can deploy to staging
- Reporter: Read-only access

**Environment Protection:**
- Production: Requires manual approval
- Staging: Auto-deploys on merge

## Scaling Considerations

### Horizontal Scaling

The MCP server is stateless and can scale horizontally:

**Load Balancing:**
```yaml
# Multiple server instances
server1: python main.py
server2: python main.py
server3: python main.py
```

**Shared Cache:**
- Use network-mounted cache directory
- Or replicate cache to all instances

### Vertical Scaling

For high load:

**Resource Limits:**
```yaml
resources:
  memory: 512MB  # Sufficient for cache
  cpu: 0.5       # Low CPU usage
```

**Optimization:**
- Use pickle.gz for smallest cache
- Enable HTTP compression
- Implement CDN for static docs

## Support

For deployment issues:
1. Check pipeline logs in GitLab
2. Review CICD_GUIDE.md
3. Consult README.md
4. Open GitLab issue

For production incidents:
1. Check monitoring dashboard
2. Review feedback logs
3. Generate analytics report
4. Follow rollback procedure if needed
