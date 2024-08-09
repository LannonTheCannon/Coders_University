#running_app_4.py
import streamlit as st

def interactive_app_page():
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
