import streamlit as st
import pandas as pd
import altair as alt
import time

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


@st.cache_data
def load_data():
    return pd.DataFrame({
        'Element': ['Text', 'Button', 'Slider', 'Input', 'Chart'],
        'Usage': [90, 75, 60, 85, 70]
    })


def main():
    st.sidebar.title("🚀 Streamlit Masterclass")
    sections = [
        ':coffee: Home',
        "🛠 Setup",
        "🧱 Basic Elements",
        "🔢 Interactive App",
        "▶️ Running the App",
        "🔑 Session State",
        "🖐️ Hands-on Activity",
        "🎓 Wrap-up",
        "🎨 CSS Wrapping",
        '🧠 Quizzes'
    ]
    selected_section = st.sidebar.radio("Navigation", sections)
    st.sidebar.divider()

    if selected_section == ':coffee: Home':
        home()
    elif selected_section == "🛠 Setup":
        setup()
    elif selected_section == "🧱 Basic Elements":
        basic_elements()
    elif selected_section == "🔢 Interactive App":
        interactive_app()
    elif selected_section == "▶️ Running the App":
        running_app()
    elif selected_section == '🔑 Session State':
        sess_state()
    elif selected_section == "🖐️ Hands-on Activity":
        hands_on_activity()
    elif selected_section == "🎓 Wrap-up":
        wrap_up()
    elif selected_section == "🎨 CSS Wrapping":  # New condition
        css_wrapping()
    elif selected_section == "🧠 Quizzes":
        display_quiz()


def home():
    st.title("Welcome to Streamlit Masterclass! 🎉")
    st.subheader("Empowering 6th-9th grade Python coders")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        Streamlit is an amazing Python library that lets you create stunning web apps with ease. 
        In this masterclass, you'll learn:
        - 🔧 How to set up Streamlit
        - 🧱 Basic Streamlit elements
        - 🔢 Building interactive apps
        - 🚀 Running your Streamlit creations
        """)

    with col2:
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

    st.info("Ready to begin your Streamlit journey? Navigate through the lessons using the sidebar! 👈")


def setup():
    st.title("🛠️ Setting Up Streamlit")
    st.write("Let's get your development environment ready!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Step 1: Install Streamlit")
        st.code("pip install streamlit")

    with col2:
        st.subheader("Step 2: Verify Installation")
        st.code("streamlit hello")

    st.subheader("Step 3: Create Your First App")
    st.code("""
    # Save this as 'hello_streamlit.py'
    import streamlit as st
    st.title("Hello, Streamlit!")
    st.write("Welcome to your first Streamlit app!")
    """)

    st.success("You're all set! Let's dive into the exciting world of Streamlit! 🎈")


def basic_elements():
    st.title("🧱 Basic Streamlit Elements")
    st.write("Explore the building blocks of Streamlit apps!")

    tab1, tab2, tab3 = st.tabs(["Text Elements", "Input Elements", "Display Elements"])

    with tab1:
        st.subheader("Text Elements")
        st.title("This is a title")
        st.header("This is a header")
        st.subheader("This is a subheader")
        st.text("This is plain text")
        st.markdown("This is **bold** and *italic* text")
        st.latex(r"e^{i\pi} + 1 = 0")

    with tab2:
        st.subheader("Input Elements")
        name = st.text_input("What's your name?")
        age = st.slider("How old are you?", 10, 15)
        st.write(f"Hello, {name}! You are {age} years old.")

    with tab3:
        st.subheader("Display Elements")
        st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=200)

        data = load_data()
        chart = alt.Chart(data).mark_bar().encode(
            x='Element',
            y='Usage',
            color=alt.value("#4e54c8")
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)


def interactive_app():
    st.title("🔢 Interactive Streamlit App")
    st.write("Let's build a fun calculator!")

    col1, col2 = st.columns(2)

    with col1:
        num1 = st.number_input("Enter first number", value=0.0, step=0.1)
        num2 = st.number_input("Enter second number", value=0.0, step=0.1)
        operation = st.selectbox("Choose operation", ["+", "-", "*", "/"])

    with col2:
        st.write("Result:")
        if st.button("Calculate", key="calc"):
            with st.spinner("Calculating..."):
                time.sleep(1)  # Simulating calculation time
                if operation == "+":
                    result = num1 + num2
                elif operation == "-":
                    result = num1 - num2
                elif operation == "*":
                    result = num1 * num2
                else:
                    result = num1 / num2 if num2 != 0 else "Error: Division by zero"
                st.success(f"Result: {result}")
                st.balloons()


def running_app():
    st.title("▶️ Running Your Streamlit App")
    st.write("Time to see your creation come to life!")

    st.code("streamlit run your_app_name.py")

    st.info("Make sure you're in the correct directory in your terminal or command prompt.")

    with st.expander("Pro Tips"):
        st.markdown("""
        - Use `streamlit run --server.port 8080 your_app.py` to specify a port
        - Enable auto-reloading with `streamlit run --server.runOnSave true your_app.py`
        - For more options, try `streamlit run --help`
        """)


def sess_state():
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


def hands_on_activity():
    st.title("🖐️ Hands-on Activity")
    st.write("Now it's your turn to create something awesome!")

    st.code("""
import streamlit as st
import random

st.title("Guess the Number Game")

# Generate a random number between 1 and 100
secret_number = random.randint(1, 100)

# Get the player's guess
guess = st.number_input("Guess a number between 1 and 100", min_value=1, max_value=100)

if st.button("Check my guess"):
    if guess == secret_number:
        st.success("Congratulations! You guessed it right!")
        st.balloons()
    elif guess < secret_number:
        st.warning("Try a higher number!")
    else:
        st.warning("Try a lower number!")
    """)

    st.success("Challenge: Can you add a feature to count the number of guesses?")


def wrap_up():
    st.title("🎓 Wrap-up")
    st.write("Congratulations on completing the Streamlit Masterclass!")

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    st.success("You've learned the basics of Streamlit and are now ready to create amazing web apps!")
    st.balloons()

    st.markdown("""
    Remember:
    - Streamlit turns data scripts into shareable web apps in minutes
    - All it takes is a few lines of Python code
    - The possibilities are endless!

    Keep exploring, keep coding, and most importantly, have fun! 🚀
    """)


def css_wrapping():
    st.title("🎨 Customizing Your Streamlit App with CSS Wrapping")
    st.write("Learn how to use CSS to make your Streamlit app look amazing!")

    st.header("1. Introduction")
    st.write("CSS is like the paint and decorations for your web page.")
    st.info("We'll see how CSS can transform the look of your Streamlit app.")

    st.header("2. Basic CSS in Streamlit")
    st.code("""
st.markdown('''
<style>
/* CSS goes here */
</style>
''', unsafe_allow_html=True)
    """)
    st.write("We use `unsafe_allow_html=True` to tell Streamlit it's okay to use our custom HTML and CSS.")

    st.header("3. Changing Text Color and Size")
    st.code("""
st.markdown('''
<style>
.big-red-text {
    color: red;
    font-size: 24px;
}
</style>
''', unsafe_allow_html=True)

st.markdown('<p class="big-red-text">This is big red text!</p>', unsafe_allow_html=True)
    """)
    st.markdown('<p style="color: red; font-size: 24px;">This is big red text!</p>', unsafe_allow_html=True)

    st.header("4. Styling Buttons")
    st.code("""
st.markdown('''
<style>
.stButton>button {
    color: white;
    background-color: purple;
    border-radius: 10px;
}
</style>
''', unsafe_allow_html=True)

st.button("Click me!")
    """)
    st.markdown('''
    <style>
    .stButton>button {
        color: white;
        background-color: purple;
        border-radius: 10px;
    }
    </style>
    ''', unsafe_allow_html=True)
    st.button("Click me!")

    st.header("5. Changing Background Color")
    st.code("""
st.markdown('''
<style>
.stApp {
    background-color: lightblue;
}
</style>
''', unsafe_allow_html=True)
    """)
    st.write("Note: This will change the background of the entire app.")

    st.header("6. Mini-Project: Theme Your App")
    st.write("Try creating a simple theme for your app using what you've learned.")
    st.write("Customize at least:")
    st.write("1. A title")
    st.write("2. A button")
    st.write("3. The background color")

    st.header("7. Wrap-up")
    st.write("Remember:")
    st.write("• CSS is about experimenting and having fun with design.")
    st.write("• Always consider readability when choosing colors.")
    st.write("• Keep practicing to create even more amazing Streamlit apps!")


def display_quiz():
    import random

    st.title("🧠 Streamlit Quizzes")

    # Create tabs for different quizzes
    tab1, tab2 = st.tabs(["Session State Quiz", "Streamlit Basics Quiz"])

    with tab1:
        display_session_quiz()

    with tab2:
        streamlit_basics_quiz()


def display_session_quiz():
    import random

    # Set page config
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

    st.header("Streamlit Session State Quiz")

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

    # Explanation of session_state usage in this app
    st.sidebar.title("How session_state is used here")
    st.sidebar.write("""
    This quiz app demonstrates the use of session_state in several ways:

    1. Tracking the current question (st.session_state.current_question)
    2. Keeping score (st.session_state.score)
    3. Maintaining quiz state (st.session_state.quiz_complete)

    These variables persist across reruns, allowing the quiz to maintain its state even when the user interacts with it.
    """)


def streamlit_basics_quiz():
    st.header("Streamlit Basics Quiz")

    # Initialize session state variables for the second quiz
    if 'sb_current_question' not in st.session_state:
        st.session_state.sb_current_question = 0
    if 'sb_score' not in st.session_state:
        st.session_state.sb_score = 0
    if 'sb_quiz_complete' not in st.session_state:
        st.session_state.sb_quiz_complete = False

    # Quiz questions for Streamlit Basics
    quiz_data = [
        {
            "question": "What function is used to display text in Streamlit?",
            "options": ["st.text()", "st.write()", "st.display()", "st.show()"],
            "correct_answer": 1
        },
        {
            "question": "How do you create a button in Streamlit?",
            "options": ["st.button()", "st.create_button()", "st.input_button()", "st.add_button()"],
            "correct_answer": 0
        },
        {
            "question": "Which function is used to display a DataFrame in Streamlit?",
            "options": ["st.table()", "st.dataframe()", "st.show_data()", "st.display_df()"],
            "correct_answer": 1
        },
        # Add more questions as needed
    ]

    # Quiz logic (similar to session_state_quiz, but with different variable names)
    if not st.session_state.sb_quiz_complete:
        question = quiz_data[st.session_state.sb_current_question]
        st.write(f"Question {st.session_state.sb_current_question + 1} of {len(quiz_data)}")
        st.write(question["question"])

        answer = st.radio("Choose your answer:", question["options"], key=f"sb_q{st.session_state.sb_current_question}")

        if st.button("Submit Answer", key="sb_submit"):
            if question["options"].index(answer) == question["correct_answer"]:
                st.session_state.sb_score += 1
                st.success("Correct!")
            else:
                st.error(f"Wrong. The correct answer was: {question['options'][question['correct_answer']]}")

            if st.session_state.sb_current_question < len(quiz_data) - 1:
                st.session_state.sb_current_question += 1
            else:
                st.session_state.sb_quiz_complete = True
            st.rerun()

    else:
        st.write("Quiz completed!")
        st.write(f"Your final score: {st.session_state.sb_score} out of {len(quiz_data)}")

        if st.button("Restart Quiz", key="sb_restart"):
            st.session_state.sb_current_question = 0
            st.session_state.sb_score = 0
            st.session_state.sb_quiz_complete = False
            st.rerun()


if __name__ == "__main__":
    main()
