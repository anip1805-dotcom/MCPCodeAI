# AI Development Guidelines MCP Server

## Overview
An MCP (Model Context Protocol) server that provides AI agents with professional development guidelines, coding standards, and best practices. The server uses an AI orchestration layer powered by Anthropic Claude to intelligently select and deliver the right documentation based on incoming agent requests.

## Purpose
- Provide AI agents with professional-level coding rules and guidelines
- Deliver context-aware development documentation through MCP protocol
- Enable agents to write production-quality code using curated best practices

## Current State
Development in progress - Setting up core MCP server infrastructure with AI orchestration.

## Project Architecture
- **Language**: Python 3.11+
- **MCP Server**: Using official MCP Python SDK
- **AI Orchestration**: Anthropic Claude API for intelligent context selection
- **Documentation**: Pre-built templates for rules, skills, and steering

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
│   ├── rules.md               # Professional coding rules
│   ├── skills.md              # Development skills and practices
│   └── steering.md            # AI agent steering instructions
├── config.yaml                 # Server configuration
└── main.py                     # Entry point
```

## Recent Changes
- 2025-10-27: Initial project setup, MCP SDK installation

## User Preferences
- Use Anthropic Claude for AI orchestration
- Python-based implementation
- Professional-level development standards
