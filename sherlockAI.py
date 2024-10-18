import streamlit as st
import openai
import time
import json
import os
import datetime
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Streamlit page config
st.set_page_config(page_title="Sherlock Holmes Chatbot", page_icon="🕵️", layout="wide")

# OpenAI and Google Calendar setup
ASSISTANT_ID = 'asst_OUgnR5TbpMHivgAvdaG28t3I'
THREAD_ID = 'thread_Pt1GEInDiECkbOIMMM6AJwBj'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Google Calendar Functions
def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                '.streamlit/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def get_calendar_events(service, days=7, max_results=10):
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + datetime.timedelta(days=days)).isoformat() + 'Z'
    
    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                          timeMax=time_max, maxResults=max_results, 
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    event_list = []
    for event in events:
        event_dict = {
            'summary': event['summary'],
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'location': event.get('location', 'No location specified'),
            'description': event.get('description', 'No description')
        }
        event_list.append(event_dict)
    
    return event_list

# Sherlock Holmes AI Function
def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Create a run with function calling
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_calendar_events",
                    "description": "Get the user's calendar events",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "days": {
                                "type": "integer",
                                "description": "Number of days to fetch events for"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of events to return"
                            }
                        },
                        "required": ["days", "max_results"]
                    }
                }
            }]
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            elif run_status.status == 'requires_action':
                # Handle function calling
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "get_calendar_events":
                        arguments = json.loads(tool_call.function.arguments)
                        events = get_calendar_events(st.session_state.service, 
                                                     days=arguments['days'], 
                                                     max_results=arguments['max_results'])
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread_id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(events)
                            }]
                        )
            time.sleep(1)

        # Retrieve the assistant's messages
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        
        # Return the latest assistant message
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm afraid an error has occurred in our communication, Watson. Let us try again."

# Main Streamlit App
st.title("🕵️ Sherlock Holmes AI with Calendar Integration")
st.markdown("*I am Sherlock Holmes, the world's only consulting detective. How may I assist you with your case or schedule?*")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'service' not in st.session_state:
    st.session_state.service = None

# Google Calendar Connection
if st.session_state.service is None:
    if st.sidebar.button('Connect to Google Calendar'):
        st.session_state.service = get_calendar_service()
        st.sidebar.success('Successfully connected to Google Calendar!')
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if st.session_state.service:
    prompt = st.chat_input("Describe your case or ask about your schedule, dear Watson...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_assistant_response(ASSISTANT_ID, THREAD_ID, prompt)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.warning("Please connect to Google Calendar first using the sidebar button.")

# Sidebar with interesting facts about Sherlock Holmes
st.sidebar.title("Did you know?")
st.sidebar.write("Sherlock Holmes never said 'Elementary, my dear Watson' in any of Sir Arthur Conan Doyle's stories.")
