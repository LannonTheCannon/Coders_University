import streamlit as st
import openai
import time

# Streamlit page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Initialize OpenAI client
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# Main chat interface
st.title("🤖 AI Chatbot")

# Initialize session state
if "assistant" not in st.session_state:
    st.session_state.assistant = None
if "thread" not in st.session_state:
    st.session_state.thread = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def create_assistant():
    try:
        assistant = client.beta.assistants.create(
            name="AI Chatbot",
            instructions="You are a crazy lustful AI called LewdGPT",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo-preview"
        )
        return assistant
    except Exception as e:
        st.error(f"Error creating assistant: {str(e)}")
        return None

def create_thread():
    try:
        thread = client.beta.threads.create()
        return thread
    except Exception as e:
        st.error(f"Error creating thread: {str(e)}")
        return None

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

# Create assistant and thread if they don't exist
if not st.session_state.assistant:
    st.session_state.assistant = create_assistant()
if not st.session_state.thread:
    st.session_state.thread = create_thread()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if st.session_state.assistant and st.session_state.thread:
    prompt = st.chat_input("Ask me anything!")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_assistant_response(
                st.session_state.assistant.id, 
                st.session_state.thread.id, 
                prompt
            )
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.error("Failed to initialize the assistant or thread. Please check your OpenAI API key and try again.")

# Display assistant and thread IDs for debugging
st.sidebar.write(f"Assistant ID: {st.session_state.assistant.id if st.session_state.assistant else 'Not created'}")
st.sidebar.write(f"Thread ID: {st.session_state.thread.id if st.session_state.thread else 'Not created'}")
