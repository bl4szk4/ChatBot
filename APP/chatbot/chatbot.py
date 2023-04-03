import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


def bot_initialization():
    # chatbot
    logging.info('Bot initialization')
    bot = ChatBot(
        'test1',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        logic_adapters=[
            'chatterbot.logic.BestMatch',
            {
                'import_path': 'APP.chatbot.MyMathAdapter.MyMathAdapter'
            },
            {
                'import_path': 'APP.chatbot.MyTimeAdapter.MyTimeAdapter'
            },
            {
                'import_path': 'APP.chatbot.MyCurrencyAdapter.MyCurrencyAdapter'
            }
        ]
    )
    return bot


def bot_training(bot):
    # trenowanie na podstawie bazy danych
    logging.info("Bot training")

    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.polish.komputery",
                  "chatterbot.corpus.polish.konwersacja",
                  "chatterbot.corpus.polish.nauka",
                  "chatterbot.corpus.polish.powitanie")
