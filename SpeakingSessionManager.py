from gptengine.conversationalists.general_conversationalist import GeneralConversationalist
from gptengine.utils.text_to_speech import TextToSpeechEngine
from gptengine.utils.speech_to_text import SpeechToTextEngine


class SpeakingSessionManager:

    def __init__(self,
                 text_to_text_engine: GeneralConversationalist,
                 number_of_questions: int = 5,
                 verbose: bool = True,
                 text_to_speech_engine: TextToSpeechEngine = TextToSpeechEngine(),
                 speech_to_text_engine: SpeechToTextEngine = SpeechToTextEngine()):

        self.text_to_speech_engine = text_to_speech_engine
        self.speech_to_text_engine = speech_to_text_engine
        self.text_to_text_engine = text_to_text_engine
        self.number_of_questions = number_of_questions
        self.current_question_index = 0
        self.end_of_speaking_session = False
        self.verbose = verbose

    def __call__(self, audio, output_file, *args, **kwargs):
        self.current_question_index += 1

        # Convert user's audio answer to text
        answer_text = self.speech_to_text_engine(audio)

        # Get the relevant response from AI Engine
        response_text = self.text_to_text_engine(answer_text)

        # Convert AI Engine's response from text to audio
        response_audio = self.text_to_speech_engine(response_text, output_file)

        return {
            "audio": response_audio,
            "response_text": response_text,
            "answer_text": answer_text
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
