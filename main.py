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
    messages = [
        {"role": "system", "content": "You are a chat bot designed only to answer questions about Programming. You know everything about coding and programming in any language. You are designed to help developers, testers, and coders."},
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
st.title("CodeMate: Your AI Programming Assistant")

# Display an image placeholder
st.image("Coding.jpg", width=700, caption="Hello Programmer")

# Adjust CSS for better layout
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    background-color: #1E1E1E;
}
.message-user, .message-ai {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.message-user img, .message-ai img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    margin-right: 10px;
}
</style>
""", unsafe_allow_html=True)

# User and AI profile images
user_profile_pic = "user.png"
ai_profile_pic = "ai.png"

# Input box for user query
query = st.text_input("Enter your query:")

# Button to get response
if st.button("Search"):
    if query:
        # Get response from the Groq model
        response = get_groq_response(query)

        # Append user and AI messages to session state
        st.session_state.conversation.append({"role": "user", "content": query})
        st.session_state.conversation.append({"role": "assistant", "content": response})

# Display chat history inside a scrollable container
st.markdown("### Chat History")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for message in st.session_state.conversation:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.image(user_profile_pic, width=38)
            st.markdown(f"**You:** {message['content']}")
    else:
        with st.chat_message("assistant"):
            st.image(ai_profile_pic, width=38)
            st.markdown(f"**CodeMate:** {message['content']}")

st.markdown("</div>", unsafe_allow_html=True)

# Sidebar Information
st.sidebar.header("About This App")
st.sidebar.markdown('<div class="sidebar-text">CodeMate is an AI-powered chatbot designed to help programmers with coding-related queries. Whether you\'re debugging an issue, learning a new programming language, or optimizing your code, CodeMate is here to assist.</div>', unsafe_allow_html=True)

# Add a footer
st.markdown("---")
st.markdown("Made with Streamlit")
