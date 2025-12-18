# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Agent SDK project that sets up a LiteLLM proxy server for managing AI model API calls. The project provides a unified interface for accessing multiple AI models through DeepSeek API.

## Development Setup

### Environment Setup

This project uses uv for fast package installation with requirements.txt:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install dependencies using uv
uv pip install -r requirements.txt
```

### Required Environment Variables

The project requires these environment variables to be set:

```bash
export DEEPSEEK_API_KEY="sk-76595a859876480cb1de7ed3a7ee9239"
export LITELLM_MASTER_KEY="sk-1234"
```

## Common Commands

### Running the LiteLLM Proxy Server

```bash
# Start the proxy server
litellm --config litellm_config.yaml --port 8000

# Or with environment variables explicitly set
DEEPSEEK_API_KEY=sk-76595a859876480cb1de7ed3a7ee9239 LITELLM_MASTER_KEY=sk-1234 litellm --config litellm_config.yaml
```

### Testing API Configuration

```bash
# Test DeepSeek API directly
curl -X POST https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "stream": false
  }'

# Test via LiteLLM proxy
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "user", "content": "Hello!"
    ]
  }'
```

## Architecture

### Key Components

1. **LiteLLM Configuration** ([`litellm_config.yaml`](litellm_config.yaml))
   - Defines available models (deepseek-chat, deepseek-coder)
   - Configures API authentication through environment variables
   - Sets up master key for proxy authentication

2. **MCP Server References** ([`refs/`](refs/))
   - Contains reference documentation for Claude Agent SDK
   - MCP server setup commands and configurations
   - API integration examples

3. **Dependencies** ([`requirements.txt`](requirements.txt))
   - `claude-agent-sdk`: Python SDK for building Claude Agent applications
   - `litellm[proxy]`: LiteLLM with proxy server support

### Model Access

The project provides access to these models through the LiteLLM proxy:
- `deepseek-chat`: General purpose chat model
- `deepseek-coder`: Code-focused model

## Configuration Files

- `litellm_config.yaml`: LiteLLM proxy server configuration
- `requirements.txt`: Python dependencies

## Security Notes

- API keys are stored in environment variables, not in configuration files
- The `.gitignore` prevents accidental commits of sensitive data
- Proxy server uses master key authentication for additional security layer

## Development Workflow

1. Set up environment variables
2. Create and activate virtual environment
3. Run `uv pip install -r requirements.txt` to install dependencies
4. Start the LiteLLM proxy server
5. Test API endpoints to verify configuration
6. Use Claude Agent SDK to build applications on top of the proxy

## MCP Integration

The project includes MCP (Model Context Protocol) server configurations for:
- Web search capabilities
- Document reading
- Context management
- Z AI model access

These are configured through the Claude MCP commands documented in [`refs/my_mcp.md`](refs/my_mcp.md).