import streamlit as st

# Initialize session states for navigation
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


def main():
    st.title("Python Programming Course")

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")

        # Level selection
        level = st.radio(
            "Select Level",
            options=list(COURSE_STRUCTURE.keys()),
            key="level_radio"
        )

        # Update current level in session state
        if st.session_state.current_level != level:
            st.session_state.current_level = level
            st.session_state.current_subsection = COURSE_STRUCTURE[level]["sections"][0]

        # Subsection selection
        st.subheader(f"Sections in {level}")
        subsection = st.radio(
            "Select Section",
            options=COURSE_STRUCTURE[level]["sections"],
            key="section_radio"
        )

        # Update current subsection in session state
        st.session_state.current_subsection = subsection

    # Main content area
    def render_content():
        st.header(st.session_state.current_subsection)

        # Example of content rendering based on current section
        if st.session_state.current_subsection == "1.1 Introduction to IDLE":
            st.write("Welcome to Python programming! Let's start with IDLE...")
            st.code("""
            # Your first Python program
            print("Hello, World!")
            """)

        elif st.session_state.current_subsection == "1.2 Variables and Data Types":
            st.write("Let's learn about variables and data types in Python...")
            st.code("""
            # Variables and data types
            name = "John"          # string
            age = 25              # integer
            height = 1.75         # float
            is_student = True     # boolean
            """)

        # Add more content conditions here...
        else:
            st.info("Content for this section is being developed...")

        # Add navigation buttons
        col1, col2 = st.columns(2)
        current_sections = COURSE_STRUCTURE[st.session_state.current_level]["sections"]
        current_index = current_sections.index(st.session_state.current_subsection)

        with col1:
            if current_index > 0:
                if st.button("← Previous Section"):
                    st.session_state.current_subsection = current_sections[current_index - 1]
                    st.experimental_rerun()

        with col2:
            if current_index < len(current_sections) - 1:
                if st.button("Next Section →"):
                    st.session_state.current_subsection = current_sections[current_index + 1]
                    st.experimental_rerun()

    render_content()


if __name__ == "__main__":
    main()