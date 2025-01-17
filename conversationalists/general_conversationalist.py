import os
from environs import Env
from openai import OpenAI
env = Env()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class GeneralConversationalist:
    prompt_by_language = {
        "english": os.path.join(BASE_DIR, 'prompts', 'general', 'english.txt'),
        "german": os.path.join(BASE_DIR, 'prompts', 'general', 'german.txt'),
    }
    """
    A class to handle English conversations using OpenAI's GPT-3 model.
    """

    def __init__(self, language: str = 'english'):
        """
        Initialize the EnglishConversationalist with a prompt file and OpenAI API key.
        """
        prompt_file = self.prompt_by_language[language]
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=env.str('OPENAI_API_KEY'),
        )

        with open(prompt_file, 'r') as file:
            self.prompt = file.read()
        self.chat_history = []
        self.number_of_questions = 5

    def get_chat_gpt_response(self):
        """
        Get a response from the GPT-3 model based on the chat history.
        """
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=self.chat_history,
                temperature=0
            )
            response_role = completion.choices[0].message.role
            response_content = completion.choices[0].message.content
            self.chat_history.append({
                "role": response_role,
                "content": response_content
            })
        except Exception as exeption:
            print(f"{exeption}")
            response_content = None
        return response_content

    def __call__(self, answer, is_partial_response: bool = False, *args, **kwargs):
        """
        Add the user's answer to the chat history and get a response from the GPT-3 model.
        """
        if answer is not None:  # carry on with the conversation
            self.chat_history.append(
                {
                    "role": "user",
                    "content": str({
                        "part": 1 if is_partial_response else 2,
                        "text": answer
                    })

                }
            )
        else:  # Beginning of the session
            self.chat_history = [
                {
                    "role": "system",
                    "content": self.prompt
                },
            ]
        return self.get_chat_gpt_response()
