from chatterbot.logic import LogicAdapter


class MyTimeAdapter(LogicAdapter):

    def __int__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        time_phrases = ['która', 'jest', 'godzina']
        if all(x in statement.text.lower().split() for x in time_phrases):
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        import  datetime

        response = statement
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute

        # take hour as a number and change it to proper word to be spoken
        hour_words = ('północ', 'pierwsza', 'druga', 'trzecia', 'czwarta', 'piąta', 'szósta', 'siódma', 'ósma', 'dziewiąta', \
                     'dziesiata', 'jedenasta', 'dwunasta', 'trzynasta', 'cztersnasta', 'piętnasta', 'szesnasta', \
                    'siedemnasta', 'osiemnasta', 'dziewiętnasta', 'dwudziesta', 'dwudziesta pierwsza', 'dwudziesta druga', \
                     'dwudziesta trzecia')

        try:
            response.text = 'Jest teraz {} {}'.format(hour_words[hour], minute)
            response.confidence = 1
        except IndexError:
            response.confidence = 0
            response.text = 'Nie mogę niestety powiedzieć'

        return response
