import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Define the tools
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user."""
    return f"Hello {name}, I hope you are well today!"

# Page setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.caption("Powered by LangGraph, LangChain, and Groq")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    # Standard Groq free-tier models (available in free tier limits)
    model_name = st.selectbox(
        "Model",
        options=["qwen/qwen3.6-27b", "llama-3.3-70b-versatile", "llama3-8b-8192", "gemma2-9b-it"],
        index=0,
        help="Select a free-tier Groq model"
    )
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Run agent
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        st.error("Please set GROQ_API_KEY in your .env file.")
    else:
        try:
            # Initialize model & agent
            model = ChatGroq(model=model_name, temperature=0)
            tools = [calculator, say_hello]
            agent_executor = create_react_agent(model, tools)

            # Build history
            lc_messages = []
            for m in st.session_state.messages[:-1]:
                if m["role"] == "user":
                    lc_messages.append(HumanMessage(content=m["content"]))
                elif m["role"] == "assistant":
                    lc_messages.append(AIMessage(content=m["content"]))
            lc_messages.append(HumanMessage(content=prompt))

            # Stream response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Show spinner while thinking
                with st.spinner("Thinking..."):
                    for chunk in agent_executor.stream({"messages": lc_messages}):
                        if "agent" in chunk and "messages" in chunk["agent"]:
                            for message in chunk["agent"]["messages"]:
                                if message.content:
                                    full_response += message.content
                                    message_placeholder.markdown(full_response + "▌")
                        elif "tools" in chunk and "messages" in chunk["tools"]:
                            for message in chunk["tools"]["messages"]:
                                st.info(f"🔧 Tool Output ({message.name}): {message.content}")

                # Final response without cursor
                message_placeholder.markdown(full_response if full_response else "*Thinking complete.*")
                
                # Append assistant message
                st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")