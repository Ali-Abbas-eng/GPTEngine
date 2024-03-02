from openai import OpenAI
import os

from gptengine.conversationalists.general_conversationalist import GeneralConversationalist
from gptengine.globals import (
    IELTS_PART_1_PROMPT,
    IELTS_PART_2_PROMPT,
    IELTS_PART_3_PROMPT,
    IELTS_POSSIBLE_TOPICS_LIST,
)
import random
from environs import Env
env = Env()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IELTS_PART_COUNT = 3


class ChatGPTIELTSExaminer(GeneralConversationalist):
    """
    This class simulates an IELTS examiner using OpenAI's GPT-3.5 model.
    """

    def __init__(self):
        """
        Initializes the ChatGPTIELTSExaminer class.
        """
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=env.str('OPENAI_API_KEY'),
        )
        self.session_topic = random.choice(IELTS_POSSIBLE_TOPICS_LIST)
        self.part_prompts = [
            IELTS_PART_1_PROMPT,
            IELTS_PART_2_PROMPT,
            IELTS_PART_3_PROMPT
        ]

        self.chat_history = [
            {
                "role": "system",
                "content": self.part_prompts[0]
            }
        ]
        self.test_parts_lengths = [1 + 1, 1, 2]
        self.current_question_count = [0, 0, 0]
        self.current_part = 0
        self.chat_history_by_part = []
        self.number_of_questions = sum(self.test_parts_lengths)

    def manage_session_borders(self):
        self.current_question_count[self.current_part] += 1
        if self.current_question_count[self.current_part] == self.test_parts_lengths[self.current_part]:
            self.current_part += 1
            self.current_question_count[self.current_part] += 1
            self.chat_history = [
                {
                    "role": "system",
                    "content": self.part_prompts[self.current_part]
                },
            ]

    def __call__(self, answer, *args, **kwargs):
        """
        Appends the user's response to the chat history and returns the response from get_chat_gpt_response.

        Args:
            answer (str): The user's response.

        Returns:
            str: The response from the GPT-3.5 model.
        """
        if answer is not None:
            self.chat_history.append(
                {
                    "role": "user",
                    "content": answer
                }
            )
        self.manage_session_borders()
        if self.current_question_count == self.test_parts_lengths:
            return None
        return self.get_chat_gpt_response()

