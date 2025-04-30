class Agent:
    def __init__(self, sale_history):
        self.sale_history = sale_history
        self.profit = 0

    def execute(self):
        # Tutaj odpalić to co było w sale history i ustawić profit.
        # Jest taki problem że może próbować kupować jak nie ma pieniędzy
        # i sprzedawać jak nie ma akcji, to ja bym mu wtedy ustawiał profit
        # na zero albo dawał jakąś karę.
        pass