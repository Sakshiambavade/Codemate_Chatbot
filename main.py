import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch the GROQ_API_KEY from the environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-70b-8192'

def get_groq_response(question):
    """Fetch response from the Groq API."""
    messages = [
        {"role": "system", "content": "You are CodeMate, an AI assistant for programmers, designed to help with coding, debugging, and software development."},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096
    )

    return response.choices[0].message.content

# Initialize chat history if not already set
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Streamlit app title
st.title("💻 CodeMate: Your AI Programming Assistant")

# Display an image placeholder
st.image("Coding.jpg", width=700, caption="Hello, Programmer! 🚀")

# Apply custom CSS for chat UI
st.markdown("""
<style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 10px;
        background-color: #1E1E1E;
    }
    .message {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .message img {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .user-message {
        color: #00E676;
    }
    .ai-message {
        color: #00B0FF;
    }
</style>
""", unsafe_allow_html=True)

# Display chat history inside a scrollable container **at the top**
st.markdown("### 📜 Chat History")
chat_container = st.container()

with chat_container:
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f"<div class='message user-message'><strong>👤 You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message ai-message'><strong>🤖 CodeMate:</strong> {message['content']}</div>", unsafe_allow_html=True)

# Input box for user query **at the bottom**
query = st.text_input("💬 Enter your question:", key="query_input")

# Button to get response
if st.button("Send", key="send_button"):
    if query:
        # Get response from the Groq model
        response = get_groq_response(query)

        # Append user and AI messages to session state
        st.session_state.conversation.append({"role": "user", "content": query})
        st.session_state.conversation.append({"role": "assistant", "content": response})

        # Rerun app to update chat history
        st.experimental_rerun()

# Sidebar Information
st.sidebar.header("ℹ️ About CodeMate")
st.sidebar.markdown("CodeMate is an AI-powered chatbot designed to help programmers with coding-related queries. Whether you're debugging an issue, learning a new programming language, or optimizing your code, CodeMate is here to assist.")

# Footer
st.markdown("---")
st.markdown("Made By Sakshi Ambavade")
