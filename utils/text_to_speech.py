from typing import Union
import os
import boto3
from io import BytesIO
from environs import Env
env = Env()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TextToSpeechEngine:
    """
    This class encapsulate the process of converting text to speech
    :example usage:
        text_to_speech_converter = TextToSpeechEngine(secret_key_file_path,
                                                      access_key_id_file_path,
                                                      region_name_file_path,
                                                      voice_id, output_format,
                                                      output_directory)
        text_to_speech_converter("text you'd like to here read aloud", file_id) -> audio file in specified output dir
    """

    def __init__(self,
                 secret_access_key: Union[str, os.PathLike] = env.str("AWS_SECRET_ACCESS_KEY"),
                 access_key_id: Union[str, os.PathLike] = env.str("AWS_ACCESS_KEY_ID"),
                 region_name_file: Union[str, os.PathLike] = env.str("AWS_REGION_NAME"),
                 voice_id: str = env.str("AWS_VOICE_ID"),
                 output_format: str = env.str("AWS_POLY_OUTPUT_FORMAT"),
                 output_directory: Union[str, os.PathLike] = os.path.join(BASE_DIR, 'output', 'audios')):
        """
        initialise the Text to Speech Engine with the variable representing the Amazon Polly Account Configurations.
        :param secret_access_key: str or os.PathLike, /path/to/SECRET_ACCESS_KEY.txt.
        :param access_key_id: str or os.PathLike, /path/to/ACCESS_KEY_ID.txt.
        :param region_name_file: str or PathLike, /path/to/REGION_NAME.txt.
        :param voice_id: str, the name of the synthesis voice to be used .
        :param output_format: str, the extension of the output file (.mp3).
        :param output_directory: str or os.PathLike, the directory to which the audio streams will be written.
        """
        self.voice_id = voice_id
        self.output_format = output_format
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)
        self.polly_service_handle = boto3.client('polly',
                                                 region_name=region_name_file,
                                                 aws_access_key_id=access_key_id,
                                                 aws_secret_access_key=secret_access_key)

    def __call__(self, text, output_file_path):
        """
        writes (hopefully) an audio file to the specified output directory.
        given text, the call will generate an audio file at specified_output_directory/{file_id}.{outputformat}
        :param text: str, the string to be read aloud.
        :param output_file_path: str or os.PathLike, path to the output file.
        :return:
        """
        aws_polly_service_response = self.polly_service_handle.synthesize_speech(Text=text,
                                                                                 OutputFormat=self.output_format,
                                                                                 VoiceId=self.voice_id)
        file_path = output_file_path + '.' +self.output_format
        if "AudioStream" in aws_polly_service_response:
            with aws_polly_service_response['AudioStream'] as audio_stream:
                audio_data = BytesIO(audio_stream.read())
                try:
                    with open(file_path, 'wb') as file_output_handle:
                        file_output_handle.write(audio_data.getvalue())
                        file_output_handle.close()
                    return file_path
                except IOError as error:
                    print(error)
                    return None
        else:
            print('Could not stream audio')
            return None

