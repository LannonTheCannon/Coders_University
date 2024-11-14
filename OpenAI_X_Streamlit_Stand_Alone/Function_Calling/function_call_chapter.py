import openai
import streamlit as st
import json
import time

# Page configuration
st.set_page_config(page_title="OpenAI Assistant Tutorial", layout="wide")

# Sidebar navigation
st.sidebar.title("Assistant Implementation Guide")
section = st.sidebar.radio(
    "Choose a section",
    ["1. Setup & Basics",
     "2. Error Handling",
     "3. Complete Code",
     "4. Live Demo"]
)

# Initialize OpenAI client
if 'messages' not in st.session_state:
    st.session_state.messages = []


# Your actual assistant implementation
def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Create message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Check for active runs
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        active_run = next((run for run in runs.data if run.status == "in_progress"), None)

        if active_run:
            while active_run.status == "in_progress":
                time.sleep(1)
                active_run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=active_run.id
                )

        # Create new run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for completion
        while run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."


if section == "1. Setup & Basics":
    st.title("Setting Up the Assistant")
    st.markdown("""
    ### Basic Setup
    ```python
    import openai
    import streamlit as st
    import time

    api_key = st.secrets['OPENAI_API_KEY']
    client = openai.OpenAI(api_key=api_key)

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    ```

    ### Key Components:
    1. **OpenAI Client**: Handles communication with OpenAI's API
    2. **Session State**: Stores chat history
    3. **Assistant & Thread IDs**: Unique identifiers for your assistant
    """)

elif section == "2. Error Handling":
    st.title("Error Handling Implementation")
    st.markdown("""
    ### Key Error Prevention Features

    1. **Active Run Check**:
    ```python
    # Check for active runs
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    active_run = next((run for run in runs.data if run.status == "in_progress"), None)

    if active_run:
        while active_run.status == "in_progress":
            time.sleep(1)
            active_run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=active_run.id
            )
    ```

    2. **Try-Except Block**:
    ```python
    try:
        # API calls here
    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred..."
    ```

    3. **Loading Indicator**:
    ```python
    with st.spinner('Getting response...'):
        full_response = get_assistant_response(...)
    ```
    """)

elif section == "3. Complete Code":
    st.title("Complete Implementation")
    with st.expander("View Full Code"):
        st.code('''
import openai
import streamlit as st
import time

api_key = st.secrets['OPENAI_API_KEY']
client = openai.OpenAI(api_key=api_key)

if 'messages' not in st.session_state:
    st.session_state.messages = []

def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Create message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Check for active runs
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        active_run = next((run for run in runs.data if run.status == "in_progress"), None)

        if active_run:
            while active_run.status == "in_progress":
                time.sleep(1)
                active_run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=active_run.id
                )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."

def main():
    st.title("AI Assistant Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner('Getting response...'):
                full_response = get_assistant_response(
                    ASSISTANT_ID,
                    THREAD_ID,
                    prompt
                )
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == '__main__':
    main()
''', language='python')

elif section == "4. Live Demo":
    st.title("Live Assistant Demo")

    # Initialize OpenAI client
    api_key = st.secrets['OPENAI_API_KEY']
    client = openai.OpenAI(api_key=api_key)

    # Your actual chat interface implementation here
    st.markdown("Try out the assistant with error handling:")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner('Getting response...'):
                full_response = get_assistant_response(
                    ASSISTANT_ID,
                    THREAD_ID,
                    prompt
                )
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})