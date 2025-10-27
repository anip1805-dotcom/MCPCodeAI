"""AI orchestrator for intelligent context selection."""

import os
from typing import Optional
from anthropic import Anthropic


class AIOrchestrator:
    """
    AI-powered orchestrator that selects and combines documentation
    based on agent requests using Anthropic Claude.
    """
    
    def __init__(self, model: str, max_tokens: int = 4000, temperature: float = 0.7):
        """
        Initialize AI orchestrator.
        
        Args:
            model: Anthropic model name to use
            max_tokens: Maximum tokens for AI response
            temperature: Temperature for AI responses (0-1)
        """
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    def get_custom_guidance(
        self,
        query: str,
        rules: str,
        skills: str,
        steering: str,
        context: Optional[str] = None
    ) -> str:
        """
        Generate custom guidance based on a specific query and available documentation.
        
        Args:
            query: The agent's question or context description
            rules: Professional coding rules documentation
            skills: Development skills documentation
            steering: AI steering instructions
            context: Optional additional context about the agent's situation
        
        Returns:
            AI-generated custom guidance tailored to the query
        """
        system_prompt = """You are an expert software engineering advisor. Your role is to provide 
professional development guidance to AI agents assisting with coding tasks.

You have access to three comprehensive documentation sources:
1. Professional coding rules and standards
2. Development skills and best practices
3. AI agent steering instructions

Based on the agent's query, select the most relevant information from these sources and create
a focused, actionable response. Combine insights from multiple sources when appropriate.

Provide clear, professional guidance that helps the agent write production-quality code.
Be specific and practical. Include code examples when helpful."""

        context_section = f"\n\nAdditional Context: {context}" if context else ""
        
        user_prompt = f"""Agent Query: {query}{context_section}

Available Documentation:

=== PROFESSIONAL CODING RULES ===
{rules}

=== DEVELOPMENT SKILLS & PRACTICES ===
{skills}

=== AI STEERING INSTRUCTIONS ===
{steering}

Based on the agent's query and the documentation above, provide targeted guidance that will help
the agent accomplish their task professionally and effectively. Focus on the most relevant parts
of the documentation for this specific situation."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            content_block = message.content[0]
            if hasattr(content_block, 'text'):
                return content_block.text
            else:
                return str(content_block)
        
        except Exception as e:
            return f"Error generating custom guidance: {str(e)}"
    
    def analyze_request(self, request_description: str) -> dict[str, bool]:
        """
        Analyze a request to determine which documentation types would be most helpful.
        
        Args:
            request_description: Description of what the agent needs help with
        
        Returns:
            Dictionary indicating which docs are relevant (rules, skills, steering)
        """
        system_prompt = """You are analyzing an AI agent's development request to determine which 
types of documentation would be most helpful. You must respond with ONLY a JSON object containing 
three boolean fields: rules, skills, and steering.

- rules: true if the request involves coding standards, security, testing, or code quality
- skills: true if the request involves problem-solving, debugging, architecture, or methodology
- steering: true if the request involves decision-making, planning, or context awareness

Respond ONLY with valid JSON, nothing else."""

        user_prompt = f"""Analyze this request and determine which documentation types are needed:

Request: {request_description}

Respond with JSON only: {{"rules": true/false, "skills": true/false, "steering": true/false}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            import json
            content_block = message.content[0]
            if hasattr(content_block, 'text'):
                response_text = content_block.text.strip()
            else:
                response_text = str(content_block).strip()
            
            result = json.loads(response_text)
            
            return {
                'rules': result.get('rules', True),
                'skills': result.get('skills', True),
                'steering': result.get('steering', True)
            }
        
        except Exception:
            return {'rules': True, 'skills': True, 'steering': True}
