"""
Master Research Agent - Intelligent multi-tool research agent
"""
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.gnews_tool import GNewsSearchTool
from tools.tavily_tool import TavilySearchTool
from tools.youtube_tool import YouTubeSearchTool
from tools.wikipedia_tool import WikipediaSearchTool


class MasterResearchAgent:
    """Intelligent research agent that selects the best tool for each query."""
    
    def __init__(self, google_api_key: str, gnews_api_key: str, tavily_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        # Initialize all available tools
        self.tools = [
            GNewsSearchTool(gnews_api_key),
            TavilySearchTool(tavily_api_key),
            YouTubeSearchTool(),
            WikipediaSearchTool()
        ]
        
        # Create ReAct-style prompt for intelligent tool selection
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a highly intelligent research assistant. Your goal is to find the most accurate and insightful information for a given topic to help create a LinkedIn post.

You have access to these tools:
- **gnews_search**: For recent events, breaking news, and timely industry developments
- **tavily_search**: For general questions, lists, explanations, tutorials, and comprehensive web content (PRIMARY TOOL)
- **youtube_search**: For video content, tutorials, reviews, and expert discussions
- **wikipedia_search**: For definitions, historical context, and foundational knowledge

**Your Reasoning Process:**
1. Analyze the user's request carefully
2. Determine which tool will provide the most valuable information
3. Use this decision logic:
   - Recent events/breaking news → **gnews_search**
   - General questions, "best tools for...", "how to...", lists, opinions → **tavily_search** (DEFAULT)
   - Complex terms needing definition, historical entities, company backgrounds → **wikipedia_search**
   - Video tutorials, reviews, visual content → **youtube_search**
4. Execute the chosen tool and provide comprehensive results

**Important:** Always explain your tool choice in your thought process. Be thorough in your research to provide rich content for LinkedIn post creation.

Begin your analysis and tool selection:"""),
            ("human", "Research this topic for LinkedIn content creation: {field}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        # Create agent with enhanced reasoning
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def research(self, field_or_topic: str) -> dict:
        """Conduct intelligent research using the best available tool."""
        try:
            result = self.agent_executor.invoke({"field": field_or_topic})
            
            # Extract tool selection reasoning from the agent's output
            output = result.get("output", "")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Better tool detection from intermediate steps
            used_tool = "Unknown"
            reasoning = f"Analyzed query: {field_or_topic}"
            
            # Check intermediate steps for tool usage
            for step in intermediate_steps:
                if len(step) >= 2:
                    action = step[0]
                    if hasattr(action, 'tool'):
                        tool_name = action.tool
                        if tool_name == "gnews_search":
                            used_tool = "GNews Search"
                            reasoning = f"Selected news search for recent developments in: {field_or_topic}"
                        elif tool_name == "tavily_search":
                            used_tool = "Tavily Web Search"
                            reasoning = f"Selected web search for comprehensive information on: {field_or_topic}"
                        elif tool_name == "youtube_search":
                            used_tool = "YouTube Search"
                            reasoning = f"Selected video search for tutorials/discussions on: {field_or_topic}"
                        elif tool_name == "wikipedia_search":
                            used_tool = "Wikipedia Search"
                            reasoning = f"Selected Wikipedia for foundational knowledge on: {field_or_topic}"
                        break
            
            # Fallback: check output content for tool indicators
            if used_tool == "Unknown":
                output_lower = output.lower()
                if "article" in output_lower and "news" in output_lower:
                    used_tool = "GNews Search"
                    reasoning = f"Detected news content for: {field_or_topic}"
                elif "wikipedia" in output_lower or "definition" in output_lower:
                    used_tool = "Wikipedia Search"
                    reasoning = f"Detected encyclopedia content for: {field_or_topic}"
                elif "video" in output_lower or "youtube" in output_lower:
                    used_tool = "YouTube Search"
                    reasoning = f"Detected video content for: {field_or_topic}"
                else:
                    used_tool = "Tavily Web Search"
                    reasoning = f"Used web search for: {field_or_topic}"
            
            return {
                "research_data": output,
                "tool_used": used_tool,
                "reasoning": reasoning
            }
            
        except Exception as e:
            return {
                "research_data": f"Error during research: {str(e)}",
                "tool_used": "None",
                "reasoning": f"Failed to complete research: {str(e)}"
            }
