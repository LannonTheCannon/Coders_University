import streamlit as st 

def setup_page():
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
