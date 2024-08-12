# Basic Elements Page
# basic_elements_3.py
import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data():
    return pd.DataFrame({
        'Element': ['Text', 'Button', 'Slider', 'Input', 'Chart'],
        'Usage': [90, 75, 60, 85, 70]
    })


def basic_elements_page():
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
