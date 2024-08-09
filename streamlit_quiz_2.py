import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Streamlit Session State Quiz", page_icon="🧠")

# Initialize session state variables
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False

# Quiz questions and answers
quiz_data = [
    {
        "question": "What is the primary purpose of Streamlit's session_state?",
        "options": [
            "To create beautiful visualizations",
            "To persist data across reruns of the app",
            "To connect to databases",
            "To optimize app performance"
        ],
        "correct_answer": 1
    },
    {
        "question": "How do you initialize a variable in session_state?",
        "options": [
            "st.session_state.variable = value",
            "st.init_state(variable, value)",
            "st.state.set(variable, value)",
            "st.set_state(variable, value)"
        ],
        "correct_answer": 0
    },
    {
        "question": "Which of the following is TRUE about session_state?",
        "options": [
            "It's only used for numerical data",
            "It resets every time the app reruns",
            "It can store various data types including lists and dictionaries",
            "It's mainly used for styling Streamlit apps"
        ],
        "correct_answer": 2
    },
    {
        "question": "How do you access a variable stored in session_state?",
        "options": [
            "st.get_state('variable')",
            "st.state.variable",
            "st.session_state.variable",
            "st.variable"
        ],
        "correct_answer": 2
    },
    {
        "question": "When is it appropriate to use session_state?",
        "options": [
            "Only for storing user inputs",
            "When you need to persist data across reruns or share data between different parts of your app",
            "Only for backend operations",
            "When you want to create static content"
        ],
        "correct_answer": 1
    },
    {
        "question": "What happens to session_state variables when you close the Streamlit app?",
        "options": [
            "They are automatically saved to a file",
            "They persist indefinitely",
            "They are reset to their initial values",
            "They are cleared from memory"
        ],
        "correct_answer": 3
    },
    {
        "question": "How can you check if a variable exists in session_state?",
        "options": [
            "st.session_state.has(variable)",
            "variable in st.session_state",
            "st.session_state.exists(variable)",
            "st.has_state(variable)"
        ],
        "correct_answer": 1
    },
    {
        "question": "What's the difference between st.session_state.variable and st.session_state['variable']?",
        "options": [
            "They are completely different and store separate values",
            "st.session_state.variable is faster",
            "st.session_state['variable'] is more secure",
            "There is no difference, both access the same value"
        ],
        "correct_answer": 3
    },
    {
        "question": "How can you delete a variable from session_state?",
        "options": [
            "st.session_state.delete(variable)",
            "del st.session_state.variable",
            "st.session_state.remove(variable)",
            "st.remove_state(variable)"
        ],
        "correct_answer": 1
    },
    {
        "question": "Which of the following is NOT a common use case for session_state?",
        "options": [
            "Storing user preferences",
            "Caching large datasets",
            "Implementing undo/redo functionality",
            "Defining the layout of the Streamlit app"
        ],
        "correct_answer": 3
    }
]

# Streamlit app
st.title("🧠 Streamlit Session State Quiz")

if not st.session_state.quiz_complete:
    question = quiz_data[st.session_state.current_question]
    st.write(f"Question {st.session_state.current_question + 1} of {len(quiz_data)}")
    st.write(question["question"])

    # Use radio buttons for answer options
    answer = st.radio("Choose your answer:", question["options"], key=f"q{st.session_state.current_question}")

    if st.button("Submit Answer"):
        if question["options"].index(answer) == question["correct_answer"]:
            st.session_state.score += 1
            st.success("Correct!")
        else:
            st.error(f"Wrong. The correct answer was: {question['options'][question['correct_answer']]}")

        if st.session_state.current_question < len(quiz_data) - 1:
            st.session_state.current_question += 1
        else:
            st.session_state.quiz_complete = True
        st.rerun()

else:
    st.write("Quiz completed!")
    st.write(f"Your final score: {st.session_state.score} out of {len(quiz_data)}")

    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_complete = False
        st.rerun()

# Display current score
st.sidebar.write(f"Current Score: {st.session_state.score}/{len(quiz_data)}")

# Explanation of session_state usage in this app
st.sidebar.title("How session_state is used here")
st.sidebar.write("""
This quiz app demonstrates the use of session_state in several ways:

1. Tracking the current question (st.session_state.current_question)
2. Keeping score (st.session_state.score)
3. Maintaining quiz state (st.session_state.quiz_complete)

These variables persist across reruns, allowing the quiz to maintain its state even when the user interacts with it.
""")