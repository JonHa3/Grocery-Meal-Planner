import json
import os
from categories import categories, get_category

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

saved_recipes = {}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
meal_plan = {day: { "Breakfast": None, "Lunch": None, "Dinner": None} for day in days}
extras_list = []
checked_off = []
category_overrides = {}


def load_data():
    global saved_recipes, meal_plan, extras_list, checked_off, category_overrides
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                saved_recipes = data.get("recipes", {})
                meal_plan = data.get("meal_plan", meal_plan)
                extras_list = data.get("extras", [])
                checked_off = data.get("checked_off", [])
                category_overrides = data.get("category_overrides", {})
            print("Data loaded successfully!")
        except json.JSONDecodeError:
            print("Warning: Data file corrupted. Starting fresh.")
        except Exception as e:
            print(f"Warning: Could not load data ({e}). Starting fresh.")

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "recipes": saved_recipes,
            "meal_plan": meal_plan,
            "extras_list": extras_list,
            "checked_off": checked_off,
            "category_overrides": category_overrides
            }, f, indent=4)

def get_ingredient_category(ingredient):
    if ingredient in category_overrides:
        return category_overrides[ingredient]
    return get_category(ingredient)

def add_recipe():
    print("0. Cancel")
    name = input("Enter the name of the recipe: ")
    if name.strip() == "" :
        print("Recipe name cannot be empty. Recipe not saved.")
        return
    if name == "0":
        return

    while True:
        print("0. Cancel")
        ingredients = input("Enter the ingredients (comma separated): ")
        if ingredients == "0":
            return
        if ingredients.strip() == "":
            print("No ingredients entered. Please try again.")
            continue
        ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip() != ""]
        if not ingredient_list:
            print("No valid ingredients entered. Please try again.")
            continue
        break

    saved_recipes[name] = ingredient_list
    save_data()
    print(f"\n'{name}' added successfully!")

def edit_recipe():
    if not saved_recipes:
        print("\nNo recipes saved yet.")
        return

    print("\n=== Edit a Recipe ===")
    recipe_list = sorted(saved_recipes.keys())
    for i, recipe in enumerate(recipe_list, 1):
        print(f"{i}. {recipe}")
    print("0. Go Back")

    choice = input("\nEnter the number corresponding to the recipe you want to edit: ")

    if choice == "0":
        return
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(recipe_list):
        print("Invalid choice. Please try again.")
        return

    selected_recipe = recipe_list[int(choice) - 1]

    while True:
        print(f"\nWhat would you like to do with '{selected_recipe}'?")
        print("1. Add an Ingredient")
        print("2. Remove an Ingredient")
        print("3. Replace All Ingredients")
        print("4. Rename Recipe")
        print("5. Delete Recipe")
        print("0. Go Back")

        action = input("\nEnter your choice: ")

        if action == "0":
            return
        elif action == "1":
            new_ingredient = input("Enter the ingredient to add: ")
            if new_ingredient == "0":
                return
            if new_ingredient.strip() == "":
                print("Ingredient cannot be empty. Please try again.")
                continue
            saved_recipes[selected_recipe].append(new_ingredient.strip())
            save_data()
            print(f"\n'{new_ingredient}' added to '{selected_recipe}' successfully!") 
        elif action == "2":
            if not saved_recipes[selected_recipe]:
                print(f"\nNo ingredients to remove from '{selected_recipe}'!")
                continue
            print(f"\nCurrent ingredients for {selected_recipe}:")
            for i, ingredient in enumerate(saved_recipes[selected_recipe], 1):
                print(f"{i}. {ingredient}")
            delete_choice = input("\nEnter the number corresponding to the ingredient you want to remove: ")
            if delete_choice == "0":
                return
            if not delete_choice.isdigit() or int(delete_choice) < 1 or int(delete_choice) > len(saved_recipes[selected_recipe]):
                print("Invalid choice. Please try again.")
                continue
            removed_ingredient = saved_recipes[selected_recipe].pop(int(delete_choice) - 1)
            save_data()
            print(f"\n'{removed_ingredient}' removed from '{selected_recipe}' successfully!")
    
        elif action == "3":
            print(f"\nCurrent ingredients for '{selected_recipe}':")
            for ingredient in saved_recipes[selected_recipe]:
                print(f"  - {ingredient}")
            print("\nEnter new ingredients (this will replace the current list)")
            while True:
                new_ingredients = input("Enter ingredients with quantities, separated by commas: ")
                if new_ingredients == "0":
                    break
                if new_ingredients.strip() == "":
                    print("Ingredients cannot be blank!")
                    continue
                ingredient_list = [i.strip() for i in new_ingredients.split(',') if i.strip() != ""]
                if not ingredient_list:
                    print("No valid ingredients entered. Please try again.")
                    continue
                saved_recipes[selected_recipe] = ingredient_list
                save_data()
                print(f"\n'{selected_recipe}' updated successfully!")
                break
        elif action == "4":
            new_name = input("Enter the new name for the recipe: ")
            if new_name.strip() == "":
                print("Recipe name cannot be empty. Please try again.")
                continue
            if new_name == "0":
                continue
            if new_name in saved_recipes:
                print("A recipe with that name already exists. Please choose a different name.")
                continue
            saved_recipes[new_name] = saved_recipes.pop(selected_recipe)
            save_data()
            print(f"\n'{selected_recipe}' renamed to '{new_name}' successfully!")
            return
        elif action == "5":
            confirm = input(f"\nAre you sure you want to delete '{selected_recipe}'? (yes/no): ")
            if confirm.lower() == "yes":
                del saved_recipes[selected_recipe]
                save_data()
                print(f"\n'{selected_recipe}' deleted successfully!")
                return
            else:
                print("\nDeletion cancelled.")
        else:
            print("Invalid choice. Please try again.")

def view_extras():
    print("\n=== Extras List ===")
    if not extras_list:
        print("\nNo extras added yet.")
    else:
        for i, item in enumerate(extras_list, 1):
            print(f"{i}. {item}")

def manage_extras():
    while True:
        print("\n=== Manage Extras ===")
        print("1. View Extras List")
        print("2. Add an Extra")
        print("3. Remove an Extra")
        print("0. Go Back")

        choice = input("\nEnter your choice: ")

        if choice == "0":
            return
        elif choice == "1":
            view_extras()
        elif choice == "2":
            item = input("Enter item to add (e.g. '1tsp salt'): ")
            if item == "0":
                return
            extras_list.append(item)
            save_data()
            print(f"\n'{item}' added to extras list successfully!")
        elif choice == "3":
            if not extras_list:
                print("\nNo extras to remove!")
                continue
            view_extras()
            delete_choice = input("\nEnter the number corresponding to the extra you want to remove: ")
            if delete_choice == "0":
                return
            if not delete_choice.isdigit() or int(delete_choice) < 1 or int(delete_choice) > len(extras_list):
                print("Invalid choice. Please try again.")
                continue
            removed_item = extras_list.pop(int(delete_choice) - 1)
            save_data()
            print(f"\n'{removed_item}' removed from extras list successfully!")
        else:
            print("Invalid choice. Please try again.")

def override_category():
    print("\n=== Override Ingredient Category ===")
    all_ingredients = []

    for recipe, ingredients in saved_recipes.items():
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    for item in extras_list:
        if item not in all_ingredients:
            all_ingredients.append(item)

    if not all_ingredients:
        print("\nNo ingredients found!")
        return

    print("\nAll ingredients:")
    for i, ingredient in enumerate(all_ingredients, 1):
        current_category = get_ingredient_category(ingredient)
        print(f"  {i}. {ingredient} (currently: {current_category})")
    print("0. Go Back")

    choice = input("\nEnter the number of the ingredient to override: ")

    if choice == "0":
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(all_ingredients):
        print("Invalid choice. Please try again.")
        return

    selected_ingredient = all_ingredients[int(choice) - 1]

    category_list = sorted(categories.keys()) + ["Other"]
    print(f"\nSelect a new category for '{selected_ingredient}':")
    for i, category in enumerate(category_list, 1):
        print(f"  {i}. {category}")
    print("0. Go Back")

    cat_choice = input("\nEnter your choice: ")

    if cat_choice == "0":
        return

    if not cat_choice.isdigit() or int(cat_choice) < 1 or int(cat_choice) > len(category_list):
        print("Invalid choice. Please try again.")
        return

    selected_category = category_list[int(cat_choice) - 1]
    category_overrides[selected_ingredient] = selected_category
    save_data()
    print(f"\n'{selected_ingredient}' category set to '{selected_category}' successfully!")

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
    print("0. Go Back")

    day_choice = input("\nEnter the number corresponding to the day: ")
    if not day_choice.isdigit() or int(day_choice) < 1 or int(day_choice) > len(days):
        print("Invalid choice. Please try again.")
        return

    selected_day = days[int(day_choice) - 1]

    print("\n1. Breakfast")
    print("2. Lunch")
    print("3. Dinner")
    print("0. Go Back")

    meal_choice = input("\nEnter the number corresponding to the meal type: ")

    if meal_choice == "0":
        return
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
        print(f"{len(recipe_list) + 1}. Enter Custom Meal")
        print("0. Go Back")
        recipe_choice = input("\nEnter Choice: ")
        if recipe_choice == "0":
            return
        elif recipe_choice.isdigit() and int(recipe_choice) in range(1, len(recipe_list) + 1):
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
    categorized = {}

    for day, meals in meal_plan.items():
        for meal_type, meal_name in meals.items():
            if meal_name and meal_name in saved_recipes:
                for ingredient in saved_recipes[meal_name]:
                    category = get_ingredient_category(ingredient)
                    if category not in categorized:
                        categorized[category] = []
                    if ingredient not in categorized[category]:
                        categorized[category].append(ingredient)
                    
    if not categorized and not extras_list:
        print("\nNo ingredients found! Make sure your meals have saved recipes.")
    else:
        for category, ingredients in sorted(categorized.items()):
            print(f"\n{category}:")
            for ingredient in ingredients:
                status = "✓" if ingredient in checked_off else " "
                print(f" - [{status}] {ingredient}")
        
        if extras_list:
            print("\nExtras/Spices:")
            for item in extras_list:
                status = "✓" if item in checked_off else " "
                print(f" - [{status}] {item}")

def check_off_items():
    print("\n=== Check Off Items ===")
    all_ingredients = []

    for day, meals in meal_plan.items():
        for meal_type, meal_name in meals.items():
            if meal_name and meal_name in saved_recipes:
                for ingredient in saved_recipes[meal_name]:
                    if ingredient not in all_ingredients:
                        all_ingredients.append(ingredient)
    
    for item in extras_list:
        if item not in all_ingredients:
            all_ingredients.append(item)

    if not all_ingredients:
        print("\nNo ingredients found!")
        return
    
    while True:
        print("\nYour Grocery List: (✓ = already have it): ")
        for i, ingredient in enumerate(all_ingredients, 1):
            status = "✓" if ingredient in checked_off else " "
            print(f"{i}. [{status}] {ingredient}")

        print("\n0. Go Back")
        print("Enter the number corresponding to the item you want to check off: ")
        print("Type 'clear' to reset all checked off items.")

        choice = input("\nEnter your choice: ")

        if choice == "0":
            return
        elif choice.lower() == "clear":
            checked_off.clear()
            save_data()
            print("All items have been unchecked.")
        elif choice.isdigit() and int(choice) in range(1, len(all_ingredients) + 1):
            item = all_ingredients[int(choice) - 1]
            if item in checked_off:
                checked_off.remove(item)
                print(f"'{item}' unchecked!")
            else: 
                checked_off.append(item)
                print(f"'{item}' checked off!")
            save_data()
        else:
            print("Invalid choice. Please try again.")

def export_grocery_list():
    print("\n=== Export Grocery List ===")
    categorized = {}

    for day, meals in meal_plan.items():
        for meal_type, meal_name in meals.items():
            if meal_name and meal_name in saved_recipes:
                for ingredient in saved_recipes[meal_name]:
                    category = get_ingredient_category(ingredient)
                    if category not in categorized:
                        categorized[category] = []
                    if ingredient not in categorized[category]:
                        categorized[category].append(ingredient)
    if not categorized and not extras_list:
        print("\nNo ingredients found! Make sure your meals have saved recipes.")
        return
    
    filename = input("Enter filename to export to (e.g. 'grocery_list.txt'): ")
    if filename.strip() == "":
        print("Defaulting to 'grocery_list.txt'")
        filename = "grocery_list.txt"
    filename = filename.strip().replace(" ", "_").replace("/", "-").replace("\\", "-").replace(":", "-")
    if not filename.endswith(".txt"):
        filename += ".txt"
    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "w",encoding="utf-8") as f:
        f.write("==== Grocery List ====\n")
        f.write(f"Generated on: {__import__('datetime').datetime.now().strftime('%B %d, %Y')}\n")
        f.write("=" * 30 + "\n")

        for category, ingredients in sorted(categorized.items()):
            f.write(f"\n{category}:\n")
            for ingredient in ingredients:
                status = "✓" if ingredient in checked_off else " "
                f.write(f" - [{status}] {ingredient}\n")
        
        if extras_list:
            f.write("\nExtras/Spices:\n")
            for item in extras_list:
                status = "✓" if item in checked_off else " "
                f.write(f" - [{status}] {item}\n")

    print(f"Grocery list exported successfully to '{filename}'!")
    print(f"Saved to: {filepath}")
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

def delete_meal():
    print("\n=== Delete a Meal ===")
    print("Select a day:")
    for i, day in enumerate(days, 1):
        print(f"{i}. {day}")
    print("0. Go Back")

    day_choice = input("\nEnter the number corresponding to the day: ")

    if day_choice == "0":
        return
    if not day_choice.isdigit() or int(day_choice) < 1 or int(day_choice) > len(days):
        print("Invalid choice. Please try again.")
        return
    selected_day = days[int(day_choice) - 1]

    print(f"\nCurrent meals for {selected_day}:")
    print(f"1. Breakfast: {meal_plan[selected_day]['Breakfast'] or 'Not Set'}")
    print(f"2. Lunch: {meal_plan[selected_day]['Lunch'] or 'Not Set'}")
    print(f"3. Dinner: {meal_plan[selected_day]['Dinner'] or 'Not Set'}")
    print("0. Go Back")

    meal_choice = input("\nEnter the number corresponding to the meal to delete: ")
    if meal_choice == "0":
        return
    meal_types = {"1": "Breakfast", "2": "Lunch", "3": "Dinner"}
    if meal_choice not in meal_types:
        print("Invalid choice. Please try again.")
        return
    
    selected_meal = meal_types[meal_choice]
    
    if meal_plan[selected_day][selected_meal] is None:
        print(f"{selected_meal.capitalize()} for {selected_day} is already empty!")
        return
    
    confirm = input(f"Are you sure you want to delete {selected_meal} for {selected_day}? (yes/no): ").lower()
    if confirm == "yes":
        meal_plan[selected_day][selected_meal] = None
        save_data()
        print(f"{selected_meal.capitalize()} for {selected_day} deleted successfully!")
    else:
        print("Delete action cancelled.")

def main():
    load_data()
    while True:
        print("\n======Grocery-Meal-Planner======")
        print("Welcome to the Grocery Meal Planner!")
        print("This program will help you plan your grocery shopping and meals for the week.")
        print("1. View Weekly Meal Plan")
        print("2. Add a Meal to the Meal Plan")
        print("3. Delete a Meal from the Meal Plan")
        print("4. View Saved Recipes")
        print("5. Add a New Recipe")
        print("6. Edit a Recipe/Delete a Recipe")
        print("7. View Grocery List")
        print("8. Check Off Items")
        print("9. Export Grocery List")
        print("10. Manage Extras/Spices")
        print("11. Override Ingredient Category")
        print("12. Clear Weekly Plan")
        print("13. Exit")

        choice = input("\nPlease enter your choice (1-13): ")

        if choice == "1":
            view_meal_plan()
        elif choice == "2":
            add_meal()
        elif choice == "3":
            delete_meal()
        elif choice == "4":
            view_recipes()
        elif choice == "5":
            add_recipe()
        elif choice == "6":
            edit_recipe()
        elif choice == "7":
            view_grocery_list()
        elif choice == "8":
            check_off_items()
        elif choice == "9":
            export_grocery_list()
        elif choice == "10":
            manage_extras()
        elif choice == "11":
            override_category()
        elif choice == "12":
            clear_meal_plan()
        elif choice == "13":
            confirm = input("Are you sure you want to exit? (yes/no): ")
            if confirm.lower() == "yes":
                print("Goodbye!")
                break
            else:
                print("Exit cancelled, Returning to main menu...")
        else:
            print("Invalid choice. Please try again.")

main()