"""
Drafting Agent - Writes engaging LinkedIn posts based on topic and angle
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


class DraftingAgent:
    """Agent responsible for writing LinkedIn post drafts."""
    
    def __init__(self, google_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.5
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert LinkedIn content writer specializing in creating engaging, professional posts that drive meaningful engagement.

Your role is to write a well-structured, compelling first draft of a LinkedIn post based on the given topic and chosen angle.

LinkedIn Post Best Practices:
1. **Hook**: Start with an attention-grabbing first line that makes people want to read more
2. **Structure**: Use short paragraphs (1-3 lines each) for easy mobile reading
3. **Storytelling**: Include personal anecdotes, case studies, or examples when relevant
4. **Value**: Provide actionable insights, thought-provoking questions, or useful information
5. **Engagement**: End with a question or call-to-action to encourage comments
6. **Length**: Aim for 150-300 words for optimal engagement
7. **Tone**: Professional but conversational, authentic and relatable

Content Structure:
- Opening hook (1-2 lines)
- Context/background (2-3 lines)
- Main insight/message (3-4 lines)
- Supporting points or examples (3-5 lines)
- Closing thought and engagement question (2-3 lines)

Writing Guidelines:
- Use "I", "you", and "we" to create connection
- Include specific examples or data points when possible
- Avoid jargon; write for a broad professional audience
- Create natural line breaks for readability
- Don't include hashtags or emojis (the formatting agent will add these)

Write a complete, engaging LinkedIn post that follows these guidelines."""),
            ("human", "Write a LinkedIn post draft for this topic and angle:\n\nTopic: {topic}\n\nChosen Angle: {angle}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def draft_post(self, topic: str, angle: str) -> str:
        """Draft a LinkedIn post based on topic and angle."""
        try:
            result = self.chain.invoke({"topic": topic, "angle": angle})
            return result
        except Exception as e:
            return f"Error drafting post: {str(e)}"
