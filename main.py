import streamlit as st
import pandas as pd
import altair as alt
import time
from src.landing_1 import landing_page
from src.setup_2 import setup_page
from src.basic_elements_3 import basic_elements_page
from src.interactive_app_4 import interactive_app_page
from src.running_app_5 import running_app_page
from src.sess_state_6 import sess_state_page
from src.hands_on_act_7 import hands_on_activity_page
from src.wrap_up_8 import wrap_up_page
from src.css_wrap_9 import css_wrapping_page
from src.disp_quiz_10 import display_quiz_page

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
            "🎓 Wrap-up",
            "🎨 CSS Wrapping",
            '🧠 Quizzes'
        ]
        selected_streamlit_section = st.radio("Navigation", streamlit_sections)

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
        elif selected_streamlit_section == "🎓 Wrap-up":
            wrap_up_page()
        elif selected_streamlit_section == "🎨 CSS Wrapping":  
            css_wrapping_page()
        elif selected_streamlit_section == "🧠 Quizzes":
            display_quiz_page()


if __name__ == "__main__":
    main()
