import logging
from APP.chatbot.morph import morph_phrase
from chatterbot.logic import LogicAdapter
import requests


class MyCurrencyAdapter(LogicAdapter):
    currencies = {'bat': 'THB', 'dolar amerykański': 'USD', 'dolar australijski': 'AUD', 'dolar hongkong': 'HKD',
                  'dolar kanadyjski': 'CAD', 'dolar nowozelandzki': 'NZD', 'dolar singapurksi': 'SGD', 'euro': 'EUR',
                  'forint': 'HUF', 'frank szwajcarski': 'CHF', 'funt szterling': 'GPB', 'hrywna': 'UAH', 'jen': 'JPY',
                  'korona czeski': 'CZK', 'korona duński': 'DKK', 'korona islandzki': 'ISK', 'korona norweski': 'NOK',
                  'korona szwedzki': 'SEK', 'lej': 'RON', 'lew': 'BGN', 'lira': 'TRY', 'szekel': 'ILS',
                  'peso chilijskie': 'CLP', 'peso filipińskie': 'PHP', 'peso meksykańskie': 'MXN', 'rand': 'ZAR',
                  'real': 'BRL', 'ringgit': 'MYR', 'rupia indonezyjski': 'IDR', 'rupia indyjski': 'INR', 'won': 'KRW',
                  'juan': 'CNY', 'SDR': 'XDR'}

    def __int__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        if 'podaj kurs' in statement.text.lower() or 'jaki jest kurs' in statement.text.lower() \
                or 'jaki kurs ma' in statement.text.lower():
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        url_template = "http://api.nbp.pl/api/exchangerates/rates/a/{}/"
        response = statement
        input_text = statement.text

        logging.info('Morphology of "{}"'.format(input_text))
        text = morph_phrase(input_text)
        if text:
            logging.info('Text after morphology: "{}"'.format(text))
            for x in self.currencies.keys():
                if x in text:
                    rate = requests.get(url_template.format(self.currencies[x])).json()["rates"][0]["mid"]
                    try:
                        rate = float(rate)
                        rate = rate.__round__(2)
                    except Exception:
                        pass
                    response.text = 'kurs {} wynosi {} złotego'.format(x, rate)
                    response.confidence = 1
                    return response

        response.text = 'Nie potrafię znaleźć tej waluty, spróbuj ponownie'
        response.confidence = 1
        return response


