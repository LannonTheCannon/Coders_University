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
from googleapiclient.errors import HttpError
import pytz
from dateutil import parser
# from notion_client import Client


# Streamlit page config
st.set_page_config(page_title="Sherlock Holmes Chatbot", page_icon="🕵️", layout="wide")

# OpenAI and Google Calendar setup
ASSISTANT_ID = 'asst_OUgnR5TbpMHivgAvdaG28t3I'
THREAD_ID = 'thread_a9hmNenXCeOMVGl9K0Cuk4lr'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#notion = Client(auth=st.secrets['NOTION_API_KEY'])

# Create function to interact with notion database
# def get_notion_data(database_id):
#     try:
#         response = notion.databases.query(database_id=database_id)
#         return response['results']
#     except Exception as e:
#         print(f'An error occured while fetching Notion data: {e}')
#         return None

# Get current event
def get_current_date_info():
    current_date = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
    return {
        'current_date': current_date.strftime('%Y-%m-%d'),
        'current_day':  current_date.strftime('%A'),
        'current_time': current_date.strftime('%H:%M:%S'),
        'datetime_obj': current_date
    }

# Google Calendar Functions
def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file('.secrets/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def get_calendar_events(service, days=7, max_results=10):
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + datetime.timedelta(days=days)).isoformat() + 'Z'

    print(f"Fetching events from {time_min} to {time_max}")

    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                          timeMax=time_max, maxResults=max_results, 
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_list = []
    for event in events:
        event_dict = {
            'id': event['id'],
            'summary': event['summary'],
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'location': event.get('location', 'No location specified'),
            'description': event.get('description', 'No description')
        }
        event_list.append(event_dict)
        print(f"Found event: {event_dict['summary']} (ID: {event_dict['id']})")

    return event_list

def create_calendar_event(service, summary, start_time, end_time, description='', location=''):
    current_date_info = get_current_date_info()
    current_date = current_date_info['datetime_obj'].date()

    start_dt = parser.parse(start_time)
    end_dt = parser.parse(end_time)

    if start_dt.year == 1900:
        start_dt = start_dt.replace(year=current_date.year, month=current_date.month, day=current_date.day)
    if end_dt.year == 1900:
        end_dt = end_dt.replace(year=current_date.year, month=current_date.month, day=current_date.day)

    if start_dt.date() < current_date:
        start_dt += datetime.timedelta(days=1)
    if end_dt.date() < current_date:
        end_dt += datetime.timedelta(days=1)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'America/Los_Angeles'
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('htmlLink')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def delete_calendar_event(service, event_id):
    try:
        print(f"Attempting to delete event with ID: {event_id}")
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Successfully deleted event with ID: {event_id}")
        return True
    except HttpError as error:
        if error.resp.status == 404:
            print(f"Event with ID {event_id} not found. It may have already been deleted.")
        else:
            print(f"An error occurred while deleting the event: {error}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while deleting the event: {e}")
        return False

# Sherlock Holmes AI Function
def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        date_info = get_current_date_info() 

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"Current date: {date_info['current_date']}, Day: {date_info['current_day']}, Time: {date_info['current_time']}\n\nUser message: {user_input}"
        )

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
                            "days": {"type": "integer", "description": "Number of days to fetch events for"},
                            "max_results": {"type": "integer", "description": "Maximum number of events to return"}
                        },
                        "required": ["days", "max_results"]
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'create_calendar_event',
                    'description': 'Create a new calendar event',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'summary': {'type': 'string', 'description': 'Title of the event'},
                            'start_time': {'type': 'string', 'description': 'Start time of the event'},
                            'end_time': {'type': 'string', 'description': 'End time of the event'},
                            'description': {'type': 'string', 'description': 'Description of the event'},
                            'location': {'type': 'string', 'description': 'Location of the event'}
                        },
                        'required': ['summary', 'start_time', 'end_time']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'delete_calendar_event',
                    'description': 'Delete a calendar event',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'event_id': {'type': 'string', 'description': 'ID of the event to delete'}
                        },
                        'required': ['event_id']
                    }
                }
            }]
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            elif run_status.status == 'requires_action':
                tool_outputs = []
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "get_calendar_events":
                        arguments = json.loads(tool_call.function.arguments)
                        events = get_calendar_events(st.session_state.service, 
                                                     days=arguments['days'], 
                                                     max_results=arguments['max_results'])
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(events)
                        })
                    elif tool_call.function.name == 'create_calendar_event':
                        arguments = json.loads(tool_call.function.arguments)
                        event_link = create_calendar_event(
                            st.session_state.service,
                            summary=arguments['summary'],
                            start_time=arguments['start_time'],
                            end_time=arguments['end_time'],
                            description=arguments.get('description', ''),
                            location=arguments.get('location', '')
                        )
                        tool_outputs.append({
                            'tool_call_id': tool_call.id,
                            'output': json.dumps({'event_link': event_link})
                        })
                    elif tool_call.function.name == 'delete_calendar_event':
                        arguments = json.loads(tool_call.function.arguments)
                        event_id = arguments['event_id']
                        print(f"Assistant is attempting to delete event with ID: {event_id}")
                        success = delete_calendar_event(
                            st.session_state.service,
                            event_id=event_id
                        )
                        tool_outputs.append({
                            'tool_call_id': tool_call.id,
                            'output': json.dumps({'success': success})
                        })
                        print(f"Delete operation for event {event_id} {'succeeded' if success else 'failed'}")
                
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm afraid an error has occurred in our communication, Watson. Let us try again."

# Main Streamlit App
st.title("🕵️ Sherlock Holmes AI with Calendar Integration")
st.markdown("*I am Sherlock Holmes, the world's only consulting detective. How may I assist you with your case or schedule?*")

# Display current date
current_date_info = get_current_date_info()
st.sidebar.write(f"Current Date: {current_date_info['current_date']}")
st.sidebar.write(f"Day: {current_date_info['current_day']}")
st.sidebar.write(f"Time: {current_date_info['current_time']}")

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
