# css_wrapping_9.py

import streamlit as st

def css_wrapping_page():
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


