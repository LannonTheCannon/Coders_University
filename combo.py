# app.py

import streamlit as st
from login_combo import init_db, login_page, update_student_data, get_student_data
import pandas as pd
import random
from datetime import datetime

# Initialize session states
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'portal'  # 'portal' or 'lessons'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'current_level' not in st.session_state:
    st.session_state.current_level = None
if 'current_subsection' not in st.session_state:
    st.session_state.current_subsection = None

# Course structure definition
COURSE_STRUCTURE = {
    "Level 1: Python Basics": {
        "sections": [
            "1.1 Introduction to IDLE",
            "1.2 Variables and Data Types",
            "1.3 Basic Operations",
            "1.4 Input and Output",
            "1.5 Conditional Statements",
            "1.6 While Loops",
            "1.7 For Loops",
            "1.8 Lists",
            "1.9 Dictionaries",
            "1.10 Basic Functions",
            "1.11 String Operations",
            "1.12 File Operations"
        ],
        "description": "Fundamentals of Python programming"
    },
    "Level 2: Functions & Games": {
        "sections": [
            "2.1 Function Parameters",
            "2.2 Return Values",
            "2.3 Scope",
            "2.4 Game Planning",
            "2.5 Game Structure",
            "2.6 Player Input",
            "2.7 Game Logic",
            "2.8 Game States",
            "2.9 Error Handling",
            "2.10 Game Testing"
        ],
        "description": "Advanced functions and game development"
    },
    "Level 3: Web Development": {
        "sections": [
            "3.1 Intro to Streamlit",
            "3.2 Basic Layouts",
            "3.3 User Input",
            "3.4 Data Display",
            "3.5 Charts and Graphs",
            "3.6 File Upload/Download",
            "3.7 Session State",
            "3.8 App Deployment"
        ],
        "description": "Web application development with Streamlit"
    }
}


# Portal Functions
def render_navigation():
    """Render the main portal navigation menu"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button('Dashboard', use_container_width=True):
            st.session_state.current_page = 'dashboard'
    with col2:
        if st.button('Progress', use_container_width=True):
            st.session_state.current_page = 'progress'
    with col3:
        if st.button('Achievements', use_container_width=True):
            st.session_state.current_page = 'achievements'
    with col4:
        if st.button('Resources', use_container_width=True):
            st.session_state.current_page = 'resources'


def render_dashboard():
    """Render a youth-focused dashboard"""
    student = st.session_state.student_data[st.session_state.username]

    # Welcome Section with Time-based greeting
    current_hour = datetime.now().hour
    greeting = "Good morning! 🌅" if 5 <= current_hour < 12 else \
        "Good afternoon! ☀️" if 12 <= current_hour < 17 else \
            "Good evening! 🌙"

    st.header(f"{greeting} {student['name']}")

    # Top Stats in Modern Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='padding: 20px; background-color: #f0f2f6; border-radius: 10px; text-align: center;'>
            <h3>Coding Streak 🔥</h3>
            <h2>5 Days</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Calculate level based on total progress
        total_progress = sum(student['progress'].values())
        level = int(total_progress / 100) + 1
        st.markdown(f"""
        <div style='padding: 20px; background-color: #f0f2f6; border-radius: 10px; text-align: center;'>
            <h3>Coder Level 🚀</h3>
            <h2>Level {level}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Calculate achievements percentage
        total_achievements = len(student['achievements'])
        st.markdown(f"""
        <div style='padding: 20px; background-color: #f0f2f6; border-radius: 10px; text-align: center;'>
            <h3>Achievements 🏆</h3>
            <h2>{total_achievements}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Current Mission & Progress
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎯 Current Mission")
        current_module = student['current_module']
        progress_value = student['progress'].get(
            current_module.lower().replace(' ', '_'), 0
        )

        st.markdown(f"""
        ### {current_module}
        Progress: {progress_value}%
        """)
        st.progress(progress_value / 100)

        # Next milestone
        next_milestone = (progress_value // 10 + 1) * 10
        if progress_value < 100:
            st.caption(f"🎯 Next Milestone: {next_milestone}%")

    with col2:
        st.subheader("⭐ Quick Stats")
        st.markdown(f"""
        - 🏃‍♂️ Active Days: 12
        - ✅ Tasks Completed: {int(total_progress / 10)}
        - 📝 Lines of Code: {int(total_progress * 20)}
        """)

    # Recent Achievements
    st.subheader("🏆 Recent Achievements")
    if student['achievements']:
        achievements_col1, achievements_col2, achievements_col3 = st.columns(3)
        for idx, achievement in enumerate(student['achievements'][-3:]):
            with [achievements_col1, achievements_col2, achievements_col3][idx]:
                st.markdown(f"""
                <div style='padding: 15px; background-color: #e6f3ff; border-radius: 10px; text-align: center;'>
                    <h4>🏆 {achievement}</h4>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Complete lessons to earn your first achievement! 🎯")

    # Skill Progress Bars with Icons
    st.subheader("💪 Your Skills")
    skills_col1, skills_col2 = st.columns(2)

    with skills_col1:
        st.markdown("#### Core Skills")
        for skill, progress in student['progress'].items():
            if skill in ['python_basics', 'functions']:
                icon = "🐍" if skill == "python_basics" else "⚡"
                st.markdown(f"**{icon} {skill.replace('_', ' ').title()}**")
                st.progress(progress / 100)
                st.caption(f"{progress}% Mastered")

    with skills_col2:
        st.markdown("#### Advanced Skills")
        for skill, progress in student['progress'].items():
            if skill in ['web_dev', 'ai_integration']:
                icon = "🌐" if skill == "web_dev" else "🤖"
                st.markdown(f"**{icon} {skill.replace('_', ' ').title()}**")
                st.progress(progress / 100)
                st.caption(f"{progress}% Mastered")

    # Quick Actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📚 Resume Learning", use_container_width=True):
            st.session_state.current_view = 'lessons'
            st.rerun()

    with col2:
        if st.button("🎯 Set Goals", use_container_width=True):
            st.info("Goals feature coming soon!")

    with col3:
        if st.button("👥 Join Community", use_container_width=True):
            st.info("Community feature coming soon!")

    with col4:
        if st.button("🎮 Practice Games", use_container_width=True):
            st.info("Coding games coming soon!")

    # Weekly Activity Calendar
    st.subheader("📅 Weekly Activity")
    cols = st.columns(7)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for idx, (col, day) in enumerate(zip(cols, days)):
        with col:
            activity_level = random.choice(['🟢', '🟡', '⚪'])  # Mock activity data
            st.markdown(f"""
            <div style='text-align: center;'>
                <p>{day}</p>
                <h3>{activity_level}</h3>
            </div>
            """, unsafe_allow_html=True)

def render_progress():
    """Render the progress tracking page"""
    st.header("Progress Tracker")

    student = st.session_state.student_data[st.session_state.username]

    progress_pages = ['Course Progress', 'Test Scores', 'Project Status']
    selected_progress = st.radio("Select View", progress_pages)

    if selected_progress == 'Course Progress':
        st.subheader("Course Completion Status")
        df = pd.DataFrame({
            'Module': list(student['progress'].keys()),
            'Progress': list(student['progress'].values()),
            'Status': ['Completed' if p >= 100 else 'In Progress' if p > 0 else 'Not Started'
                       for p in student['progress'].values()]
        })
        st.dataframe(df)
    elif selected_progress == 'Test Scores':
        st.subheader("Test Performance")
        if student['test_scores']:
            st.line_chart(student['test_scores'])
        else:
            st.info("No test scores recorded yet.")
    elif selected_progress == 'Project Status':
        st.subheader("Project Submissions")
        st.info(f"Current Module: {student['current_module']}")
        current_progress = student['progress'].get(
            student['current_module'].lower().replace(' ', '_'), 0
        )
        st.progress(current_progress / 100)
        st.caption(f"{current_progress}% Complete")


def render_achievements():
    """Render the achievements page"""
    st.header("Achievements")
    student = st.session_state.student_data[st.session_state.username]
    if student['achievements']:
        for achievement in student['achievements']:
            st.success(f"🏆 {achievement}")
    else:
        st.info("Complete lessons to earn achievements!")


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


def render_lesson_content(subsection):
    """Render the lesson content"""
    st.header(subsection)

    if subsection == "1.1 Introduction to IDLE":
        st.write("Welcome to Python programming! Let's start with IDLE...")
        st.code("""
        # Your first Python program
        print("Hello, World!")
        """)

        if st.button("Mark Complete"):
            student_data = st.session_state.student_data[st.session_state.username]
            progress = student_data['progress']
            progress['python_basics'] = min(100, progress['python_basics'] + 8.33)  # 100/12 sections

            # Update progress in database
            update_student_data(st.session_state.username, 'progress', progress)

            # Update achievements if needed
            if "First Python Program" not in student_data['achievements']:
                achievements = student_data['achievements']
                achievements.append("First Python Program")
                update_student_data(st.session_state.username, 'achievements', achievements)

            # Refresh student data
            st.session_state.student_data[st.session_state.username] = get_student_data(st.session_state.username)
            st.success("Progress updated!")
            st.rerun()

    elif subsection == "1.2 Variables and Data Types":
        st.write("Let's learn about variables and data types in Python...")
        st.code("""
        # Variables and data types
        name = "John"          # string
        age = 25              # integer
        height = 1.75         # float
        is_student = True     # boolean
        """)

        if st.button("Mark Complete"):
            student_data = st.session_state.student_data[st.session_state.username]
            progress = student_data['progress']
            progress['python_basics'] = min(100, progress['python_basics'] + 8.33)
            update_student_data(st.session_state.username, 'progress', progress)
            st.session_state.student_data[st.session_state.username] = get_student_data(st.session_state.username)
            st.success("Progress updated!")
            st.rerun()
    else:
        st.info("Content for this section is being developed...")
        if st.button("Mark Complete"):
            student_data = st.session_state.student_data[st.session_state.username]
            progress = student_data['progress']

            # Determine which module to update based on current level
            if st.session_state.current_level.startswith("Level 1"):
                progress['python_basics'] = min(100, progress['python_basics'] + 8.33)
            elif st.session_state.current_level.startswith("Level 2"):
                progress['functions'] = min(100, progress['functions'] + 10)
            elif st.session_state.current_level.startswith("Level 3"):
                progress['web_dev'] = min(100, progress['web_dev'] + 12.5)

            update_student_data(st.session_state.username, 'progress', progress)
            st.session_state.student_data[st.session_state.username] = get_student_data(st.session_state.username)
            st.success("Progress updated!")
            st.rerun()

    # Navigation buttons
    if st.session_state.current_level:
        current_sections = COURSE_STRUCTURE[st.session_state.current_level]["sections"]
        current_index = current_sections.index(st.session_state.current_subsection)

        col1, col2 = st.columns(2)
        with col1:
            if current_index > 0:
                if st.button("← Previous Section"):
                    st.session_state.current_subsection = current_sections[current_index - 1]
                    st.rerun()
        with col2:
            if current_index < len(current_sections) - 1:
                if st.button("Next Section →"):
                    st.session_state.current_subsection = current_sections[current_index + 1]
                    st.rerun()


def main():
    # Initialize database
    init_db()

    # Initialize login state if not exists
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    # Show login page if not logged in
    if not login_page():
        return

    # Show logout button in sidebar when logged in
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.student_data = None
            st.rerun()

    st.title("Python Programming Platform")

    # Sidebar
    with st.sidebar:
        st.header("Navigation")

        # Portal/Lessons Toggle
        if st.button("Return to Portal" if st.session_state.current_view == 'lessons' else "Go to Lessons",
                     use_container_width=True):
            st.session_state.current_view = 'portal' if st.session_state.current_view == 'lessons' else 'lessons'
            st.rerun()

        st.divider()

        # Lesson Navigation (only shown in lessons view)
        if st.session_state.current_view == 'lessons':
            level = st.radio(
                "Select Level",
                options=list(COURSE_STRUCTURE.keys()),
                key="level_radio"
            )

            if st.session_state.current_level != level:
                st.session_state.current_level = level
                st.session_state.current_subsection = COURSE_STRUCTURE[level]["sections"][0]

            st.subheader(f"Sections in {level}")
            subsection = st.radio(
                "Select Section",
                options=COURSE_STRUCTURE[level]["sections"],
                key="section_radio"
            )
            st.session_state.current_subsection = subsection

    # Main Content Area
    if st.session_state.current_view == 'portal':
        render_navigation()

        if st.session_state.current_page == 'dashboard':
            render_dashboard()
        elif st.session_state.current_page == 'progress':
            render_progress()
        elif st.session_state.current_page == 'achievements':
            render_achievements()
        elif st.session_state.current_page == 'resources':
            render_resources()
    else:  # Lessons view
        render_lesson_content(st.session_state.current_subsection)


if __name__ == "__main__":
    main()