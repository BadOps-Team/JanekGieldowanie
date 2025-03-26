import numpy as np
from typing import List, Dict, Any
import random


# Agent and GeneticAlgorithm must implement at least the following methods:
# - Agent.make_decision(current_prices: dict, day: int) -> dict
# - Agent.execute_transaction(ticker: str, decision: dict, price: float, day: int) -> dict or None
# - Agent.get_total_profit() -> float
# - GeneticAlgorithm.evolve(agents: List[Agent]) -> List[Agent]


class Simulation:
    """
    Symulacja ruchów giełdowych.

    Implementacja symulacji ruchów giełdowych na podstawie modelu matematycznego.
    Model zakłada:
      - Dyskretyzację czasu (T = 100 dni),
      - Stochastyczny model zmian cen akcji,
      - Niezależnych inwestorów (agentów) reagujących na sytuacje rynkowe,
      - Uwzględnienie ograniczeń (kapitał, liczba transakcji, czas trzymania akcji, dywersyfikacja, itp.).

    Atrybuty:
      agents: Lista obiektów Agent reprezentujących inwestorów.
      stock_utilities: Słownik mapujący symbole akcji (np. 'AAPL', 'MSFT', 'TSLA') na obiekty StockUtility.
      T: Całkowita liczba kroków czasowych (dni) symulacji.
      dt: Krok czasowy (domyślnie 1 dzień).
      market_history: Historia cen akcji dla każdej spółki.
      transaction_log: Lista zarejestrowanych transakcji.
      genetic_algorithm: Instancja algorytmu genetycznego, używana do ewolucji strategii agentów.
    """

    def __init__(self, agents: List[Any], stock_utilities: Dict[str, Any], T: int = 100, dt: int = 1):
        self.agents = agents
        self.stock_utilities = stock_utilities  # np. {'AAPL': StockUtility('AAPL'), ...}
        self.T = T
        self.dt = dt  # time step (1 day)
        self.current_day = 0

        # Inicjujemy historię cen - dla każdej spółki przechowujemy listę cen
        self.market_history = {ticker: [] for ticker in stock_utilities.keys()}

        # Log transakcji wykonanych przez agentów
        self.transaction_log = []

        # Placeholder for genetic algorithm integration
        self.genetic_algorithm = None

    def simulate_market_movement(self):
        """
        Symulacja zmiany cen akcji przy użyciu uproszczonego modelu stochastycznego.
        W tej implementacji wykorzystujemy model ruchu Browna (geometric Brownian motion).
        """
        for ticker in self.stock_utilities.keys():
            # Pobieramy ostatnią cenę; jeśli brak, ustawiamy cenę początkową (np. 100)
            if self.market_history[ticker]:
                last_price = self.market_history[ticker][-1]
            else:
                last_price = 100.0

            # Parametry modelu: oczekiwana stopa zwrotu (mu) oraz zmienność (sigma)
            mu = 0.0005  # oczekiwany zwrot dzienny
            sigma = 0.02  # zmienność dzienna

            # Obliczenie nowej ceny wg modelu GBM:
            # new_price = last_price * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*N(0,1))
            random_shock = np.random.normal()
            new_price = last_price * np.exp((mu - 0.5 * sigma ** 2) * self.dt + sigma * np.sqrt(self.dt) * random_shock)
            new_price = max(new_price, 0.1)  # zapewniamy, że cena nie spadnie poniżej 0.1

            self.market_history[ticker].append(new_price)

    def get_current_market_data(self) -> Dict[str, float]:
        """
        Zwraca aktualne ceny akcji dla wszystkich spółek.
        """
        current_data = {}
        for ticker, prices in self.market_history.items():
            current_data[ticker] = prices[-1] if prices else 100.0
        return current_data

    def run_step(self, day: int):
        """
        Wykonuje symulację dla pojedynczego dnia:
          - Aktualizacja cen akcji.
          - Każdy agent pobiera aktualne dane rynkowe, podejmuje decyzję i wykonuje transakcję.
          - Transakcje są rejestrowane.
        """
        self.simulate_market_movement()
        current_prices = self.get_current_market_data()

        # Każdy agent podejmuje decyzję na podstawie bieżących cen
        for agent in self.agents:
            # Zakładamy, że metoda make_decision zwraca słownik np.:
            # { 'AAPL': {'action': 'buy', 'quantity': 10}, 'TSLA': {'action': 'sell', 'quantity': 5} }
            decisions = agent.make_decision(current_prices, day)

            # Agent wykonuje transakcje zgodnie z decyzjami
            for ticker, decision in decisions.items():
                transaction = agent.execute_transaction(
                    ticker,
                    decision,
                    current_prices[ticker],
                    day
                )
                # Jeśli transakcja została zrealizowana, dodajemy ją do logu
                if transaction:
                    self.transaction_log.append(transaction)

    def run_simulation(self) -> float:
        """
        Uruchamia symulację przez T dni.
        Po zakończeniu, wyliczana jest funkcja celu F(t).

        Funkcja celu jest zdefiniowana jako:

            F(t) = (∑_{l=1}^{t} X'(l)) / √t

        gdzie X'(l) reprezentuje miarę zysku (może być np. łączny zysk wszystkich agentów).
        """
        for day in range(1, self.T + 1):
            self.current_day = day
            self.run_step(day)

        # Ewaluacja funkcji celu – przykładowo sumujemy zyski agentów
        fitness = self.evaluate_objective()
        return fitness

    def evaluate_objective(self) -> float:
        """
        Oblicza funkcję celu, która może reprezentować np. łączny zysk znormalizowany przez √T.
        W niniejszej implementacji funkcja celu sumuje zyski wszystkich agentów.
        """
        total_profit = sum(agent.get_total_profit() for agent in self.agents)
        F_t = total_profit / np.sqrt(self.T)
        return F_t

    def set_genetic_algorithm(self, genetic_algorithm: Any):
        """
        Ustawia instancję algorytmu genetycznego, która będzie wykorzystywana do ewolucji strategii agentów.
        """
        self.genetic_algorithm = genetic_algorithm

    def evolve_agents(self):
        """
        Stosuje algorytm genetyczny do ewolucji populacji agentów.
        Metoda ta może wykonywać operacje selekcji, krzyżowania i mutacji,
        aby zoptymalizować decyzje inwestycyjne zgodnie z zadanym celem.
        """
        if self.genetic_algorithm is not None:
            self.agents = self.genetic_algorithm.evolve(self.agents)
        else:
            raise ValueError("Genetic algorithm not set. Use set_genetic_algorithm() to set it.")

# Przykład użycia jak zaimplementujecie pozostałe klaski:
#
# agents = [Agent(...), Agent(...), ...]
# stock_utilities = {
#     'AAPL': StockUtility('AAPL'),
#     'MSFT': StockUtility('MSFT'),
#     'TSLA': StockUtility('TSLA')
# }
# simulation = Simulation(agents, stock_utilities, T=100)
#
# # Opcjonalnie ustaw algorytm genetyczny:
# # genetic_algo = GeneticAlgorithm(...)
# # simulation.set_genetic_algorithm(genetic_algo)
#
# fitness = simulation.run_simulation()
# print(f"Simulation fitness (objective function value): {fitness}")
