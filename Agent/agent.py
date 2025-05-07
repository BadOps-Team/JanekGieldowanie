class Agent:
    def __init__(self, sale_history):
        # Taki słownik: {
        #   'ticker1': [1, 2, -1, -2, 3] <- Tyle elementów listy ile dni, dodatni to kupno, ujemny to sprzedaż
        #   'ticker2': [9, 2, -2, 3, 0] 
        # }
        self.sale_history = sale_history
        
        self.profit = 0

    def execute(self):
        # Tutaj odpalić to co było w sale history i ustawić profit.
        # Jest taki problem że może próbować kupować jak nie ma pieniędzy
        # i sprzedawać jak nie ma akcji, to ja bym mu wtedy ustawiał profit
        # na zero albo dawał jakąś karę.
        pass