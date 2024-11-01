# wrap_up_8.py
import streamlit as st
import time

def wrap_up_page():
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
