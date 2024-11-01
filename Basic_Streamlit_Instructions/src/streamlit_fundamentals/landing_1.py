import streamlit as st

def landing_page():
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
