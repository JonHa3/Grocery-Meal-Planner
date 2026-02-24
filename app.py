import tkinter as tk
from tkinter import font
import json
import os
from categories import categories, get_category

# --- Constants ------------------------------------------------------------------------
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

# Colors 
BG_MAIN = "#D4DE95"
BG_CONTENT = "#D4DE95"
BG_SIDEBAR = "#3D4127"
BG_CARD = "#FFFFFF"
BTN_COLOR = "#636B2F"
BTN_HOVER = "#4a5022"
TEXT_LIGHT = "#FFFFFF"
TEXT_DARK = "#2C2C2C"
HEADER_BG = "#3D4127"

# Fonts 
FONT_TITLE = ("Helvetica", 22, "bold")
FONT_SUBTITLE = ("Helvetica", 14, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_SMALL = ("Helvetica", 9)
FONT_BTN = ("Helvetica", 11, "bold")

# Data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# ---- Data --------------------------------------------------------------------------------
saved_recipes = {}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# Categories and their associated keywords for ingredient classification

meal_plan = {day: { "Breakfast": None, "Lunch": None, "Dinner": None} for day in days}
# Initialize meal plan with days of the week and meal types set to None

extras_list = []
checked_off = []
category_overrides = {}


def load_data():
    # Load data from JSON file if it exists, otherwise start with empty/default values
    global saved_recipes, meal_plan, extras_list, checked_off, category_overrides
    if os.path.exists(DATA_FILE):
        # Try to load data and handle potential JSON decoding errors or other exceptions gracefully
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
    # Save current data to JSON file, ensuring that all relevant information is stored for future sessions
    data = {
        "recipes": saved_recipes,
        "meal_plan": meal_plan,
        "extras": extras_list,
        "checked_off": checked_off,
        "category_overrides": category_overrides
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {e}")


def get_ingredient_category(ingredient):
    # First check if there is a user override for this ingredient's category, if so return that. Otherwise, use the get_category function to determine the category based on keywords.
    if ingredient in category_overrides:
        return category_overrides[ingredient]
    return get_category(ingredient)

# ------ App --------------------------------------------------------------------------------
class MealPlannerApp:

    nav_items = [
        ("🏠  Home", "home"),
        ("📅  Meal Planner", "planner"),
        ("📖  Recipes", "recipes"),
        ("🛒  Grocery List", "grocery"),
        ("🧂  Extras", "extras"),
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Grocery & Meal Planner")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        load_data()
        self._build_layout()
        self.show_frame("home")

    def _build_layout(self):
        # Header
        self.header = tk.Frame(self.root, bg=HEADER_BG, height=60)
        self.header.pack(fill='x', side='top')
        self.header.pack_propagate(False)

        tk.Label(
            self.header,
            text="🥗 Grocery & Meal Planner",
            bg=HEADER_BG,
            fg=TEXT_LIGHT,
            font=FONT_TITLE
        ).pack(side='left', padx=20, pady=10)

        self.body = tk.Frame(self.root, bg=BG_CONTENT)
        self.body.pack(fill='both', expand=True)

        self.sidebar = tk.Frame(self.body, bg=BG_SIDEBAR, width=200)
        self.sidebar.pack(fill='y', side='left')
        self.sidebar.pack_propagate(False)

        self.nav_buttons = {}
        for label, frame_name in self.nav_items:
            btn = tk.Button(
                self.sidebar,
                text=label,
                font=FONT_BTN,
                bg=BG_SIDEBAR,
                fg=TEXT_LIGHT,
                activebackground=BTN_HOVER,
                activeforeground=TEXT_LIGHT,
                bd=0,
                anchor='w',
                padx=20,
                pady=8,
                cursor="hand2",
                command=lambda name=frame_name: self.show_frame(name)
            )
            btn.pack(fill='x',pady=2)
            self.nav_buttons[frame_name] = btn

        # --- Main Content Area ---
        self.content = tk.Frame(self.body, bg=BG_CONTENT)
        self.content.pack(fill='both', expand=True, side='left')

        # --- Frames ---
        self.frames = {}
        for frame_name in ["home", "planner", "recipes", "grocery", "extras"]:
            frame = tk.Frame(self.content, bg=BG_CONTENT)
            self.frames[frame_name] = frame
            frame.place(relwidth=1, relheight=1)
        
        self._build_home()
        self._build_planner()
        self._build_recipes()

    def show_frame(self, name):
        for frame_name, btn in self.nav_buttons.items():
            btn.configure(bg=BG_SIDEBAR)
        if name in self.nav_buttons:
            self.nav_buttons[name].configure(bg=BTN_COLOR)
        self.frames[name].lift()
    
    def _build_home(self):
        frame = self.frames["home"]

        tk.Label(
            frame,
            text="Welcome to your Grocery & Meal Planner!",
            bg=BG_CONTENT,
            fg=TEXT_DARK,
            font=FONT_TITLE
        ).pack(pady = (60,5))
        
        stats_frame = tk.Frame(frame, bg=BG_CONTENT)
        stats_frame.pack()

        stats = [
            ("📖", f"{len(saved_recipes)}", "Saved Recipes"),
            ("📅", f"{sum(1 for d in meal_plan.values() for m in d.values() if m)}", "Meals Planned"),
            ("🛒", f"{sum(len(saved_recipes.get(m, [])) for d in meal_plan.values() for m in d.values() if m and m in saved_recipes)}", "Ingredients"),
        ]

        for icon, count, label in stats:
            card = tk.Frame(stats_frame, bg=BG_CARD, padx=30, pady=20)
            card.pack(side='left', padx=15)
            tk.Label(card, text=icon, font=("Helvetica", 28), bg=BG_CARD).pack()
            tk.Label(card, text=count, font=FONT_TITLE, bg=BG_CARD, fg=BTN_COLOR).pack()
            tk.Label(card, text=label, font=FONT_BODY, bg=BG_CARD, fg=TEXT_DARK).pack() 

    def _build_planner(self):
        frame = self.frames["planner"]

        tk.Label(
            frame,
            text="Meal Planner",
            font=FONT_TITLE,
            bg=BG_CONTENT,
            fg=TEXT_DARK
        ).grid(row=0, column=0, columnspan=4, pady=(20,10), padx=20, sticky='w')      

        for col, header in enumerate(["Day", "Breakfast", "Lunch", "Dinner"]):
            tk.Label(
                frame,
                text=header,
                font=FONT_SUBTITLE,
                bg=BG_CONTENT,
                fg=BTN_COLOR
            ).grid(row=1, column=col, padx=20, pady=(0,10), sticky='w')

        for row, day in enumerate(days,2):     
            tk.Label(
                frame,
                text=day,
                font=FONT_BTN,
                bg=BG_CONTENT,
                fg=TEXT_DARK,
                width=10,
                anchor='w'
            ).grid(row=row, column=0, padx=20, pady=5, sticky='w')

            for col, meal_type in enumerate(["Breakfast", "Lunch", "Dinner"],1):
                meal = meal_plan[day][meal_type] or "Not Set"
                btn = tk.Button(
                    frame,
                    text=meal,
                    font=FONT_BODY,
                    bg=BG_CARD,
                    fg=TEXT_DARK,
                    activebackground=BTN_HOVER,
                    activeforeground=TEXT_LIGHT,
                    width=18,
                    anchor='w',
                    padx=10,
                    bd=1,
                    cursor="hand2",
                    command=lambda d=day, m=meal_type: self._edit_meal_popup(d, m)
                )
                btn.grid(row=row, column=col, padx=10, pady=5)

        frame.configure(bg=BG_CONTENT)

    def _edit_meal_popup(self, day, meal_type):
        popup = tk.Toplevel(self.root)
        popup.title(f"{day} - {meal_type.capitalize()}")
        popup.geometry("400x500")
        popup.resizable(False, False)
        popup.configure(bg=BG_CONTENT)
        popup.grab_set()

        tk.Label(
            popup,
            text=f"Set {meal_type.capitalize()} for {day}",
            font=FONT_SUBTITLE,
            bg=BG_CONTENT,
            fg=TEXT_DARK
        ).pack(pady=(20, 10))

        # Search bar
        tk.Label(
            popup,
            text="Search recipes:",
            font=FONT_BODY,
            bg=BG_CONTENT,
            fg=TEXT_DARK
        ).pack(anchor="w", padx=20)

        search_var = tk.StringVar()
        search_entry = tk.Entry(popup, textvariable=search_var, font=FONT_BODY, width=30)
        search_entry.pack(padx=20, pady=(0, 10))

        # Recipe listbox
        listbox_frame = tk.Frame(popup, bg=BG_CONTENT)
        listbox_frame.pack(fill='both', expand=True, padx=20)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')

        listbox = tk.Listbox(
            listbox_frame,
            font=FONT_BODY,
            selectbackground=BTN_COLOR,
            selectforeground=TEXT_LIGHT,
            height=10,
            yscrollcommand=scrollbar.set
        )
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview) 

        # Populate listbox with recipes
        def populate_listbox(filter_text=""):
            listbox.delete(0, tk.END)
            for recipe in sorted(saved_recipes.keys()):
                if filter_text.lower() in recipe.lower():
                    listbox.insert(tk.END, recipe)

        populate_listbox()

        # Search filter
        def on_search(*args):
            populate_listbox(search_var.get())

        search_var.trace_add("write",on_search)

        # Custom Meal Entry
        tk.Label(
            popup,
            text="Or enter custom meal:",
            font=FONT_BODY,
            bg=BG_CONTENT,
            fg=TEXT_DARK
        ).pack(anchor="w", padx=20, pady=(10, 0))

        custom_entry = tk.Entry(popup, font=FONT_BODY, width=30)
        custom_entry.pack(padx=20, pady=(0, 10))

        # Buttons
        btn_frame = tk.Frame(popup, bg=BG_CONTENT)
        btn_frame.pack(pady=10)

        def save_meal():
            if custom_entry.get().strip():
                meal_name = custom_entry.get().strip()
            elif listbox.curselection():
                meal_name = listbox.get(listbox.curselection())
            else:
                return  # No selection or input, do nothing
            meal_plan[day][meal_type] = meal_name
            save_data()
            self._refresh_planner()
            popup.destroy()

        def clear_meal():
            meal_plan[day][meal_type] = None
            save_data()
            self._refresh_planner()
            popup.destroy()
        
        tk.Button(
            btn_frame,
            text="Save",
            font=FONT_BTN,
            bg=BTN_COLOR,
            fg=TEXT_LIGHT,
            padx=20,
            cursor="hand2",
            command=save_meal
        ).pack(side='left', padx=10)

        tk.Button(
            btn_frame,
            text="Clear",
            font=FONT_BTN,
            bg="#8B0000",
            fg=TEXT_LIGHT,
            padx=20,
            cursor="hand2",
            command=clear_meal
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=FONT_BTN,           
            bg=BG_CARD,
            fg=TEXT_DARK,
            padx=20,
            cursor="hand2",
            command=popup.destroy
        ).pack(side="left", padx=10)

    def _refresh_planner(self):
        # Refresh the meal planner view to reflect any changes made to the meal plan
        for widget in self.frames["planner"].winfo_children():
            widget.destroy()
        self._build_planner()


    def _build_recipes(self):
        frame = self.frames["recipes"]

        # Title and Add button
        top_frame = tk.Frame(frame, bg=BG_CONTENT)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

        tk.Label(
            top_frame,
            text="Recipes",
            font=FONT_TITLE,
            bg=BG_CONTENT,
            fg=TEXT_DARK
        ).pack(side="left")

        tk.Button(
            top_frame,
            text="+ Add Recipe",
            font=FONT_BTN,
            bg=BTN_COLOR,
            fg=TEXT_LIGHT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: print("Add Recipe functionality to be implemented")
        ).pack(side="right")

        # Left side: Recipe list
        left_frame = tk.Frame(frame, bg=BG_CONTENT, width=300)
        left_frame.grid(row=1, column=0, sticky="ns", padx=(20, 10), pady=10)
        left_frame.grid_propagate(False)

        # Search bar
        tk.Label(
            left_frame,
            text="Search recipes:",
            font=FONT_BODY,
            bg=BG_CONTENT,
            fg=TEXT_DARK
        ).pack(anchor="w")

        search_var = tk.StringVar()
        search_entry = tk.Entry(left_frame, textvariable=search_var, font=FONT_BODY, width=30)
        search_entry.pack(anchor="w", pady=(0, 10))

        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(left_frame)
        scrollbar.pack(side='right', fill='y')

        recipe_listbox = tk.Listbox(
            left_frame,
            font=FONT_BODY,
            selectbackground=BTN_COLOR,
            selectforeground=TEXT_LIGHT,
            yscrollcommand=scrollbar.set,
            height=20,
            width=30
        )
        
        recipe_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=recipe_listbox.yview)

        # Populate listbox with recipes
        def populate_listbox(filter_text=""):
            recipe_listbox.delete(0, tk.END)
            for recipe in sorted(saved_recipes.keys()):
                if filter_text.lower() in recipe.lower():
                    recipe_listbox.insert(tk.END, recipe)

        populate_listbox()

        def on_search(*args):
            populate_listbox(search_var.get())
        
        search_var.trace("w", on_search)

        # Right side: Recipe details (to be implemented)
        right_frame = tk.Frame(frame, bg=BG_CARD, padx=20, pady=20)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)

        selected_label = tk.Label(
            right_frame,
            text="Select a recipe to view details",
            font=FONT_SUBTITLE,
            bg=BG_CARD,
            fg=TEXT_DARK
        )
        selected_label.pack(anchor="w", pady=(0, 10))

        ingredients_frame = tk.Frame(right_frame, bg=BG_CARD)
        ingredients_frame.pack(fill='both', expand=True, anchor="w")

        # Action buttons (Edit, Delete) - functionality to be implemented
        action_btn_frame = tk.Frame(right_frame, bg=BG_CARD)
        action_btn_frame.pack(pady=(10,0), anchor="w")

        edit_btn = tk.Button(
            action_btn_frame,
            text="Edit Recipe",
            font=FONT_BTN,
            bg=BTN_COLOR,
            fg=TEXT_LIGHT,
            padx=15,
            pady=5,
            cursor="hand2",
            state="disabled",
        )
        edit_btn.pack(side="left", padx=(0,10))

        delete_btn = tk.Button(
            action_btn_frame,
            text="Delete Recipe",   
            font=FONT_BTN,
            bg="#8B0000",
            fg=TEXT_LIGHT,
            padx=15,
            pady=5,
            cursor="hand2",
            state="disabled",
        )
        delete_btn.pack(side="left")

        def show_ingredients(event):
            # Clear previous details
            for widget in ingredients_frame.winfo_children():
                widget.destroy()

            # Get selected recipe
            if not recipe_listbox.curselection():
                return
            
            recipe_name = recipe_listbox.get(recipe_listbox.curselection())
            selected_label.config(text=recipe_name)

            # Display ingredients
            ingredients = saved_recipes.get(recipe_name, [])
            print(type(ingredients), ingredients)  # Debugging line to check the structure of ingredients
            if isinstance(ingredients[0], list):
                ingredients = ingredients[0]
            for ingredient in ingredients:
                tk.Label(
                    ingredients_frame,
                    text=f"• {ingredient}",
                    font=FONT_BODY,
                    bg=BG_CARD,
                    fg=TEXT_DARK,
                    anchor="w"
                ).pack(pady=2, anchor="w")
                

            # Enable action buttons
            edit_btn.config(
                state="normal",
                command=lambda: self._edit_recipe_popup(recipe_name)
            )
            delete_btn.config(
                state="normal",
                command=lambda: self._delete_recipe(recipe_name)
            )
        recipe_listbox.bind("<<ListboxSelect>>", show_ingredients)
        frame.grid_columnconfigure(1, weight=1)





    # ----- Run --------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()