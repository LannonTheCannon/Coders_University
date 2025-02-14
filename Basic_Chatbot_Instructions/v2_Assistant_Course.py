# Streamlit V2 Assistant API

import streamlit as st
import base64
from streamlit_ace import st_ace
import random

def main():
    st.set_page_config(page_title="AI Chatbot Project Explorer", page_icon="🤖", layout="wide")

    topics = [
        "Introduction",
        "Project Setup",
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
    elif topic == 'Project Setup':
        project_setup() 
    elif topic == "Setting Up the Project":
        setting_up()
    elif topic == "Creating the Assistant":
        creating_assistant()
    elif topic == "Building the Chat Interface":
        building_interface()
    # elif topic == "How It All Works":
    #     how_it_works()
    # elif topic == "Fun with AI":
    #     fun_with_ai()
    elif topic == "Quiz Time!":
        quiz_time()

def introduction():
    st.title("🤖 AI Chatbot Project Explorer")
    st.markdown("Welcome, future AI developers! Let's dive into the exciting world of chatbots!")

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

def project_setup():
    st.header("Setting Up Your Project Environment 🛠️")
    st.write("Before we start coding our chatbot, we need to set up our project environment. Let's go through this process step by step!")

    with st.expander("1. Creating a Virtual Environment 🏝️"):
        st.markdown("""
        A virtual environment is like a separate playground for your project. It keeps all your project's toys (libraries) in one place, so they don't get mixed up with other projects.

        Here's how to create one:

        1. Open your terminal or command prompt.
        2. Navigate to your project folder. For example:
        """)
        st.code("cd C:\\Users\\YourName\\Documents\\ChatbotProject", language="bash")
        st.markdown("3. Run this command to create a virtual environment:")
        st.code("python -m venv myenv", language="bash")
        st.markdown("""
        4. Activate your virtual environment:
           - On Windows: `myenv\\Scripts\\activate`
           - On macOS and Linux: `source myenv/bin/activate`
        
        Now you're in your virtual playground! 🎉
        """)

    with st.expander("2. Creating the .env File 🔑"):
        st.markdown("""
        The .env file is like a secret diary where we keep important information, like our OpenAI API key. Let's create it using the command prompt:

        1. Make sure you're in your project directory.
        2. On Windows, use this command to create the .env file:
        """)
        st.code("echo OPENAI_API_KEY=your-api-key-goes-here > .env", language="bash")
        st.markdown("""
        3. On macOS or Linux, use this command:
        """)
        st.code("echo 'OPENAI_API_KEY=your-api-key-goes-here' > .env", language="bash")
        st.markdown("""
        4. Now, open the .env file in a text editor and replace 'your-api-key-goes-here' with your actual OpenAI API key.

        Remember, keep this file secret! Don't share it with anyone or upload it to GitHub.
        """)

    with st.expander("3. Creating the requirements.txt File 📋"):
        st.markdown("""
        The requirements.txt file is like a shopping list of all the libraries your project needs.

        1. In your command prompt, make sure you're in your project directory.
        2. Create the requirements.txt file with this command:
        """)
        st.code("""echo streamlit==1.24.0 > requirements.txt
echo openai==0.27.8 >> requirements.txt
echo python-dotenv==1.0.0 >> requirements.txt""", language="bash")
        st.markdown("""
        3. To install these libraries, run this command in your terminal:
        """)
        st.code("pip install -r requirements.txt", language="bash")

    with st.expander("4. Creating the .streamlit Folder and secrets.toml File 🗄️"):
        st.markdown("""
        The .streamlit folder is where we keep special Streamlit settings. The secrets.toml file is another place to store secret information.

        1. In your command prompt, create the .streamlit folder:
        """)
        st.code("mkdir .streamlit", language="bash")
        st.markdown("2. Create the secrets.toml file:")
        st.code("""echo OPENAI_API_KEY = "your-api-key-goes-here" > .streamlit\\secrets.toml""", language="bash")
        st.markdown("3. Open the secrets.toml file in a text editor and replace 'your-api-key-goes-here' with your actual OpenAI API key.")

    with st.expander("5. Updating the .gitignore File 🙈"):
        st.markdown("""
        The .gitignore file tells Git which files to ignore when you're sharing your code.

        1. In your command prompt, create the .gitignore file:
        """)
        st.code("""echo # Virtual environment > .gitignore
echo myenv/ >> .gitignore
echo # Environment variables >> .gitignore
echo .env >> .gitignore
echo # Streamlit secrets >> .gitignore
echo .streamlit/secrets.toml >> .gitignore
echo # Python cache files >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo # OS generated files >> .gitignore
echo .DS_Store >> .gitignore
echo Thumbs.db >> .gitignore""", language="bash")
        st.markdown("This helps keep your secret information and unnecessary files private when you share your code.")

    st.write("Great job! You've now set up your project environment using the command prompt. You're ready to start building your chatbot! 🚀")

    # Add an interactive element
    if st.button("🎉 Project Setup Complete!"):
        st.write("Congratulations! You've successfully set up your project environment using the command prompt. You're now ready to start coding your AI chatbot!")
        st.balloons()

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
    st.write("Now comes the fun part - creating our AI assistant! Let's break this down step by step.")

    with st.expander("1. Setting up our environment 🌍"):
        st.write("First, we need to set up our project environment. Here's what our setup code looks like:")
        
        code1 = """
import streamlit as st
import openai
from dotenv import load_dotenv
import os
load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        """
        st.code(code1, language='python')
        
        st.markdown("""
        - We import the libraries we need.
        - `load_dotenv()` reads our secret API key from a special file.
        - We create an OpenAI client to talk to the AI models.
        """)

    with st.expander("2. Creating the Assistant 🤖"):
        st.write("Now, let's create our AI assistant:")
        
        code2 = """
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
        st.code(code2, language='python')
        
        st.markdown("""
        - We ask OpenAI to create a new AI assistant.
        - We give it a name, instructions to act like Kaiba, and some tools.
        - If anything goes wrong, we show an error message.
        """)

    with st.expander("3. Creating a Thread 🧵"):
        st.write("Next, we create a 'thread'. Think of this like starting a new conversation:")
        
        code3 = """
def create_thread():
    try:
        thread = client.beta.threads.create()
        return thread
    except Exception as e:
        st.error(f"Error creating thread: {str(e)}")
        return None
        """
        st.code(code3, language='python')
        
        st.markdown("""
        - A thread is like a container for our conversation with the AI.
        - Every message we send and receive will be part of this thread.
        - This helps the AI remember what we've been talking about.
        """)

    with st.expander("4. Putting it all together 🏗️"):
        st.write("Finally, we have a special part of our code that runs when we start our program:")
        
        code4 = """
if __name__ == '__main__': 
    assistant = create_assistant()
    thread = create_thread()
    if assistant:
        print(f'Assistant ID {assistant.id}')
    else:
        print('Failed to create an assistant')
    if thread:
        print(f'Thread created with id {thread.id}')
    else:
        print('Failed to create a thread')
        """
        st.code(code4, language='python')
        
        st.markdown("""
        - `if __name__ == '__main__':` is a special Python phrase. It means "Only do this if you're running this file directly".
        - We create our assistant and our thread.
        - If everything works, we print out some information about them.
        - If something goes wrong, we print an error message.
        """)

    st.write("And that's it! We've now set up our environment, created an AI assistant that thinks it's Kaiba, and started a new conversation thread. We're ready to start chatting with our AI!")

    # Add an interactive element
    if st.button("🎉 Create Your Own Kaiba Assistant!"):
        st.write("Congratulations! You've just created your very own Kaiba-themed AI assistant!")
        st.balloons()


def building_interface():
    st.header("Building the Chat Interface 💬")
    st.write("Let's explore how we build our cool AI chatbot interface! We'll break it down step by step.")

    with st.expander("1. Setting up our project 🚀"):
        st.code("""
import streamlit as st
import openai
import time
import os 

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
ASSISTANT_ID='asst_etfqF0fCZ4pxXIwuiwy6kqfL'
THREAD_ID='thread_eODfW5yPUYFxjbd7WBEL09L6'
        """, language='python')
        st.markdown("""
        - We import the libraries we need: `streamlit` for our web app, `openai` to talk to the AI, `time` for waiting, and `os` for system stuff.
        - We set up our Streamlit page with a title and icon.
        - We define our `ASSISTANT_ID` and `THREAD_ID`. These are like special codes to identify our AI assistant and conversation.
        """)

    with st.expander("2. Setting up our OpenAI client 🔑"):
        st.code("""
api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error('OpenAI API Key was not found. Please set it in Streamlit secrets or as an ')
    st.stop()
client = openai.OpenAI(api_key=api_key)
        """, language='python')
        st.markdown("""
        - We try to get our OpenAI API key from Streamlit secrets or environment variables.
        - If we can't find the key, we show an error message and stop the app.
        - We create an OpenAI client using our API key. This client helps us talk to the AI.
        """)

    with st.expander("3. Creating our chat interface 💬"):
        st.code("""
st.title("🤖 AI Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []
        """, language='python')
        st.markdown("""
        - We give our chat a title: "🤖 AI Chatbot".
        - We create a place to store our messages using `st.session_state`.
        - This helps us remember the conversation even if we refresh the page.
        """)

    with st.expander("4. Getting responses from our AI assistant 🤖"):
        st.code("""
def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )
        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)
        # Retrieve the assistant's messages
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        
        # Return the latest assistant message
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."
        """, language='python')
        st.markdown("""
        - This function talks to our AI assistant and gets its response.
        - It adds our message to the conversation thread.
        - It tells the AI to think about our message (that's the "run" part).
        - It waits for the AI to finish thinking.
        - Then it gets the AI's response and returns it.
        - If anything goes wrong, it shows an error message.
        """)

    with st.expander("5. Displaying the chat 📜"):
        st.code("""
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        """, language='python')
        st.markdown("""
        - This part shows all the messages in our chat.
        - It goes through each message we've saved.
        - It displays each message in a chat bubble, showing if it's from the user or the AI.
        """)

    with st.expander("6. Handling user input and AI responses 🗨️"):
        st.code("""
prompt = st.chat_input("Ask me anything!")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_assistant_response(
            ASSISTANT_ID,
            THREAD_ID,  
            prompt
        )
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
        """, language='python')
        st.markdown("""
        - We create a text box where you can type your message.
        - When you send a message:
          1. We save your message and show it in the chat.
          2. We ask our AI assistant for a response.
          3. We show the AI's response in the chat.
          4. We save the AI's response too.
        """)

    with st.expander("7. Debugging information ℹ️"):
        st.code("""
st.sidebar.write(f"Assistant ID: {ASSISTANT_ID}")
st.sidebar.write(f"Thread ID: {THREAD_ID}")
        """, language='python')
        st.markdown("""
        - This shows our Assistant ID and Thread ID in the sidebar.
        - It's helpful for checking if we're connected to the right AI assistant and conversation thread.
        """)

    st.write("And that's our whole chatbot interface! It lets us talk to our AI assistant in a fun and interactive way. 😎")

    # Add an interactive element
    if st.button("🚀 Launch the Chatbot"):
        st.write("Awesome job! You've just learned how a real AI chatbot interface works. Why not try talking to it?")
        st.balloons()

# ... (rest of the code remains the same)
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
    st.header("🧠 Quiz Time: Test Your AI Chatbot Knowledge!")
    st.write("Let's see how much you've learned about AI chatbots and Python programming!")

    questions = [
        {
            "question": "What programming language are we using for this project?",
            "options": ["JavaScript", "Python", "Java", "C++"],
            "correct": "Python"
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
        },
        {
            "question": "Which file do we use to store our OpenAI API key?",
            "options": [".env", "config.py", "secrets.py", "api_key.txt"],
            "correct": ".env"
        },
        {
            "question": "What is a virtual environment used for?",
            "options": ["To create a 3D world for the chatbot", "To isolate project dependencies", "To speed up Python code", "To connect to the internet"],
            "correct": "To isolate project dependencies"
        },
        {
            "question": "Which file lists all the Python libraries our project needs?",
            "options": ["libraries.txt", "dependencies.py", "requirements.txt", "packages.list"],
            "correct": "requirements.txt"
        },
        {
            "question": "What does the .gitignore file do?",
            "options": ["Deletes unnecessary files", "Tells Git which files to ignore", "Speeds up Git operations", "Creates backup copies of files"],
            "correct": "Tells Git which files to ignore"
        },
        {
            "question": "Which of these is NOT a valid Streamlit command?",
            "options": ["st.write()", "st.markdown()", "st.display()", "st.balloons()"],
            "correct": "st.display()"
        },
        {
            "question": "What is the purpose of the 'threading' concept in our chatbot?",
            "options": ["To make the code run faster", "To create multiple chatbots", "To maintain context in conversations", "To reduce memory usage"],
            "correct": "To maintain context in conversations"
        },
        {
            "question": "Which library do we use to interact with the OpenAI API?",
            "options": ["openai", "gpt3", "ai_interface", "chatgpt"],
            "correct": "openai"
        }
    ]

    # Shuffle the questions
    random.shuffle(questions)

    # Initialize session state for score if it doesn't exist
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False

    def check_answer():
        if st.session_state.user_answer == questions[st.session_state.current_question]["correct"]:
            st.session_state.quiz_score += 1
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(questions):
            st.session_state.quiz_completed = True

    if not st.session_state.quiz_completed:
        q = questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
        st.write(q["question"])
        st.radio("Select your answer:", q["options"], key="user_answer", on_change=check_answer)
        
        # Progress bar
        progress = st.progress(st.session_state.current_question / len(questions))
        
        # Current score
        st.metric("Current Score", f"{st.session_state.quiz_score}/{st.session_state.current_question}")
    else:
        final_score = st.session_state.quiz_score
        st.subheader("🎉 Quiz Completed!")
        st.write(f"Your final score: {final_score} out of {len(questions)}")
        
        if final_score == len(questions):
            st.balloons()
            st.success("🏆 Perfect score! You're an AI chatbot expert!")
        elif final_score >= len(questions) * 0.8:
            st.success("🌟 Great job! You're well on your way to becoming an AI expert!")
        elif final_score >= len(questions) * 0.6:
            st.info("👍 Good effort! Keep learning and you'll master this in no time!")
        else:
            st.info("🌱 Nice try! Review the material and give it another shot!")
        
        if st.button("Try Again"):
            st.session_state.quiz_score = 0
            st.session_state.current_question = 0
            st.session_state.quiz_completed = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
