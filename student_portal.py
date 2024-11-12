# pages/home.py
import streamlit as st
import pandas as pd
from pathlib import Path

# Initialize session state variables if they don't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'current_subpage' not in st.session_state:
    st.session_state.current_subpage = None
if 'student_data' not in st.session_state:
    # Mock student data - replace with your actual data storage solution
    st.session_state.student_data = {
        'john_doe': {
            'name': 'John Doe',
            'progress': {
                'python_basics': 80,
                'functions': 65,
                'web_dev': 45,
                'ai_integration': 30
            },
            'achievements': ['First Python Program', 'Escape Room Complete'],
            'current_module': 'Functions and APIs',
            'test_scores': [85, 90, 75, 95]
        }
    }


def render_navigation():
    """Render the main navigation menu"""
    main_pages = {
        'Dashboard': 'dashboard',
        'Progress Tracker': 'progress',
        'Achievements': 'achievements',
        'Resources': 'resources'
    }

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button('Dashboard', use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.session_state.current_subpage = None
    with col2:
        if st.button('Progress', use_container_width=True):
            st.session_state.current_page = 'progress'
            st.session_state.current_subpage = None
    with col3:
        if st.button('Achievements', use_container_width=True):
            st.session_state.current_page = 'achievements'
            st.session_state.current_subpage = None
    with col4:
        if st.button('Resources', use_container_width=True):
            st.session_state.current_page = 'resources'
            st.session_state.current_subpage = None


def render_dashboard():
    """Render the dashboard page"""
    st.header("Student Dashboard")

    # Mock student data - replace with actual student
    student = st.session_state.student_data['john_doe']

    # Overview cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Progress", "65%", "+5%")
    with col2:
        st.metric("Current Module", student['current_module'])
    with col3:
        st.metric("Latest Test Score", "95/100", "+10")

    # Progress bars for different areas
    st.subheader("Skills Progress")
    for skill, progress in student['progress'].items():
        st.progress(progress / 100)
        st.caption(f"{skill.replace('_', ' ').title()}: {progress}%")


def render_progress():
    """Render the progress tracking page"""
    st.header("Progress Tracker")

    # Sub-navigation for progress
    progress_pages = ['Course Progress', 'Test Scores', 'Project Status']
    selected_progress = st.radio("Select View", progress_pages)

    if selected_progress == 'Course Progress':
        st.subheader("Course Completion Status")
        df = pd.DataFrame({
            'Module': ['Python Basics', 'Functions', 'Web Development', 'AI Integration'],
            'Progress': [80, 65, 45, 30],
            'Status': ['Completed', 'In Progress', 'Started', 'Not Started']
        })
        st.dataframe(df)

    elif selected_progress == 'Test Scores':
        st.subheader("Test Performance")
        scores = st.session_state.student_data['john_doe']['test_scores']
        st.line_chart(scores)

    elif selected_progress == 'Project Status':
        st.subheader("Project Submissions")
        st.info("Current Project: Escape Room Game")
        st.progress(0.7)
        st.caption("70% Complete")


def render_achievements():
    """Render the achievements page"""
    st.header("Achievements")

    achievements = st.session_state.student_data['john_doe']['achievements']

    for achievement in achievements:
        st.success(f"🏆 {achievement}")


def render_resources():
    """Render the resources page"""
    st.header("Learning Resources")

    resource_types = ['Documentation', 'Practice Exercises', 'Additional Materials']
    selected_resource = st.radio("Resource Type", resource_types)

    if selected_resource == 'Documentation':
        st.markdown("""
        - [Python Basics Guide](/)
        - [Function Reference](/)
        - [API Documentation](/)
        """)
    elif selected_resource == 'Practice Exercises':
        st.markdown("""
        - Exercise Set 1: Variables and Data Types
        - Exercise Set 2: Control Flow
        - Exercise Set 3: Functions
        """)
    elif selected_resource == 'Additional Materials':
        st.markdown("""
        - Recommended Reading
        - Video Tutorials
        - External Resources
        """)


def main():
    st.title("Coding Workshop Student Portal")

    # Render the main navigation
    render_navigation()

    # Render the selected page
    if st.session_state.current_page == 'dashboard':
        render_dashboard()
    elif st.session_state.current_page == 'progress':
        render_progress()
    elif st.session_state.current_page == 'achievements':
        render_achievements()
    elif st.session_state.current_page == 'resources':
        render_resources()


if __name__ == "__main__":
    main()