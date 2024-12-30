import csv
import time

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
        return f"L'action {self.name} coûte {self.cost}€ et rapportera {self.percent_profit}€ au bout de 2 ans."

    def __repr__(self):
        return str(self.name)

    def __lt__(self, other):
        return self.cost < other.cost


def convert_percent_to_float(percent):
    return float(percent[:-1]) / 100


def load_action_info():
    try:
        actions = []
        with open('data/action_info.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                action = Action(line[0], int(line[1]), convert_percent_to_float(line[2]))
                actions.append(action)
        return actions
    except FileNotFoundError:
        print("File not found")
        return []

def get_best_invest(actions):
    n = len(actions)
    matrix = [[0 for _ in range(BUDGET + 1)] for _ in range(n + 1)]
    # use knapsack algorithm to calculate the best profit
    for i in range(1, n + 1):
        for j in range(1, BUDGET + 1):
            if actions[i - 1].cost <= j:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i-1][j-actions[i - 1].cost] + actions[i - 1].profit)
            else:
                matrix[i][j] = matrix[i - 1][j]

    result = []
    current_budget = BUDGET
    number_actions = len(actions)
    # from the best profit loop until we get all the actions used to calculate it
    while current_budget >= 0 and number_actions >= 0 :
        if matrix[number_actions][current_budget] != matrix[number_actions - 1][current_budget]:
            result.append(actions[number_actions - 1])
            current_budget -= actions[number_actions - 1].cost
        number_actions -= 1
    return matrix[n][BUDGET], result


def main():
    start_time = time.time()
    actions = load_action_info()
    actions.sort()

    best_profit, result = get_best_invest(actions)
    total_cost = sum(action.cost for action in result)
    print("--- %s seconds end ---" % (time.time() - start_time))
    print("Meilleur investissement = ", result)
    print("Coût total = ", total_cost)
    print("Bénéfice total = ", best_profit)


if __name__ == '__main__':
    main()
