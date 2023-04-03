import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import speech_recognition
import logging


def wav_to_spectogram(q_in, q_out):
    logging.basicConfig(filename='LOGS/logs_spectogram.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s     %(funcName)s - %(levelname)s - %(message)s')
    logging.info("Process started")
    while True:
        audio = q_in.get()

        if not audio:
            logging.info("Process finished")
            q_out.put(False)
            break

        logging.info("Audio received")

        list_files = os.listdir("APP/voice/record_voice/data_wav")
        if len(list_files):
            last_file = list_files[len(list_files) - 1]
            last_file = last_file.split('.')
            n = int(last_file[0]) + 1
        else:
            n = 1
        with open("APP/voice/record_voice/data_wav/{0}.wav".format(n), 'wb') as f:
            f.write(audio.get_wav_data())
        path_load = "APP/voice/record_voice/data_wav/{0}.wav".format(n)
        path_save = "APP/voice/record_voice/data_spec/{0}.jpg".format(n)
        y, sr = librosa.load(path_load)
        yt, _ = librosa.effects.trim(y)
        y = yt
        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=100)
        mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
        librosa.display.specshow(mel_spect, y_axis='mel', fmax=20000, x_axis='time')
        plt.savefig(path_save)

        logging.info("Spectogram saved in {}".format(path_save))
        logging.info("Adding path to queue")

        q_out.put(path_save)
