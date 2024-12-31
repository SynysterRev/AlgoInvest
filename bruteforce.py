import csv
import time

BUDGET = 500


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


def calculate_best_invest(combinations):
    best_invest = None
    best_profit = 0
    for c in combinations:
        for result in c:
            profit = sum(action.profit for action in result)
            if best_profit < profit:
                best_invest = result
                best_profit = profit

    return best_invest


def generate_combinations(actions, subset_length):
    def combine(start, subset):
        if len(subset) == subset_length:
            result.append(list(subset))
            return
        for j in range(start, len(actions)):
            subset.append(actions[j])
            combine(j + 1, subset)
            subset.pop()

    result = []
    final_result = []

    combine(0, [])
    for combination in result:
        if sum(action.cost for action in combination) <= BUDGET:
            final_result.append(combination)
    return final_result


def main():
    start_time = time.time()
    actions = load_action_info()
    length = len(actions)
    combinations = []
    for subset_length in range(1, length + 1):
        combinations.append(generate_combinations(actions, subset_length))
    best_invest = calculate_best_invest(combinations)
    print("Meilleur investissement = ", best_invest)
    print("Coût total = ", sum(action.cost for action in best_invest))
    print("Bénéfice total = ", sum(action.profit for action in best_invest))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
