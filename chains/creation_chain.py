"""
Creation Chain - Orchestrates content creation agents for LinkedIn posts
"""
from langchain_core.runnables import RunnableLambda
from agents.angle_generator import AngleGeneratorAgent
from agents.drafting_agent import DraftingAgent
from agents.critique_agent import CritiqueAgent
from agents.formatting_agent import FormattingAgent


class CreationChain:
    """Chain that links content creation agents for LinkedIn post generation."""
    
    def __init__(self, google_api_key: str):
        self.angle_generator = AngleGeneratorAgent(google_api_key)
        self.drafting_agent = DraftingAgent(google_api_key)
        self.critique_agent = CritiqueAgent(google_api_key)
        self.formatting_agent = FormattingAgent(google_api_key)
        
        # Create the chain using LCEL
        self.chain = (
            RunnableLambda(self._generate_angles) |
            RunnableLambda(self._draft_post) |
            RunnableLambda(self._critique_draft) |
            RunnableLambda(self._format_final_post)
        )
    
    def _generate_angles(self, input_data: dict) -> dict:
        """Generate content angles for the selected topic."""
        topic = input_data["selected_topic"]
        angles = self.angle_generator.generate_angles(topic)
        
        return {
            "selected_topic": topic,
            "angles": angles,
            "selected_angle": input_data.get("selected_angle", "")
        }
    
    def _draft_post(self, input_data: dict) -> dict:
        """Draft the LinkedIn post based on topic and angle."""
        topic = input_data["selected_topic"]
        selected_angle = input_data["selected_angle"]
        
        # If no specific angle is selected, use the first generated angle
        if not selected_angle and input_data["angles"]:
            # Extract first angle from the generated angles
            angles_text = input_data["angles"]
            # Simple extraction - in a real implementation, you might want more sophisticated parsing
            selected_angle = "Use the first angle from the generated options"
        
        draft = self.drafting_agent.draft_post(topic, selected_angle)
        
        return {
            "selected_topic": topic,
            "angles": input_data["angles"],
            "selected_angle": selected_angle,
            "draft": draft
        }
    
    def _critique_draft(self, input_data: dict) -> dict:
        """Provide critique feedback on the draft."""
        draft = input_data["draft"]
        critique = self.critique_agent.critique(draft)
        
        return {
            "selected_topic": input_data["selected_topic"],
            "angles": input_data["angles"],
            "selected_angle": input_data["selected_angle"],
            "draft": draft,
            "critique": critique
        }
    
    def _format_final_post(self, input_data: dict) -> dict:
        """Create the final formatted post."""
        draft = input_data["draft"]
        critique = input_data["critique"]
        final_post = self.formatting_agent.format_final_post(draft, critique)
        
        return {
            "selected_topic": input_data["selected_topic"],
            "angles": input_data["angles"],
            "selected_angle": input_data["selected_angle"],
            "draft": draft,
            "critique": critique,
            "final_post": final_post
        }
    
    def invoke(self, selected_topic: str, selected_angle: str = "") -> dict:
        """Execute the creation chain."""
        try:
            result = self.chain.invoke({
                "selected_topic": selected_topic,
                "selected_angle": selected_angle
            })
            return result
        except Exception as e:
            return {
                "selected_topic": selected_topic,
                "selected_angle": selected_angle,
                "angles": f"Error generating angles: {str(e)}",
                "draft": f"Error drafting post: {str(e)}",
                "critique": f"Error during critique: {str(e)}",
                "final_post": f"Error creating final post: {str(e)}"
            }
