<div align="center">

# Grammar Fix Ai MCP

**MCP server for grammar fix ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-grammar-fix-ai-mcp)](https://pypi.org/project/meok-grammar-fix-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Grammar Fix Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `fix_grammar` | Check and fix grammar errors including homophones, punctuation, capitalization,  |
| `check_spelling` | Check spelling against a comprehensive dictionary of common misspellings with su |
| `improve_readability` | Analyze and suggest improvements for readability using Flesch-Kincaid and other  |
| `analyze_tone` | Analyze writing tone and style: formal/informal, positive/negative, assertive/te |

## Installation

```bash
pip install meok-grammar-fix-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "grammar-fix-ai": {
      "command": "python",
      "args": ["-m", "meok_grammar_fix_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
