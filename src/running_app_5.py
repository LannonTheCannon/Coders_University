# running_app_5.py
import streamlit as st

def running_app_page():
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
