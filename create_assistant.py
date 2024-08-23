import streamlit as st
import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_assistant():
    try:
        assistant = client.beta.assistants.create(
            name="AI Chatbot",
            instructions="You are Kaiba from YU GI OH! Your job is to sound just like him",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo-preview"
        )
        return assistant
    except Exception as e:
        st.error(f"Error creating assistant: {str(e)}")
        return None

def create_thread():
    try:
        thread = client.beta.threads.create()
        return thread
    except Exception as e:
        st.error(f"Error creating thread: {str(e)}")
        return None

if __name__ == '__main__': 
    assistant = create_assistant()
    thread = create_thread()

    if assistant:
        print(f'Assistant ID {assistant.id}')
    else:
        print('Failed to create an assistant')

    if thread:
        print(f'Thread created with id {thread.id}')
    else:
        print('Failed to create a thread')


