import openai
import os
from gptengine.globals import (
    IELTS_PART_1_PROMPT,
    IELTS_PART_2_PROMPT,
    IELTS_PART_3_PROMPT,
    IELTS_PART_1_DUMMY_START_TRIGGER,
    IELTS_PART_2_DUMMY_START_TRIGGER,
    IELTS_PART_3_DUMMY_START_TRIGGER,
    IELTS_POSSIBLE_TOPICS_LIST,
)
import random
from environs import Env
env = Env()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ChatGPTIELTSExaminer:
    """
    This class simulates an IELTS examiner using OpenAI's GPT-3.5 model.
    """

    def __init__(self):
        """
        Initializes the ChatGPTIELTSExaminer class.
        """
        openai.api_key = env.str('OPENAI_API_KEY')
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
