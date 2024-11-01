import openai
import streamlit as st
import json
import time

# Page configuration and sidebar setup
st.set_page_config(page_title="OpenAI Assistant Tutorial", layout="wide")

# Sidebar navigation
st.sidebar.title("Tutorial Sections")
section = st.sidebar.radio(
    "Choose a section",
    ["1. Setup & Introduction",
     "2. Creating the Assistant",
     "3. Function Definitions",
     "4. Assistant Response Handler",
     "5. Chat Interface",
     "6. Complete Implementation"]
)

# Initialize OpenAI client (shown in all sections)
api_key = st.secrets['OPENAI_API_KEY']
client = openai.OpenAI(api_key=api_key)

ASSISTANT_ID = 'your_assistant_id'
THREAD_ID = 'your_thread_id'

def weather_function():
    return """
    {
        'type': 'function',
        'function': {
            'name': 'get_current_temperature',
            'description': 'Get the current temperature for a specific location.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': 'The city and state, e.g., San Francisco, CA'
                    },
                    'unit': {
                        'type': 'string',
                        'enum': ['Celsius', 'Fahrenheit'],
                        'description': 'The temperature unit to use'
                    }
                },
                'required': ['location', 'unit']
            }
        }
    }
    """


if section == "1. Setup & Introduction":
    st.title("1. Setup & Introduction")
    st.markdown("""
    ### Setting up OpenAI Assistant with Functions

    In this tutorial, we'll build a weather assistant using OpenAI's Assistant API with function calling.

    #### Prerequisites:
    1. OpenAI API key (stored in Streamlit secrets)
    2. Required packages:
        ```python
        pip install openai streamlit
        ```

    #### Initial Setup:
    ```python
    import openai
    import streamlit as st
    import json
    import time

    api_key = st.secrets['OPENAI_API_KEY']
    client = openai.OpenAI(api_key=api_key)

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    ```
    """)

elif section == "2. Creating the Assistant":
    st.title("2. Creating the Assistant")
    st.markdown("""
    ### Creating the Assistant in OpenAI Playground

    1. Go to OpenAI platform (platform.openai.com)
    2. Navigate to "Assistants" in the left sidebar
    3. Click "Create" and configure your assistant:

    #### Assistant Configuration:
    - Name: Weather Assistant
    - Model: GPT-4
    - Instructions: "You are a helpful weather assistant..."

    #### Adding the Function:
    In the "Tools" section, add this function definition:
    """)

    st.code(weather_function(), language="python")

    st.markdown("""
    Save the assistant and note the Assistant ID and Thread ID for use in your code:
    ```python
    ASSISTANT_ID = 'asst_xxx...'
    THREAD_ID = 'thread_xxx...'
    ```
    """)

elif section == "3. Function Definitions":
    st.title("3. Function Definitions")
    st.markdown("""
    ### Implementing the Weather Function

    Define the function that will handle temperature requests:
    """)

    st.code("""
    def get_current_temperature(location: str, unit: str) -> str:
        return f'75°{unit[0]}'  # Mock implementation
    """, language="python")

    st.markdown("""
    This is a mock implementation. In a real application, you would:
    1. Connect to a weather API
    2. Fetch real-time data
    3. Handle errors and edge cases
    4. Format the response appropriately
    """)

elif section == "4. Assistant Response Handler":
    st.title("4. Assistant Response Handler")
    st.markdown("""
    ### Creating the Assistant Response Handler

    This function manages the interaction with the OpenAI API:
    1. Sends user messages
    2. Creates runs
    3. Handles function calls
    4. Returns responses
    """)

    st.code("""
    def get_assistant_response(assistant_id, thread_id, user_input):
        try:
            # Create message in thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role='user',
                content=user_input
            )

            # Create run with tools
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                tools=[...])  # Function definition here

            # Poll for completion and handle function calls
            while True:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )

                if run_status.status == 'completed':
                    break
                elif run_status.status == 'requires_action':
                    # Handle function calls
                    tool_outputs = []
                    # Process tool calls...

            # Return final response
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            return messages.data[0].content[0].text.value

        except Exception as e:
            return f'Error: {str(e)}'
    """, language="python")

elif section == "5. Chat Interface":
    st.title("5. Chat Interface")
    st.markdown("""
    ### Building the Streamlit Chat Interface

    The main function creates the chat interface:
    """)

    st.code("""
    def main():
        st.title("🌤️ Weather Assistant")
        st.markdown("*Ask me about the weather in any location!*")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about the weather..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = get_assistant_response(
                    ASSISTANT_ID,
                    THREAD_ID,
                    prompt
                )
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    """, language="python")

else:  # Complete Implementation
    st.title("6. Complete Implementation")
    st.markdown("### The Complete Weather Assistant Implementation")

    with st.expander("View Full Code"):
        st.code("""
import openai
import streamlit as st
import json
import time

api_key = st.secrets['OPENAI_API_KEY']
client = openai.OpenAI(api_key=api_key)

if 'messages' not in st.session_state:
    st.session_state.messages = []

ASSISTANT_ID = 'asst_OUgnR5TbpMHivgAvdaG28t3I'
THREAD_ID = 'thread_HsRMBEiRx5uOBn0x5IcZnsEt'

def get_current_temperature(location: str, unit: str) -> str:
    return f'75°{unit[0]}'  # Changed * to ° for better formatting

def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            tools=[
                {
                    'type': 'function',
                    'function': {
                        'name': 'get_current_temperature',
                        'description': 'Get the current temperature for a specific location.',
                        'parameters': {
                            'type': 'object',  # Added required type field
                            'properties': {
                                'location': {
                                    'type': 'string',
                                    'description': 'The city and state, e.g., San Francisco, CA'
                                },
                                'unit': {
                                    'type': 'string',
                                    'enum': ['Celsius', 'Fahrenheit'],  # Fixed spelling
                                    'description': 'The temperature unit to use'
                                }
                            },
                            'required': ['location', 'unit']
                        }
                    }
                }
            ]
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            if run_status.status == 'completed':
                break
            elif run_status.status == 'requires_action':
                tool_outputs = []
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == 'get_current_temperature':
                        arguments = json.loads(tool_call.function.arguments)
                        temperature = get_current_temperature(
                            location=arguments['location'],
                            unit=arguments['unit']
                        )

                        tool_outputs.append({
                            'tool_call_id': tool_call.id,
                            'output': json.dumps({'temperature': temperature})
                        })

                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs  # Fixed parameter name
                )
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        st.error(f'Error getting assistant response: {str(e)}')
        return 'I apologize, but I encountered an error. Please try again!'

def main():
    # Add title and description
    st.title("🌤️ Weather Assistant")
    st.markdown("*Ask me about the weather in any location!*")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about the weather..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_assistant_response(
                ASSISTANT_ID,
                THREAD_ID,
                prompt
            )
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == '__main__':
    main()
""" + st.session_state.get('full_code', ''), language="python")

    st.markdown("""
    ### Key Points to Remember:
    1. Always store API keys securely in `.streamlit/secrets.toml`
    2. Update the Assistant in the OpenAI playground first
    3. Test function calls with simple implementations before adding complexity
    4. Handle errors appropriately
    5. Consider rate limits and API costs

    ### Running the Application:
    ```bash
    streamlit run weather_app.py
    ```
    """)

    if st.button("Try the Weather Assistant"):
        st.markdown("---")
        # Initialize session state for messages if needed
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Rest of your main() function implementation...
        st.markdown('''<iframe src='https://func-call.streamlit.app/?embed=True' width='800' height='600'></iframe>''',
                    unsafe_allow_html=True)