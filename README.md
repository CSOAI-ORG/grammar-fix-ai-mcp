# Grammar Fix Ai

> By [MEOK AI Labs](https://meok.ai) — MEOK AI Labs — Grammar correction, spelling fixes, readability analysis, and tone detection.

Grammar correction, spelling fixes, and writing improvement. — MEOK AI Labs.

## Installation

```bash
pip install grammar-fix-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install grammar-fix-ai-mcp
```

## Tools

### `fix_grammar`
Check and fix grammar errors including homophones, punctuation, capitalization, and common mistakes.

**Parameters:**
- `text` (str)
- `dialect` (str)

### `check_spelling`
Check spelling against a comprehensive dictionary of common misspellings with suggestions.

**Parameters:**
- `text` (str)

### `improve_readability`
Analyze and suggest improvements for readability using Flesch-Kincaid and other metrics.

**Parameters:**
- `text` (str)
- `target_level` (str)

### `analyze_tone`
Analyze writing tone and style: formal/informal, positive/negative, assertive/tentative.

**Parameters:**
- `text` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/grammar-fix-ai-mcp](https://github.com/CSOAI-ORG/grammar-fix-ai-mcp)
- **PyPI**: [pypi.org/project/grammar-fix-ai-mcp](https://pypi.org/project/grammar-fix-ai-mcp/)

## License

MIT — MEOK AI Labs
