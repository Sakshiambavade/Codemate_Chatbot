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

# Function to get response
def get_groq_response(question):
    messages = [
        {"role": "system", "content": "You are an AI assistant designed to answer programming-related questions. You provide guidance on coding, debugging, and best practices for developers, testers, and coders."},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096
    )

    return response.choices[0].message.content

# Initialize chat history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Page Title
st.title("💻 CodeMate: Your AI Programming Assistant")

# Display Banner Image (Ensure Coding.jpg exists in the directory)
st.image("Coding.jpg", width=700, caption="Hello, Programmer! 🚀")

# Chat History at the Top
st.markdown("### Chat History")
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 15px;">
                <div style="background-color: #0078ff; color: white; padding: 10px; border-radius: 15px; max-width: 75%; text-align: left;">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 15px;">
                <div style="background-color: #444; color: white; padding: 10px; border-radius: 15px; max-width: 75%; text-align: left;">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Input Box at the Bottom
st.markdown("### Ask CodeMate")
query = st.text_input("Enter your query:")

if st.button("Ask"):
    if query:
        response = get_groq_response(query)
        st.session_state.conversation.append({"role": "user", "content": query})
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.rerun()

# Sidebar Information
st.sidebar.header("📌 About This App")
st.sidebar.markdown("**CodeMate** is an AI-powered chatbot designed to help programmers with coding-related queries. Whether you are debugging an issue, learning a new programming language, or optimizing your code, CodeMate is here to assist.")

# Footer
st.markdown("---")
st.markdown("🚀 Made By Sakshi Ambavade")
