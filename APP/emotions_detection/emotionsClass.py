import numpy as np


class emotionsClass():
    emotions = 'angry', 'calm', 'fearful', 'happy', 'neutral', 'sad', 'surprised'

    def __init__(self) -> object:
        self.emotions_values = np.empty(7)
        self.emotions_medians = np.empty(7)
        self.first_emotion = True

    def get_dominating_emotion(self):
        return self.emotions[np.argmax(self.emotions_medians)]

    def get_median(self):
        return self.emotions_medians

    def get_values(self):
        return self.emotions_values

    def add_values(self, new_val):
        if self.first_emotion:
            self.emotions_values = np.array(new_val)
            self.first_emotion = False
        else:
            self.emotions_values = np.vstack((self.emotions_values, new_val))

    def calc_median(self):
        self.emotions_medians = np.median(self.emotions_values, axis=0)
