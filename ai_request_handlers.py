import random
from io import BytesIO
import assemblyai as aai
import os
import boto3
from typing import Union
import openai
from .globals import (
    OPENAI_API_KEY,
    ASSEMBLYAI_API_KEY,
    IELTS_PART_1_PROMPT,
    IELTS_PART_2_PROMPT,
    IELTS_PART_3_PROMPT,
    IELTS_PART_1_DUMMY_START_TRIGGER,
    IELTS_PART_2_DUMMY_START_TRIGGER,
    IELTS_PART_3_DUMMY_START_TRIGGER,
    IELTS_POSSIBLE_TOPICS_LIST,
    AWS_API_KEY,
    AWS_ACCESS_KEY_ID,
    AWS_REGION_NAME,
    AWS_POLY_VOICE_ID,
    AWS_POLY_OUTPUT_FORMAT,
    AWS_POLY_OUTPUT_DIRECTORY
)


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
                 secret_access_key: Union[str, os.PathLike] = AWS_API_KEY,
                 access_key_id: Union[str, os.PathLike] = AWS_ACCESS_KEY_ID,
                 region_name_file: Union[str, os.PathLike] = AWS_REGION_NAME,
                 voice_id: str = AWS_POLY_VOICE_ID,
                 output_format: str = AWS_POLY_OUTPUT_FORMAT,
                 output_directory: Union[str, os.PathLike] = AWS_POLY_OUTPUT_DIRECTORY):
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

    def __call__(self, text, file_id):
        """
        writes (hopefully) an audio file to the specified output directory.
        given text, the call will generate an audio file at specified_output_directory/{file_id}.{outputformat}
        :param text: str, the string to be read aloud.
        :param file_id: int, a unique number to be assigned to the file (the server should save it to access it later).
        :param write: bool, whether to write the audio to a file (the server should save it to access it).
        :return:
        """
        aws_polly_service_response = self.polly_service_handle.synthesize_speech(Text=text,
                                                                                 OutputFormat=self.output_format,
                                                                                 VoiceId=self.voice_id)
        file_path = os.path.join(self.output_directory, f'{file_id}.{self.output_format}')
        print("I'm trying to write the audio")
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


class SpeechToTextEngine:
    def __init__(self, api_key: Union[str, os.PathLike] = ASSEMBLYAI_API_KEY):
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


class ChatGPTIELTSExaminer:
    """
    This class simulates an IELTS examiner using OpenAI's GPT-3.5 model.
    """

    def __init__(self):
        """
        Initializes the ChatGPTIELTSExaminer class.
        """
        openai.api_key = OPENAI_API_KEY
        self.session_topic = random.choice(IELTS_POSSIBLE_TOPICS_LIST)
        self.part_prompts = [
            IELTS_PART_1_PROMPT,
            IELTS_PART_2_PROMPT.replace("%%TOPIC%%", self.session_topic),
            IELTS_PART_3_PROMPT.replace("%%TOPIC%%", self.session_topic)
        ]
        self.dummy_part_start_triggers = [
            IELTS_PART_1_DUMMY_START_TRIGGER,
            IELTS_PART_2_DUMMY_START_TRIGGER,
            IELTS_PART_3_DUMMY_START_TRIGGER
        ]

        self.current_part = 0
        self.chat_history = [
            {
                "role": "system",
                "content": self.part_prompts[0]
            }
        ]
        self.chat_history_by_part = []

    def get_chat_gpt_response(self):
        """
        Sends the current chat history to the GPT-3.5 model and returns the response.

        Returns:
            str: The response from the GPT-3.5 model.
        """
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=self.chat_history
            )
            response_role = completion.choices[0].message.role
            response_content = completion.choices[0].message.content
            self.chat_history.append({
                "role": response_role,
                "content": response_content
            })
        except openai.error.ServiceUnavailableError:
            print("Server ran into a problem, please try again later.")
            response_content = None
        return response_content

    def initialise_test_part(self, part_index):
        """
        Initializes a new part of the IELTS speaking test by setting the appropriate prompt and resetting the chat history.

        Args:
            part_index (int): The index of the part to initialize.

        Returns:
            str: The response from the GPT-3.5 model.
        """
        self.chat_history = [
            {
                "role": "system",
                "content": self.part_prompts[part_index]
            },
        ]
        return self.get_chat_gpt_response()

    def __call__(self, answer, *args, **kwargs):
        """
        Appends the user's response to the chat history and returns the response from get_chat_gpt_response.

        Args:
            answer (str): The user's response.

        Returns:
            str: The response from the GPT-3.5 model.
        """
        self.chat_history.append(
            {
                "role": "user",
                "content": answer
            }
        )
        return self.get_chat_gpt_response()


class BaseConversationalist:
    """
    This class simulates a general speaking assistant using OpenAI's GPT-3.5 model.
    """

    def __init__(self, media_root):
        """
        Initializes the ChatGPTIELTSExaminer class.
        """
        openai.api_key = OPENAI_API_KEY
        self.speech_to_text_engine = SpeechToTextEngine()
        self.text_to_speech_engine = TextToSpeechEngine()
        self.media_root = media_root
        self.chat_history = []

    def __call__(self, audio_bytes, message_id, *args, **kwargs):
        """
        Appends the user's response to the chat history and returns the response from get_chat_gpt_response.

        Args:
            audio_bytes: binary data representing the input voice message.
            message_id: unique identifier for the file to be written to disk
        Returns:
            str: The response from the GPT-3.5 model.
        """
        audio_file_path = os.path.join(self.media_root, 'audios')
        os.makedirs(audio_file_path, exist_ok=True)
        audio_file_path = os.path.join(audio_file_path, str(message_id) + '.wav')
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_bytes)
            audio_file.close()
        transcript = self.speech_to_text_engine(file_url=audio_file_path)
        self.chat_history.append(transcript)
        text_response = "This is a dummy response, later to be replaced with ChatGPT responses."
        audio_response = self.text_to_speech_engine(text_response, file_id=message_id)
        audio_url = 'http://127.0.0.1:8000/media/audios/' + str(message_id) + '.wav'
        return {
            'user_transcript': transcript,
            'gpt_response': text_response,
            'audio_response': audio_response,
            'audio_url': audio_url
        }


def test_text_to_speech():
    text_test = 'Hi, my name is Ali, and I really really need this call to work'
    file_id = 0
    tts_engin = TextToSpeechEngine()
    tts_engin(text_test, file_id=file_id)


def test_speech_to_text():
    """
    Test the SpeechToTextEngine class.

    This function initializes a SpeechToTextEngine object and uses it to transcribe an audio file.
    The path to the audio file should be provided as an argument to the stt_engine function.
    The transcript is then printed to the console.

    Args:
        None

    Returns:
        None
    """
    stt_engine = SpeechToTextEngine()
    transcript = stt_engine(os.path.join('test_files', 'test.mp3'))
    print(transcript)


def test_ielts_chat_engine():
    """
    Test the ChatGPTIELTSExaminer class.

    This function initializes a ChatGPTIELTSExaminer object and uses it to simulate an IELTS speaking test.
    The examiner asks questions, and the user provides answers.
    The user's answers are then used to generate new questions until the test is complete.

    Args:
        None

    Returns:
        None
    """
    examiner = ChatGPTIELTSExaminer()

    # Part 1: Introduction and Interview
    question = examiner.initialise_test_part(0)
    for i in range(3):
        answer = input(f"Examiner: {question}\n")
        question = examiner(answer)

    # Part 2: Long Turn
    card = examiner.initialise_test_part(1)
    answer = input(f"Examiner: {card}\n")

    # Part 3: Discussion
    question = examiner.initialise_test_part(2)
    for i in range(4):
        answer = input(f"Examiner: {question}\n")
        question = examiner(answer)


if __name__ == '__main__':
    test_text_to_speech()
    test_speech_to_text()
    test_ielts_chat_engine()
