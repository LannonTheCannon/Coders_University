import streamlit as st
import openai
import io
import json
from pydub import AudioSegment
import base64
import asyncio
import websockets

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def audio_to_item_create_event(audio_bytes: bytes) -> str:
    # Load the audio file from the byte stream
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # Resample to 24kHz mono pcm16
    pcm_audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2).raw_data

    # Encode to base64 string
    pcm_base64 = base64.b64encode(pcm_audio).decode()

    event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [{
                "type": "input_audio",
                "audio": pcm_base64
            }]
        }
    }
    return json.dumps(event)

async def connect_to_realtime_api(event_json):
    # Replace with the actual Realtime API WebSocket endpoint
    websocket_url = "wss://api.openai.com/v1/realtime/conversations"

    headers = {
        'Authorization': f"Bearer {openai.api_key}",
        'Content-Type': 'application/json'
    }

    async with websockets.connect(websocket_url, extra_headers=headers) as websocket:
        # Send the event to the Realtime API
        await websocket.send(event_json)

        # Receive and display responses
        while True:
            response = await websocket.recv()
            response_data = json.loads(response)
            yield response_data

def main():
    st.title("OpenAI Realtime API with Streamlit")

    # Allow the user to upload an audio file
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a", "ogg"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        audio_bytes = uploaded_file.read()

        # Generate the event JSON
        event_json = audio_to_item_create_event(audio_bytes)

        st.write("Event JSON:")
        st.json(json.loads(event_json))

        # Display a placeholder for the streaming responses
        response_placeholder = st.empty()

        # Define an asynchronous function to handle the WebSocket connection
        async def run_realtime_api():
            responses = connect_to_realtime_api(event_json)
            async for response_data in responses:
                # Update the placeholder with new responses
                response_placeholder.write(response_data)

        # Run the asynchronous function
        asyncio.run(run_realtime_api())

if __name__ == "__main__":
    main()
