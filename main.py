import streamlit as st
import pandas as pd
import altair as alt
import time
import openai

# Streamlit Fundamentals Library 
from src.streamlit_fundamentals.landing_1 import landing_page
from src.streamlit_fundamentals.setup_2 import setup_page
from src.streamlit_fundamentals.basic_elements_3 import basic_elements_page
from src.streamlit_fundamentals.interactive_app_4 import interactive_app_page
from src.streamlit_fundamentals.running_app_5 import running_app_page
from src.streamlit_fundamentals.sess_state_6 import sess_state_page
from src.streamlit_fundamentals.hands_on_act_7 import hands_on_activity_page
from src.streamlit_fundamentals.wrap_up_8 import wrap_up_page
from src.streamlit_fundamentals.css_wrap_9 import css_wrapping_page
from src.streamlit_fundamentals.disp_quiz_10 import display_quiz_page

# Github and Github Desktop Tutorials
from src.github_topics.github_intro_1 import intro_to_git

# Set page config
st.set_page_config(
    page_title="Streamlit Masterclass",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chatbot functions
ASSISTANT_ID = 'asst_mgnLV1tlOpmytiq1eUCixZ0N'
THREAD_ID = 'thread_gpesqxGVn0zvniW08rTWhitW'

def wait_for_run_complete(client, thread_id, run_id):
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.completed_at:
            return run.status
        time.sleep(1)

def get_assistant_response(client, user_input):
    client.threads.messages.create(
        thread_id=THREAD_ID,
        role='user',
        content=user_input
    )
    run = client.threads.runs.create(
        thread_id=THREAD_ID,
        assistant_id=ASSISTANT_ID
    )
    wait_for_run_complete(client, THREAD_ID, run.id)
    messages = client.beta.threads.messages.list(thread_id=THREAD_ID)
    return messages.data[0].content[0].text.value

def display_chatbot():
    st.title("🤖 AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if "openai_api_key" in st.session_state and st.session_state.openai_api_key:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        prompt = st.chat_input("Ask me anything about Streamlit or GitHub!")
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



# Custom CSS
# noinspection PyInterpreter
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #4e54c8, #8f94fb);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #4e54c8, #8f94fb);
    }
    .Widget>label {
        color: white;
        font-family: monospace;
    }
    .stTextInput>div>div>input {
        color: #4e54c8;
    }
    .stButton>button {
        color: #4e54c8;
        background-color: white;
        border-radius: 20px;
    }
    .stProgress .st-bo {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def display_streamlit_content(subsection):
    if subsection == '☕ 1.0 Home':
        landing_page()
    elif subsection == "🧰 1.1 Setup":
        setup_page()
    elif subsection == "🧱 1.2 Basic Elements":
        basic_elements_page()
    elif subsection == "🔢 1.3 Interactive App":
        interactive_app_page()
    elif subsection == "🎳 1.4 Running the App":
        running_app_page()
    elif subsection == '🔑 1.5 Session State':
        sess_state_page()
    elif subsection == "👋 1.6 Hands-on Activity":
        hands_on_activity_page()
    elif subsection == "🎨 1.7 CSS Wrapping":  
        css_wrapping_page()
    elif subsection == "🧠 1.8 Quizzes":
        display_quiz_page()
    elif subsection == "🎓 1.9 Wrap-up":
        wrap_up_page()

def display_github_content(subsection):
    if subsection == "📘 2.0 Introduction to Git":
        intro_to_git()
    elif subsection == "🌿 2.1 Branching and Merging":
        pass
    elif subsection == "🔄 2.2 Pull Requests":
        pass
    elif subsection == "🚀 2.3 GitHub Actions":
        pass
    elif subsection == "📊 2.4 GitHub Projects":
        pass
    elif subsection == "🧠 2.5 Quizzes":
        pass
    elif subsection == "🎓 2.6 Wrap-up":
        pass

def main():
    st.sidebar.title("🚀 Streamlit Masterclass")

        # API key input in sidebar
    st.sidebar.title("Setup")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        st.session_state.openai_api_key = api_key


    # use session state
    if 'active_section' not in st.session_state:
        st.session_state.active_section = None
    
    with st.sidebar.expander('Your Journey Begins Here'):
        streamlit_section = st.radio('Choose a subsection:',
            ['☕ 1.0 Home',
            "🧰 1.1 Setup",
            "🧱 1.2 Basic Elements",
            "🔢 1.3 Interactive App",
            "🎳 1.4 Running the App",
            "🔑 1.5 Session State",
            "👋 1.6 Hands-on Activity",
            "🎨 1.7 CSS Wrapping",
            '🧠 1.8 Quizzes',
            "🎓 1.9 Wrap-up",],
        key='intro')
        if st.button('Activate Streamlit Section', key='streamlit_button'):
            st.session_state.active_section = 'intro'

    with st.sidebar.expander('Github Lessons'):
        github_section = st.radio('Choose a subsection:',
            ["📘 2.0 Introduction to Git",
            "🌿 2.1 Branching and Merging",
            "🔄 2.2 Pull Requests",
            "🚀 2.3 GitHub Actions",
            "📊 2.4 GitHub Projects",
            '🧠 2.5 Quizzes',
            "🎓 2.6 Wrap-up",],
        key='github')
        if st.button('Activate Github Section', key='github_button'):
            st.session_state.active_section = 'github'

        # Add new expander for AI Assistant
    with st.sidebar.expander('AI Assistant'):
        if st.button('Activate AI Assistant', key='ai_assistant_button'):
            st.session_state.active_section = 'ai_assistant'
        
    # Main section
    if st.session_state.active_section == 'intro':
        display_streamlit_content(streamlit_section)
    elif st.session_state.active_section == 'github':
        display_github_content(github_section)
    elif st.session_state.active_section == 'ai_assistant':
        display_chatbot()

if __name__ == "__main__":
    main()
