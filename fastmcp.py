"""
Simple FastMCP implementation for MCP (Model Context Protocol) tools.
This is a local implementation since the package is not available on PyPI.
"""

import asyncio
import json
from typing import Any, Callable, Dict, List, Optional
from functools import wraps


class FastMCP:
    """
    Simple MCP server implementation for creating tools.
    """
    
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.tools: Dict[str, Callable] = {}
        self.tool_descriptions: Dict[str, str] = {}
    
    def tool(self, name: Optional[str] = None, description: Optional[str] = None):
        """
        Decorator to register a tool function.
        """
        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            tool_description = description or func.__doc__ or f"Tool: {tool_name}"
            
            self.tools[tool_name] = func
            self.tool_descriptions[tool_name] = tool_description
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    return {"error": str(e)}
            
            return wrapper
        return decorator
    
    def get_tools(self) -> Dict[str, Callable]:
        """Get all registered tools."""
        return self.tools
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all tools."""
        return self.tool_descriptions
    
    def call_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Call a specific tool by name."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        return self.tools[tool_name](*args, **kwargs)


class FastMCPClient:
    """
    Simple MCP client implementation.
    """
    
    def __init__(self, server_name: str):
        self.server_name = server_name
    
    def call_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Call a tool on the server."""
        # This is a simplified implementation
        # In a real MCP setup, this would communicate with the server
        return {"message": f"Tool {tool_name} called on {self.server_name}"}


class Client:
    """
    Simple MCP client for testing.
    """
    
    def __init__(self, server_name: str):
        self.server_name = server_name
    
    def call_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Call a tool on the server."""
        return {"message": f"Tool {tool_name} called on {self.server_name}"}
