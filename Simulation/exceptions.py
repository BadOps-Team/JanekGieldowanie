from typing import List


class InconsistentTickerDataSize(Exception):
    def __init__(self, tickers : List[tuple]):
        self.message = "Inconsistent size of data for tickers:"
        for ticker_name, data_len in tickers:
            self.message += f" {ticker_name} has size {data_len}"
        super().__init__(self.message)