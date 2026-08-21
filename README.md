# 🤖 GenAI Agentic Chatbot (LangGraph + Groq)

A modular, intelligent conversational AI assistant built using **LangGraph**, **LangChain**, and **Groq Cloud API**. This project implements a **ReAct (Reasoning and Acting)** agent architecture capable of autonomous reasoning, dynamic tool selection, real-time response streaming, and an interactive **Streamlit web UI** with a sleek dark theme.

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Workflow & Execution Flow](#-workflow--execution-flow)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started & Installation](#-getting-started--installation)
  - [Prerequisites](#prerequisites)
  - [1. Clone / Navigate to Project](#1-clone--navigate-to-project)
  - [2. Create and Activate Virtual Environment](#2-create-and-activate-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Run the Application](#5-run-the-application)
- [Available Tools & Capabilities](#-available-tools--capabilities)
- [Streamlit UI & Theme](#-streamlit-ui--theme)
- [Extending the Agent (Adding New Tools)](#-extending-the-agent-adding-new-tools)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)
- [License](#-license)

---

## 🌟 Overview

The **GenAI Agentic Chatbot** demonstrates the implementation of an agentic workflow powered by fast inference using Groq LLMs (e.g., `qwen/qwen3.6-27b` or `llama-3.3-70b-versatile`) coupled with LangGraph's prebuilt ReAct agent framework, all wrapped in a polished **Streamlit web application**.

Instead of operating solely as a static text predictor, the agent can:
1. **Analyze** incoming user queries via the Streamlit chat interface.
2. **Reason** whether an external function/tool is required.
3. **Execute** appropriate tools (e.g., arithmetic calculations, greeting helpers).
4. **Synthesize** tool results into a coherent final response streamed live in the browser.

---

## ✨ Key Features

- **⚡ Blazing-Fast Inference**: Integrates with [Groq API](https://console.groq.com/) for near-instantaneous token generation and low-latency LLM responses.
- **🧠 ReAct Framework**: Built with `langgraph.prebuilt.create_react_agent`, establishing a robust reasoning and acting cycle.
- **🌐 Streamlit Web UI**: Full browser-based chat interface with real-time streaming, a sidebar for model selection, and a clear chat button.
- **🎨 Custom Dark Theme**: Configured via `.streamlit/config.toml` with a deep dark background (`#09090B`) and vibrant cyan accents (`#00F2FE`).
- **🔧 Tool Execution Transparency**: In-UI display of tool outputs using `st.info()` banners so users can see exactly what tools were called.
- **🛠️ Extensible Tool Registry**: Easy-to-extend Python `@tool` definitions allowing the LLM to call custom APIs, databases, or local functions.
- **🌊 Streaming Responses**: Real-time token streaming into the Streamlit chat message placeholder.
- **💬 Multi-turn Conversation**: Full chat history tracked via `st.session_state` and passed as LangChain message objects to the agent on each turn.
- **🔒 Secure Configuration**: Uses `.env` files and `python-dotenv` for API key management, with `.env.example` as a safe template.

---

## 🏗️ System Architecture

The application adopts a modular ReAct architecture where LangGraph manages state transitions between the Streamlit UI, the LLM reasoning engine, and tool execution nodes.

```mermaid
graph TD
    User([👤 User / Browser]) -->|Sends Query| StreamlitUI[🌐 Streamlit Web UI\nmain.py]
    StreamlitUI -->|Passes LangChain Messages| AgentExecutor[🤖 LangGraph ReAct Agent]

    subgraph LangGraph Agent Core
        AgentExecutor --> LLM[🧠 ChatGroq LLM Engine\ne.g. qwen/qwen3.6-27b]
        Decision{Requires Tool Call?}

        Decision -- Yes --> ToolRouter[🔀 Tool Execution Node]
        Decision -- No --> DirectResponse[📝 Direct Answer]

        subgraph Tool Registry
            ToolRouter --> CalcTool[🧮 calculator tool]
            ToolRouter --> HelloTool[👋 say_hello tool]
            ToolRouter --> FutureTools[➕ Custom Tools]
        end

        CalcTool --> ToolFeedback[📬 Tool Output Observation]
        HelloTool --> ToolFeedback
        FutureTools --> ToolFeedback
        ToolFeedback --> LLM
    end

    DirectResponse --> Streamer[🌊 Streamlit Response Streamer]
    Streamer -->|Real-time Output + Tool Banners| User
```

---

## 🔄 Workflow & Execution Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Streamlit UI (Browser)
    participant App as main.py (Streamlit App)
    participant Agent as LangGraph ReAct Agent
    participant Groq as ChatGroq (LLM)
    participant Tools as Tool Functions

    User->>UI: Opens http://localhost:8501
    App->>App: Loads .env variables (GROQ_API_KEY)
    App->>App: Renders chat history from st.session_state
    User->>UI: Selects model from sidebar dropdown
    User->>UI: Types message (e.g., "Add 45 and 92")

    App->>App: Appends user message to session_state
    App->>Agent: Builds LangChain message history & calls agent_executor.stream()
    Agent->>Groq: Evaluates intent & tool schemas

    alt Tool Call Needed
        Groq-->>Agent: Returns Tool Call Request (calculator(45, 92))
        Agent->>Tools: Executes calculator(a=45, b=92)
        Tools-->>Agent: Returns "The sum of 45 and 92 is 137"
        App->>UI: Displays 🔧 Tool Output banner via st.info()
        Agent->>Groq: Sends Tool Observation back
        Groq-->>Agent: Generates final synthesized response
    else General Conversation
        Groq-->>Agent: Generates conversational response directly
    end

    Agent-->>App: Streams output chunks
    App->>UI: Updates message_placeholder in real-time (cursor)
    App->>App: Appends assistant response to session_state
    UI-->>User: Displays final response

    User->>UI: Clicks "Clear Chat" to reset session
```

---

## 💻 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **[Python 3.10+](https://www.python.org/)** | Core programming language |
| **[LangGraph](https://github.com/langchain-ai/langgraph)** | Agent graph construction and ReAct orchestration |
| **[LangChain Core](https://github.com/langchain-ai/langchain)** | Standardized message interfaces (`HumanMessage`, `AIMessage`) and `@tool` decorators |
| **[LangChain Groq](https://github.com/langchain-ai/langchain-groq)** | High-speed LLM integration via Groq Cloud API |
| **[Streamlit](https://streamlit.io/)** | Browser-based interactive web UI with streaming chat support |
| **[Python Dotenv](https://github.com/theskumar/python-dotenv)** | Environment variable management from `.env` |

---

## 📁 Project Structure

```text
GenAI_KLEBCA/
│
├── .env                      # Environment configuration (API keys) [Ignored in VCS]
├── .env.example              # Safe template for environment variables
├── .gitignore                # Files and directories excluded from version control
├── .streamlit/
│   └── config.toml           # Streamlit theme & server configuration (dark mode)
├── .venv/                    # Python virtual environment directory
├── env_samples/              # Additional environment configuration samples
├── main.py                   # Streamlit web application & LangGraph ReAct agent
├── requirements.txt          # Project dependencies list
└── README.md                 # Project documentation and setup guide
```

---

## 🚀 Getting Started & Installation

Follow these steps to set up and run the chatbot locally on your machine.

### Prerequisites
- **Python 3.10** or higher installed on your system.
- A **Groq Cloud API Key** (Free tier available at [console.groq.com](https://console.groq.com/keys)).

---

### 1. Clone / Navigate to Project

Open your terminal and navigate to the project directory:
```bash
cd c:\Users\HP\Desktop\GenAI_KLEBCA
```

---

### 2. Create and Activate Virtual Environment

It is recommended to use an isolated Python virtual environment:

#### On Windows (PowerShell):
```powershell
# Create virtual environment (if not already created)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):
```cmd
.venv\Scripts\activate.bat
```

#### On Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Copy the provided example file and fill in your credentials:

```bash
# Copy the template
cp .env.example .env
```

Then edit `.env`:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Model Selection (e.g. qwen/qwen3.6-27b, llama-3.3-70b-versatile)
GROQ_MODEL=qwen/qwen3.6-27b
```

> ⚠️ **Security Tip:** Never commit your actual `.env` file containing secrets to version control. It is already listed in `.gitignore` to prevent accidental exposure.

---

### 5. Run the Application

Start the Streamlit web application:

```bash
streamlit run main.py
```

This will automatically open the application in your default web browser at **`http://localhost:8501`**.

**Using the app:**
- 🎛️ **Sidebar** — Select from available free-tier Groq models (`qwen/qwen3.6-27b`, `llama-3.3-70b-versatile`, `llama3-8b-8192`, `gemma2-9b-it`).
- 💬 **Chat Input** — Type your message at the bottom and press Enter.
- 🔧 **Tool Banners** — When the agent invokes a tool, a blue info banner appears showing the tool name and its output.
- 🗑️ **Clear Chat** — Click the "Clear Chat" button in the sidebar to reset the conversation.

---

## 🛠️ Available Tools & Capabilities

The agent currently ships with built-in tools defined via `@tool`:

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `calculator` | `a: float`, `b: float` | Computes the arithmetic sum of two numbers. |
| `say_hello` | `name: str` | Generates a friendly greeting tailored to the provided name. |

---

## 🎨 Streamlit UI & Theme

The application uses a custom **dark theme** configured in `.streamlit/config.toml`:

| Setting | Value | Description |
| :--- | :--- | :--- |
| `primaryColor` | `#00F2FE` | Cyan accent color for interactive elements |
| `backgroundColor` | `#09090B` | Deep dark main background |
| `secondaryBackgroundColor` | `#18181B` | Slightly lighter sidebar/input background |
| `textColor` | `#F4F4F5` | Off-white text for readability |

The server is also configured for headless operation (`headless = true`) with CORS and XSRF protection disabled for local development convenience.

---

## 🧩 Extending the Agent (Adding New Tools)

You can easily register custom tools for the agent to use. Simply define your function with the `@tool` decorator in `main.py`:

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Fetch current weather report for a given city."""
    # Custom API call or logic here
    return f"The weather in {city} is sunny and 25°C."

# Add the new tool to the tools list inside the chat handler:
tools = [calculator, say_hello, get_weather]
```

LangGraph automatically extracts the docstring and type hints to create the tool schema for the LLM.

---

## ❓ Troubleshooting & FAQs

### 1. `GROQ_API_KEY is not set in environment`
- Ensure that the `.env` file exists in the project root directory and contains `GROQ_API_KEY=gsk_...`.
- Make sure `load_dotenv()` is called at the top of `main.py` before `os.getenv()`.
- You can reference `.env.example` for the expected format.

### 2. `ModuleNotFoundError`
- Ensure your virtual environment is active — `(.venv)` should appear in your terminal prompt.
- Re-run `pip install -r requirements.txt`.

### 3. Streamlit page not opening
- Manually open **`http://localhost:8501`** in your browser.
- Ensure no other service is running on port 8501. You can specify a different port with:
  ```bash
  streamlit run main.py --server.port 8502
  ```

### 4. `fatal: 'origin' does not appear to be a git repository`
- Your local repo has no remote configured yet. Add one with:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

---

## 📄 License

This project is created for educational and experimental purposes under **GenAI / KLE BCA** coursework. Feel free to adapt and expand it for your agentic AI workflows.

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Workflow & Execution Flow](#-workflow--execution-flow)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started & Installation](#-getting-started--installation)
  - [Prerequisites](#prerequisites)
  - [1. Clone / Navigate to Project](#1-clone--navigate-to-project)
  - [2. Create and Activate Virtual Environment](#2-create-and-activate-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Run the Application](#5-run-the-application)
- [Available Tools & Capabilities](#-available-tools--capabilities)
- [Extending the Agent (Adding New Tools)](#-extending-the-agent-adding-new-tools)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)
- [License](#-license)

---

## 🌟 Overview

The **GenAI Agentic Chatbot** demonstrates the implementation of an agentic workflow powered by fast inference using Groq LLMs (e.g., `qwen/qwen3.6-27b` or `llama-3.3-70b-versatile`) coupled with LangGraph's prebuilt ReAct agent framework.

Instead of operating solely as a static text predictor, the agent can:
1. **Analyze** incoming user queries.
2. **Reason** whether an external function/tool is required.
3. **Execute** appropriate tools (e.g., arithmetic calculations, greeting helpers).
4. **Synthesize** tool results into a coherent final response streamed live to the console.

---

## ✨ Key Features

- **⚡ Blazing-Fast Inference**: Integrates with [Groq API](https://console.groq.com/) for near-instantaneous token generation and low-latency LLM responses.
- **🧠 ReAct Framework**: Built with `langgraph.prebuilt.create_react_agent`, establishing a robust reasoning and acting cycle.
- **🛠️ Extensible Tool Registry**: Easy-to-extend Python `@tool` definitions allowing the LLM to call custom APIs, databases, or local functions.
- **🌊 Streaming Responses**: Real-time token streaming to the terminal for an interactive user experience.
- **🔒 Secure Configuration**: Uses `.env` files and `python-dotenv` for API key and model selection management.

---

## 🏗️ System Architecture

The application adopts a modular ReAct architecture where LangGraph manages state transitions between the user, the LLM reasoning engine, and tool execution nodes.

```mermaid
graph TD
    User([👤 User / Streamlit Web UI]) -->|Sends Query| MainLoop[🔄 Streamlit App in main.py]
    MainLoop -->|Passes Message| AgentExecutor[🤖 LangGraph ReAct Agent]
    
    subgraph LangGraph Agent Core
        AgentExecutor --> LLM[🧠 ChatGroq LLM Engine\n'llama-3.3-70b-versatile']
        Decision{Requires Tool Call?}
        
        Decision -- Yes --> ToolRouter[🔀 Tool Execution Node]
        Decision -- No --> DirectResponse[📝 Direct Answer]
        
        subgraph Tool Registry
            ToolRouter --> CalcTool[🧮 calculator tool]
            ToolRouter --> HelloTool[👋 say_hello tool]
            ToolRouter --> FutureTools[➕ Custom Tools]
        end
        
        CalcTool --> ToolFeedback[📬 Tool Output Observation]
        HelloTool --> ToolFeedback
        FutureTools --> ToolFeedback
        ToolFeedback --> LLM
    end
    
    DirectResponse --> Streamer[🌊 Response Streamer]
    Streamer -->|Real-time Output| User
```

---

## 🔄 Workflow & Execution Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App as main.py (App Loop)
    participant Agent as LangGraph ReAct Agent
    participant Groq as ChatGroq (LLM)
    participant Tools as Tool Functions

    User->>App: Launches `streamlit run main.py`
    App->>App: Loads .env variables (GROQ_API_KEY, GROQ_MODEL)
    App->>Agent: Initializes ChatGroq & binds registered tools
    
    loop Interactive Chat Session
        User->>App: Inputs message (e.g., "Add 45 and 92")
        App->>Agent: Passes `HumanMessage(content=user_input)`
        Agent->>Groq: Evaluates intent & tool schemas
        
        alt Tool Call Needed
            Groq-->>Agent: Returns Tool Call Request (`calculator(45, 92)`)
            Agent->>Tools: Executes `calculator(a=45, b=92)`
            Tools-->>Agent: Returns `"The sum of 45 and 92 is 137"`
            Agent->>Groq: Sends Tool Observation back
            Groq-->>Agent: Generates final synthesized response
        else General Conversation
            Groq-->>Agent: Generates conversational response directly
        end
        
        Agent-->>App: Streams output chunks
        App-->>User: Displays real-time response in console
    end

    User->>App: Inputs "quit"
    App->>User: Exits session
```

---

## 💻 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **[Python 3.10+](https://www.python.org/)** | Core programming language |
| **[LangGraph](https://github.com/langchain-ai/langgraph)** | Agent graph construction and ReAct orchestration |
| **[LangChain Core](https://github.com/langchain-ai/langchain)** | Standardized message interfaces and `@tool` decorators |
| **[LangChain Groq](https://github.com/langchain-ai/langchain-groq)** | High-speed LLM integration via Groq Cloud API |
| **[Python Dotenv](https://github.com/theskumar/python-dotenv)** | Environment variable management from `.env` |

---

## 📁 Project Structure

```text
GenAI_KLEBCA/
│
├── .env                  # Environment configuration (API keys, model name) [Ignored in VCS]
├── .env.example          # Sample environment configuration template
├── .venv/                # Python virtual environment directory
├── main.py               # Streamlit web application & LangGraph ReAct agent
├── requirements.txt      # Project dependencies list
└── README.md             # Project documentation and setup guide
```

---

## 🚀 Getting Started & Installation

Follow these steps to set up and run the chatbot locally on your machine.

### Prerequisites
- **Python 3.10** or higher installed on your system.
- A **Groq Cloud API Key** (Free tier available at [console.groq.com](https://console.groq.com/keys)).

---

### 1. Clone / Navigate to Project

Open your terminal and navigate to the project directory:
```bash
cd c:\Users\HP\Desktop\GenAI_KLEBCA
```

---

### 2. Create and Activate Virtual Environment

It is recommended to use an isolated Python virtual environment:

#### On Windows (PowerShell):
```powershell
# Create virtual environment (if not already created)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):
```cmd
.venv\Scripts\activate.bat
```

#### On Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory (or edit the existing one):

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Model Selection (e.g. qwen/qwen3.6-27b, llama-3.3-70b-versatile)
GROQ_MODEL=qwen/qwen3.6-27b
```

> ⚠️ **Security Tip:** Never commit your actual `.env` file containing secrets to version control (e.g., GitHub). Keep `.env` in your `.gitignore`.

---

### 5. Run the Application

Start the Streamlit web application:

```bash
streamlit run main.py
```

This will automatically open the application in your default web browser (usually at `http://localhost:8501`).

You can choose different free-tier models (like `llama-3.3-70b-versatile`) from the sidebar, type messages in the chat input at the bottom, and observe the agent's real-time thoughts and tool execution logs as it answers your queries!

---

## 🛠️ Available Tools & Capabilities

The agent currently ships with built-in tools defined via `@tool`:

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `calculator` | `a: float`, `b: float` | Computes the arithmetic sum of two numbers. |
| `say_hello` | `name: str` | Generates a friendly greeting tailored to the provided name. |

---

## 🧩 Extending the Agent (Adding New Tools)

You can easily register custom tools for the agent to use. Simply define your function with the `@tool` decorator in `main.py`:

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Fetch current weather report for a given city."""
    # Custom API call or logic here
    return f"The weather in {city} is sunny and 25°C."

# Add the new tool to the tools list in main():
tools = [calculator, say_hello, get_weather]
```

LangGraph automatically extracts the docstring and type hints to create the tool schema for the LLM.

---

## ❓ Troubleshooting & FAQs

### 1. `GROQ_API_KEY is not set in environment`
- Ensure that the `.env` file exists in the project root directory and contains `GROQ_API_KEY=gsk_...`.
- Make sure `load_dotenv()` is called prior to `os.getenv()`.

### 2. ModuleNotFoundError
- Ensure your virtual environment is active (`(.venv)` should appear in your terminal prompt).
- Re-run `pip install -r requirements.txt`.

### 3. Exiting the Chatbot
- Type `quit` in lowercase to cleanly terminate the session.

---

## 📄 License

This project is created for educational and experimental purposes under GenAI / KLE BCA coursework. Feel free to adapt and expand it for your agentic AI workflows.

