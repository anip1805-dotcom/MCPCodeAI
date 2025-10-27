"""MCP Server implementation for AI development guidelines."""

import asyncio
import time
from typing import Any
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, EmbeddedResource
import mcp.server.stdio

from src.utils.config import Config
from src.utils.document_loader import DocumentLoader
from src.ai_orchestrator import AIOrchestrator
from src.token_optimizer import TokenOptimizer
from src.feedback_collector import FeedbackCollector
from src.cache_manager import CacheManager


class DevelopmentGuidelinesServer:
    """MCP Server that provides AI development guidelines."""
    
    def __init__(self, enable_feedback: bool = True, enable_cache: bool = True):
        """
        Initialize the MCP server.
        
        Args:
            enable_feedback: Whether to enable feedback collection
            enable_cache: Whether to enable compressed cache
        """
        self.config = Config()
        self.doc_loader = DocumentLoader()
        self.token_optimizer = TokenOptimizer(max_tokens=4000)
        self.feedback_collector = FeedbackCollector() if enable_feedback else None
        self.cache_manager = CacheManager() if enable_cache else None
        self.ai_orchestrator: AIOrchestrator | None = None
        
        try:
            self.ai_orchestrator = AIOrchestrator(
                model=self.config.ai_model,
                max_tokens=self.config.ai_max_tokens,
                temperature=self.config.ai_temperature
            )
        except ValueError as e:
            print(f"Warning: AI Orchestrator not initialized: {e}")
            print("The 'get_custom_guidance' tool will not be available.")
        
        if self.cache_manager:
            cache_info = self.cache_manager.get_cache_info()
            if cache_info.get("available"):
                print(f"✓ Compressed cache loaded (version {cache_info.get('version')})")
        
        self.server = Server(self.config.server_name)
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up MCP server handlers."""
        
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available documentation resources."""
            return [
                Resource(
                    uri="guidelines://rules",
                    name="Professional Coding Rules",
                    mimeType="text/markdown",
                    description="Comprehensive professional coding rules and standards"
                ),
                Resource(
                    uri="guidelines://skills",
                    name="Development Skills & Practices",
                    mimeType="text/markdown",
                    description="Essential development skills and best practices"
                ),
                Resource(
                    uri="guidelines://steering",
                    name="AI Steering Instructions",
                    mimeType="text/markdown",
                    description="Instructions for AI agents to code effectively"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri) -> str:
            """
            Read a documentation resource.
            
            Args:
                uri: Resource URI (e.g., 'guidelines://rules')
            
            Returns:
                Resource content as markdown
            """
            uri_str = str(uri)
            if uri_str == "guidelines://rules":
                return self.doc_loader.get_rules(self.config.rules_path)
            elif uri_str == "guidelines://skills":
                return self.doc_loader.get_skills(self.config.skills_path)
            elif uri_str == "guidelines://steering":
                return self.doc_loader.get_steering(self.config.steering_path)
            else:
                raise ValueError(f"Unknown resource URI: {uri_str}")
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            tools = [
                Tool(
                    name="get_coding_rules",
                    description="Get professional coding rules and standards for writing production-quality code. "
                                "Includes security, testing, code organization, documentation, and best practices.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_development_skills",
                    description="Get development skills, best practices, and professional techniques. "
                                "Covers problem-solving, debugging, refactoring, testing, API design, and more.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_steering_instructions",
                    description="Get AI agent steering instructions for context-aware development. "
                                "Includes thinking frameworks, code generation guidelines, and decision-making patterns.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
            
            tools.append(
                Tool(
                    name="get_custom_guidance",
                    description="Get AI-curated guidance tailored to your specific development context or question. "
                                "The AI orchestrator analyzes your query and selects the most relevant guidelines. "
                                "Note: Requires ANTHROPIC_API_KEY to be set.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Your question or description of what you need help with"
                            },
                            "context": {
                                "type": "string",
                                "description": "Optional additional context about your situation"
                            }
                        },
                        "required": ["query"]
                    }
                )
            )
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """
            Handle tool calls with feedback collection and caching.
            
            Args:
                name: Tool name
                arguments: Tool arguments
            
            Returns:
                List of text content responses
            """
            start_time = time.time()
            content = ""
            success = True
            error_msg = None
            
            try:
                if name == "get_coding_rules":
                    if self.cache_manager:
                        cached = self.cache_manager.get_document("rules")
                        content = cached if cached else self.doc_loader.get_rules(self.config.rules_path)
                    else:
                        content = self.doc_loader.get_rules(self.config.rules_path)
                
                elif name == "get_development_skills":
                    if self.cache_manager:
                        cached = self.cache_manager.get_document("skills")
                        content = cached if cached else self.doc_loader.get_skills(self.config.skills_path)
                    else:
                        content = self.doc_loader.get_skills(self.config.skills_path)
                
                elif name == "get_steering_instructions":
                    if self.cache_manager:
                        cached = self.cache_manager.get_document("steering")
                        content = cached if cached else self.doc_loader.get_steering(self.config.steering_path)
                    else:
                        content = self.doc_loader.get_steering(self.config.steering_path)
                
                elif name == "get_custom_guidance":
                    query = arguments.get("query", "")
                    context = arguments.get("context")
                    
                    if not query:
                        content = "Error: 'query' parameter is required"
                        success = False
                    elif self.ai_orchestrator is None:
                        content = ("AI Orchestrator is not available. Please set the ANTHROPIC_API_KEY environment variable to enable AI-powered custom guidance. "
                                 "In the meantime, you can use the other tools (get_coding_rules, get_development_skills, get_steering_instructions) "
                                 "to access the documentation directly.")
                        success = False
                    else:
                        all_docs = self.doc_loader.get_all_docs(
                            self.config.rules_path,
                            self.config.skills_path,
                            self.config.steering_path
                        )
                        
                        content = self.ai_orchestrator.get_custom_guidance(
                            query=query,
                            rules=all_docs['rules'],
                            skills=all_docs['skills'],
                            steering=all_docs['steering'],
                            context=context
                        )
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
            except Exception as e:
                content = f"Error processing request: {str(e)}"
                success = False
                error_msg = str(e)
            
            finally:
                response_time_ms = (time.time() - start_time) * 1000
                
                if self.feedback_collector and success:
                    tokens_used = self.token_optimizer.estimate_tokens(content)
                    self.feedback_collector.record_call(
                        tool_name=name,
                        arguments=arguments,
                        response_size=len(content),
                        tokens_used=tokens_used,
                        response_time_ms=response_time_ms,
                        success=success,
                        error=error_msg
                    )
            
            return [TextContent(type="text", text=content)]
    
    async def run(self) -> None:
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point."""
    server = DevelopmentGuidelinesServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
