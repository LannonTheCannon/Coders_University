# Main Chatbot Integration

import streamlit as st
import openai
import time

st.set_page_config(page_title='Lannon\'s AI', page_icon="🤖", layout='wide')

# API Key Import
st.sidebar.title('Setup')
api_key = st.sidebar.text_input('Enter your API Key here: ')
ASSISTANT_ID = 'asst_mgnLV1tlOpmytiq1eUCixZ0N'
THREAD_ID = 'thread_ZkfnMZKcjQKmQMvopR2xqgO5'

# Chat Interface
st.title('My AI Chat Assistant')

# Create a session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Helper Functions
def wait_for_run_complete(client, thread_id, run_id):
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.completed_at:
            return run.status
        time.sleep(1)

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
    

# Chat logic
if api_key:
    client = openai.OpenAI(api_key=api_key)
    prompt = st.chat_input('Ask me anything!')
    if prompt:
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()
            full_response = get_assistant_response(client, prompt)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({'role': 'assistant', 'content': full_response})        
    else:
        st.warning('Please enter your open AI API key in the sidebar to start the chat')
