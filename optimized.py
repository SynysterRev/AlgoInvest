import csv
import time

BUDGET = 500
actions_cost = []

class Action:
    def __init__(self, number, cost, percent_profit):
        self.number = number
        self.cost = cost
        self.percent_profit = percent_profit
        self.profit = self.calculate_profit()

    def calculate_profit(self):
        return round(self.cost * self.percent_profit, 2)

    def __str__(self):
        return f"L'action {self.number} coûte {self.cost}€ et rapportera {self.profit}€ au bout de 2 ans."

    def __repr__(self):
        return str(self.number)

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
                action = Action(line[0].split("-")[-1], int(line[1]), convert_percent_to_float(line[2]))
                actions.append(action)
        return actions
    except FileNotFoundError:
        print("File not found")
        return []

def calculate_best_invest(combinations, actions):
    best_invest = None
    best_profit = 0
    for c in combinations:
        for result in c:
            profit = sum(actions[index].profit for index in result)
            if best_profit < profit:
                best_invest = result
                best_profit = profit

    return best_invest

def generate_combinations(actions, subset_length, best_profit):
    def combine(start, subset, total_cost, best_profit):
        if len(subset) == subset_length:
            # profit = sum(actions[index].profit for index in subset)
            # if best_profit < profit:
            #     best_profit = profit
            result.append(list(subset))
            return best_profit
        for j in range(start, len(actions)):
            cost = actions_cost[j] + total_cost
            if cost <= BUDGET:
                subset.append(j)
                best_profit = combine(j + 1, subset, cost, best_profit)
                subset.pop()
            else:
                return best_profit

    result = []
    best_profit = combine(0, [], 0, best_profit)
    return result, best_profit



def main():
    start_time = time.time()
    actions = load_action_info()
    actions.sort()
    for i in range(len(actions)):
        actions_cost.append(actions[i].cost)
    total_cost = 0
    max_length = 0

    # reduce length of combinations
    for i in range(len(actions_cost)):
        total_cost += actions_cost[i]
        if total_cost > BUDGET:
            max_length = i
            break

    combinations = []
    best_profit = 0
    for subset_length in range(1, max_length + 1):
        result, best_profit = generate_combinations(actions, subset_length, best_profit)
        combinations.append(result)

    best_invest = calculate_best_invest(combinations, actions)
    print("Meilleur investissement = ", best_invest)
    print("Coût total = ", sum(actions[index].cost for index in best_invest))
    print("Bénéfice total = ", sum(actions[index].profit for index in best_invest))
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()