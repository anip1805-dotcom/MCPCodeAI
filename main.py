#!/usr/bin/env python3
"""Main entry point for the MCP Development Guidelines Server."""

import asyncio
import sys
from src.mcp_server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)
