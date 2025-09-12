"""
Custom LangChain tool for fetching news from GNews API
"""
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import os


class GNewsSearchInput(BaseModel):
    """Input for GNews search tool."""
    query: str = Field(description="Search keywords for news articles")


class GNewsSearchTool(BaseTool):
    """Tool for searching news articles using GNews API."""
    
    name: str = "gnews_search"
    description: str = "Search for recent news articles using keywords. Returns top 3-5 relevant articles with titles and summaries."
    args_schema: Type[BaseModel] = GNewsSearchInput
    api_key: str
    
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)
    
    def _run(self, query: str) -> str:
        """Execute the news search."""
        try:
            # GNews API endpoint
            url = "https://gnews.io/api/v4/search"
            
            params = {
                'q': query,
                'token': self.api_key,
                'lang': 'en',
                'country': 'us',
                'max': 5,  # Get top 5 articles
                'sortby': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            if not articles:
                return f"No news articles found for query: {query}"
            
            # Format the results
            formatted_results = []
            for i, article in enumerate(articles[:5], 1):
                title = article.get('title', 'No title')
                description = article.get('description', 'No description')
                url = article.get('url', '')
                published_at = article.get('publishedAt', '')
                
                formatted_article = f"""
Article {i}:
Title: {title}
Description: {description}
Published: {published_at}
URL: {url}
"""
                formatted_results.append(formatted_article)
            
            return "\n".join(formatted_results)
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching news: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        # For simplicity, we'll use the sync version
        return self._run(query)
