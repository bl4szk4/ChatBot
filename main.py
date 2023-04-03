import os.path
import time

import numpy as np
import pyttsx3
import speech_recognition as sr
from APP.chatbot.chatbot import bot_initialization, bot_training
from APP.emotions_detection.emotionsClass import emotionsClass
from APP.voice.voice2text.voice_to_text_google import *
from fastai.vision.all import *
from APP.emotions_detection.check_emotion import emotion_from_audio
import pathlib
import logging
from APP.chatbot.helpFunction import help
from multiprocessing import Process
from multiprocessing import Queue
from threading import Thread
from APP.voice.record_voice.wav_to_spectogram import wav_to_spectogram


def initialization():
    global learn, r, mic, bot, engine
    logging.basicConfig(filename='LOGS/logs.log', filemode='w', level=logging.INFO, format='%(asctime)s      %(funcName)s - '
                                                                                      '%(levelname)s - %(message)s')
    logging.info('Initialization Start')
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath


    list_files = os.listdir("DATA")
    if len(list_files):
        last_file = list_files[len(list_files) - 1]
        last_file = last_file.split('.')
        n = int(last_file[0]) + 1
    else:
        n = 1
    path = 'DATA/{}.txt'.format(n)

    with open(path, 'w') as f:
        f.write(time.asctime())
        f.write('\n')
        f.write("'angry', 'calm', 'fearful', 'happy', 'neutral', 'sad', 'surprised'")
        f.write('\n')


    logging.info('Deleting old files start')
    dir_path = "APP/voice/record_voice/data_wav/"
    for file_name in os.listdir(dir_path):
        file = dir_path + file_name
        if os.path.isfile(file):
            os.remove(file)
    dir_path = "APP/voice/record_voice/data_spec/"
    for file_name in os.listdir(dir_path):
        file = dir_path + file_name
        if os.path.isfile(file):
            os.remove(file)
    logging.info('Deleting old files finish')

    learn = load_learner('voice_emotion_model_v4.pkl')
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)

    emotions_class = emotionsClass()
    bot = bot_initialization()
    bot_training(bot)
    noise_adjustment(mic, r)

    engine = pyttsx3.init()
    engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAULINA_11.0")
    engine.setProperty("rate", "100")

    logging.info('Initialization Finish')

    return emotions_class


def main(emotions_class, q):
    global learn, r, mic, bot, engine
    logging.info("Starting programme")

    while 1:
        audio_captured = voice_capture(mic, r)
        if audio_captured:
            logging.info("Audio captured")
            user_input = text_from_voice(audio_captured, r)

            if user_input:
                logging.info("Received user input")
                logging.info("Adding audio to queue")
                q.put(audio_captured)

                print("User:", user_input)
                if 'koniec rozmowy' in user_input.lower():
                    logging.info("End of conversation")
                    break
                elif 'co potrafisz' in user_input.lower() or 'twoje funkcje' in user_input.lower():
                    logging.info("Help menu")
                    help(engine)
                else:
                    try:
                        bot_response = bot.get_response(user_input)

                        logging.info("User: {}".format(user_input))
                        logging.info("Bot: {}".format(bot_response))

                        print(bot_response)

                        engine.say(bot_response)
                        engine.runAndWait()

                        # Press ctrl-c or ctrl-d on the keyboard to exit

                    except (KeyboardInterrupt, EOFError, SystemExit):
                        logging.info("Interrupted")
                        break
            else:
                logging.info("Nothing was said")
                pass

    q.put(False)
    engine.say("Dziękuję za rozmowę, do usłyszenia")
    engine.runAndWait()
    print("Koniec programu")


if __name__ == "__main__":
    emotions_class = initialization()

    logging.info("Creating queue")
    process_q = Queue()
    thread_q = Queue()

    logging.info("Creating Process")
    spectogram_save = Process(name='Spectogram save', target=wav_to_spectogram, args=(process_q, thread_q))

    logging.info("Creating Thread")
    emotions_detector = Thread(name='Emotions Detector', target=emotion_from_audio, args=(learn, emotions_class, thread_q))
    emotions_detector.daemon = True

    spectogram_save.start()
    emotions_detector.start()
    logging.info("Starting main")
    main(emotions_class, process_q)
    spectogram_save.join()
