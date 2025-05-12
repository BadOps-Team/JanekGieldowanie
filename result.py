import sys
import matplotlib.pyplot as plt
from pathlib import Path

from main import main
path = "configs"
configs = Path(path)

for f in configs.glob("*.json"):
    agent_dicts = list(filter(lambda x: x["profit"] > 0,sorted(main(path + "/" + f.name), key=lambda x: x["profit"])))

    for i, agent in enumerate(agent_dicts[-5:] + agent_dicts[:5]):
        for stock, ops in agent['history'].items():
            x = list(range(len(ops)))
            y = [ops[0]]
            for j in range(1, len(ops)):
                y.append(ops[j] + y[j-1])
            plt.plot(x, y, label=stock)
        
        plt.title(f"Number of Agent{i} stocks, Profit - {agent['profit']}")
        plt.xlabel("Day")
        plt.ylabel("Number of stocks")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"graphs/no_stocks_agent{i}{f.name}.png", dpi=300)
        plt.close()
