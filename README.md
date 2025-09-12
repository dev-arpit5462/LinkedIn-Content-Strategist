# LangChain Content Strategist

A sophisticated AI-powered LinkedIn content creation application that leverages a hierarchical team of AI agents built with LangChain framework. The application uses Google's Gemini 2.0 Flash model and GNews API to research, analyze, and create engaging LinkedIn posts.

## 🏗️ Architecture

### Hierarchical Agent System

**Level 0: Orchestrator**
- Main Streamlit application that coordinates the entire workflow

**Level 1: Chain Controllers**
- `AnalysisChain`: Links NewsResearcher → TopicAnalyst
- `CreationChain`: Links AngleGenerator → Drafting → Critique → Formatting

**Level 2: Specialist Agents**
- **NewsResearcherAgent**: Gathers relevant news using GNews API
- **TopicAnalystAgent**: Identifies compelling LinkedIn topics from news data
- **AngleGeneratorAgent**: Creates 3 distinct content angles (Contrarian, How-To, Future-Looking)
- **DraftingAgent**: Writes initial LinkedIn post drafts
- **CritiqueAgent**: Provides adversarial feedback for improvement
- **FormattingAgent**: Creates final polished posts with hashtags and formatting

## 🚀 Features

- **Real-time News Research**: Fetches latest industry news using GNews API
- **Multi-Agent Content Pipeline**: Hierarchical AI agents for comprehensive content creation
- **Interactive Topic Selection**: Choose from AI-identified compelling topics
- **Adversarial Quality Control**: Built-in critique system for content improvement
- **Professional Formatting**: LinkedIn-optimized posts with hashtags and proper structure
- **Workflow Transparency**: Real-time logging of agent activities
- **One-Click Publishing**: Copy-to-clipboard functionality

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **Language Model**: Google Gemini 2.0 Flash
- **News Source**: GNews API
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- GNews API key

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

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Configure API Keys**
   - Enter your Google Gemini API key in the sidebar
   - Enter your GNews API key in the sidebar

3. **Generate Content**
   - Enter your professional field and interests
   - Click "Research & Generate Ideas"
   - Select a topic from the generated options
   - Click "Generate LinkedIn Post"
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
│   ├── news_researcher.py     # News gathering agent
│   ├── topic_analyst.py       # Topic identification agent
│   ├── angle_generator.py     # Content angle creation agent
│   ├── drafting_agent.py      # Post drafting agent
│   ├── critique_agent.py      # Quality control agent
│   └── formatting_agent.py    # Final formatting agent
├── chains/                    # LangChain orchestration
│   ├── __init__.py
│   ├── analysis_chain.py      # News → Topics chain
│   └── creation_chain.py      # Angles → Final post chain
└── tools/                     # Custom LangChain tools
    ├── __init__.py
    └── gnews_tool.py          # GNews API integration
```

## 🔄 Workflow

1. **Research Phase**
   - NewsResearcherAgent searches for relevant industry news
   - TopicAnalystAgent identifies 2-3 compelling topics

2. **Creation Phase**
   - AngleGeneratorAgent creates 3 distinct content angles
   - DraftingAgent writes initial post based on selected topic/angle
   - CritiqueAgent provides improvement feedback
   - FormattingAgent creates final polished post

3. **Output**
   - Professional LinkedIn post with proper formatting
   - Relevant hashtags and strategic emoji usage
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
