# AI Development Guidelines MCP Server

## Overview
An MCP (Model Context Protocol) server that provides AI agents with professional development guidelines, coding standards, and best practices. The server uses an AI orchestration layer powered by Anthropic Claude to intelligently select and deliver the right documentation based on incoming agent requests.

## Purpose
- Provide AI agents with professional-level coding rules and guidelines
- Deliver context-aware development documentation through MCP protocol
- Enable agents to write production-quality code using curated best practices

## Current State
✅ **Complete** - Fully functional MCP server with AI orchestration layer

## Project Architecture
- **Language**: Python 3.11+
- **MCP Server**: Using official MCP Python SDK (v1.19.0)
- **AI Orchestration**: Anthropic Claude API for intelligent context selection (optional)
- **Documentation**: Comprehensive templates for rules, skills, and steering
- **Testing**: Complete test suite with test client

## Structure
```
/
├── src/
│   ├── mcp_server.py          # Main MCP server implementation
│   ├── ai_orchestrator.py     # AI-powered context selector
│   └── utils/
│       ├── config.py           # Configuration management
│       └── document_loader.py  # Documentation file loader
├── docs/
│   ├── rules.md               # Professional coding rules (5,513 chars)
│   ├── skills.md              # Development skills and practices (8,576 chars)
│   └── steering.md            # AI agent steering instructions (9,960 chars)
├── config.yaml                 # Server configuration
├── main.py                     # Entry point
├── test_client.py              # Test client for validation
└── README.md                   # Complete documentation
```

## Features Implemented
- ✅ 4 MCP tools (get_coding_rules, get_development_skills, get_steering_instructions, get_custom_guidance)
- ✅ 3 MCP resources (guidelines://rules, guidelines://skills, guidelines://steering)
- ✅ AI orchestration with graceful degradation when API key not set
- ✅ Comprehensive test coverage
- ✅ Full documentation and README
- ✅ GitLab CI/CD pipeline with multi-stage deployment
- ✅ Token optimizer (6,012 total tokens tracked)
- ✅ Feedback collection system (auto-tracking all calls)
- ✅ Compressed cache system (59.7% size reduction)
- ✅ Analytics and metrics tracking

## Recent Changes
- 2025-10-27: Initial project setup, MCP SDK installation
- 2025-10-27: Implemented all core features and AI orchestration
- 2025-10-27: Added comprehensive test suite
- 2025-10-27: Architect review and approval - all critical issues addressed
- 2025-10-27: Added CI/CD pipeline with GitLab integration
- 2025-10-27: Implemented token optimizer, feedback collector, and cache manager
- 2025-10-27: Built compressed cache (60% compression achieved)

## User Preferences
- Use Anthropic Claude for AI orchestration
- Python-based implementation
- Professional-level development standards
