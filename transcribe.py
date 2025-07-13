from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv


load_dotenv()
elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVEN_API"),
)


def transcribe(file):
    """
    Transcribes given video

    :param file:  location of mp4 file

    :return: video transcription in srt format
    """
    try:
        with open(file, "rb") as vid:
            transcription = elevenlabs.speech_to_text.convert(
            file=vid,
            model_id="scribe_v1",
            tag_audio_events=False,
            language_code="isl",
            timestamps_granularity="character",
            diarize=True,
            additional_formats=[
                {
                    "format": "srt"
                }
            ]
        )
    except:
        print('error opening file', file)
    
    formats = transcription.additional_formats
    if formats and formats[0] and formats[0].requested_format == "srt":
        text = formats[0].content
    
    return text


for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('.mp4'):
            mp4_path = os.path.join(root, file)
            srt_path = mp4_path[:-3] + 'srt'
            if not os.path.exists(srt_path):
                print(f'Bý til texta fyrir {mp4_path}')
                try:
                    srt = transcribe(mp4_path)
                    with open(srt_path, 'w', encoding='utf-8') as srt_file:
                        srt_file.write('\ufeff')
                        srt_file.write(srt)
                except:
                    print(f'Ekki tókst að búa til texta fyrir {mp4_path}')

input('Keyslu lokið :)')