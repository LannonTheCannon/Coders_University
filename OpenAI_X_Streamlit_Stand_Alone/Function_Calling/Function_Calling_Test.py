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