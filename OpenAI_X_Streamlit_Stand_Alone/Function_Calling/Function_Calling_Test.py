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
    return f'75°{unit[0]}'


def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Create message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=user_input
        )

        # Check for active runs
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        active_run = next((run for run in runs.data if run.status == "in_progress"), None)

        if active_run:
            while active_run.status == "in_progress":
                time.sleep(1)
                active_run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=active_run.id
                )

        # Create new run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            tools=[{
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
            }]
        )

        # Wait for run completion
        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            if run.status == 'completed':
                break
            elif run.status == 'requires_action':
                tool_outputs = []
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
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
                    tool_outputs=tool_outputs
                )

            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        st.error(f'Error getting assistant response: {str(e)}')
        return 'I apologize, but I encountered an error. Please try again!'


def main():
    st.title("🌤️ Weather Assistant")
    st.markdown("*Ask me about the weather in any location!*")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the weather..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner('Getting response...'):  # Added spinner
                full_response = get_assistant_response(
                    ASSISTANT_ID,
                    THREAD_ID,
                    prompt
                )
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == '__main__':
    main()