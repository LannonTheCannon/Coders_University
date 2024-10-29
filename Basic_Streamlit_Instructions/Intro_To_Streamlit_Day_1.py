#Intro to streamlit day 1
import streamlit as st
from src.landing_1 import introduction
from src.setup_2 import setup
from src.basic_3 import basicStreamlitElements
from src.interative_4 import interativeApp
from src.run_5 import runApp
from src.capturing_6 import capturingVariables
from src.hands_7 import handsOnActivity
from src.wrap_8 import wrapUp
from src.todo_9 import toDoList
from src.quiz_10 import quiz
def main():
    st.title("Intro to streamlit :dark_sunglasses:")


    #add a sidebar
    st.sidebar.title("Lesson section")
    sections = [
        ":one: Introduction",
        ":two: Setup",
        ":three: Basic Streamlit Elements",
        ":four: Simple Interative App",
        ":five: Running the App",
        ":six: Capturing Variables",
        ":seven: Hands on Activity",
        ":eight: :red[Wrap up]" ,
        ":nine: ToDo List",
        ":one::zero: Quiz",
        

    ]

    selected_section = st.sidebar.radio("Go to", sections)
    #main content
    if selected_section == ":one: Introduction":
        introduction()
    elif selected_section == ":two: Setup":
        setup()
    elif selected_section == ":three: Basic Streamlit Elements":
        basicStreamlitElements()
    elif selected_section == ":four: Simple Interative App":
        interativeApp()
    elif selected_section == ":five: Running the App":
        runApp()
    elif selected_section == ":six: Capturing Variables":
        capturingVariables()

    elif selected_section == ":seven: Hands on Activity":
        handsOnActivity() 
    elif selected_section == ":eight: :red[Wrap up]":
        wrapUp()
    elif selected_section == ":nine: ToDo List":
        toDoList()
    elif selected_section == ":one::zero: Quiz":
        quiz()
        st.divider()









if __name__ == "__main__":
    main()

