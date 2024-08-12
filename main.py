import streamlit as st
import pandas as pd
import altair as alt
import time

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
        
    # Main section
    if st.session_state.active_section == 'intro':
        display_streamlit_content(streamlit_section)
    elif st.session_state.active_section == 'github':
        display_github_content(github_section)

if __name__ == "__main__":
    main()
