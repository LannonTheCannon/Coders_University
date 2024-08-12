# hands_on_act_7

import streamlit as st 

def hands_on_activity_page():
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
