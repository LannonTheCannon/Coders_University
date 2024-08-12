# intro_github_1.py
#
 
import streamlit as st

def intro_to_git():
    st.title("📘 Introduction to Git")
    st.write("Welcome to the exciting world of Git! Let's learn how to save and share our code like pro developers!")

    st.header("What is Git?")
    st.write("""
    Git is like a magical notebook for your code. It helps you:
    - 📝 Keep track of all changes you make
    - ⏰ Go back in time to older versions of your code
    - 👥 Work with friends on the same project without messing things up
    """)

    st.header("Why do we use Git?")
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        1. **Save our progress**: Like saving a game, Git lets us save our code at different points.
        2. **Experiment safely**: Try new ideas without fear of breaking your working code.
        3. **Collaborate**: Work on projects with classmates, just like real developers!
        4. **Back up our code**: Keep your hard work safe in the cloud.
        """)
    with col2:
        st.image("https://raw.githubusercontent.com/codeallthethingz/git-art/main/git-logo.png", width=200)

    st.header("Git Basics: The 3-Step Dance")
    st.write("Using Git is like a simple 3-step dance. Let's learn the moves!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. Stage 🎭")
        st.write("Tell Git which changes you want to save.")
        st.code("git add filename.py")
    with col2:
        st.subheader("2. Commit 💾")
        st.write("Save your changes with a short message.")
        st.code('git commit -m "Add cool new feature"')
    with col3:
        st.subheader("3. Push 🚀")
        st.write("Send your changes to GitHub for others to see.")
        st.code("git push")

    st.header("Let's Practice!")
    st.write("Try out these Git commands in your command prompt or terminal:")
    
    code = st.text_area("Type your Git commands here:", height=150)
    if st.button("Check My Commands"):
        check_git_commands(code)

    st.header("Git Vocabulary")
    st.write("Learn these words and impress your friends with your Git knowledge!")
    terms = {
        "Repository (Repo)": "The project's folder where Git keeps track of all your files.",
        "Branch": "A separate line of development, like a copy of your project where you can experiment.",
        "Merge": "Combining changes from different branches.",
        "Clone": "Making a copy of a repository on your computer.",
        "Pull": "Getting the latest changes from GitHub to your computer."
    }
    for term, definition in terms.items():
        with st.expander(term):
            st.write(definition)

    st.header("📚 Your First Git Project")
    st.write("""
    Let's create your first Git project! Follow these steps:
    1. Create a new folder on your computer for your project.
    2. Open your command prompt or terminal in that folder.
    3. Type `git init` to start using Git in your project.
    4. Create a new file called `README.md` and write a short description of your project.
    5. Use the 3-step dance to save your changes:
       - `git add README.md`
       - `git commit -m "Create README file"`
    6. Create a repository on GitHub and follow the instructions to push your local project.
    """)

    st.success("Congratulations! You've just created your first Git project. You're on your way to becoming a coding superhero! 🦸‍♂️🦸‍♀️")

    st.header("🎮 Git Adventure Game")
    st.write("Play this mini-game to test your Git knowledge!")
    play_git_game()

def check_git_commands(code):
    correct_commands = ["git add", "git commit", "git push"]
    user_commands = code.lower().split("\n")
    
    correct = all(any(cmd in user_cmd for user_cmd in user_commands) for cmd in correct_commands)
    
    if correct:
        st.success("Great job! You've mastered the 3-step Git dance! 🎉")
    else:
        st.error("Oops! Make sure you include all three steps: add, commit, and push. Try again!")

def play_git_game():
    st.subheader("🎮 Git Adventure: Save the Code Kingdom")
    st.write("Help Code Knight save the kingdom by answering Git questions!")
    
    questions = [
        {
            "question": "What Git command do you use to save your changes?",
            "options": ["git save", "git commit", "git store", "git keep"],
            "correct": "git commit"
        },
        {
            "question": "Which command sends your changes to GitHub?",
            "options": ["git send", "git upload", "git push", "git deliver"],
            "correct": "git push"
        },
        {
            "question": "What's a good commit message for adding a new login feature?",
            "options": ["'Did stuff'", "'asdfghjkl'", "'New feature'", "'Add user login functionality'"],
            "correct": "'Add user login functionality'"
        }
    ]
    
    score = 0
    for i, q in enumerate(questions):
        st.write(f"Question {i+1}: {q['question']}")
        answer = st.radio(f"Select your answer for Q{i+1}:", q['options'], key=f"q{i}")
        if answer == q['correct']:
            score += 1
    
    if st.button("Complete Quest"):
        if score == len(questions):
            st.balloons()
            st.success(f"Congratulations, Code Knight! You saved the Code Kingdom with a perfect score of {score}/{len(questions)}! 🏆")
        elif score >= len(questions) // 2:
            st.success(f"Well done, Code Knight! You saved the kingdom with a score of {score}/{len(questions)}. Keep practicing to achieve perfection! 🛡️")
        else:
            st.warning(f"Oh no! The Code Kingdom is in trouble. You scored {score}/{len(questions)}. Train harder and try again, brave Code Knight! 💪")
