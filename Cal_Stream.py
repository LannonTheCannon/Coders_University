import streamlit as st
import os
import datetime
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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

def get_events(service, days=7, max_results=10):
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + datetime.timedelta(days=days)).isoformat() + 'Z'
    
    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                          timeMax=time_max, maxResults=max_results, 
                                          singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])

def main():
    st.title('📅 My Google Calendar App')

    # Initialize session state
    if 'service' not in st.session_state:
        st.session_state.service = None

    if st.session_state.service is None:
        if st.button('Connect to Google Calendar'):
            st.session_state.service = get_calendar_service()
            st.success('Successfully connected to Google Calendar!')
            st.rerun()

    if st.session_state.service:
        days = st.slider('Number of days to fetch', 1, 30, 7)
        max_results = st.slider('Maximum number of events', 1, 50, 10)

        if st.button('Fetch Events'):
            events = get_events(st.session_state.service, days, max_results)

            if not events:
                st.write('No upcoming events found.')
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    
                    with st.expander(f"{start} - {event['summary']}"):
                        st.write(f"Start: {start}")
                        st.write(f"End: {end}")
                        st.write(f"Location: {event.get('location', 'No location specified')}")
                        st.write(f"Description: {event.get('description', 'No description')}")

if __name__ == '__main__':
    main()
