from gptengine.conversationalists.general_conversationalist import GeneralConversationalist
from gptengine.utils.text_to_speech import TextToSpeechEngine
from gptengine.utils.speech_to_text import SpeechToTextEngine
from gptengine.conversationalists.ielts_examiner import ChatGPTIELTSExaminer


class SpeakingSessionManager:
    conversation_backends = {
        "general_english": lambda: GeneralConversationalist('english'),
        "ielts": ChatGPTIELTSExaminer,
        "general_german": lambda: GeneralConversationalist('german')
    }

    def __init__(self,
                 session_type,
                 verbose: bool = True,
                 text_to_speech_engine: TextToSpeechEngine = TextToSpeechEngine(),
                 speech_to_text_engine: SpeechToTextEngine = SpeechToTextEngine()):

        self.text_to_speech_engine = text_to_speech_engine
        self.speech_to_text_engine = speech_to_text_engine
        self.text_to_text_engine = self.conversation_backends[session_type]()
        self.number_of_questions = self.text_to_text_engine.number_of_questions
        self.current_question_index = 0
        self.end_of_speaking_session = False
        self.verbose = verbose

    def __call__(self, audio, output_file, is_partial_response, *args, **kwargs):
        self.current_question_index += 1
        if self.current_question_index == self.number_of_questions:
            answer_text = "This is the end of the speaking session, thank you very much for attending the IELTS test."
            response_audio = self.text_to_speech_engine(answer_text, output_file)
            return {
                "audio": response_audio,
                "response_text": answer_text,
                "answer_text": None
            }

        # if this is the beginning of the conversation
        answer_text = None
        # otherwise the user has sent an audio
        if audio is not None:
            # Convert user's audio answer to text
            answer_text = self.speech_to_text_engine(audio)

        # Get the relevant response from AI Engine
        response_text = self.text_to_text_engine(answer_text, is_partial_response)

        # Convert AI Engine's response from text to audio
        response_audio = self.text_to_speech_engine(response_text, output_file)

        return {
            "audio": response_audio,
            "response_text": response_text,
            "answer_text": answer_text
        }
