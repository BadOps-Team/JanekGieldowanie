import sys, json
import matplotlib.pyplot as plt
from pathlib import Path

from main import main
path = "configs"
configs = Path(path)

for f in configs.glob("config1_0.json"):
    print(str(f))
    with open(f, "r") as conf:
        cnf = json.load(conf)
    start_asset = cnf["start_asset"]
    agents, days_best_agent, best_agent = main(path + "/" + f.name)
    agent_dicts = list(filter(lambda x: x["profit"] > 0,sorted(agents, key=lambda x: x["profit"])))
    for i, agent in enumerate(agent_dicts[-1:]):
        for stock, ops in agent['history'].items():
            x = list(range(len(ops)))
            y = [ops[0]]
            for j in range(1, len(ops)):
                y.append(ops[j] + y[j-1])
            plt.plot(x, y, label=stock)
        
        plt.title(f"Number of Agent{i} stocks, Profit - {agent['profit'] - start_asset}")
        plt.xlabel("Day")
        plt.ylabel("Number of stocks")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        sd = cnf["start_date"]
        ed = cnf["end_date"]
        plt.savefig(f"graphs/no_stocks_agent{i}{f.name}{sd}{ed}.png", dpi=300)
        plt.close()

    plt.plot([i for i in range(len(days_best_agent))], days_best_agent)
    plt.title(f"Each day's best agent's profit")
    plt.xlabel("Day")
    plt.ylabel("Profit")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"graphs/days_best_profit{f.name}.png", dpi=300)
    plt.close()

    plt.plot([i for i in range(len(best_agent))], best_agent)
    plt.title(f"Best agent's profit each day")
    plt.xlabel("Day")
    plt.ylabel("Profit")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"graphs/best_profit_per_day{f.name}.png", dpi=300)
    plt.close()