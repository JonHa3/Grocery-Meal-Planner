import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

saved_recipes = {}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
meal_plan = {day: { "Breakfast": None, "Lunch": None, "Dinner": None} for day in days}

def load_data():
    global saved_recipes, meal_plan
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            saved_recipes = data.get("recipes", {})
            meal_plan = data.get("meal_plan", meal_plan)
        print("Data loaded successfully!")

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"recipes": saved_recipes, "meal_plan": meal_plan}, f, indent=4)

def add_recipe():
    name = input("Enter the name of the recipe: ")
    ingredients = input("Enter the ingredients (comma separated): ")
    ingredients_list = [i.strip() for i in ingredients.split(',')]
    saved_recipes[name] = ingredients_list
    save_data()
    print(f"\n'{name}' added successfully!")

def view_recipes():
    if not saved_recipes:
        print("\nNo recipes saved yet.")
    else:
        print("\n=== Saved Recipes ===")
        for meal, ingredients in sorted(saved_recipes.items()):
            print(f"\n{meal}: ")
            for ingredient in ingredients:
                print(f" - {ingredient}")

def view_meal_plan():
    print("\n=== Weekly Meal Plan ===")
    for day, meals in meal_plan.items():
        print(f"\n{day}:")
        print(f" Breakfast: {meals['Breakfast'] or 'Not Set'}")
        print(f" Lunch: {meals['Lunch'] or 'Not Set'}")
        print(f" Dinner: {meals['Dinner'] or 'Not Set'}")

def add_meal():
    print("\n=== Add/Edit a Meal ===")
    print("Select a day:")
    for i, day in enumerate(days, 1):
        print(f"{i}. {day}")

    day_choice = input("\nEnter the number corresponding to the day: ")
    if not day_choice.isdigit() or int(day_choice) < 1 or int(day_choice) > len(days):
        print("Invalid choice. Please try again.")
        return

    selected_day = days[int(day_choice) - 1]

    print("\n1. Breakfast")
    print("2. Lunch")
    print("3. Dinner")

    meal_choice = input("\nEnter the number corresponding to the meal type: ")
    meal_types = {"1": "Breakfast", "2": "Lunch", "3": "Dinner"}
    if meal_choice not in ["1", "2", "3"]:
        print("Invalid choice. Please try again.")
        return

    selected_meal = meal_types[meal_choice]

    if saved_recipes:
        print("\nSaved Recipes:")
        recipe_list = sorted(saved_recipes.keys())
        for i, recipe in enumerate(recipe_list,1):
            print(f"{i}. {recipe}")
            print(f" {len(recipe_list) + 1}. Enter Custom Meal")

        recipe_choice = input("\nEnter Choice: ")
        if recipe_choice.isdigit() and int(recipe_choice) in range(1, len(recipe_list) + 1):
            meal_name = recipe_list[int(recipe_choice) - 1]
        else:
            meal_name = input("Enter Meal Name: ")
    else: 
        meal_name = input("Enter Meal Name: ")
        
    meal_plan[selected_day][selected_meal] = meal_name
    save_data()
    print(f"Set {selected_meal.capitalize()} for {selected_day} to '{meal_name}' successfully!")

def view_grocery_list():
    print("\n=== Grocery List ===")
    grocery_list = {}

    for day, meals in meal_plan.items():
        for meal_type, meal_name in meals.items():
            if meal_name and meal_name in saved_recipes:
                for ingredient in saved_recipes[meal_name]:
                    if ingredient in grocery_list:
                        grocery_list[ingredient] += 1
                    else:
                        grocery_list[ingredient] = 1
    if not grocery_list:
        print("\nNo ingredients found! Make sure your meals have saved recipes")
    else:
        print("\nIngredients needed for the week: ")
        for ingredient, count in grocery_list.items():
            if count > 1:
                print(f" - {ingredient} (x{count})")
            else:
                print(f" - {ingredient}")

def clear_meal_plan():
    global meal_plan
    print("\nAre you sure you want to clear the weekly meal plan? This action cannot be undone. (yes/no)")
    choice = input().lower()
    if choice == "yes":
        meal_plan = {day: { "Breakfast": None, "Lunch": None, "Dinner": None} for day in days}
        save_data()
        print("Weekly meal plan cleared successfully!")
    else:
        print("Clear action cancelled.")

def main():
    load_data()
    while True:
        print("\n======Grocery-Meal-Planner======")
        print("Welcome to the Grocery Meal Planner!")
        print("This program will help you plan your grocery shopping and meals for the week.")
        print("1. View Weekly Meal Plan")
        print("2. Add/Edit a Meal")
        print("3. View Saved Recipes")
        print("4. Add a New Recipe")
        print("5. View Grocery List")
        print("6. Clear Weekly Plan")
        print("7. Exit")

        choice = input("\nPlease enter your choice (1-7): ")

        if choice == "1":
            view_meal_plan()
        elif choice == "2":
            add_meal()
        elif choice == "3":
            view_recipes()
        elif choice == "4":
            add_recipe()
        elif choice == "5":
            view_grocery_list()
        elif choice == "6":
            clear_meal_plan()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Option coming soon!")

main()