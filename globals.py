import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IELTS_PART_1_PROMPT_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_1_SYSTEM_PROMPT.txt')
IELTS_PART_1_PROMPT = open(IELTS_PART_1_PROMPT_FILE).read()

IELTS_PART_2_PROMPT_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_2_SYSTEM_PROMPT.txt')
IELTS_PART_2_PROMPT = open(IELTS_PART_2_PROMPT_FILE).read()

IELTS_PART_3_PROMPT_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_3_SYSTEM_PROMPT.txt')
IELTS_PART_3_PROMPT = open(IELTS_PART_3_PROMPT_FILE).read()

IELTS_POSSIBLE_TOPICS_LIST_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'IELTS_POSSIBLE_TOPICS.json')
IELTS_POSSIBLE_TOPICS_LIST = json.load(open(IELTS_POSSIBLE_TOPICS_LIST_FILE))