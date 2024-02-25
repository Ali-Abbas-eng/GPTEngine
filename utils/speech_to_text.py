import assemblyai as aai
from typing import Union
import os
from environs import Env
env = Env()


class SpeechToTextEngine:
    def __init__(self, api_key: Union[str, os.PathLike] = env.str('ASSEMBLYAI_API_KEY')):
        aai.settings.api_key = api_key
        self.assembly_ai_service_handle = aai.Transcriber()

    def __call__(self, file_url, *args, **kwargs):
        """
        given the path to the audio file, the function calls the AssemblyAI endpoint to transcribe the audio
        :param file_url:
        :return: str
            the transcription of the audio
        """
        transcript = self.assembly_ai_service_handle.transcribe(file_url)
        return transcript.text

