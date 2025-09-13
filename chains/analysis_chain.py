"""
Analysis Chain - Orchestrates MasterResearch and TopicAnalyst agents
"""
from langchain_core.runnables import RunnableLambda
from agents.master_research_agent import MasterResearchAgent
from agents.topic_analyst import TopicAnalystAgent


class AnalysisChain:
    """Chain that links MasterResearchAgent and TopicAnalystAgent."""
    
    def __init__(self, google_api_key: str, gnews_api_key: str, tavily_api_key: str):
        self.master_researcher = MasterResearchAgent(google_api_key, gnews_api_key, tavily_api_key)
        self.topic_analyst = TopicAnalystAgent(google_api_key)
        
        # Create the chain using LCEL
        self.chain = (
            RunnableLambda(self._research_news) |
            RunnableLambda(self._analyze_topics)
        )
    
    def _research_news(self, input_data: dict) -> dict:
        """Research information for the given professional field."""
        professional_field = input_data["professional_field"]
        research_result = self.master_researcher.research(professional_field)
        
        return {
            "professional_field": professional_field,
            "research_data": research_result["research_data"],
            "tool_used": research_result["tool_used"],
            "reasoning": research_result["reasoning"]
        }
    
    def _analyze_topics(self, input_data: dict) -> dict:
        """Analyze research data to identify compelling topics."""
        research_data = input_data["research_data"]
        topics = self.topic_analyst.analyze(research_data)
        
        return {
            "professional_field": input_data["professional_field"],
            "research_data": research_data,
            "tool_used": input_data["tool_used"],
            "reasoning": input_data["reasoning"],
            "topics": topics
        }
    
    def invoke(self, professional_field: str) -> dict:
        """Execute the analysis chain."""
        try:
            result = self.chain.invoke({"professional_field": professional_field})
            return result
        except Exception as e:
            return {
                "professional_field": professional_field,
                "research_data": f"Error during research: {str(e)}",
                "tool_used": "None",
                "reasoning": f"Failed to complete research: {str(e)}",
                "topics": f"Error during topic analysis: {str(e)}"
            }
