#!/usr/bin/env python3
"""Test client for the MCP Development Guidelines Server."""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """Test the MCP server by calling its tools."""
    
    print("=" * 60)
    print("Testing AI Development Guidelines MCP Server")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("\n✓ Server initialized successfully")
                
                print("\n--- Testing Resources ---")
                resources = await session.list_resources()
                print(f"Available resources: {len(resources.resources)}")
                for resource in resources.resources:
                    print(f"  - {resource.name} ({resource.uri})")
                
                print("\n--- Testing Tools ---")
                tools = await session.list_tools()
                print(f"Available tools: {len(tools.tools)}")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description[:80]}...")
                
                print("\n--- Testing get_coding_rules Tool ---")
                result = await session.call_tool("get_coding_rules", {})
                content = result.content[0].text if result.content else ""
                print(f"Received coding rules ({len(content)} characters)")
                print(f"Preview: {content[:200]}...")
                
                print("\n--- Testing get_development_skills Tool ---")
                result = await session.call_tool("get_development_skills", {})
                content = result.content[0].text if result.content else ""
                print(f"Received skills documentation ({len(content)} characters)")
                print(f"Preview: {content[:200]}...")
                
                print("\n--- Testing get_steering_instructions Tool ---")
                result = await session.call_tool("get_steering_instructions", {})
                content = result.content[0].text if result.content else ""
                print(f"Received steering instructions ({len(content)} characters)")
                print(f"Preview: {content[:200]}...")
                
                print("\n--- Testing get_custom_guidance Tool ---")
                result = await session.call_tool("get_custom_guidance", {
                    "query": "How should I handle errors in Python web applications?",
                    "context": "Building a Flask REST API"
                })
                content = result.content[0].text if result.content else ""
                print(f"Received custom guidance ({len(content)} characters)")
                if "AI Orchestrator is not available" in content:
                    print("Note: AI Orchestrator not configured (ANTHROPIC_API_KEY not set)")
                    print("This is expected - the tool gracefully degrades without the API key")
                else:
                    print(f"Preview: {content[:200]}...")
                
                print("\n--- Testing Resource Reading ---")
                resource_content = await session.read_resource("guidelines://rules")
                content_text = resource_content.contents[0].text if resource_content.contents else ""
                print(f"Read resource 'guidelines://rules' ({len(content_text)} characters)")
                
                print("\n" + "=" * 60)
                print("✓ All tests passed successfully!")
                print("=" * 60)
                
    except Exception as e:
        print(f"\n✗ Error during testing: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
