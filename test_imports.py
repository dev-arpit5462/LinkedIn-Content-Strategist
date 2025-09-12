"""
Test script to validate import structure and basic functionality
"""
import sys
import os

def test_imports():
    """Test if all modules can be imported correctly."""
    print("Testing import structure...")
    
    try:
        # Test tools import
        sys.path.append(os.path.dirname(__file__))
        from tools import GNewsSearchTool
        print("✅ Tools module imported successfully")
        
        # Test agents import
        from agents import (
            NewsResearcherAgent, TopicAnalystAgent, AngleGeneratorAgent,
            DraftingAgent, CritiqueAgent, FormattingAgent
        )
        print("✅ All agent modules imported successfully")
        
        # Test chains import
        from chains import AnalysisChain, CreationChain
        print("✅ Chain modules imported successfully")
        
        print("\n🎉 All imports successful! The application structure is correct.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def validate_file_structure():
    """Validate that all required files exist."""
    print("\nValidating file structure...")
    
    required_files = [
        "app.py",
        "requirements.txt", 
        ".env.example",
        "README.md",
        "tools/__init__.py",
        "tools/gnews_tool.py",
        "agents/__init__.py",
        "agents/news_researcher.py",
        "agents/topic_analyst.py",
        "agents/angle_generator.py",
        "agents/drafting_agent.py",
        "agents/critique_agent.py",
        "agents/formatting_agent.py",
        "chains/__init__.py",
        "chains/analysis_chain.py",
        "chains/creation_chain.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

if __name__ == "__main__":
    print("=" * 50)
    print("LangChain Content Strategist - Validation Test")
    print("=" * 50)
    
    structure_valid = validate_file_structure()
    imports_valid = test_imports() if structure_valid else False
    
    print("\n" + "=" * 50)
    if structure_valid and imports_valid:
        print("🎉 APPLICATION READY FOR USE!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up your .env file with API keys")
        print("3. Run the app: streamlit run app.py")
    else:
        print("❌ Application has issues that need to be resolved")
    print("=" * 50)
