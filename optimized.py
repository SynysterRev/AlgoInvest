import csv
import time
import timeit

BUDGET = 500


class Action:
    def __init__(self, name, cost, percent_profit):
        self.name = name
        self.cost = cost
        self.percent_profit = percent_profit
        self.profit = self.calculate_profit()

    def calculate_profit(self):
        return round(self.cost * self.percent_profit, 2)

    def __str__(self):
        return (f"L'action {self.name} coûte {self.cost}€ "
                f"et rapportera {self.profit}€ au bout de 2 ans.")

    def __repr__(self):
        return str(self.name)

    def __lt__(self, other):
        return self.cost < other.cost


def convert_percent_to_float(percent):
    if percent[-1] == "%":
        return float(percent[:-1]) / 100
    else:
        return float(percent) / 100


def load_action_info():
    try:
        actions = []
        with open('data/data_set_1.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                action = Action(line[0], abs(float(line[1])), convert_percent_to_float(line[2]))
                actions.append(action)
        return actions
    except FileNotFoundError:
        print("File not found")
        return []

def knap_sack_memory_opti(actions):
    n = len(actions)
    precision = 100
    budget_int = int(BUDGET * precision)
    dp = [0 for _ in range(budget_int + 1)]
    # use to keep track of selected actions
    trace = [[] for _ in range(budget_int + 1)]
    for i in range(1, n + 1):
        action_cost = int(actions[i - 1].cost * precision)
        # loop backward because it allows us to keep track of the "previous line" before updating the values
        for j in range(budget_int, 0, -1):
            if action_cost <= j:
                if dp[j - action_cost] + actions[i - 1].profit > dp[j]:
                    trace[j] = trace[j - action_cost] + [i - 1]
                    dp[j] = dp[j - action_cost] + actions[i - 1].profit
                else:
                    dp[j] = dp[j]

    selected_actions = [actions[action_index] for action_index in trace[budget_int]]
    return dp[budget_int], selected_actions


def main():
    start_time = time.time()
    actions = load_action_info()
    actions.sort()
    best_profit, result = knap_sack_memory_opti(actions)
    print("--- %s knap sack end ---" % (time.time() - start_time))
    total_cost = sum(action.cost for action in result)
    print("Meilleur investissement = ", result)
    print("Coût total = ", total_cost)
    print("Bénéfice total = ", best_profit)
    print("Rendement global = ", round(best_profit / total_cost * 100, 2), "%")


def knapsack_time():
    SETUP_CODE = '''
from __main__ import knap_sack_memory_opti
from __main__ import load_action_info
    '''

    TEST_CODE = '''
actions = load_action_info()
actions.sort()
best_profit, result = knap_sack_memory_opti(actions)
    '''
    times = timeit.repeat(setup=SETUP_CODE,
                          stmt=TEST_CODE,
                          repeat=100,
                          number=1)
    print("Temps moyen exécution : ", sum(t for t in times) / len(times))


if __name__ == '__main__':
    main()
    # knapsack_time()
