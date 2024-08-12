# sess_state_6.py
import streamlit as st

def sess_state_page():
    st.title("🔑 Streamlit Session State")
    st.write("Learn how to persist data across reruns in your Streamlit app!")

    st.header("What is Session State?")
    st.write("Session State allows you to store and persist data across reruns of your Streamlit app.")

    st.header("Basic Usage")
    st.code("""
import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.write(f"Counter: {st.session_state.counter}")

if st.button("Increment"):
    st.session_state.counter += 1
    """)

    st.header("Live Demo")
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    st.write(f"Counter: {st.session_state.counter}")

    if st.button("Increment"):
        st.session_state.counter += 1
        # st.rerun()

    st.header("When to Use Session State")
    st.write("""
    Use Session State when you need to:
    1. Persist data across reruns
    2. Share data between different parts of your app
    3. Implement more complex app logic and state management
    """)

    st.header("Advanced Example: To-Do List")
    st.code("""
import streamlit as st

if 'todos' not in st.session_state:
    st.session_state.todos = []

todo = st.text_input("Enter a to-do item")
if st.button("Add"):
    st.session_state.todos.append(todo)
    st.rerun()

st.write("To-Do List:")
for i, todo in enumerate(st.session_state.todos):
    st.write(f"{i+1}. {todo}")
    """)

    st.success("Try implementing this to-do list in your own Streamlit app!")
