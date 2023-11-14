from ai_request_handlers import SpeechToTextEngine, TextToSpeechEngine, ChatGPTIELTSExaminer
from globals import END_OF_IELTS_SPEAKING_SESSION


class SpeakingSessionManager:
    """
    Manages an IELTS speaking session with a student, handling questions and responses.
    """

    def __init__(self, number_of_questions: int = 8, verbose: bool = True):
        """
        Initialize a SpeakingSessionManager.

        Args:
            number_of_questions (int): The number of questions in the session.
            verbose (bool): Whether to print verbose output.
        """
        self.text_to_speech_engine = TextToSpeechEngine()
        self.speech_to_text_engine = SpeechToTextEngine()
        self.text_to_text_chat_gpt = ChatGPTIELTSExaminer()
        self.number_of_questions = number_of_questions
        self.current_question_index = 0
        self.current_examination_part = -1
        self.end_of_speaking_session = False
        self.verbose = verbose

    def __call__(self, audio_file_url, response_file_id, *args, **kwargs):
        """
        Process a student's response to an IELTS speaking question.

        Args:
            audio_file_url (str): URL of the student's audio response.
            response_file_id (int): Identifier for the response file.

        Returns:
            dict: A dictionary with audio and text transcription of the examiner's response.
        """
        if self.current_question_index % self.number_of_questions == 0:
            # Start a new examination part or finish the session if it's the third part.
            self.current_question_index = 0
            self.current_examination_part += 1
            if self.current_examination_part == 1:
                # If it's part 1, skip the initial questions.
                self.current_question_index += self.number_of_questions
            if self.current_examination_part == 3:
                # If it's part 3, mark the end of the session.
                self.end_of_speaking_session = True
                return {
                    "audio": self.text_to_speech_engine(END_OF_IELTS_SPEAKING_SESSION, response_file_id),
                    "text_transcription": END_OF_IELTS_SPEAKING_SESSION
                }
            examiner_response = self.text_to_text_chat_gpt.initialise_test_part(self.current_examination_part)
            if self.verbose:
                print(f'Transcription of your response: {examiner_response}')

        else:
            # Process the student's response.
            answer_text = self.speech_to_text_engine(audio_file_url)
            if self.verbose:
                print(f"Transcription of your response: {answer_text}")
            examiner_response = self.text_to_text_chat_gpt(answer_text)

        audio_examiner_response_audio_file = self.text_to_speech_engine(examiner_response, response_file_id)
        if self.verbose:
            print(f'Transcription of your response: {examiner_response}')
        self.current_question_index += 1

        return {
            "audio": audio_examiner_response_audio_file,
            "text_transcription": examiner_response
        }


def test_speaking_session_manager():
    """
    Test the SpeakingSessionManager by simulating an IELTS speaking session with a student.

    This function simulates an IELTS speaking session, interacting with the SpeakingSessionManager
    class. It allows a student to respond to questions and records their audio responses.

    Usage:
    1. Create an instance of the SpeakingSessionManager with a specified number of questions.
    2. Initialize an audio stream manager and set the student's initial audio response to None.
    3. Record and process student responses until the end of the speaking session is reached.

    Detailed Steps:
    - Create an instance of SpeakingSessionManager with a specified number of questions per session.
    - Initialize the audio stream manager (PyAudio) for recording audio.
    - Set the initial student's audio response to None.
    - Initialize a file identifier for naming response files.
    - Continuously loop until the end of the speaking session is reached.
    - For each session step, get an examiner's question using the SpeakingSessionManager.
    - Play the audio of the examiner's question using the 'playsound' library.
    - Open an audio stream for recording the student's response.
    - Record and collect audio data in chunks for a specified duration (5 seconds in this case).
    - Stop the audio stream and close it.
    - Save the recorded student response as a temporary WAV file ('temp.wav').
    - Update the file identifier for the next response file.

    This function is a crucial part of testing and evaluating the functionality of the SpeakingSessionManager
    for conducting IELTS speaking sessions with students.
    """
    import pyaudio
    import playsound
    import wave
    import os

    # Create an instance of the SpeakingSessionManager with a specific number of questions per session.
    speaking_session_manager = SpeakingSessionManager(number_of_questions=3)

    # Initialize the audio stream manager using PyAudio.
    audio_stream_manager = pyaudio.PyAudio()

    # Set the initial student's audio response to None.
    student_audio_response = None

    # Initialize a file identifier for naming response files.
    file_id = 0

    # Continuously loop until the end of the speaking session is reached.
    while not speaking_session_manager.end_of_speaking_session:
        # Get an examiner's question using the SpeakingSessionManager.
        examiner_question = speaking_session_manager(student_audio_response, file_id)

        # Play the audio of the examiner's question.
        playsound.playsound(rf"{examiner_question['audio']}")

        # Open an audio stream for recording the student's response.
        stream = audio_stream_manager.open(format=pyaudio.paInt16,
                                           channels=2,
                                           rate=44100,
                                           input=True,
                                           frames_per_buffer=1024)

        # Display a message indicating that recording has started.
        print('Recording...')

        # Initialize a list to store audio data chunks.
        frames = []

        # Record and collect audio data in chunks for a specified duration (5 seconds).
        for i in range(0, int(44100 / 1024 * 5)):
            data = stream.read(1024)
            frames.append(data)

        # Stop the audio stream and close it.
        stream.stop_stream()
        stream.close()

        # Save the recorded student response as a temporary WAV file ('temp.wav').
        student_audio_response = os.path.join('inputs', 'audios', f'{file_id}.wav')
        student_response_audio_file = wave.open(student_audio_response, 'wb')
        student_response_audio_file.setnchannels(2)
        student_response_audio_file.setsampwidth(audio_stream_manager.get_sample_size(pyaudio.paInt16))
        student_response_audio_file.setframerate(44100)
        student_response_audio_file.writeframes(b"".join(frames))
        student_response_audio_file.close()

        # Update the file identifier for the next response file.
        file_id += 1


if __name__ == '__main__':
    test_speaking_session_manager()
