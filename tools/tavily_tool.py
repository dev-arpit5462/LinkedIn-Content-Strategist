"""
Tavily Search Tool - Primary web search tool for comprehensive research
"""
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient
import os


class TavilySearchInput(BaseModel):
    """Input for Tavily search tool."""
    query: str = Field(description="Search query for web content")


class TavilySearchTool(BaseTool):
    """Tool for comprehensive web searches using Tavily API."""
    
    name: str = "tavily_search"
    description: str = "Search the web for comprehensive information, articles, tutorials, and expert opinions. Best for general questions, lists, explanations, and evergreen content."
    args_schema: Type[BaseModel] = TavilySearchInput
    api_key: str
    
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)
    
    def _run(self, query: str) -> str:
        """Execute the web search."""
        try:
            # Create client for this search
            client = TavilyClient(api_key=self.api_key)
            
            # Perform search with Tavily
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
                include_answer=True,
                include_raw_content=False
            )
            
            if not response or 'results' not in response:
                return f"No search results found for query: {query}"
            
            # Format the results
            formatted_results = []
            
            # Include the AI-generated answer if available
            if response.get('answer'):
                formatted_results.append(f"**Summary Answer:** {response['answer']}\n")
            
            # Format individual results
            results = response.get('results', [])
            for i, result in enumerate(results[:5], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content')
                url = result.get('url', '')
                
                formatted_result = f"""
**Result {i}:**
Title: {title}
Content: {content[:300]}{'...' if len(content) > 300 else ''}
URL: {url}
"""
                formatted_results.append(formatted_result)
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        return self._run(query)
