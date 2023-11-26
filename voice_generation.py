import os
from dotenv import load_dotenv

from elevenlabs import set_api_key, generate, play, save, Voice, VoiceSettings, voices


def generate_voice(text): 
    set_api_key("")

    audio = generate(
        text,
        voice=Voice(
            voice_id='ymqAVHpxO8dk95Ub7B4Z',
            settings=VoiceSettings(
                stability=0.5, similarity_boost=0.75, style=0, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2"
    )

    save(audio, 'static/message.mp3')

if __name__ == "__main__": 
    generate_voice("this is the greates test")