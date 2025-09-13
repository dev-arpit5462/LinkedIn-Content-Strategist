# LinkedIn Content Strategist v2.0

A sophisticated AI-powered LinkedIn content creation application featuring intelligent multi-tool research capabilities. Version 2.0 introduces a **MasterResearchAgent** that intelligently selects the best research tool (web search, news, Wikipedia, YouTube) for each query, delivering richer and more relevant content than ever before.

## 🚀 What's New in v2.0

### Multi-Tool Intelligent Research
- **Smart Tool Selection**: AI automatically chooses the best research source
- **4 Research Tools**: Web search, news, Wikipedia, and YouTube integration
- **Enhanced Content Quality**: Richer, more diverse research data
- **Transparent Decision Making**: See which tool was selected and why

## 🏗️ Architecture

### Hierarchical Agent System

**Level 0: Orchestrator**
- Main Streamlit application with enhanced workflow visualization

**Level 1: Chain Controllers**
- `AnalysisChain`: Links MasterResearchAgent → TopicAnalyst
- `CreationChain`: Links AngleGenerator → Drafting → Critique → Formatting

**Level 2: Specialist Agents**
- **MasterResearchAgent**: Intelligently selects and uses the best research tool
- **TopicAnalystAgent**: Identifies compelling LinkedIn topics from research data
- **AngleGeneratorAgent**: Creates 3 distinct content angles (Contrarian, How-To, Future-Looking)
- **DraftingAgent**: Writes initial LinkedIn post drafts
- **CritiqueAgent**: Provides adversarial feedback for improvement
- **FormattingAgent**: Creates final polished posts with hashtags and formatting

### Research Tools

**1. Tavily Web Search** (Primary Tool)
- Comprehensive web search with AI-generated summaries
- Best for: General questions, tutorials, lists, expert opinions
- Advanced search depth with curated results

**2. GNews API**
- Real-time breaking news and industry developments
- Best for: Recent events, timely content, industry updates

**3. Wikipedia Integration**
- Foundational knowledge and definitions
- Best for: Background context, company information, historical data

**4. YouTube Search**
- Video content discovery
- Best for: Tutorials, reviews, expert discussions

## 🚀 Features

- **Intelligent Tool Selection**: AI automatically chooses the best research source
- **Multi-Source Research**: Web, news, Wikipedia, and YouTube integration
- **Enhanced Workflow Visibility**: See tool selection reasoning in real-time
- **Multi-Agent Content Pipeline**: Hierarchical AI agents for comprehensive content creation
- **Interactive Topic Selection**: Choose from AI-identified compelling topics
- **Adversarial Quality Control**: Built-in critique system for content improvement
- **Professional Formatting**: LinkedIn-optimized posts with hashtags and proper structure
- **Transparent Decision Making**: Complete visibility into AI reasoning process
- **One-Click Publishing**: Copy-to-clipboard functionality

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **Language Model**: Google Gemini 2.0 Flash
- **Research Sources**: Tavily API, GNews API, Wikipedia, YouTube
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- GNews API key
- Tavily API key (New in v2.0)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkedin-content-strategist
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your API keys
   GOOGLE_API_KEY="your_gemini_api_key_here"
   GNEWS_API_KEY="your_gnews_api_key_here"
   TAVILY_API_KEY="your_tavily_api_key_here"
   ```

## 🔑 API Keys Setup

### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### GNews API Key
1. Visit [GNews.io](https://gnews.io/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy the key to your `.env` file

### Tavily API Key (New in v2.0)
1. Visit [Tavily.com](https://tavily.com/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Copy the key to your `.env` file

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **API Keys**
   - API keys are automatically loaded from your `.env` file
   - No manual configuration needed in the UI

3. **Generate Content**
   - Enter your professional field and interests
   - Click "Find Topics" to start intelligent research
   - Watch the workflow log to see tool selection reasoning
   - Select a topic from the AI-identified options
   - Click "Create Post" to generate your LinkedIn content
   - Copy the final post to clipboard

## 📁 Project Structure

```
linkedin-content-strategist/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── agents/                    # AI agent implementations
│   ├── __init__.py
│   ├── master_research_agent.py # Intelligent multi-tool research agent
│   ├── topic_analyst.py       # Topic identification agent
│   ├── angle_generator.py     # Content angle creation agent
│   ├── drafting_agent.py      # Post drafting agent
│   ├── critique_agent.py      # Quality control agent
│   └── formatting_agent.py    # Final formatting agent
├── chains/                    # LangChain orchestration
│   ├── __init__.py
│   ├── analysis_chain.py      # Research → Topics chain
│   └── creation_chain.py      # Angles → Final post chain
└── tools/                     # Custom LangChain tools
    ├── __init__.py
    ├── gnews_tool.py          # GNews API integration
    ├── tavily_tool.py         # Tavily web search integration
    ├── youtube_tool.py        # YouTube search integration
    └── wikipedia_tool.py      # Wikipedia search integration
```

## 🔄 v2.0 Workflow

1. **Intelligent Research Phase**
   - MasterResearchAgent analyzes the user's request
   - AI selects the optimal tool: Tavily (web), GNews (news), Wikipedia (definitions), or YouTube (videos)
   - Comprehensive research data gathered from the chosen source
   - TopicAnalystAgent identifies 2-3 compelling topics from research

2. **Content Creation Phase**
   - AngleGeneratorAgent creates 3 distinct content angles
   - DraftingAgent writes initial post based on selected topic/angle
   - CritiqueAgent provides improvement feedback
   - FormattingAgent creates final polished post

3. **Enhanced Output**
   - Professional LinkedIn post with proper formatting
   - Relevant hashtags and strategic emoji usage
   - Complete workflow transparency showing tool selection reasoning
   - Copy-to-clipboard functionality

## 🎯 Content Quality Features

- **Hook Optimization**: Attention-grabbing opening lines
- **Mobile-First Formatting**: Short paragraphs for mobile readability
- **Professional Tone**: Balanced professional yet conversational style
- **Engagement Focus**: Built-in call-to-action and discussion prompts
- **LinkedIn Best Practices**: Optimized length, structure, and formatting

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure API keys are correctly set in `.env` file
   - Verify API keys are valid and have sufficient quota

2. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Activate virtual environment before running

3. **News Search Issues**
   - Check GNews API key validity
   - Ensure internet connection is stable

### Error Logging

The application includes comprehensive error handling and logging. Check the "Workflow Log" in the Streamlit interface for detailed error information.

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
The application can be deployed on:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Docker containers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain for the powerful agent framework
- Google for the Gemini API
- GNews.io for news data
- Streamlit for the web interface

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the workflow logs in the application
3. Create an issue in the repository

---

**Built with ❤️ using LangChain, Google Gemini, and Streamlit**
