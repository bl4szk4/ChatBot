import speech_recognition


def noise_adjustment(microphone, regonizer):
    with microphone as source:
        regonizer.adjust_for_ambient_noise(source, duration=2)


def voice_capture(microphone, recognizer):
    print("Recording voice:")
    try:
        with microphone as source:
            response = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            return response
    except speech_recognition.WaitTimeoutError:
        print("Nothing was said")
        return False
    except speech_recognition.UnknownValueError:
        print("Something went wrong")
        return False


def text_from_voice(audio, recognizer):
    try:
        response = recognizer.recognize_google(audio, language='pl-PL')
    except speech_recognition.UnknownValueError:
        return False
    return response
