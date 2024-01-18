import csv
from z3 import Int, Optimize, Sum, sat

file_path = 'data/taco_bell_menu.csv'


def maximize_calories_with_z3(menu_items, budget):
    solver = Optimize()

    # Create a variable for each menu item to represent its quantity in the order
    quantities = {item['Item']: Int(item['Item']) for item in menu_items}

    # Add constraints: each quantity must be non-negative
    for quantity in quantities.values():
        solver.add(quantity >= 0)

    # Add constraint: total cost must not exceed the budget
    total_cost = Sum([quantities[item['Item']] * float(item['Price']) for item in menu_items])
    solver.add(total_cost <= budget)

    # Objective: Maximize total calories
    total_calories = Sum([quantities[item['Item']] * int(item['Calories']) for item in menu_items])
    solver.maximize(total_calories)

    # Solve the problem
    if solver.check() == sat:
        model = solver.model()
        order = {item['Item']: model.evaluate(quantities[item['Item']]).as_long() for item in menu_items}
        # Calculate the total calories based on the quantities of each item in the optimal order
        total_calories_value = sum(int(item['Calories']) * order[item['Item']] for item in menu_items if order[item['Item']] > 0)
        # Return both the order and the total calories as a dictionary
        return {
            'order': order,
            'total_calories': total_calories_value
        }
    else:
        return {
            'order': "No solution found",
            'total_calories': 0
        }


if __name__ == '__main__':
    menu_items = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            menu_items.append(row)

    budget = input("Enter your taco bell budget: ")

    optimal_order = maximize_calories_with_z3(menu_items, budget)
    print(optimal_order)
