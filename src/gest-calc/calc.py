import re

class Calculator:
    def __init__(self):
        self.state = ""
        self.actions = [
            'C', '<',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

    def modify_state(self, action):
        if action not in self.actions:
            return

        if self.state == "Error":
            self.state = ""
            if action == '<':
                return
            
        if action == 'C':
            self.state = ""
        elif action == '<':
            self.state = self.state[:-1]
        elif action == '=':
            self.state = self.calculate()
        else:    
            self.state = self.state + action

    def calculate(self):
        if not self.state:
            return ""
        try:
            result = eval(self.state)
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result)
        except (SyntaxError, ZeroDivisionError, TypeError, OverflowError):
            return "Error"