"""
LangChain Content Strategist - AI-powered LinkedIn content creation
"""
import streamlit as st
import os
from dotenv import load_dotenv
import pyperclip
from chains.analysis_chain import AnalysisChain
from chains.creation_chain import CreationChain

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LinkedIn Content Strategist",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .workflow-step {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0066cc;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'workflow_log' not in st.session_state:
        st.session_state.workflow_log = []
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'creation_result' not in st.session_state:
        st.session_state.creation_result = None
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'show_topic_selection' not in st.session_state:
        st.session_state.show_topic_selection = False
    if 'show_final_post' not in st.session_state:
        st.session_state.show_final_post = False

def add_to_workflow_log(step, message, status="info"):
    """Add step to workflow log"""
    st.session_state.workflow_log.append({
        "step": step,
        "message": message,
        "status": status
    })

def display_workflow_log():
    """Show workflow progress"""
    with st.expander("🔍 Workflow Log", expanded=True):
        if not st.session_state.workflow_log:
            st.info("Progress will show here...")
        else:
            for entry in st.session_state.workflow_log:
                if entry["status"] == "success":
                    st.success(f"**{entry['step']}:** {entry['message']}")
                elif entry["status"] == "error":
                    st.error(f"**{entry['step']}:** {entry['message']}")
                else:
                    st.info(f"**{entry['step']}:** {entry['message']}")

def parse_topics_from_analysis(topics_text):
    """Extract topics from analysis"""
    topics = []
    lines = topics_text.split('\n')
    current_topic = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('Topic'):
            if current_topic:
                topics.append(current_topic)
            if ':' in line:
                current_topic = {"title": line.split(':', 1)[1].strip()}
            else:
                current_topic = {"title": line}
        elif line.startswith('Why it matters:'):
            current_topic["why"] = line.replace('Why it matters:', '').strip()
        elif line.startswith('Key angle:'):
            current_topic["angle"] = line.replace('Key angle:', '').strip()
    
    if current_topic:
        topics.append(current_topic)
    
    return topics

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🚀 LangChain Content Strategist</h1>', unsafe_allow_html=True)
    
    # Load API keys from environment
    google_api_key = os.getenv("GOOGLE_API_KEY")
    gnews_api_key = os.getenv("GNEWS_API_KEY")
    
    # Validation
    if not google_api_key or not gnews_api_key:
        st.error("⚠️ API keys not found in environment variables.")
        st.info("""
        **Setup Required:**
        1. Create a `.env` file in the project directory
        2. Add your API keys:
           ```
           GOOGLE_API_KEY="your_gemini_api_key"
           GNEWS_API_KEY="your_gnews_api_key"
           ```
        3. Restart the application
        
        **Get API Keys:**
        - **Google Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
        - **GNews API**: [GNews.io](https://gnews.io/)
        """)
        return
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Content Generation")
        
        # Input field
        professional_field = st.text_area(
            "Your Field & Interests",
            placeholder="e.g., AI in Healthcare, Digital Marketing, Finance, etc.",
            height=100,
            help="What industry or topics do you work with?"
        )
        
        # Main action button
        if st.button("🔍 Find Topics", type="primary", disabled=not professional_field.strip()):
            if professional_field.strip():
                # Clear previous results
                st.session_state.analysis_result = None
                st.session_state.creation_result = None
                st.session_state.selected_topic = None
                st.session_state.show_topic_selection = False
                st.session_state.show_final_post = False
                st.session_state.workflow_log = []
                
                # Initialize chains
                try:
                    add_to_workflow_log("Setup", "Getting ready...", "info")
                    analysis_chain = AnalysisChain(google_api_key, gnews_api_key)
                    
                    # Execute analysis chain
                    add_to_workflow_log("Research", "Looking for recent news...", "info")
                    with st.spinner("🔍 Finding relevant topics..."):
                        result = analysis_chain.invoke(professional_field)
                        st.session_state.analysis_result = result
                    
                    if "Error" not in result.get("topics", ""):
                        add_to_workflow_log("Analysis", "Found some good topics", "success")
                        st.session_state.show_topic_selection = True
                    else:
                        add_to_workflow_log("Error", f"Failed to analyze topics: {result.get('topics', 'Unknown error')}", "error")
                        
                except Exception as e:
                    add_to_workflow_log("Error", f"Failed to initialize or execute analysis: {str(e)}", "error")
        
        # Topic Selection
        if st.session_state.show_topic_selection and st.session_state.analysis_result:
            st.subheader("🎯 Pick a Topic")
            
            topics = parse_topics_from_analysis(st.session_state.analysis_result.get("topics", ""))
            
            if topics:
                topic_options = []
                for i, topic in enumerate(topics):
                    title = topic.get("title", f"Topic {i+1}")
                    why = topic.get("why", "")
                    option = f"{title}"
                    if why:
                        option += f" - {why[:100]}..."
                    topic_options.append(option)
                
                selected_index = st.radio(
                    "Which topic interests you?",
                    range(len(topic_options)),
                    format_func=lambda x: topic_options[x]
                )
                
                selected_topic_data = topics[selected_index]
                st.session_state.selected_topic = selected_topic_data.get("title", "")
                
                # Create post button
                if st.button("✨ Create Post", type="primary"):
                    try:
                        add_to_workflow_log("Writing", "Creating your post...", "info")
                        creation_chain = CreationChain(google_api_key)
                        
                        with st.spinner("✨ Working on it..."):
                            creation_result = creation_chain.invoke(st.session_state.selected_topic)
                            st.session_state.creation_result = creation_result
                        
                        if "Error" not in creation_result.get("final_post", ""):
                            add_to_workflow_log("Done", "Post is ready!", "success")
                            st.session_state.show_final_post = True
                        else:
                            add_to_workflow_log("Error", f"Failed to generate post: {creation_result.get('final_post', 'Unknown error')}", "error")
                            
                    except Exception as e:
                        add_to_workflow_log("Error", f"Failed to generate content: {str(e)}", "error")
            else:
                st.error("No topics could be parsed from the analysis. Please try again.")
        
        # Show final post
        if st.session_state.show_final_post and st.session_state.creation_result:
            st.subheader("🎉 Your Post")
            
            final_post = st.session_state.creation_result.get("final_post", "")
            
            if final_post and "Error" not in final_post:
                # Display the final post
                st.markdown("### 📋 Ready to Publish:")
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #dee2e6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #000000;">
                {final_post.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_copy, col_restart = st.columns(2)
                
                with col_copy:
                    if st.button("📋 Copy to Clipboard"):
                        try:
                            pyperclip.copy(final_post)
                            st.success("✅ Post copied to clipboard!")
                        except Exception as e:
                            st.error(f"Failed to copy: {str(e)}")
                            st.code(final_post)
                
                with col_restart:
                    if st.button("🔄 Start Over"):
                        # Clear all session state
                        for key in list(st.session_state.keys()):
                            del st.session_state[key]
                        st.rerun()
            else:
                st.error("Failed to generate the final post. Please check the workflow log for details.")
    
    with col2:
        display_workflow_log()
        
        # Show intermediate results in expanders
        if st.session_state.analysis_result:
            with st.expander("📊 Analysis Results"):
                st.text_area("News Data", st.session_state.analysis_result.get("news_data", ""), height=150)
                st.text_area("Identified Topics", st.session_state.analysis_result.get("topics", ""), height=200)
        
        if st.session_state.creation_result:
            with st.expander("📝 Creation Process"):
                st.text_area("Generated Angles", st.session_state.creation_result.get("angles", ""), height=150)
                st.text_area("Initial Draft", st.session_state.creation_result.get("draft", ""), height=150)
                st.text_area("Critique Feedback", st.session_state.creation_result.get("critique", ""), height=150)

if __name__ == "__main__":
    main()
