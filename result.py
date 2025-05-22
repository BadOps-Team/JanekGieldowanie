import json
import matplotlib.pyplot as plt
from pathlib import Path

from main import main
path = "configs"
configs = Path(path)

for f in configs.glob("config1_0.json"):
    for it in range(10):
        print(str(f), f"test number {it}")
        with open(f, "r", encoding="utf-8-sig") as conf:
            cnf = json.load(conf)
        start_asset = cnf["start_asset"]
        best_agent, iteration_best_agent, best_agents_profit = main(path + "/" + f.name, it)

        for stock, ops in best_agent['history'].items():
            x = list(range(len(ops)))
            y = [ops[0]]
            for j in range(1, len(ops)):
                y.append(ops[j] + y[j-1])
            plt.plot(x, y, label=stock)

        plt.title(f"Best agent profit - {best_agent['profit'] - start_asset}")
        plt.xlabel("Day")
        plt.ylabel("Number of stocks")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        sd = cnf["start_date"]
        ed = cnf["end_date"]
        plt.savefig(f"graphs/best_agent_stocks{f.name}{sd}{ed}{it}.png", dpi=300)
        plt.close()

        plt.plot([i for i in range(len(iteration_best_agent))], iteration_best_agent)
        plt.title(f"Each iteration's best agent's profit")
        plt.xlabel("Iteration")
        plt.ylabel("Profit")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"graphs/iterations_best_profit{f.name}{it}.png", dpi=300)
        plt.close()

        plt.plot([i for i in range(len(best_agents_profit))], best_agents_profit)
        plt.title(f"Best agent's profit each iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Profit")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"graphs/best_profit_per_iteration{f.name}{it}.png", dpi=300)
        plt.close()