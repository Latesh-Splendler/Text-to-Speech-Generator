import streamlit as st
import requests
import os
from murf import Murf
from api_key import API_KEY


client = Murf(api_key=API_KEY)


VOICE_MOODS = {
    "Abigail": {
        "voice_id": "en-US-abigail",
        "moods": ["Narration", "Conversational"]
    },
    "Miles": {
        "voice_id": "en-US-miles",
        "moods": ["Conversational", "Promo", "Sports Commentary", "Narration", "Newscast", "Sad", "Angry", "Calm", "Terrified", "Inspirational", "Pirate"]
    },
    "Aiden": {
        "voice_id": "en-UK-aiden",
        "moods": ["Narration", "Character"]
    },
    "Natalie": {
        "voice_id": "en-US-natalie",
        "moods": ["Promo", "Narration", "Newscast Formal", "Meditative", "Sad", "Angry", "Conversational", "Newscast Casual", "Furious", "Sorrowful", "Terrified", "Inspirational"]
    }
}

st.title("🎙️ Pirate Z VoiceOver")
st.markdown("Convert text to speech with AI-powered voiceovers!")


text_input = st.text_area("Enter some text to generate voice:", height=150)


voice_selection = st.selectbox("Select a voice", list(VOICE_MOODS.keys()))


moods_list = VOICE_MOODS[voice_selection]["moods"]
mood_selection = st.selectbox("Select a mood", moods_list)


voice_speed = st.slider("Adjust Pitch", min_value=-30, max_value=30, value=0, step=1)

def generate_audio():
    selected_voice = voice_selection
    voice_id = VOICE_MOODS[selected_voice]["voice_id"]

    if not text_input.strip():
        st.error("🚨 Please enter some text!")
        return None
    
    try:
        response = client.text_to_speech.generate(
            format="MP3",
            sample_rate=48000.0,
            channel_type="STEREO",
            text=text_input,
            voice_id=voice_id,
            style=mood_selection,
            pitch=voice_speed
        )
        return response.audio_file if hasattr(response, "audio_file") else None

    except Exception as e:
        st.error(f"❌ Error generating audio: {e}")
        return None


if st.button("🎤 Generate Voice"):
    audio_url = generate_audio()
    
    if audio_url:
        try:
            response = requests.get(audio_url, stream=True)
            if response.status_code == 200:
                file_path = "audio.mp3"
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                
                # Display success message and audio player
                st.success("✅ Audio successfully generated!")
                st.audio(file_path, format="audio/mp3")
            else:
                st.error(f"❌ Error downloading audio: {response.status_code}")

        except Exception as e:
            st.error(f"❌ Error saving and playing audio: {e}")
