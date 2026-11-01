# AI Research Assistant

An AI-powered research assistant built using Python, Google Gemini, and Tavily Search.

The application understands user questions, decides when internet research is required, searches the web using Tavily, and uses Gemini to analyse the results and generate a response.

The project is designed with a modular architecture so that we can add more tools, AI providers, and interfaces in the future.

---

## 1. Project Overview

The AI Research Assistant follows an agent-based workflow.

When a user asks a question:

1. The application receives the user's question.
2. Google Gemini understands the question.
3. Gemini decides whether an external search is required.
4. If search is required, Gemini requests the `search_web` tool.
5. Python executes the requested tool.
6. Tavily searches the internet and returns relevant results.
7. The search results are sent back to Gemini.
8. Gemini analyses the information and generates the final answer.
9. The application displays the answer in the console.

### Example

**User:**

Give me the latest top 3 AI news.

**Agent workflow:**

- Gemini understands the request.
- Gemini requests an internet search.
- Python executes the search tool.
- Tavily retrieves relevant information.
- Gemini analyses the results.
- The assistant presents the top 3 news stories.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google Gemini | AI model and decision-making |
| Tavily | Internet search |
| Google Gen AI SDK | Gemini API integration |
| Python Dotenv | Environment variable management |

---

## 3. Project Folder Structure

```text
AI-Research-Assistant/
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   └── gemini_client.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── research_service.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_tool.py
│   │   ├── tool_registry.py
│   │   ├── tool_definitions.py
│   │   └── tool_executor.py
│   │
│   └── interfaces/
│       ├── __init__.py
│       └── console.py
│
├── main.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Main Components

| Component | Responsibility |
|---|---|
| `core` | Application configuration |
| `clients` | Communication with AI providers |
| `services` | Main research workflow |
| `tools` | External tools available to the AI |
| `interfaces` | User interaction |
| `main.py` | Application entry point |

---

## 4. Prerequisites

Before running the project, install:

- Python 3.10 or newer
- Git
- Visual Studio Code (recommended)
- Google Gemini API key
- Tavily API key

### Get API Keys

**Google Gemini API:**

https://aistudio.google.com/app/apikey

**Tavily API:**

https://app.tavily.com/

Keep your API keys private. Never commit them to GitHub.

---

## 5. Initial Project Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd AI-Research-Assistant
```

If you are creating the project locally for the first time, open your existing project folder instead.

### Step 2: Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Note: If you get any errror Runnning script add this command and try again the activate command

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
```

Install all required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root.

Copy the structure from `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model_name
GEMINI_TIMEOUT=120000
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholder values with your actual API keys and the Gemini model name supported by your API account.

**Important:** Never upload `.env` to GitHub.

---

## 6. Run the Application

Make sure your virtual environment is activated.

From the project root, execute:

```bash
python main.py
```

The console interface should start.

Enter your question and interact with the AI Research Assistant.

To exit the application, use the exit command supported by the console interface or press `Ctrl + C`.

---

## 7. Architecture and Responsibilities

### Gemini Client

File: `app/clients/gemini_client.py`

Responsible for communicating with Google's Gemini API.

### LLM Client

File: `app/clients/llm_client.py`

Defines a common interface for AI model providers. This helps us add other providers, such as OpenAI, in the future.

### Research Service

File: `app/services/research_service.py`

Coordinates the research workflow, tool requests, tool execution, and final response generation.

### Search Tool

File: `app/tools/search_tool.py`

Contains the actual Tavily internet search implementation.

### Tool Definitions

File: `app/tools/tool_definitions.py`

Describes the available tools and their parameters to Gemini.

### Tool Registry

File: `app/tools/tool_registry.py`

Maintains the mapping between tool names and their corresponding Python functions.

### Tool Executor

File: `app/tools/tool_executor.py`

Finds and executes the Python function requested by Gemini.

### Console Interface

File: `app/interfaces/console.py`

Provides the terminal interface for user interaction.

---

## 8. How Tool Calling Works

The project uses function calling to allow Gemini to request external tools.

The workflow is:

```text
User Question
     |
     v
Google Gemini
     |
     v
Does it need a tool?
     |
     +---- No ----> Generate Final Answer
     |
     +---- Yes ---> Request search_web
                         |
                         v
                    Python Executor
                         |
                         v
                     Tavily Search
                         |
                         v
                   Search Results
                         |
                         v
                    Google Gemini
                         |
                         v
                   Final Answer
```

Gemini decides which tool to request, but Python executes the actual function.

This is the foundation of our agentic AI workflow.

---

## 9. Running Tests

Individual components can be tested separately.

Examples:

```bash
python test_tavily.py
python test_search_tool.py
python test_tool_registry.py
python test_gemini_function_calling.py
python test_tool_executor.py
```

Run these commands only if the corresponding test files exist in your project root.

---

## 10. Security Guidelines

- Never commit API keys or passwords.
- Keep `.env` excluded through `.gitignore`.
- Share `.env.example` instead of `.env`.
- Do not commit your virtual environment.
- Validate tool arguments before executing external operations.
- Handle API errors and rate limits gracefully.
- Avoid exposing sensitive information in application logs.

---

## 11. Future Enhancements

The project can be extended with:

- OpenAI API integration.
- Additional search and research tools.
- Website content extraction.
- Source verification and citation generation.
- Conversation history.
- SQLite database integration.
- FastAPI backend.
- React TypeScript frontend.
- Multi-agent research workflows.
- Research report generation in PDF format.

---

## 12. Project Goal

The goal of this project is to understand and build an AI agent from the ground up using Python.

Rather than relying entirely on an agent framework, we implement the fundamental building blocks ourselves:

- LLM integration
- Tool definitions
- Tool registration
- Tool execution
- Agent decision-making
- Iterative tool-calling workflow

This project will serve as a foundation for learning and developing more advanced agentic AI applications.
