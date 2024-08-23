# Streamlit V2 Assistant API

import streamlit as st
import base64
from streamlit_ace import st_ace

def main():
    st.set_page_config(page_title="AI Chatbot Project Explorer", page_icon="🤖", layout="wide")
    st.title("🤖 AI Chatbot Project Explorer")
    st.markdown("Welcome, future AI developers! Let's dive into the exciting world of chatbots!")

    topics = [
        "Introduction",
        "Setting Up the Project",
        "Creating the Assistant",
        "Building the Chat Interface",
        "How It All Works",
        "Fun with AI",
        "Quiz Time!"
    ]

    topic = st.sidebar.radio("Choose a topic:", topics)

    if topic == "Introduction":
        introduction()
    elif topic == "Setting Up the Project":
        setting_up()
    elif topic == "Creating the Assistant":
        creating_assistant()
    elif topic == "Building the Chat Interface":
        building_interface()
    elif topic == "How It All Works":
        how_it_works()
    elif topic == "Fun with AI":
        fun_with_ai()
    elif topic == "Quiz Time!":
        quiz_time()

def introduction():
    st.header("Welcome to the AI Chatbot Project! 🎉")
    st.write("In this project, we're going to create an AI chatbot that thinks it's Kaiba from Yu-Gi-Oh!")
    st.write("Here's what we'll be doing:")
    st.markdown("""
    1. Setting up our project with the necessary tools 🛠️
    2. Creating an AI assistant with a unique personality 🧠
    3. Building a chat interface where you can talk to the AI 💬
    4. Learning how it all works behind the scenes 🕵️‍♀️
    """)
    st.write("Are you ready to start your journey into the world of AI? Let's go!")

def setting_up():
    st.header("Setting Up the Project 🛠️")
    st.write("Before we can create our AI chatbot, we need to set up our project. Here's what we need:")
    st.markdown("""
    - Python: The programming language we'll use 🐍
    - Streamlit: A cool tool for creating web apps easily 🌟
    - OpenAI API: This gives us access to powerful AI models 🤖
    - Environment variables: A safe way to store secret information 🔒
    """)
    st.subheader("Let's look at some code!")
    code = """
import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    """
    st.code(code, language='python')
    st.write("This code sets up our project by importing the necessary libraries and setting up our OpenAI client.")

def creating_assistant():
    st.header("Creating the Assistant 🧠")
    st.write("Now comes the fun part - creating our AI assistant!")
    st.write("We're going to create an assistant that thinks it's Kaiba from Yu-Gi-Oh!")
    code = """
def create_assistant():
    try:
        assistant = client.beta.assistants.create(
            name="AI Chatbot",
            instructions="You are Kaiba from YU GI OH! Your job is to sound just like him",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo-preview"
        )
        return assistant
    except Exception as e:
        st.error(f"Error creating assistant: {str(e)}")
        return None
    """
    st.code(code, language='python')
    st.write("This function creates our assistant with a specific personality and abilities.")
    st.write("We also create a 'thread', which is like a conversation history for our chatbot.")

def building_interface():
    st.header("Building the Chat Interface 💬")
    st.write("Now that we have our assistant, let's create a way to talk to it!")
    st.write("We'll use Streamlit to create a cool chat interface.")
    code = """
st.title("🤖 AI Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
prompt = st.chat_input("Ask me anything!")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_assistant_response(ASSISTANT_ID, THREAD_ID, prompt)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    """
    st.code(code, language='python')
    st.write("This code creates a chat input box and displays messages from you and the AI.")

def how_it_works():
    st.header("How It All Works 🕵️‍♀️")
    st.write("Let's break down how our AI chatbot works:")
    st.markdown("""
    1. You type a message and hit enter.
    2. Your message is sent to the AI assistant we created.
    3. The AI thinks about your message and comes up with a response.
    4. The response is sent back to our chat interface.
    5. You see the AI's response in the chat!
    """)
    st.write("It's like having a conversation, but with an AI friend!")

def fun_with_ai():
    st.header("Fun with AI 🎮")
    st.write("Now that we understand how our AI chatbot works, let's have some fun with it!")
    st.write("Remember, our AI thinks it's Kaiba from Yu-Gi-Oh. Try asking it some questions and see how it responds!")
    st.write("Here are some ideas:")
    st.markdown("""
    - Ask about its favorite Duel Monsters card
    - Challenge it to a duel
    - Ask about its company, Kaiba Corp
    - Mention Yugi or Joey Wheeler and see how it reacts!
    """)
    st.write("Remember, the AI is just pretending to be Kaiba. It's all in good fun!")

def quiz_time():
    st.header("Quiz Time! 📝")
    st.write("Let's see how much you've learned about our AI chatbot project!")
    questions = [
        {
            "question": "What programming language are we using for this project?",
            "options": ["JavaScript", "Python", "Java", "C++"],
            "correct": "Python"
        },
        {
            "question": "What character is our AI assistant pretending to be?",
            "options": ["Yugi", "Joey Wheeler", "Kaiba", "Pegasus"],
            "correct": "Kaiba"
        },
        {
            "question": "What tool are we using to create our web interface?",
            "options": ["Django", "Flask", "Streamlit", "React"],
            "correct": "Streamlit"
        },
        {
            "question": "What does API stand for in OpenAI API?",
            "options": ["Application Programming Interface", "Artificial Python Intelligence", "Automated Program Interaction", "Advanced Python Integration"],
            "correct": "Application Programming Interface"
        }
    ]
    
    score = 0
    for i, q in enumerate(questions):
        st.subheader(f"Question {i+1}")
        st.write(q["question"])
        answer = st.radio(f"Select your answer for question {i+1}:", q["options"], key=f"q{i}")
        if answer == q["correct"]:
            score += 1
    
    if st.button("Check Answers"):
        st.write(f"You scored {score} out of {len(questions)}!")
        if score == len(questions):
            st.balloons()
            st.write("Perfect score! You're a AI chatbot expert! 🎉")
        elif score >= len(questions)/2:
            st.write("Great job! You're well on your way to becoming an AI expert!")
        else:
            st.write("Keep learning! You'll be an AI expert in no time!")

if __name__ == "__main__":
    main()
