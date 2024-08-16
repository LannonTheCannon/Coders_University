import streamlit as st

def main():
    st.set_page_config(page_title="AI Chatbot Lesson Plan", page_icon="🤖", layout="wide")

    st.title("🤖 AI Chatbot Lesson Plan")
    st.write("Welcome to the AI Chatbot Lesson Plan! This guide will help you create your own AI chatbot using Streamlit and the OpenAI Assistant API.")

    sections = [
        "Introduction",
        "Code Breakdown",
        "Setup Instructions",
        'Helper Functions',
        "Customization Ideas",
        "Full Code"
    ]

    selection = st.sidebar.radio("Navigation", sections)

    if selection == "Introduction":
        show_introduction()
    elif selection == "Code Breakdown":
        show_code_breakdown()
    elif selection == "Setup Instructions":
        show_setup_instructions()
    elif selection == 'Helper Functions':
           helper_functions()
    elif selection == "Customization Ideas":
        show_customization_ideas()
    elif selection == "Full Code":
        show_full_code()

def show_introduction():
    st.header("Introduction")
    st.write("""
    In this lesson, you'll learn how to create an AI-powered chatbot using Streamlit and the OpenAI Assistant API. 
    This chatbot will be able to answer questions and engage in conversations on various topics.

    Key components we'll be using:
    1. Streamlit: A Python library for creating web apps
    2. OpenAI API: To power our AI assistant
    3. Python: The programming language we'll use

    By the end of this lesson, you'll have your own working AI chatbot!
    """)

def show_code_breakdown():
    st.header("Code Breakdown")
    
    st.subheader("1. Imports and Page Configuration")
    st.code("""
import streamlit as st
import openai
import time

st.set_page_config(page_title="My AI Chatbot", page_icon="🤖", layout="wide")
    """)
    st.write("We import necessary libraries and set up the Streamlit page configuration.")

    st.subheader("2. API Key Input")
    st.code("""
st.sidebar.title("Setup")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    """)
    st.write("We create a sidebar for users to input their OpenAI API key.")

    st.subheader("3. Chat Interface")
    st.code("""
st.title("🤖 My AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    """)
    st.write("We set up the main chat interface and initialize the message history.")

    st.subheader("4. Assistant and Thread IDs")
    st.code("""
ASSISTANT_ID = 'your_assistant_id_here'
THREAD_ID = 'your_thread_id_here'
    """)
    st.write("We define constants for the Assistant ID and Thread ID.")

    st.subheader("5. Helper Functions")
    st.code("""
def wait_for_run_complete(client, thread_id, run_id):
    # Function implementation...

def get_assistant_response(client, user_input):
    # Function implementation...
    """)
    st.write("These functions handle the interaction with the OpenAI API.")

    st.subheader("6. Chat Logic")
    st.code("""
if api_key:
    client = openai.OpenAI(api_key=api_key)
    prompt = st.chat_input("Ask me anything!")
    if prompt:
        # Handle user input and get AI response
else:
    st.warning("Please enter your OpenAI API key in the sidebar to start the chat.")
    """)
    st.write("This section handles the main chat logic, including user input and AI responses.")

def show_setup_instructions():
    st.header("Setup Instructions")
    st.write("""
    Follow these steps to set up your AI chatbot:

    1. Install required libraries:
       ```
       pip install streamlit openai
       ```

    2. Sign up for an OpenAI account and get your API key from the OpenAI dashboard.

    3. Create a new Python file (e.g., `chatbot.py`) and copy the full code into it.

    4. Replace `'your_assistant_id_here'` with your actual OpenAI Assistant ID.

    5. Run your Streamlit app:
       ```
       streamlit run chatbot.py
       ```

    6. Enter your OpenAI API key in the sidebar when the app launches.

    That's it! You should now have a working AI chatbot.
    """)

def helper_functions():

    st.subheader("5. Helper Functions")
    
    st.write("Let's break down our two helper functions:")
    
    st.markdown("#### a) wait_for_run_complete function")
    st.code("""
def wait_for_run_complete(client, thread_id, run_id):
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.completed_at:
            return run.status
        time.sleep(1)
    """)
    st.write("""
    This function is responsible for waiting until the AI has finished processing our request. Here's what it does:
    
    1. It enters a loop that continues until the run is completed.
    2. Inside the loop, it checks the status of the run using `client.beta.threads.runs.retrieve()`.
    3. If the run is completed (`run.completed_at` is not None), it returns the run's status.
    4. If the run isn't completed, it waits for 1 second (`time.sleep(1)`) before checking again.
    5. This process repeats until the run is completed.

    This function is crucial because AI processing can take a variable amount of time, and we need to wait for it to finish before we can get the response.
    """)

    st.markdown("#### b) get_assistant_response function")
    st.code("""
def get_assistant_response(client, user_input):
    client.beta.threads.messages.create(
        thread_id=THREAD_ID,
        role='user',
        content=user_input
    )
    run = client.beta.threads.runs.create(
        thread_id=THREAD_ID,
        assistant_id=ASSISTANT_ID
    )
    wait_for_run_complete(client, THREAD_ID, run.id)
    messages = client.beta.threads.messages.list(thread_id=THREAD_ID)
    return messages.data[0].content[0].text.value
    """)
    st.write("""
    This function handles the entire process of getting a response from the AI. Here's a step-by-step breakdown:

    1. It adds the user's message to the thread using `client.beta.threads.messages.create()`.
       - `thread_id`: The ID of the conversation thread.
       - `role`: Set to 'user' to indicate it's a user message.
       - `content`: The actual message from the user.

    2. It creates a new 'run', which is essentially asking the AI to process the conversation, using `client.beta.threads.runs.create()`.
       - `thread_id`: The ID of the conversation thread.
       - `assistant_id`: The ID of the AI assistant we're using.

    3. It calls our `wait_for_run_complete()` function to wait until the AI has finished processing.

    4. Once the run is complete, it retrieves all messages in the thread using `client.beta.threads.messages.list()`.

    5. Finally, it returns the content of the latest message (which is the AI's response).
       - `messages.data[0]` gets the most recent message.
       - `.content[0].text.value` accesses the text content of that message.

    This function encapsulates the entire process of sending a message to the AI and getting its response, making the main code cleaner and easier to understand.
    """)

def show_customization_ideas():
    st.header("Customization Ideas")
    st.write("""
    Here are some ideas to customize and enhance your chatbot:

    1. Change the chatbot's personality by modifying the Assistant's instructions in the OpenAI platform.

    2. Add a feature to save conversation history.

    3. Implement different "modes" for the chatbot (e.g., casual, professional, educational).

    4. Integrate with other APIs to give the chatbot additional capabilities (e.g., weather information, news updates).

    5. Add visual elements like charts or images based on the conversation context.

    6. Implement user authentication to create personalized experiences.

    Remember, the key to learning is experimentation. Don't be afraid to try new ideas and features!
    """)

def show_full_code():
    st.header("Full Code")
    st.code("""
import streamlit as st
import openai
import time

# Streamlit page config
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖", layout="wide")

# Sidebar for API key input
st.sidebar.title("Setup")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Main chat interface
st.title("🤖 My AI Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Replace these with your own Assistant ID and Thread ID
ASSISTANT_ID = 'your_assistant_id_here'
THREAD_ID = 'your_thread_id_here'

def wait_for_run_complete(client, thread_id, run_id):
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.completed_at:
            return run.status
        time.sleep(1)

def get_assistant_response(client, user_input):
    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=THREAD_ID,
        role='user',
        content=user_input
    )
    # Create a run
    run = client.beta.threads.runs.create(
        thread_id=THREAD_ID,
        assistant_id=ASSISTANT_ID
    )
    # Wait for the run to complete
    wait_for_run_complete(client, THREAD_ID, run.id)
    # Retrieve the assistant's messages
    messages = client.beta.threads.messages.list(thread_id=THREAD_ID)
    
    # Return the latest assistant message
    return messages.data[0].content[0].text.value

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if api_key:
    client = openai.OpenAI(api_key=api_key)
    prompt = st.chat_input("Ask me anything!")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_assistant_response(client, prompt)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.warning("Please enter your OpenAI API key in the sidebar to start the chat.")
    """, language="python")
    st.write("This is the complete code for your AI chatbot. You can copy this into a new Python file and run it with Streamlit.")

if __name__ == "__main__":
    main()
