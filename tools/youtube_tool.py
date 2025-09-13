"""
YouTube Search Tool - For finding video content and tutorials
"""
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from youtube_search import YoutubeSearch
import json


class YouTubeSearchInput(BaseModel):
    """Input for YouTube search tool."""
    query: str = Field(description="Search query for YouTube videos")


class YouTubeSearchTool(BaseTool):
    """Tool for searching YouTube videos, tutorials, and expert discussions."""
    
    name: str = "youtube_search"
    description: str = "Search YouTube for video content, tutorials, reviews, and expert discussions. Best for finding educational content and visual explanations."
    args_schema: Type[BaseModel] = YouTubeSearchInput
    
    def _run(self, query: str) -> str:
        """Execute the YouTube search."""
        try:
            # Search YouTube videos
            results = YoutubeSearch(query, max_results=5).to_dict()
            
            if not results:
                return f"No YouTube videos found for query: {query}"
            
            # Format the results
            formatted_results = []
            for i, video in enumerate(results, 1):
                title = video.get('title', 'No title')
                channel = video.get('channel', 'Unknown channel')
                duration = video.get('duration', 'Unknown duration')
                views = video.get('views', 'Unknown views')
                url = f"https://www.youtube.com{video.get('url_suffix', '')}"
                
                formatted_video = f"""
**Video {i}:**
Title: {title}
Channel: {channel}
Duration: {duration}
Views: {views}
URL: {url}
"""
                formatted_results.append(formatted_video)
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error searching YouTube: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        return self._run(query)
