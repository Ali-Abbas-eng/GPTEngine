
from io import BytesIO
import os
import boto3
from typing import Union
import openai
from environs import Env



env = Env()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConversationalist:
    """
    This class simulates a general speaking assistant using OpenAI's GPT-3.5 model.
    """

    def __init__(self, media_root):
        """
        Initializes the ChatGPTIELTSExaminer class.
        """
        openai.api_key = env.str('OPENAI_API_KEY')
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
        audio_url = f'http://{env.str("SERVER_IP")}:{env.str("SERVER_PORT")}/media/audios/' + str(message_id) + '.wav'
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
