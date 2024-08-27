import streamlit as st
import openai
import time
import os

# Streamlit page config
st.set_page_config(page_title="Sherlock Holmes Chatbot", page_icon="🕵️", layout="wide")

# Custom CSS for styling the sidebar
ASSISTANT_ID = 'asst_OUgnR5TbpMHivgAvdaG28t3I'
THREAD_ID = 'thread_E8hQrVWyhNIGue3LdhJ082ly'

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Main chat interface
st.title("🕵️ Sherlock Holmes AI")
st.markdown("*I am Sherlock Holmes, the world's only consulting detective. How may I assist you with your case?*")

if "messages" not in st.session_state:
    st.session_state.messages = []

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
        return "I'm afraid an error has occurred in our communication, Watson. Let us try again."

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Describe your case, dear Watson...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_assistant_response(ASSISTANT_ID, THREAD_ID, prompt)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with interesting facts about Sherlock Holmes
st.sidebar.title("Did you know?")
st.sidebar.write("Sherlock Holmes never said 'Elementary, my dear Watson' in any of Sir Arthur Conan Doyle's stories.")
