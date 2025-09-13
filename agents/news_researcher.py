"""
News Researcher Agent - Information gatherer for LinkedIn content strategy
"""
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.gnews_tool import GNewsSearchTool


class NewsResearcherAgent:
    """Agent responsible for gathering relevant news information."""
    
    def __init__(self, google_api_key: str, gnews_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.3
        )
        
        # Initialize tools
        self.tools = [GNewsSearchTool(gnews_api_key)]
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional news researcher specializing in finding relevant, recent news for LinkedIn content creation.

Your role:
- Search for the most current and relevant news in the user's professional field
- Focus on trends, innovations, industry developments, and newsworthy events
- Prioritize articles that would be valuable for LinkedIn professional audience
- Look for stories that offer opportunities for professional commentary and insights

When searching:
1. Use specific, targeted keywords related to the user's field
2. Focus on recent developments (last 7-14 days when possible)
3. Look for stories that professionals in this field would find valuable
4. Consider different angles: industry trends, company news, regulatory changes, technological advances

Always use the gnews_search tool to find relevant articles."""),
            ("human", "Find recent news relevant to this professional field and interests: {field}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        # Create agent
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            handle_parsing_errors=True
        )
    
    def research(self, professional_field: str) -> str:
        """Research news for the given professional field."""
        try:
            result = self.agent_executor.invoke({"field": professional_field})
            return result["output"]
        except Exception as e:
            return f"Error during news research: {str(e)}"
