import streamlit as st
import sounddevice as sd
import numpy as np
import openai
import websockets
import json
import base64
import asyncio
from scipy import signal
from pydub import AudioSegment
import io

# Initialize OpenAI client
api_key = st.secrets['OPENAI_API_KEY']

# Audio recording parameters
SAMPLE_RATE = 24000
CHANNELS = 1
DTYPE = np.int16

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.audio_data = []

    def callback(self, indata, frames, time, status):
        if status:
            print("Status:", status)
        if self.recording:
            self.audio_data.append(indata.copy())

    def start_recording(self):
        self.recording = True
        self.audio_data = []
        try:
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype=DTYPE,
                callback=self.callback
            )
            self.stream.start()
            print("Recording started successfully")
        except Exception as e:
            print(f"Error starting recording: {str(e)}")

    def stop_recording(self):
        self.recording = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        if len(self.audio_data) > 0:
            try:
                audio = np.concatenate(self.audio_data, axis=0)
                return audio
            except Exception as e:
                print(f"Error processing audio: {str(e)}")
        return None

def process_audio(audio_data):
    """Convert audio data to 24kHz mono PCM16 little-endian"""
    try:
        audio_data = audio_data.flatten()
        audio_data = audio_data.astype(np.float32) / 32768.0

        if SAMPLE_RATE != 24000:
            samples = len(audio_data)
            new_samples = int(samples * 24000 / SAMPLE_RATE)
            audio_data = signal.resample(audio_data, new_samples)

        audio_data = (audio_data * 32767).astype(np.int16)

        if audio_data.dtype.byteorder == '>':
            audio_data = audio_data.byteswap()

        raw_pcm = audio_data.tobytes()
        return base64.b64encode(raw_pcm).decode()

    except Exception as e:
        print(f"Error processing audio: {e}")
        return None


async def send_to_openai(audio_base64):
    websocket_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json',
        'OpenAI-Beta': 'realtime=v1'
    }

    current_response = {
        "text": "",
        "audio_chunks": []
    }

    try:
        async with websockets.connect(websocket_url, extra_headers=headers) as websocket:
            # Wait for initial session creation
            initial_response = await websocket.recv()
            initial_data = json.loads(initial_response)
            print("\n=== New Session Created ===")
            print(f"Session ID: {initial_data.get('session', {}).get('id')}")

            # Update session configuration
            session_update = {
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "input_audio_transcription": {
                        "model": "whisper-1"
                    },
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.9,
                        "prefix_padding_ms": 300,
                        "silence_duration_ms": 1750
                    }
                }
            }
            await websocket.send(json.dumps(session_update))
            update_response = await websocket.recv()
            print("Session configuration updated")

            # Send previous conversation history
            print(f"\n=== Rebuilding Conversation History ({len(st.session_state.messages)} messages) ===")
            for msg in st.session_state.messages:
                history_event = {
                    "type": "conversation.item.create",
                    "previous_item_id": None,  # Add to end of conversation
                    "item": {
                        "type": "message",
                        "role": msg["role"],
                        "content": [{
                            "type": "text",
                            "text": msg["content"]
                        }]
                    }
                }
                await websocket.send(json.dumps(history_event))
                create_response = await websocket.recv()
                create_data = json.loads(create_response)
                if create_data.get('type') == 'conversation.item.created':
                    print(f"Added history - {msg['role']}: {msg['content']}")
                else:
                    print(f"Warning: Unexpected response when adding history: {create_data.get('type')}")

            print("\n=== Processing New Input ===")
            # Send new audio
            audio_event = {
                "type": "input_audio_buffer.append",
                "audio": audio_base64
            }
            await websocket.send(json.dumps(audio_event))

            # Commit the audio buffer
            commit_event = {
                "type": "input_audio_buffer.commit"
            }
            await websocket.send(json.dumps(commit_event))

            # Create response
            response_event = {
                "type": "response.create"
            }
            await websocket.send(json.dumps(response_event))

            chat_placeholder = st.empty()
            while True:
                try:
                    response = await websocket.recv()
                    response_data = json.loads(response)

                    # Only print certain types of responses to keep console clean
                    if response_data.get('type') not in ['response.audio.delta']:
                        print("Received:", json.dumps(response_data, indent=2))

                    if response_data.get('type') == 'conversation.item.input_audio_transcription.completed':
                        transcript = response_data.get('transcript')
                        if transcript:
                            print(f"\nUser said: {transcript}")
                            st.session_state.messages.append({
                                "role": "user",
                                "content": transcript
                            })

                    elif response_data.get('type') == 'response.text.delta':
                        delta = response_data.get('delta', '')
                        if delta:
                            current_response["text"] += delta
                            with st.chat_message("assistant"):
                                chat_placeholder.write(current_response["text"])

                    elif response_data.get('type') == 'response.audio.delta':
                        audio_chunk = response_data.get('delta', '')
                        if audio_chunk:
                            current_response["audio_chunks"].append(base64.b64decode(audio_chunk))

                    elif response_data.get('type') == 'response.done':
                        print("\n=== Response Complete ===")
                        if current_response["text"]:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": current_response["text"]
                            })
                            print(f"Total messages in history: {len(st.session_state.messages)}")

                        # Play combined audio
                        if current_response["audio_chunks"]:
                            combined_audio = b''.join(current_response["audio_chunks"])
                            audio_segment = AudioSegment.from_raw(
                                io.BytesIO(combined_audio),
                                sample_width=2,
                                frame_rate=24000,
                                channels=1
                            )
                            audio_buffer = io.BytesIO()
                            audio_segment.export(audio_buffer, format="wav")
                            audio_bytes = audio_buffer.getvalue()

                            audio_html = f"""
                            <audio autoplay>
                                <source src="data:audio/wav;base64,{base64.b64encode(audio_bytes).decode()}" type="audio/wav">
                            </audio>
                            """
                            st.markdown(audio_html, unsafe_allow_html=True)
                        break

                except websockets.exceptions.ConnectionClosed:
                    print("\n=== WebSocket connection closed ===")
                    break
                except Exception as e:
                    print(f"\n=== Error processing response: {str(e)} ===")
                    break

    except Exception as e:
        print(f"\n=== Error connecting to WebSocket: {str(e)} ===")

def main():
    st.title("OpenAI Realtime Voice Chat")

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        print("Initializing new messages list")
    else:
        print(f"Current messages in memory: {len(st.session_state.messages)}")

    # Add this to see what's in memory
    print("Current messages:", st.session_state.messages)

    # Initialize session state
    if 'recorder' not in st.session_state:
        st.session_state.recorder = AudioRecorder()
    if 'recording' not in st.session_state:
        st.session_state.recording = False

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Recording controls
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎤 Record", type="primary", key="record_button"):
            if not st.session_state.recording:
                st.session_state.recording = True
                st.session_state.recorder.start_recording()
                st.rerun()
            else:
                st.session_state.recording = False
                audio_data = st.session_state.recorder.stop_recording()

                if audio_data is not None:
                    with st.spinner("Processing audio..."):
                        audio_base64 = process_audio(audio_data)

                        if audio_base64:
                            asyncio.run(send_to_openai(audio_base64))
                        else:
                            st.error("Failed to process audio")

    # Display recording status
    if st.session_state.recording:
        st.warning("🎙️ Recording... Click the button again to stop!")
if __name__ == "__main__":
    main()