import os
from typing import Union

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAI_API_KEY_FILE = os.path.join(BASE_DIR, 'secret', 'OpenAI', 'API_KEY.txt')
OPENAI_API_KEY = open(OPENAI_API_KEY_FILE).read()

IELTS_PART_1_PROMPT_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'PART_1_SYSTEM_PROMPT.txt')
IELTS_PART_1_PROMPT = open(IELTS_PART_1_PROMPT_FILE).read()

IELTS_PART_2_PROMPT_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'PART_2_SYSTEM_PROMPT.txt')
IELTS_PART_2_PROMPT = open(IELTS_PART_2_PROMPT_FILE).read()

IELTS_PART_3_PROMPT_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'PART_3_SYSTEM_PROMPT.txt')
IELTS_PART_3_PROMPT = open(IELTS_PART_3_PROMPT_FILE).read()

IELTS_PART_1_DUMMY_START_TRIGGER_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'PART_1_DUMMY_START_TRIGGER.txt')
IELTS_PART_1_DUMMY_START_TRIGGER: str = open(IELTS_PART_1_DUMMY_START_TRIGGER_FILE).read()

IELTS_PART_2_DUMMY_START_TRIGGER_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'PART_2_DUMMY_START_TRIGGER.txt')
IELTS_PART_2_DUMMY_START_TRIGGER: str = open(IELTS_PART_2_DUMMY_START_TRIGGER_FILE).read()

IELTS_PART_3_DUMMY_START_TRIGGER_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'PART_3_DUMMY_START_TRIGGER.txt')
IELTS_PART_3_DUMMY_START_TRIGGER: str = open(IELTS_PART_3_DUMMY_START_TRIGGER_FILE).read()

IELTS_POSSIBLE_TOPICS_LIST_FILE = os.path.join(BASE_DIR, 'secret', 'IELTS', 'IELTS_POSSIBLE_TOPICS.json')
IELTS_POSSIBLE_TOPICS_LIST = list(eval(open(IELTS_POSSIBLE_TOPICS_LIST_FILE).read()).values())

END_OF_IELTS_SPEAKING_SESSION = "Thank you for taking the IELTS test"


AWS_API_KEY_FILE = os.path.join(BASE_DIR, 'secret', 'AWS', 'SECRET_ACCESS_KEY.txt')
AWS_REGION_FILE = os.path.join(BASE_DIR, 'secret', 'AWS', 'REGION_NAME.txt')
AWS_ACCESS_KEY_ID_FILE = os.path.join(BASE_DIR, 'secret', 'AWS', 'ACCESS_KEY_ID.txt')

AWS_API_KEY = open(AWS_API_KEY_FILE).read()
AWS_ACCESS_KEY_ID = open(AWS_ACCESS_KEY_ID_FILE).read()
AWS_REGION_NAME = open(AWS_REGION_FILE).read()
AWS_POLY_VOICE_ID = 'Emma'
AWS_POLY_OUTPUT_FORMAT = 'mp3'
AWS_POLY_OUTPUT_DIRECTORY = os.path.join(BASE_DIR, 'output', 'audios')