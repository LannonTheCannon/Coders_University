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