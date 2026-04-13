#!/usr/bin/env python3
"""grammar-fix-ai-mcp — Fix grammar and style in text."""
import asyncio, json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
import mcp.types as types

server = Server("grammar-fix-ai-mcp")

@server.list_tools()
async def list_tools():
    return [Tool(name="run", description="Fix grammar and style in text.", inputSchema={"type":"object","properties":{"input":{"type":"string"}},"required":["input"]})]

@server.call_tool()
async def call_tool(name, arguments=None):
    inp = (arguments or {}).get("input", "")
    result = {"output": f"Processed: {inp}"}
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    async with stdio_server(server._read_stream, server._write_stream) as (rs, ws):
        await server.run(rs, ws, InitializationOptions(server_name="grammar-fix-ai-mcp", server_version="0.1.0", capabilities=server.get_capabilities()))

if __name__ == "__main__":
    asyncio.run(main())
