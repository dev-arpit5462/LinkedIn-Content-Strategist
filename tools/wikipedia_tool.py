"""
Wikipedia Tool - For getting definitions and foundational knowledge
"""
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import wikipedia


class WikipediaSearchInput(BaseModel):
    """Input for Wikipedia search tool."""
    query: str = Field(description="Search query for Wikipedia articles")


class WikipediaSearchTool(BaseTool):
    """Tool for searching Wikipedia for definitions, historical context, and foundational knowledge."""
    
    name: str = "wikipedia_search"
    description: str = "Search Wikipedia for definitions, historical context, foundational knowledge about topics, people, or companies. Best for factual information and background context."
    args_schema: Type[BaseModel] = WikipediaSearchInput
    
    def _run(self, query: str) -> str:
        """Execute the Wikipedia search."""
        try:
            # Search for pages
            search_results = wikipedia.search(query, results=3)
            
            if not search_results:
                return f"No Wikipedia articles found for query: {query}"
            
            formatted_results = []
            
            for i, title in enumerate(search_results[:3], 1):
                try:
                    # Get page summary
                    page = wikipedia.page(title)
                    summary = wikipedia.summary(title, sentences=3)
                    
                    formatted_result = f"""
**Article {i}: {title}**
Summary: {summary}
URL: {page.url}
"""
                    formatted_results.append(formatted_result)
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation by taking the first option
                    try:
                        page = wikipedia.page(e.options[0])
                        summary = wikipedia.summary(e.options[0], sentences=3)
                        formatted_result = f"""
**Article {i}: {e.options[0]}**
Summary: {summary}
URL: {page.url}
"""
                        formatted_results.append(formatted_result)
                    except:
                        continue
                        
                except wikipedia.exceptions.PageError:
                    continue
                except Exception:
                    continue
            
            if not formatted_results:
                return f"Could not retrieve Wikipedia content for query: {query}"
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error searching Wikipedia: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        return self._run(query)
