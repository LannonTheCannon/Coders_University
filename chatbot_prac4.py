import streamlit as st
import openai
import time
import os
from dotenv import load_dotenv

# Streamlit page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Initialize OpenAI client
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# Main chat interface
st.title("🤖 AI Chatbot")

# Initialize session state

ASSISTANT_ID='asst_mgnLV1tlOpmytiq1eUCixZ0N'
THREAD_ID='thread_MrXMPr9grJQmFWNgnvcRkzpK'

##def create_assistant():
##    try:
##        assistant = client.beta.assistants.create(
##            name="AI Chatbot",
##            instructions="You are a helpful AI assistant.",
##            tools=[{"type": "code_interpreter"}],
##            model="gpt-4o-mini"
##        )
##        return assistant
##    except Exception as e:
##        st.error(f"Error creating assistant: {str(e)}")
##        return None
##
##def create_thread():
##    try:
##        thread = client.beta.threads.create()
##        return thread
##    except Exception as e:
##        st.error(f"Error creating thread: {str(e)}")
##        return None



def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role="user",
            content=user_input
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=THREAD_ID, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)

        # Retrieve the assistant's messages
        messages = client.beta.threads.messages.list(thread_id=THREAD_ID)
        
        # Return the latest assistant message
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if ASSISTANT_ID and THREAD_ID:
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