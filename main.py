def main():
    while True:
        print("======Grocery-Main-Planner======")
        print("Welcome to the Grocery Main Planner!")
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
            print("Coming soon!")
        elif choice == "3":
            view_recipes()
        elif choice == "4":
            add_recipe()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Option coming soon!")    

saved_recipes = {}
def add_recipe():
    name = input("Enter the name of the recipe: ")
    ingredients = input("Enter the ingredients (comma separated): ")
    ingredients_list = [i.strip() for i in ingredients.split(',')]
    saved_recipes[name] = ingredients_list
    print(f"\n'{name}' added successfully!")

def view_recipes():
    if not saved_recipes:
        print("\nNo recipes saved yet.")
    else:
        print("\n=== Saved Recipes ===")
        for meal, ingredients in saved_recipes.items():
            print(f"\n{meal}: ")
            for ingredient in ingredients:
                print(f" - {ingredient}")

main()