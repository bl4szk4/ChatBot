help_text = 'Możesz zapytać się mnie o wynik prostego działania. Możesz również zapytać się mnie, która jest godzina. ' \
            'Mogę również spróbować odpowiedzieć na dowolne Twoje pytanie z dziedziny nauki. Mam nadzieję, że będę w stanie Ci pomóc'


def help(engine):
    engine.say(help_text)
    engine.runAndWait()
