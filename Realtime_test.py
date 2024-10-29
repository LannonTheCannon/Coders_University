import openai
import streamlit as st
import json
import time

# Streamlit page config
st.set_page_config(page_title="Weather Assistant", page_icon="🌤️", layout="wide")

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"], default_headers={"OpenAI-Beta": "assistants=v2"})

# Constants
ASSISTANT_ID = None  # You'll get this after creating the assistant
THREAD_ID = None  # You'll get this after creating the thread

def get_current_temperature(location: str, unit: str) -> str:
    """Mock temperature function"""
    return f"75°{unit[0]}"

def get_rain_probability(location: str) -> str:
    """Mock rain probability function"""
    return "30%"


def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Create a run with the tools
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_current_temperature",
                    "description": "Get the current temperature for a specific location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g., San Francisco, CA"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["Celsius", "Fahrenheit"],
                                "description": "The temperature unit to use"
                            }
                        },
                        "required": ["location", "unit"]
                    }
                }
            },
                {
                    "type": "function",
                    "function": {
                        "name": "get_rain_probability",
                        "description": "Get the probability of rain for a specific location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g., San Francisco, CA"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                }]
        )

        # Poll for the run to complete
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
                    if tool_call.function.name == "get_current_temperature":
                        arguments = json.loads(tool_call.function.arguments)
                        temperature = get_current_temperature(
                            location=arguments['location'],
                            unit=arguments['unit']
                        )
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps({"temperature": temperature})
                        })
                    elif tool_call.function.name == "get_rain_probability":
                        arguments = json.loads(tool_call.function.arguments)
                        probability = get_rain_probability(
                            location=arguments['location']
                        )
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps({"probability": probability})
                        })

                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            time.sleep(1)

        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I apologize, but I encountered an error. Please try again."


# Main Streamlit App
st.title("🌤️ Weather Assistant")
st.markdown("*Ask me about the weather in any location!*")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the assistant and thread if not already done
if "assistant_id" not in st.session_state:
    # Create the assistant
    assistant = client.beta.assistants.create(
        instructions="You are a helpful weather assistant. Use the provided functions to get weather information and explain it in a friendly way.",
        model="gpt-4",
        tools=[{
            "type": "function",
            "function": {
                "name": "get_current_temperature",
                "description": "Get the current temperature for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["Celsius", "Fahrenheit"],
                            "description": "The temperature unit to use"
                        }
                    },
                    "required": ["location", "unit"]
                }
            }
        },
            {
                "type": "function",
                "function": {
                    "name": "get_rain_probability",
                    "description": "Get the probability of rain for a specific location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g., San Francisco, CA"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }]
    )
    st.session_state.assistant_id = assistant.id

if "thread_id" not in st.session_state:
    # Create the thread
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

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
            st.session_state.assistant_id,
            st.session_state.thread_id,
            prompt
        )
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})