import os

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


class BaymaxVoice:
    def __init__(self):
        self.baymax_greet = 'Hello, I am Bae Max! Your personal health care companion!'
        tts = gTTS(text=self.baymax_greet, lang='en-us')
        tts.save("baymax_intro.mp3")
        playsound("baymax_intro.mp3")
        os.remove("baymax_intro.mp3")


def greet_baymax():
    BaymaxVoice()


def command_mode():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak now...")
            # Listening to microphone
            audio = r.listen(source)
            result = r.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        # speak.Speak("Could not request results from Google Speech Recognition service; {0}".format(e))
        return
    print("You said: ", result)
