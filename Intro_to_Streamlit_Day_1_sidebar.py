import streamlit as st

def main():
    st.title("Introduction to Streamlit")
    st.subheader("A lesson plan for 6th-9th grade Python coders")

    # Add a sidebar
    st.sidebar.title("Lesson Sections")
    sections = [
        "1. Introduction",
        "2. Setup",
        "3. Basic Streamlit Elements",
        "4. Simple Interactive App",
        "5. Running the App",
        "6. Hands-on Activity",
        "7. Wrap-up"
    ]
    selected_section = st.sidebar.radio("Go to", sections)

    # Main content
    if selected_section == "1. Introduction":
        introduction()
    elif selected_section == "2. Setup":
        setup()
    elif selected_section == "3. Basic Streamlit Elements":
        basic_elements()
    elif selected_section == "4. Simple Interactive App":
        interactive_app()
    elif selected_section == "5. Running the App":
        running_app()
    elif selected_section == "6. Hands-on Activity":
        hands_on_activity()
    elif selected_section == "7. Wrap-up":
        wrap_up()

def introduction():
    st.header("1. Introduction")
    st.write("Streamlit is a Python library that makes it easy to create web apps.")
    if st.button("Show Example App"):
        st.code("""
import streamlit as st
st.title("Hello, Streamlit!")
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")
        """)

def setup():
    st.header("2. Setup")
    st.write("To install Streamlit, run this command in your terminal or command prompt:")
    st.code("pip install streamlit")
    st.write("Then create a new Python file for your project.")

def basic_elements():
    st.header("3. Basic Streamlit Elements")
    st.write("Let's explore some basic Streamlit elements:")
    st.subheader("3.1 Text Elements")
    st.write("Here are examples of text elements:")
    st.code("""
st.title("This is a title")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is plain text")
st.write("This is a versatile write method")
    """)
    st.subheader("3.2 Input Elements")
    st.write("Streamlit provides various input elements:")
    name = st.text_input("Enter your name")
    age = st.slider("Select your age", 10, 15)
    st.write(f"Hello, {name}! You are {age} years old.")
    st.subheader("3.3 Display Image")
    st.write("You can display images like this:")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

def interactive_app():
    st.header("4. Simple Interactive App")
    st.write("Let's create a basic calculator:")
    num1 = st.number_input("Enter first number", value=0)
    num2 = st.number_input("Enter second number", value=0)
    operation = st.selectbox("Choose operation", ["+", "-", "*", "/"])
    if st.button("Calculate"):
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        else:
            result = num1 / num2 if num2 != 0 else "Error: Division by zero"
        st.success(f"Result: {result}")

def running_app():
    st.header("5. Running the App")
    st.write("To run your Streamlit app:")
    st.code("streamlit run your_app_name.py")
    st.write("Make sure you're in the correct directory in your terminal or command prompt.")

def hands_on_activity():
    st.header("6. Hands-on Activity")
    st.write("Now it's your turn! Try creating a simple Streamlit app.")
    st.write("Here's a template to get you started:")
    st.code("""
import streamlit as st
st.title("My First Streamlit App")
# Add your code here
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")
# Try adding more elements!
    """)

def wrap_up():
    st.header("7. Wrap-up")
    st.write("Great job! You've learned the basics of Streamlit.")
    st.write("Remember, you can create amazing web apps with just a few lines of Python code.")
    st.write("Keep exploring and have fun coding!")

if __name__ == "__main__":
    main()
