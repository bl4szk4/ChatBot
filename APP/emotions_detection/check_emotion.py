import logging
import os

from APP.emotions_detection.emotionsClass import emotionsClass
import numpy as np
from APP.voice.record_voice.wav_to_spectogram import wav_to_spectogram

emotions = 'angry', 'calm', 'fearful', 'happy', 'neutral', 'sad', 'surprised'


def emotion_from_audio(learn, emotions, q):

    logging.info("Thread started")
    list_files = os.listdir("DATA")
    if len(list_files):
        last_file = list_files[len(list_files) - 1]
        last_file = last_file.split('.')
        n = int(last_file[0])
    path = 'DATA/{}.txt'.format(n)

    while True:
        spec_path = q.get()

        if not spec_path:
            logging.info("Thread finished")
            break

        logging.info("Received path")
        logging.info("actual prediction = {}".format(learn.predict(spec_path)[0]))

        new_val = learn.predict(spec_path)[2].numpy()

        logging.info("new values = {}".format(new_val))

        emotions.add_values(new_val)
        emotions.calc_median()

        logging.info('new median = {}'.format(emotions.get_median()))
        logging.info('Dominating emotion = {}'.format(emotions.get_dominating_emotion()))
        with open (path, 'a') as f:
            f.write("new values = {}\n".format(new_val))
            f.write('new median = {}\n'.format(emotions.get_median()))
            f.write('Dominating emotion = {}\n'.format(emotions.get_dominating_emotion()))
