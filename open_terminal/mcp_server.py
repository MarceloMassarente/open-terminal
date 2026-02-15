"""MCP server — exposes every FastAPI endpoint as an MCP tool."""

from fastmcp import FastMCP

from open_terminal.main import app

mcp = FastMCP.from_fastapi(app=app, name="Open Terminal")
