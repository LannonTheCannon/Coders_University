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


def main():
    st.sidebar.title("🚀 Streamlit Masterclass")
    with st.sidebar.expander('Intro to Streamlit', expanded=False):
        streamlit_sections = [
            '☕ Home',
            "🧰 Setup",
            "🧱 Basic Elements",
            "🔢 Interactive App",
            "🎳 Running the App",
            "🔑 Session State",
            "👋 Hands-on Activity",
            "🎨 CSS Wrapping",
            '🧠 Quizzes',
            "🎓 Wrap-up",
            ]
        selected_streamlit_section = st.radio("Streamlit Topics", streamlit_sections)

    with st.sidebar.expander('Github Lessons', expanded=True):
        github_sections = [
            "📘 Introduction to Git",
            "🌿 Branching and Merging",
            "🔄 Pull Requests",
            "🚀 GitHub Actions",
            "📊 GitHub Projects",
            '🧠 Quizzes',
            "🎓 Wrap-up",
            ]

        selected_github_section = st.radio('Github Topics', github_sections)

    if selected_streamlit_section:
        if selected_streamlit_section == '☕ Home':
            landing_page()
        elif selected_streamlit_section == "🧰 Setup":
            setup_page()
        elif selected_streamlit_section == "🧱 Basic Elements":
            basic_elements_page()
        elif selected_streamlit_section == "🔢 Interactive App":
            interactive_app_page()
        elif selected_streamlit_section == "🎳 Running the App":
            running_app_page()
        elif selected_streamlit_section == '🔑 Session State':
            sess_state_page()
        elif selected_streamlit_section == "👋 Hands-on Activity":
            hands_on_activity_page()
        elif selected_streamlit_section == "🎨 CSS Wrapping":  
            css_wrapping_page()
        elif selected_streamlit_section == "🧠 Quizzes":
            display_quiz_page()
        elif selected_streamlit_section == "🎓 Wrap-up":
            wrap_up_page()

    elif selected_github_section:
        if selected_github_section == "📘 Introduction to Git":
            intro_to_git()
        elif selected_github_section == "🌿 Branching and Merging":
            pass
        elif selected_github_section == "🔄 Pull Requests":
            pass
        elif selected_github_section == "🚀 GitHub Actions":
            pass
        elif selected_github_section == "📊 GitHub Projects":
            pass
        elif selected_github_section == "🧠 Quizzes":
            pass
        elif selected_github_section == "🎓 Wrap-up":
            pass
        
if __name__ == "__main__":
    main()
