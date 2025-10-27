# AI Development Guidelines MCP Server

An MCP (Model Context Protocol) server that provides AI agents with professional development guidelines, coding standards, and best practices. The server uses an AI orchestration layer powered by Anthropic Claude to intelligently select and deliver the right documentation based on incoming agent requests.

## Features

- **Professional Coding Rules**: Comprehensive standards for writing production-quality code
- **Development Skills**: Best practices for problem-solving, debugging, testing, and more
- **AI Steering Instructions**: Context-aware guidance for AI agents
- **AI Orchestration**: Intelligent document selection using Claude
- **MCP Protocol**: Standard protocol for AI agent communication

## Architecture

The server implements the Model Context Protocol and provides:

1. **Resources**: Documentation files accessible via MCP resource URIs
2. **Tools**: Four main tools for retrieving guidelines:
   - `get_coding_rules`: Professional coding standards
   - `get_development_skills`: Development best practices
   - `get_steering_instructions`: AI agent guidance
   - `get_custom_guidance`: AI-curated context-specific advice

## Installation

### Prerequisites

- Python 3.11+
- Anthropic API key (optional, but required for `get_custom_guidance` tool)

### Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or with uv:
   ```bash
   uv sync
   ```

3. **(Optional)** Set your Anthropic API key for AI-powered custom guidance:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```
   
   **Note**: The server works without an API key, but the `get_custom_guidance` tool will return a graceful error message directing users to the other three tools. The static documentation tools (`get_coding_rules`, `get_development_skills`, `get_steering_instructions`) work fully without any API key.

## Usage

### Running the MCP Server

```bash
python main.py
```

The server runs as an MCP stdio server, communicating over standard input/output.

### MCP Client Configuration

To use this server with an MCP client (like Claude Desktop), add it to your MCP configuration:

```json
{
  "mcpServers": {
    "ai-dev-guidelines": {
      "command": "python",
      "args": ["/path/to/this/repo/main.py"],
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Available Tools

#### 1. get_coding_rules
Get professional coding rules and standards for writing production-quality code.

```python
# No parameters required
result = await session.call_tool("get_coding_rules", {})
```

#### 2. get_development_skills
Get development skills, best practices, and professional techniques.

```python
# No parameters required
result = await session.call_tool("get_development_skills", {})
```

#### 3. get_steering_instructions
Get AI agent steering instructions for context-aware development.

```python
# No parameters required
result = await session.call_tool("get_steering_instructions", {})
```

#### 4. get_custom_guidance
Get AI-curated guidance tailored to your specific development context.

```python
# Requires query parameter
result = await session.call_tool("get_custom_guidance", {
    "query": "How do I implement secure authentication in a Python web app?",
    "context": "Building a Flask application with user login"  # optional
})
```

### Available Resources

The server exposes three documentation resources:

- `guidelines://rules` - Professional Coding Rules
- `guidelines://skills` - Development Skills & Practices  
- `guidelines://steering` - AI Steering Instructions

## Configuration

Edit `config.yaml` to customize:

- Server name and version
- Documentation file paths
- AI model settings (model, max_tokens, temperature)
- Tool descriptions

## Documentation

The server includes three main documentation files in the `docs/` directory:

- **rules.md**: Professional coding standards, security practices, testing requirements
- **skills.md**: Development skills from debugging to API design
- **steering.md**: AI agent guidance for effective code generation

You can customize these documents to match your organization's standards.

## Project Structure

```
.
├── main.py                    # Entry point
├── config.yaml                # Configuration
├── src/
│   ├── mcp_server.py         # Main MCP server implementation
│   ├── ai_orchestrator.py    # AI-powered context selector
│   └── utils/
│       ├── config.py          # Configuration management
│       └── document_loader.py # Documentation file loader
├── docs/
│   ├── rules.md              # Coding rules
│   ├── skills.md             # Development skills
│   └── steering.md           # AI steering
└── README.md
```

## How It Works

1. **Agent Request**: An AI agent calls one of the MCP tools
2. **Document Loading**: The server loads relevant documentation from markdown files
3. **AI Orchestration** (for custom guidance): Claude analyzes the query and selects relevant content
4. **Response**: The server returns targeted, actionable guidance

## Development

### Running Tests

```bash
pytest
```

### Adding New Documentation

1. Create or edit markdown files in `docs/`
2. Update `config.yaml` to reference new files
3. Restart the server

### Customizing AI Behavior

Edit the system prompts in `src/ai_orchestrator.py` to change how the AI selects and presents documentation.

## Environment Variables

- `ANTHROPIC_API_KEY`: Required for AI orchestration features

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues or questions, please open a GitHub issue.
