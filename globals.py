import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IELTS_PART_1_PROMPT_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_1_SYSTEM_PROMPT.txt')
IELTS_PART_1_PROMPT = open(IELTS_PART_1_PROMPT_FILE).read()

IELTS_PART_2_PROMPT_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_2_SYSTEM_PROMPT.txt')
IELTS_PART_2_PROMPT = open(IELTS_PART_2_PROMPT_FILE).read()

IELTS_PART_3_PROMPT_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_3_SYSTEM_PROMPT.txt')
IELTS_PART_3_PROMPT = open(IELTS_PART_3_PROMPT_FILE).read()

IELTS_PART_1_DUMMY_START_TRIGGER_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_1_DUMMY_START_TRIGGER.txt')
IELTS_PART_1_DUMMY_START_TRIGGER: str = open(IELTS_PART_1_DUMMY_START_TRIGGER_FILE).read()

IELTS_PART_2_DUMMY_START_TRIGGER_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_2_DUMMY_START_TRIGGER.txt')
IELTS_PART_2_DUMMY_START_TRIGGER: str = open(IELTS_PART_2_DUMMY_START_TRIGGER_FILE).read()

IELTS_PART_3_DUMMY_START_TRIGGER_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'PART_3_DUMMY_START_TRIGGER.txt')
IELTS_PART_3_DUMMY_START_TRIGGER: str = open(IELTS_PART_3_DUMMY_START_TRIGGER_FILE).read()

IELTS_POSSIBLE_TOPICS_LIST_FILE = os.path.join(BASE_DIR, 'conversationalists/prompts', 'IELTS', 'IELTS_POSSIBLE_TOPICS.json')
IELTS_POSSIBLE_TOPICS_LIST = list(eval(open(IELTS_POSSIBLE_TOPICS_LIST_FILE).read()).values())

END_OF_IELTS_SPEAKING_SESSION = "Thank you for taking the IELTS test"
