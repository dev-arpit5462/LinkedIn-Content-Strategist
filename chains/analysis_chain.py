"""
Analysis Chain - Orchestrates NewsResearcher and TopicAnalyst agents
"""
from langchain_core.runnables import RunnableLambda
from agents.news_researcher import NewsResearcherAgent
from agents.topic_analyst import TopicAnalystAgent


class AnalysisChain:
    """Chain that links NewsResearcherAgent and TopicAnalystAgent."""
    
    def __init__(self, google_api_key: str, gnews_api_key: str):
        self.news_researcher = NewsResearcherAgent(google_api_key, gnews_api_key)
        self.topic_analyst = TopicAnalystAgent(google_api_key)
        
        # Create the chain using LCEL
        self.chain = (
            RunnableLambda(self._research_news) |
            RunnableLambda(self._analyze_topics)
        )
    
    def _research_news(self, input_data: dict) -> dict:
        """Research news for the given professional field."""
        professional_field = input_data["professional_field"]
        news_data = self.news_researcher.research(professional_field)
        
        return {
            "professional_field": professional_field,
            "news_data": news_data
        }
    
    def _analyze_topics(self, input_data: dict) -> dict:
        """Analyze news data to identify compelling topics."""
        news_data = input_data["news_data"]
        topics = self.topic_analyst.analyze(news_data)
        
        return {
            "professional_field": input_data["professional_field"],
            "news_data": news_data,
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
                "news_data": f"Error during news research: {str(e)}",
                "topics": f"Error during topic analysis: {str(e)}"
            }
