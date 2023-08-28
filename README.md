# ChatBot
Chatbot używa biblioteki chatterbot do generowania odpowiedzi na zapytania rozmówcy. Można stworzyć swoją własną bazę zapytań i odpowiedzi.
Rozmowa odbywa się za pomocą mikrofonu i słuchawek/głośników. Mowa jest rozpoznawana i zamieniana na tekst, na podstawie którego chatbot generuje odpowiedź.
Dodatkowo wyszkolona sieć neuronowa rozpoznaje emocję występującą w głosie rozmawiającego i dla lepszego rozpoznania wyznacza medianę predykcji z całej rozmowy.


pliki z polskimi zwrotami należy umieścić w folderze 'polish' w venv->lib->site-packages->chatterbot_corpus->data->polish

plik requirements.txt poprzez pip install > requirements.txt

TO DO:
- wykorzystać sieć neuronową do generowania lepszych odpowiedzi
