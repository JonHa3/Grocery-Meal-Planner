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

        if choice == '7':
            print("Thank you for using the Grocery Main Planner. Goodbye!")
            break
        else: 
            print("This feature is currently under development. Please check back later.")

main()