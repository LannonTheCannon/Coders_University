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
SAMPLE_RATE = 16000
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

    audio_chunks = []
    try:
        async with websockets.connect(websocket_url, extra_headers=headers) as websocket:
            print("WebSocket connected successfully")

            # Session setup
            session_update = {
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "input_audio_transcription": {"model": "whisper-1"},
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "prefix_padding_ms": 600,
                        "silence_duration_ms": 1000
                    }
                }
            }
            await websocket.send(json.dumps(session_update))
            await websocket.recv()  # session update response

            # Append audio data
            await websocket.send(json.dumps({"type": "input_audio_buffer.append", "audio": audio_base64}))
            await websocket.send(json.dumps({"type": "input_audio_buffer.commit"}))
            await websocket.send(json.dumps({"type": "response.create"}))

            # Process responses
            while True:
                response = await websocket.recv()
                response_data = json.loads(response)

                if response_data.get('type') == 'response.audio.delta':
                    audio_chunk = response_data.get('delta', '')
                    if audio_chunk:
                        audio_chunks.append(base64.b64decode(audio_chunk))

                elif response_data.get('type') == 'response.text.delta':
                    delta = response_data.get('delta', '')
                    if delta:
                        st.write(delta)

                elif response_data.get('type') == 'response.done':
                    print("Response complete")
                    break

    except Exception as e:
        print(f"Error: {e}")

    # Combine audio for playback
    if audio_chunks:
        combined_audio = b''.join(audio_chunks)
        audio_segment = AudioSegment.from_raw(io.BytesIO(combined_audio), sample_width=2, frame_rate=24000, channels=1)

        audio_buffer = io.BytesIO()
        audio_segment.export(audio_buffer, format="wav")
        audio_bytes = audio_buffer.getvalue()

        # Render audio player
        audio_html = f"""
        <audio autoplay controls>
            <source src="data:audio/wav;base64,{base64.b64encode(audio_bytes).decode()}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)


def main():
    st.title("OpenAI Realtime Voice Chat")

    from pydub import AudioSegment
    AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"  # Adjust path if necessary
    print(f"ffmpeg path: {AudioSegment.converter}")

    if 'recorder' not in st.session_state:
        st.session_state.recorder = AudioRecorder()
    if 'recording' not in st.session_state:
        st.session_state.recording = False

    if st.button("Hold to Record"):
        if not st.session_state.recording:
            st.session_state.recording = True
            st.session_state.recorder.start_recording()
            st.write("🎙️ Recording... Hold down to speak!")
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

if __name__ == "__main__":
    main()
