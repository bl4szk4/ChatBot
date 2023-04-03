from chatterbot.logic import LogicAdapter


class MyMathAdapter(LogicAdapter):
    math_signs = ['+', '-', 'x', '/', 'dodać', 'plus', 'minus', 'odjąć',  'razy', 'podzielić']
    math_symbol = '+'
    numbers = []
    result = 0

    def __int__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        if any(x in statement.text.split() for x in self.math_signs):
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        from chatterbot.conversation import Statement
        response = statement
        for x in statement.text.split():
            try:
                self.numbers.append((float(x)))
            except ValueError:
                pass
            if x in self.math_signs:
                self.math_symbol = x

        if len(self.numbers) == 2:
            confidence = 1
            if self.math_symbol == '+' or self.math_symbol == 'dodać' or self.math_symbol == 'plus':
                self.result = sum(self.numbers)
                self.numbers.clear()
            elif self.math_symbol == '-' or self.math_symbol == 'minus' or self.math_symbol == 'odjąć':
                self.result = self.numbers[0] - self.numbers[1]
                self.numbers.clear()
            elif self.math_symbol == '*' or self.math_symbol == 'razy':
                self.result = self.numbers[0] * self.numbers[1]
                self.numbers.clear()
            elif self.math_symbol == '/' or self.math_symbol == 'podzielić':
                if self.numbers[1] != 0:
                    self.result = self.numbers[0] / self.numbers[1]
                    self.numbers.clear()
                else:
                    self.numbers.clear()
                    response.text = 'Nie można dzielić przez zero'
                    response.confidence = confidence
                    return response
        else:
            confidence = 0

        if confidence:
            response.text = 'Wynik twojego działania to {}'.format(round(self.result, 2))
        else:
            response.text = 'Nie mogę tego policzyć'
        response.confidence = confidence
        return response
