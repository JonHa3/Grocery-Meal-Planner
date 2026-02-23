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
BG_CARD = "white"
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
        
        self.build_home()

    def show_frame(self, name):
        for frame_name, btn in self.nav_buttons.items():
            btn.configure(bg=BG_SIDEBAR)
        if name in self.nav_buttons:
            self.nav_buttons[name].configure(bg=BTN_COLOR)
        self.frames[name].lift()
    
    def build_home(self):
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

    # ----- Run --------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()