import pyttsx3

engine = pyttsx3.init()
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAULINA_11.0")
engine.setProperty("rate", "100")

def say(phrase:str):
    engine.say(phrase)
    engine.runAndWait()
