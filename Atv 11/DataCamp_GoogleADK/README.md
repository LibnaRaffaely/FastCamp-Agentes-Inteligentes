# Google ADK for Beginners - DataCamp Tutorial

🚀 **Welcome to the comprehensive journey through Google Agent Development Kit (ADK)!**

This repository contains a complete collection of AI agent implementations using Google's ADK framework, designed to teach you the fundamentals of building sophisticated AI agents with fine-grained control and Google Cloud integration.

## Project Structure

```
GoogleADK/
├── 📁 welcome_agent/          # Basic greeting agent with pirate theme
├── 📁 openai_agent/           # Using OpenAI models via LiteLLM
├── 📁 sequential_agent/       # Chain-based workflow agents
├── 📁 parallel_agent/         # Concurrent execution agents
├── 📁 session_agent/          # Session management and state persistence
├── 📁 structured_agent/       # Structured input/output schemas
├── 📁 tool_agent/             # Custom tools and function calling
├── 📁 persistent_agent/       # Database-backed persistent agents
├── 📁 gadk/                   # Virtual environment and dependencies
├── 📄 requirements.txt        # Python dependencies
├── 📄 Information.md          # Detailed setup instructions
├── 📄 habit_data.db           # SQLite database for persistent agents
└── 📷 *.jpg                   # Setup screenshots
```

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Cloud Account** (free tier available)
3. **OpenAI API Key** (optional, for openai_agent)

### Setup Instructions

#### 1. Google Cloud Setup

1. **Create a Google Cloud Project**:

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Access Google AI Studio**:

   - Navigate to [Google AI Studio](https://aistudio.google.com/)
   - Create an API Key (free tier - no credit card needed!)

3. **Environment Configuration**:
   - Copy your API key
   - Create a `.env` file in each agent directory with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

#### 2. Project Setup

```bash
# Clone the repository
git clone <repository-url>
cd GoogleADK

# Install dependwencies
pip install -r requirements.txt

# Activate virtual environment (if using gadk/)
# Windows:
gadk\Scripts\activate
# macOS/Linux:
source gadk/bin/activate
```

## 🔧 Development Best Practices

### Folder Structure

```
agent_name/
├── __init__.py      # Python package marker
├── agent.py         # Main agent logic
├── README.md        # Agent documentation
└── .env            # Environment variables
```

### Code Organization

- Always define `root_agent` in `agent.py`
- Use descriptive agent names and descriptions
- Implement proper error handling
- Document tool functions with clear descriptions

## 📖 Additional Resources

- [DataCamp Tutorial: Agent Development Kit (ADK)](https://www.datacamp.com/tutorial/agent-development-kit-adk)
- [DataCamp Blog: AI Agents](https://www.datacamp.com/blog/ai-agents)
- [DataCamp Course: Building AI Agents with Google ADK](http://datacamp.com/courses/building-ai-agents-with-google-adk)
- [Google ADK Documentation](https://google.github.io/adk-docs/)

## 🤝 Contributing

This is a learning project for the DataCamp Google ADK Tutorial. Feel free to experiment with the agents and extend their capabilities!

## 📄 License

This project is part of the DataCamp Google ADK for Beginners Tutorial.

---

**Happy Agent Building! 🚀**

_Built with ❤️ using Google ADK_
