import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, scrolledtext
import json
import requests
import os
from dotenv import load_dotenv
import ast

# Load environment variables from .env file
load_dotenv()
# Your OpenAI API key
API_KEY = os.getenv('OPENAI_API_KEY')

class SmartKitchenAssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.family_profiles = {}  # Initialize family_profiles
        self.load_profiles()  # Load profiles on startup

        self.recipe = {"title": "Select Recipe",
                        "ingredients": "None Yet",
                        "instructions": "None Yet",
                        "servings": "4",  # Placeholder; adjust based on your needs
                        "prep_time": "10 minutes",  # Placeholder; adjust based on your needs
                        "cook_time": "15 minutes" # Placeholder; adjust based on your needs
                        }  
        self.family_name_variable = tk.StringVar()
        self.member_name_variable = tk.StringVar()
        self.kitchen_name_variable = tk.StringVar()
        self.recipe_type_variable = tk.StringVar()
        self.recipe_complexity_variable = tk.StringVar()
        self.recipe_rating_variable = tk.StringVar()
        self.recipe_main_ing_variable = tk.StringVar()
        self.member_age_variable = tk.StringVar()
        self.dietary_restrictions_variable = tk.StringVar()
        self.favorite_foods_variable = tk.StringVar()

        self.family_selected = 0

        self.title("Smart Kitchen Assistant")

        # Create the main content frame
        self.main_content_frame = tk.Frame(self)
        self.main_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Show the welcome screen initially
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Display the Welcome Screen."""
        # Clear the main content area
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()


        # Placeholder for the logo image
        logo_image = tk.PhotoImage(file="Project/HomeScreen.png")  # Uncomment and set your logo path
        logo_label = tk.Label(self.main_content_frame, image=logo_image)
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Family Dropdown
        family_dropdown_label = tk.Label(self.main_content_frame, text="Select Family: ", font=("Helvetica", 14, 'bold'))
        family_dropdown_label.grid(row=1,column=0,padx=10, pady=10)
        self.family_name_variable = tk.StringVar()
        self.family_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.family_name_variable, state='readonly', font=("Helvetica", 14))
        self.family_dropdown['values'] = list(self.family_profiles.keys())  # Load family names
        self.family_dropdown.set("Family")  # Default text
        self.family_dropdown.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

                # Set the last selected family if it exists
        if self.family_selected:
            self.family_name_variable.set(self.last_family)
            self.update_family_dropdown()  # Update dropdowns after loading profiles

        # Buttons
        self.ws_button_frame = tk.Frame(self.main_content_frame, relief='ridge', borderwidth=2)
        self.ws_button_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        select_button = tk.Button(self.ws_button_frame, text="Select", command=self.select_family, font=("Helvetica", 14))
        select_button.grid(row=0, column=0, padx=50, pady=10)

        # Edit and Select Buttons
        edit_button = tk.Button(self.ws_button_frame, text="Edit", command=self.edit_profile, font=("Helvetica", 14))
        edit_button.grid(row=0, column=1, padx=50, pady=10)

        # "+" Button
        add_family_button = tk.Button(self.ws_button_frame, text="Add", command=self.add_family, font=("Helvetica", 14))
        add_family_button.grid(row=0, column=2, padx=50, pady=10)

        # Remove Button
        remove_button = tk.Button(self.ws_button_frame, text="Remove", command=self.remove_family, font=("Helvetica", 14))
        remove_button.grid(row=0, column=3, padx=50, pady=10)

    def show_main_menu_screen(self):
        """Display the Main Menu Screen."""
        # Clear the main content area
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        
        # Home Button
        home_button = tk.Button(self.main_content_frame, text="Home", command=self.show_welcome_screen, font=("Helvetica", 14))
        home_button.grid(row=0, column=0, padx=10, pady=10)

        # Edit Family Button
        edit_fam_button = tk.Button(self.main_content_frame, text="Edit Family", command=self.show_edit_profile_screen, font=("Helvetica", 14))
        edit_fam_button.grid(row=0, column=3, padx=10, pady=10)

        # Family Name Label
        family_name_label = tk.Label(self.main_content_frame, text=f"Stiring Up Some Recipes for the {self.family_name} family!", font=("Helvetica", 16, "bold"))
        family_name_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Recipe Type Dropdown
        recipe_type_label = tk.Label(self.main_content_frame, text="Recipe Type:", font=("Helvetica", 14))
        recipe_type_label.grid(row=2, column=0, padx=10, pady=10)

        self.recipe_type_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.recipe_type_variable, state='readonly', font=("Helvetica", 12))
        self.recipe_type_dropdown['values'] = ("Any", "Weekday Dinner", "Weekend Dinner", "Thanksgiving", "Birthday", "Football Game")
        self.recipe_type_dropdown.set("Any")
        self.recipe_type_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.recipe_type_dropdown.bind("<<ComboboxSelected>>", lambda event: self.sort_recipes())  # Bind event

        # Recipe Complexity Dropdown
        recipe_complexity_label = tk.Label(self.main_content_frame, text="Recipe Complexity:", font=("Helvetica", 14))
        recipe_complexity_label.grid(row=3, column=0, padx=10, pady=10)

        self.recipe_complexity_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.recipe_complexity_variable, state='readonly', font=("Helvetica", 12))
        self.recipe_complexity_dropdown['values'] = ("Any", "Make it Easy", "Challenge Me", "Cook to Impress")
        self.recipe_complexity_dropdown.set("Any")
        self.recipe_complexity_dropdown.grid(row=3, column=1, padx=10, pady=10)
        self.recipe_complexity_dropdown.bind("<<ComboboxSelected>>", lambda event: self.sort_recipes())  # Bind event

        # Recipe Rating Dropdown
        recipe_rating_label = tk.Label(self.main_content_frame, text="Recipe Rating:", font=("Helvetica", 14))
        recipe_rating_label.grid(row=2, column=2, padx=10, pady=10)

        self.recipe_rating_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.recipe_rating_variable, state='readonly', font=("Helvetica", 12))
        self.recipe_rating_dropdown['values'] = ("Any", "1", "2", "3", "4", "5", "N/R")
        self.recipe_rating_dropdown.set("Any")
        self.recipe_rating_dropdown.grid(row=2, column=3, padx=10, pady=10)
        self.recipe_rating_dropdown.bind("<<ComboboxSelected>>", lambda event: self.sort_recipes())  # Bind event

        # Recipe Complexity Dropdown
        recipe_main_ing_label = tk.Label(self.main_content_frame, text="Recipe Main Ingredient:", font=("Helvetica", 14))
        recipe_main_ing_label.grid(row=3, column=2, padx=10, pady=10)

        self.recipe_main_ing_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.recipe_main_ing_variable, state='readonly', font=("Helvetica", 12))
        self.recipe_main_ing_dropdown['values'] = ("Any", "Chicken", "Beef", "Pasta")
        self.recipe_main_ing_dropdown.set("Any")
        self.recipe_main_ing_dropdown.grid(row=3, column=3, padx=10, pady=10)
        self.recipe_main_ing_dropdown.bind("<<ComboboxSelected>>", lambda event: self.sort_recipes())  # Bind event


        # Recipe List Label
        recipe_listbox_label = tk.Label(self.main_content_frame, text="Title\t\t\tMain Ingredient\t\tComplexity\t\tType\t\tRating", font=("Helvetica", 12))
        recipe_listbox_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        # Recipe List
        self.recipe_listbox = tk.Listbox(self.main_content_frame, height=10, width=100, font=("Courier New", 12))
        self.recipe_listbox.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Buttons
        self.mm_button_frame = tk.Frame(self.main_content_frame, relief='ridge', borderwidth=2)
        self.mm_button_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        get_recipe_button = tk.Button(self.mm_button_frame, text="Get Recipe", command=self.get_recipe, font=("Helvetica", 14))
        get_recipe_button.grid(row=0, column=0, padx=15, pady=10)

        make_recipe_button = tk.Button(self.mm_button_frame, text="Make Recipe", command=self.make_recipe, font=("Helvetica", 14))
        make_recipe_button.grid(row=0, column=1, padx=15, pady=10)

        remove_recipe_button = tk.Button(self.mm_button_frame, text="Remove Item", command=self.remove_recipe, font=("Helvetica", 14))
        remove_recipe_button.grid(row=0, column=2, padx=15, pady=10)

        get_meal_plan_button = tk.Button(self.mm_button_frame, text="Get Meal Plan", command=self.get_meal_plan, font=("Helvetica", 14))
        get_meal_plan_button.grid(row=1, column=0, padx=15, pady=10)

        get_meal_plan_button = tk.Button(self.mm_button_frame, text="View Meal Plan", command=self.view_meal_plan, font=("Helvetica", 14))
        get_meal_plan_button.grid(row=1, column=1, padx=15, pady=10)

        get_grocery_list_button = tk.Button(self.mm_button_frame, text="Get Grocery List", command=self.get_grocery_list, font=("Helvetica", 14))
        get_grocery_list_button.grid(row=1, column=2, padx=15, pady=10)


        self.populate_recipe_list()  

    def show_edit_profile_screen(self):
        """Display the Edit Profile Screen for the selected family."""
        # Clear the main content area
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Home Button
        home_button = tk.Button(self.main_content_frame, text="Home", command=self.show_welcome_screen, font=("Helvetica", 14))
        home_button.grid(row=0, column=0, padx=10, pady=10)

        # Go Cook Button
        go_cook_button = tk.Button(self.main_content_frame, text="Go Cook", command=self.select_family, font=("Helvetica", 14))
        go_cook_button.grid(row=0, column=3, padx=10, pady=10)

        # Family Name Label
        family_name_label = tk.Label(self.main_content_frame, text=f"Learning More about the {self.family_name} Family", font=("Helvetica", 16, "bold"))
        family_name_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Member Name Dropdown
        member_name_label = tk.Label(self.main_content_frame, text="Member:", font=("Helvetica", 14))
        member_name_label.grid(row=2, column=0, padx=10, pady=10)

        self.member_name_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.member_name_variable, state='readonly', font=("Helvetica", 12))
        self.populate_member_names_dropdown()  # Populate this dropdown
        self.member_name_dropdown.set("All")  # Default to "All"
        self.member_name_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.member_name_dropdown.bind("<<ComboboxSelected>>", lambda event: self.filter_members())  # Bind event

        # Member Age Dropdown
        member_age_label = tk.Label(self.main_content_frame, text="Member Age:", font=("Helvetica", 14))
        member_age_label.grid(row=3, column=0, padx=10, pady=10)

        self.member_age_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.member_age_variable, state='readonly', font=("Helvetica", 12))
        age_ranges = ["All", "0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71+"]
        self.member_age_dropdown['values'] = age_ranges
        self.member_age_dropdown.set("All")  # Default to "All"
        self.member_age_dropdown.grid(row=3, column=1, padx=10, pady=10)
        self.member_age_dropdown.bind("<<ComboboxSelected>>", lambda event: self.filter_members())  # Bind event

        # Dietary Restrictions Dropdown
        dietary_restrictions_label = tk.Label(self.main_content_frame, text="Dietary Restrictions:", font=("Helvetica", 14))
        dietary_restrictions_label.grid(row=2, column=2, padx=10, pady=10)

        self.dietary_restrictions_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.dietary_restrictions_variable, state='readonly', font=("Helvetica", 12))
        self.populate_dietary_restrictions_dropdown()  # Populate this dropdown
        self.dietary_restrictions_dropdown.set("All")  # Default to "All"
        self.dietary_restrictions_dropdown.grid(row=2, column=3, padx=10, pady=10)
        self.dietary_restrictions_dropdown.bind("<<ComboboxSelected>>", lambda event: self.filter_members())  # Bind event

        # Favorite Foods Dropdown
        favorite_foods_label = tk.Label(self.main_content_frame, text="Favorite Foods:", font=("Helvetica", 14))
        favorite_foods_label.grid(row=3, column=2, padx=10, pady=10)

        self.favorite_foods_dropdown = ttk.Combobox(self.main_content_frame, textvariable=self.favorite_foods_variable, state='readonly', font=("Helvetica", 12))
        self.populate_favorite_foods_dropdown()  # Populate this dropdown
        self.favorite_foods_dropdown.set("All")  # Default to "All"
        self.favorite_foods_dropdown.grid(row=3, column=3, padx=10, pady=10)
        self.favorite_foods_dropdown.bind("<<ComboboxSelected>>", lambda event: self.filter_members())  # Bind event

        # Member List Label
        member_listbox_label = tk.Label(self.main_content_frame, text="Member\t\tAge\tDiet Restrictions\t\tFavorite Foods", font=("Helvetica", 12))
        member_listbox_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        # Member List
        self.member_listbox = tk.Listbox(self.main_content_frame, height=10, width=90, font=("Courier New", 12))
        self.member_listbox.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Buttons
        self.edit_button_frame = tk.Frame(self.main_content_frame, relief='ridge', borderwidth=2)
        self.edit_button_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        # Add Member Button
        add_member_button = tk.Button(self.edit_button_frame, text="Add Member", command=self.add_member, font=("Helvetica", 14))
        add_member_button.grid(row=6, column=0, padx=10, pady=10)

        # Remove Member Button
        edit_member_button = tk.Button(self.edit_button_frame, text="Edit Member", command=self.edit_member, font=("Helvetica", 14))
        edit_member_button.grid(row=6, column=1, padx=10, pady=10)

        # Remove Member Button
        remove_member_button = tk.Button(self.edit_button_frame, text="Remove Member", command=self.remove_member, font=("Helvetica", 14))
        remove_member_button.grid(row=6, column=2, padx=10, pady=10)

        self.populate_member_list()

    def populate_member_names_dropdown(self):
        """Populate the member name dropdown with all family members."""
        family_name = self.family_name_variable.get()
        if family_name in self.family_profiles:
            members = [member['name'] for member in self.family_profiles[family_name]['members']]
            self.member_name_dropdown['values'] = ["All"] + members  # Include "All" option

    def populate_dietary_restrictions_dropdown(self):
        """Populate the dietary restrictions dropdown with all unique dietary restrictions."""
        family_name = self.family_name_variable.get()
        if family_name in self.family_profiles:
            # Gather all unique dietary restrictions from family members
            dietary_restrictions = set()
            for member in self.family_profiles[family_name]['members']:
                dietary_restrictions.update(member['dietary_restrictions'])
            self.dietary_restrictions_dropdown['values'] = ["All"] + list(dietary_restrictions)  # Include "All" option

    def populate_favorite_foods_dropdown(self):
        """Populate the favorite foods dropdown with all unique favorite foods."""
        family_name = self.family_name_variable.get()
        if family_name in self.family_profiles:
            # Gather all unique favorite foods from family members
            favorite_foods = set()
            for member in self.family_profiles[family_name]['members']:
                favorite_foods.update(member['favorite_foods'])
            self.favorite_foods_dropdown['values'] = ["All"] + list(favorite_foods)  # Include "All" option

    def filter_members(self):
        """Filter the members list based on dropdown selections."""
        family_name = self.family_name_variable.get()

        # Get the selected values
        selected_member_name = self.member_name_variable.get()
        selected_age_range = self.member_age_variable.get()
        selected_dietary_restriction = self.dietary_restrictions_variable.get()
        selected_favorite_food = self.favorite_foods_variable.get()

        # Clear the current entries in the listbox
        self.member_listbox.delete(0, tk.END)

        if family_name in self.family_profiles:
            filtered_members = self.family_profiles[family_name]['members']

            # Filter by member name
            if selected_member_name != "All":
                filtered_members = [member for member in filtered_members if member['name'] == selected_member_name]

            # Filter by age range
            if selected_age_range != "All":
                age_ranges = {
                    "0-10": (0, 10),
                    "11-20": (11, 20),
                    "21-30": (21, 30),
                    "31-40": (31, 40),
                    "41-50": (41, 50),
                    "51-60": (51, 60),
                    "61-70": (61, 70),
                    "71+": (71, float('inf'))  # Use infinity for 71+
                }
                min_age, max_age = age_ranges[selected_age_range]
                filtered_members = [member for member in filtered_members if min_age <= member['age'] <= max_age]

            # Filter by dietary restriction
            if selected_dietary_restriction != "All":
                filtered_members = [member for member in filtered_members if selected_dietary_restriction in member['dietary_restrictions']]

            # Filter by favorite food
            if selected_favorite_food != "All":
                filtered_members = [member for member in filtered_members if selected_favorite_food in member['favorite_foods']]

            # Populate the listbox with the filtered members
            for member in filtered_members:
                dietary_restrictions = ', '.join(member['dietary_restrictions']) if member['dietary_restrictions'] else "None"
                favorite_foods = ', '.join(member['favorite_foods']) if member['favorite_foods'] else "None"
                member_info = f"{member['name']:11} {member['age']:5} {"   "} {dietary_restrictions:20} {favorite_foods}"
                self.member_listbox.insert(tk.END, member_info)  # Insert formatted member information into the listbox

    def populate_recipe_list(self):
        """Populate the recipe listbox with the family's recipes."""
        family_name = self.family_name_variable.get()

        # Clear the current entries in the listbox
        self.recipe_listbox.delete(0, tk.END)

        self.populate_dropdowns()

        if family_name in self.family_profiles:
            recipes = self.family_profiles[family_name].get('recipes', [])

        # Populate the listbox with the filtered recipes
        for recipe in recipes:
            title = recipe['title'][:30]  # Take the first 20 characters
            recipe_info = f"{title:<29} {recipe['main_ingredient']:<20} {recipe['recipe_complexity']:<15} {recipe['recipe_type']:<20} {recipe['rating'] if recipe['rating'] else 'N/R'}"
            self.recipe_listbox.insert(tk.END, recipe_info)  # Insert formatted recipe information into the listbox

    def populate_member_list(self):
        """Populate the recipe listbox with sample data."""
        # Clear the current entries in the listbox
        self.member_listbox.delete(0, tk.END)

    # Populate the listbox with the filtered recipes
        for member in self.family_profiles[self.family_name]["members"]:

            dietary_restrictions = ', '.join(member['dietary_restrictions']) if member['dietary_restrictions'] else "None"
            favorite_foods = ', '.join(member['favorite_foods']) if member['favorite_foods'] else "None"

            member_info = f"{member['name']:11} {member['age']:5} {"   "} {dietary_restrictions:20} {favorite_foods}"
            self.member_listbox.insert(tk.END, member_info)  # Insert formatted recipe information into the listbox

    def populate_dropdowns(self):
        """Populate the dropdown menus with unique values from the recipes."""
        # Initialize sets to store unique values
        main_ingredients = set()
        complexities = set()
        types = set()

        # Gather values from existing recipes
        family_name = self.family_name_variable.get()
        if family_name in self.family_profiles:
            recipes = self.family_profiles[family_name]["recipes"]
            for recipe in recipes:
                main_ingredients.add(recipe['main_ingredient'])
                complexities.add(recipe['recipe_complexity'])
                types.add(recipe['recipe_type'])

        # Add defaults to sets if they are not already present
        default_main_ingredients = {"Anything", "Chicken", "Beef"}
        default_complexities = {"Any", "Easy", "Average", "Hard"}
        default_types = {"Any", "Dinner", "Lunch", "Breakfast", "Snack", "Comfort Food"}

        main_ingredients.update(default_main_ingredients)  # Add defaults
        complexities.update(default_complexities)  # Add defaults
        types.update(default_types)  # Add defaults

        # Convert sets to sorted lists
        self.recipe_main_ing_dropdown['values'] = sorted(main_ingredients)
        self.recipe_complexity_dropdown['values'] = sorted(complexities)
        self.recipe_type_dropdown['values'] = sorted(types)

        # Set default selections if available
        if self.recipe_main_ing_dropdown['values']:
            self.recipe_main_ing_dropdown.current(0)  # Set to first value as default
        if self.recipe_complexity_dropdown['values']:
            self.recipe_complexity_dropdown.current(0)  # Set to first value as default
        if self.recipe_type_dropdown['values']:
            self.recipe_type_dropdown.current(0)  # Set to first value as default

    def get_recipe(self):
        """Get recipe based on family member preferences and selected meal type."""

        member_info = self.family_profiles[self.family_name]["members"]
        num_members = len(member_info)
        saved_recipes = self.family_profiles[self.family_name]["recipes"]
        recipe_type = self.recipe_type_variable.get() 
        complexity = self.recipe_complexity_variable.get()
        main_ingredient = self.recipe_main_ing_variable.get()
            # Initialize empty lists for favorite foods and dietary restrictions
        favorite_foods_list = []
        dietary_restrictions_list = []
        ages_list = []

        if self.family_name and member_info:
            # Loop through each member's information
            for member in member_info: 
                # Extend the lists with the current member's favorite foods and dietary restrictions
                favorite_foods_list.extend(member.get('favorite_foods', []))  # Use get to avoid KeyError
                dietary_restrictions_list.extend(member.get('dietary_restrictions', []))  # Use get to avoid KeyError
                ages_list.extend(str(member.get('age', [])))  # Use get to avoid KeyError

            # Join the lists into a single string
            if len(favorite_foods_list) > 1:
                favorite_foods = ', '.join(favorite_foods_list)
            else:
                favorite_foods = favorite_foods_list
            if len(dietary_restrictions_list) > 1:
                dietary_restrictions = ', '.join(dietary_restrictions_list)
            else:
                dietary_restrictions = dietary_restrictions_list

            ages = ', '.join(ages_list)

            # Get saved recipes and their ratings
            recipe_format = saved_recipes[0]
            saved_recipes_text = ""
            for recipe in saved_recipes:
                saved_recipes_text += f"{recipe['title']} (Rating: {recipe['rating']})\n"


            # Construct the prompt for the recipe request
            prompt = (f"Please provide a {recipe_type} recipe that uses {main_ingredient} as a main ingredient and is {complexity} difficulty. "
                    f"This recipe needs to feed a family of {num_members} and should incoorporate their favorite foods: {favorite_foods} when possible. "
                    f"Also, take into account the family's dietary restrictions: {dietary_restrictions} and ages: {ages}. "
                    f"Here are some previously saved recipes and their ratings:\n{saved_recipes_text}, make sure not to suggest a recipe that's aleady available. "
                    f"Make sure to format the output as a string representation of a python dict with the following format:{recipe_format}. ")

            # Simulate receiving a recipe response
            self.request_recipe_from_api(prompt)

        else:
            messagebox.showerror("Error", "Please select a family, member, meal type, and complexity.")

    def remove_recipe(self):
        """Remove the selected recipe from the family's profile."""
        # Get the selected recipe from the listbox
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            selected_recipe_info = self.recipe_listbox.get(selected_index)
            recipe_title = selected_recipe_info[0:30].strip()  # Extract the title (first 20 characters)

            # Confirm removal
            confirmation = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{recipe_title}'?")
            if confirmation:
                family_name = self.family_name_variable.get()
                if family_name in self.family_profiles:
                    # Find and remove the recipe
                    recipes = self.family_profiles[family_name]["recipes"]
                    self.family_profiles[family_name]["recipes"] = [r for r in recipes if r['title'] != recipe_title]
                    
                    # Save changes to profiles
                    self.save_profiles()

                    # Refresh the recipe list
                    self.populate_recipe_list()
                    messagebox.showinfo("Success", f"Recipe '{recipe_title}' has been removed.")
                else:
                    messagebox.showerror("Error", "Family not found in profiles.")
        else:
            messagebox.showerror("Error", "Please select a recipe to remove.")

    def request_recipe_from_api(self, prompt):
        """Request a recipe from the OpenAI API using the provided prompt."""
        api_url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",  # Use the API_KEY variable
            "Content-Type": "application/json"
        }

        # Construct the request payload
        data = {
            "model": "gpt-4o",  # Specify the model you want to use
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,  # Adjust as necessary to get complete recipes
            "temperature": 0.7  # Adjust the creativity of the response
        }

        try:
            # Make the request to the OpenAI API
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the response
            response_data = response.json()
            recipe_text = response_data['choices'][0]['message']['content']

            # Assuming the response is formatted as a recipe text, you can further parse this if needed
            return self.parse_and_add_recipe(recipe_text)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None  # Return None in case of an error

    def parse_and_add_recipe(self, recipe_response):
        """Parse the API response and add the recipe to the selected family's profile."""
        
        # Assuming the recipe_response is a string with the following format:
        # Title: [Recipe Title]
        # Ingredients: [Ingredient 1, Ingredient 2, ...]
        # Instructions: [Step 1, Step 2, ...]
        # Complexity: [Complexity Level]
        # Type: [Recipe Type]
        # Rating: [Rating]

        # Find the index of the first '{'
        start_index = recipe_response.find('{')
        end_index = recipe_response.rfind('}')

        # Slice the string to get the dictionary part
        response = recipe_response[start_index:end_index+1]


        """Parse the API response and add the recipe to the selected family's profile."""
    
        try:
            # Convert the string representation of the dictionary to an actual dictionary
            recipe_dict = ast.literal_eval(response)

            # Extract components from the dictionary
            title = recipe_dict['title']
            main_ingredient = recipe_dict['main_ingredient']
            recipe_complexity = recipe_dict['recipe_complexity']

            if len(recipe_complexity) > 15:
                recipe_complexity = recipe_complexity.split(' ')[0]

            recipe_type = recipe_dict['recipe_type']
            rating = recipe_dict['rating'] if recipe_dict['rating'] is not None else None
            
            # Extract ingredients and instructions
            ingredients = recipe_dict['ingredients']  # This is already a list of dictionaries
            instructions = recipe_dict['instructions']  # This is already a list of strings

            # Create the new recipe dictionary
            new_recipe = {
                "title": title[0:29].strip(),
                "main_ingredient": main_ingredient,
                "recipe_complexity": recipe_complexity,
                "recipe_type": recipe_type,
                "rating": rating,
                "ingredients": ingredients,  # Already in the correct format
                "instructions": instructions  # Already in the correct format
            }

            # Add the new recipe to the family's profile
            family_name = self.family_name_variable.get()
            if family_name in self.family_profiles:
                self.family_profiles[family_name]["recipes"].append(new_recipe)
                self.save_profiles()  # Save changes


                self.populate_recipe_list()
                messagebox.showinfo("Success", f"Recipe '{title}' added to {family_name}'s profile.")
            else:
                messagebox.showerror("Error", "Family not found in profiles.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse and add recipe: {e}")

    def get_default_recipes(self):
        """Return a list of default recipes."""
        return [
            {
                "title": "Chicken Wings",
                "main_ingredient": "Chicken",
                "recipe_complexity": "Make it Easy",
                "recipe_type": "Football Game",
                "rating": 5,
                "ingredients": [
                    {"item": "Chicken Wings", "quantity": "500g"},
                    {"item": "Hot Sauce", "quantity": "50ml"},
                    {"item": "Butter", "quantity": "30g"},
                    {"item": "Garlic Powder", "quantity": "1 tsp"},
                ],
                "instructions": [
                    "Preheat your oven to 200°C (400°F).",
                    "In a bowl, mix hot sauce, melted butter, and garlic powder.",
                    "Toss chicken wings in the sauce mixture to coat evenly.",
                    "Place wings on a baking tray and bake for 30-40 minutes until crispy."
                ]
            },
            {
                "title": "Hamburgers",
                "main_ingredient": "Beef",
                "recipe_complexity": "Challenge Me",
                "recipe_type": "Weekend Dinner",
                "rating": 4,
                "ingredients": [
                    {"item": "Ground Beef", "quantity": "250g"},
                    {"item": "Burger Buns", "quantity": "2"},
                    {"item": "Cheddar Cheese", "quantity": "2 slices"},
                    {"item": "Lettuce", "quantity": "2 leaves"},
                    {"item": "Tomato", "quantity": "1, sliced"},
                    {"item": "Onion", "quantity": "1, sliced"},
                ],
                "instructions": [
                    "Form the ground beef into patties.",
                    "Season with salt and pepper.",
                    "Grill or pan-fry the patties for about 5 minutes per side.",
                    "Assemble the burger with buns, cheese, lettuce, tomato, and onion."
                ]
            },
            {
                "title": "Mac and Cheese",
                "main_ingredient": "Pasta",
                "recipe_complexity": "Make it Easy",
                "recipe_type": "Weekday Dinner",
                "rating": None,
                "ingredients": [
                    {"item": "Macaroni", "quantity": "200g"},
                    {"item": "Cheddar Cheese", "quantity": "150g"},
                    {"item": "Milk", "quantity": "1 cup"},
                    {"item": "Butter", "quantity": "2 tbsp"},
                    {"item": "Flour", "quantity": "2 tbsp"},
                ],
                "instructions": [
                    "Cook macaroni according to package instructions.",
                    "In a saucepan, melt butter and whisk in flour to make a roux.",
                    "Gradually add milk, stirring until thickened.",
                    "Stir in cheese until melted, then mix with cooked macaroni."
                ]
            },
        ]  

    def make_recipe(self):
        """Show the details of the selected recipe in a popup."""
        # Get the selected recipe from the listbox
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            selected_recipe_info = self.recipe_listbox.get(selected_index)
            # Extract the title from the selected entry
            recipe_title = selected_recipe_info[0:30].strip()  # Assuming the title is the first word

            # Find the full recipe details
            recipes = self.family_profiles[self.family_name].get("recipes", [])
            recipe = next((r for r in recipes if r['title'] == recipe_title), None)

            if recipe:
                # Create a new window for the recipe details
                recipe_window = tk.Toplevel(self)
                recipe_window.title(recipe['title'])

                # Title of the recipe
                title_label = tk.Label(recipe_window, text=recipe['title'], font=("Helvetica", 16, "bold"))
                title_label.pack(pady=10)

                # Ingredients
                ingredients_label = tk.Label(recipe_window, text="Ingredients:", font=("Helvetica", 14))
                ingredients_label.pack(anchor="w")
                ingredients_list = tk.Text(recipe_window, height=5, width=50, wrap=tk.WORD)
                for ingredient in recipe['ingredients']:
                    ingredients_list.insert(tk.END, f"{ingredient['quantity']} of {ingredient['item']}\n")
                ingredients_list.config(state=tk.DISABLED)  # Make it read-only
                ingredients_list.pack(pady=5)

                # Instructions
                instructions_label = tk.Label(recipe_window, text="Instructions:", font=("Helvetica", 14))
                instructions_label.pack(anchor="w")
                instructions_list = tk.Text(recipe_window, height=10, width=50, wrap=tk.WORD)
                for step in recipe['instructions']:
                    instructions_list.insert(tk.END, f"{step}\n")
                instructions_list.config(state=tk.DISABLED)  # Make it read-only
                instructions_list.pack(pady=5)

                # Rating Slider
                rating_label = tk.Label(recipe_window, text="Rate this Recipe:", font=("Helvetica", 14))
                rating_label.pack(pady=10)

                # Create a scale for the rating
                self.rating_slider = tk.Scale(recipe_window, from_=0, to=5, orient=tk.HORIZONTAL, tickinterval=1, length=300, sliderlength=20)
                # Set the default value based on the recipe rating
                current_rating = recipe['rating'] if recipe['rating'] is not None else 0  # N/R as 0
                self.rating_slider.set(current_rating)
                self.rating_slider.pack(pady=10)

                # Closing button
                close_button = tk.Button(recipe_window, text="Close", command=recipe_window.destroy, font=("Helvetica", 14))
                close_button.pack(pady=10)

                # Update the rating when the slider is adjusted
                def update_rating(value):
                    # Update the rating in the family_profiles
                    updated_rating = int(value) if value != '0' else None  # Convert to int, None for N/R
                    for r in self.family_profiles[self.family_name]['recipes']:
                        if r['title'] == recipe_title:
                            r['rating'] = updated_rating  # Update the rating
                            break
                    self.populate_recipe_list()  # Refresh the recipe list to show updated ratings

                self.rating_slider.bind("<Motion>", lambda event: update_rating(self.rating_slider.get()))

            else:
                messagebox.showerror("Error", "Recipe not found.")
        else:
            messagebox.showerror("Error", "Please select a recipe.")

    def sort_recipes(self):
        """Sort the recipes based on selected criteria."""
        recipe_type = self.recipe_type_variable.get()
        recipe_complexity = self.recipe_complexity_variable.get()
        recipe_rating = self.recipe_rating_variable.get()
        main_ingredient = self.recipe_main_ing_variable.get()


        filtered_recipes = self.family_profiles[self.family_name]["recipes"]

        # Filter based on selected criteria
        if recipe_type != "Any":
            filtered_recipes = [r for r in filtered_recipes if r["recipe_type"] == recipe_type]
        if recipe_complexity != "Any":
            filtered_recipes = [r for r in filtered_recipes if r["recipe_complexity"] == recipe_complexity]
        if recipe_rating != "Any":
            if recipe_rating == "N/R":
                filtered_recipes = [r for r in filtered_recipes if (r["rating"] is None)]  
            else:              
                filtered_recipes = [r for r in filtered_recipes if (r["rating"] is not None) and (r["rating"] == int(recipe_rating))]
        if main_ingredient != "Anything":
            filtered_recipes = [r for r in filtered_recipes if r["main_ingredient"] == main_ingredient]

        # Clear the current entries in the listbox
        self.recipe_listbox.delete(0, tk.END)

    # Populate the listbox with the filtered recipes
        for recipe in filtered_recipes:
            recipe_info = f"{recipe['title']:<20} {recipe['main_ingredient']:<20} {recipe['recipe_complexity']:<15} {recipe['recipe_type']:<20} {recipe['rating'] if recipe['rating'] else 'N/R'}"
            self.recipe_listbox.insert(tk.END, recipe_info)  # Insert formatted recipe information into the listbox

    def create_meal_plan(self, window):
        """Create a meal plan based on selected options."""
        meal_type_1 = self.meal_type_variable_1.get()
        meal_type_2 = self.meal_type_variable_2.get()
        family_member = self.family_member_variable_plan.get()
        keyword = self.keywords_entry.get().strip()

        # Get the family name
        family_name = self.family_name_variable.get()

        if family_name in self.family_profiles:
            meal_plan = {
                "title": f"{meal_type_1}/{meal_type_2} Meal Plan",
                "main_ingredient": "Various",  # Can be adjusted based on recipes
                "recipe_complexity": "Average",  # Can be adjusted based on recipes
                "recipe_type": "Meal Plan",
                "rating": None,
                "recipes": []  # This will hold the recipes for the meal plan
            }

            # Pull recipes from the family's profile based on selected criteria
            recipes = self.family_profiles[family_name]['recipes']

            # Filter recipes based on the meal types
            filtered_recipes_1 = [r for r in recipes if meal_type_1 in r["recipe_type"]]
            filtered_recipes_2 = [r for r in recipes if meal_type_2 in r["recipe_type"]]

            # Ensure we have a total of 7 unique recipes
            if len(filtered_recipes_1) > 0:
                meal_plan['recipes'].append(filtered_recipes_1[0])  # Add one recipe of meal type 1

            # Generate a new recipe
            while len(meal_plan['recipes']) < 2:
                # Prompt for new recipe generation
                self.recipe_type_variable.set(meal_type_1) 
                new_recipe = self.get_recipe()

                filtered_recipes_1 = [r for r in recipes if meal_type_1 in r["recipe_type"]]
                new_recipe = filtered_recipes_1[len(meal_plan['recipes'])]

                # Add the new recipe to the meal plan
                if new_recipe and new_recipe not in meal_plan['recipes']:
                    meal_plan['recipes'].append(new_recipe)

            if len(filtered_recipes_1) > 0:
                meal_plan['recipes'].append(filtered_recipes_2[0])  # Add a recipe of meal type 2

            # Generate a new recipe
            while len(meal_plan['recipes']) < 4:
                # Prompt for new recipe generation
                self.recipe_type_variable.set(meal_type_2) 
                new_recipe = self.get_recipe()

                filtered_recipes_2 = [r for r in recipes if meal_type_2 in r["recipe_type"]]
                new_recipe = filtered_recipes_2[len(meal_plan['recipes'])-2]

                # Add the new recipe to the meal plan if it doesn't already exist
                if new_recipe and new_recipe not in meal_plan['recipes']:
                    meal_plan['recipes'].append(new_recipe)

            # Save the meal plan to the family's profile
            self.family_profiles[family_name].setdefault('recipes', []).append(meal_plan)
            self.save_profiles()  # Save changes to profiles

            # Populate recipe list to show the new meal plan
            self.populate_recipe_list()  # Refresh the recipe list to show the new meal plan
            messagebox.showinfo("Success", f"Meal Plan '{meal_plan['title']}' created successfully.")

            window.destroy()  # Close the meal plan window
        else:
            messagebox.showerror("Error", "Selected family not found.")

    def view_meal_plan(self):
        """Show the details of the selected meal plan in a popup."""
        # Get the selected meal plan from the listbox
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            selected_meal_plan_info = self.recipe_listbox.get(selected_index)
            meal_plan_title = selected_meal_plan_info.split()[0].strip()  # Extract the title

            # Find the family name
            family_name = self.family_name_variable.get()

            # Find the full meal plan details
            if family_name in self.family_profiles:
                meal_plans = self.family_profiles[family_name].get("recipes", [])
                meal_plan = next((mp for mp in meal_plans if mp['title'].split()[0].strip()  == meal_plan_title), None)
                if meal_plan:
                    # Create a new window for the meal plan details
                    meal_plan_window = tk.Toplevel(self)
                    meal_plan_window.title(meal_plan['title'])

                    # Display the first recipe
                    self.current_recipe_index = 0  # Initialize the index
                    self.current_meal_plan = meal_plan  # Store the meal plan for navigation
                    recipe = meal_plan['recipes'][self.current_recipe_index]
                    self.display_meal_plan_recipe(meal_plan_window, recipe)

                    # Create a scale for the rating
                    self.rating_slider = tk.Scale(meal_plan_window, from_=0, to=5, orient=tk.HORIZONTAL, tickinterval=1, length=300, sliderlength=20)
                    # Set the default value based on the recipe rating
                    current_rating = recipe['rating'] if recipe['rating'] is not None else 0  # N/R as 0
                    self.rating_slider.set(current_rating)
                    self.rating_slider.grid(row=5,pady=10,columnspan=3)


                    # Previous Button
                    previous_button = tk.Button(meal_plan_window, text="Previous", command=lambda: self.show_previous_recipe(meal_plan_window), font=("Helvetica", 14))
                    previous_button.grid(row=6, column=0, pady=10)

                    # Next Button
                    next_button = tk.Button(meal_plan_window, text="Next", command=lambda: self.show_next_recipe(meal_plan_window), font=("Helvetica", 14))
                    next_button.grid(row=6, column=2, pady=10)

                    # Closing button
                    close_button = tk.Button(meal_plan_window, text="Close", command=meal_plan_window.destroy, font=("Helvetica", 14))
                    close_button.grid(row=6, column=1, pady=10)
                else:
                    messagebox.showerror("Error", "Meal Plan not found.")
            else:
                messagebox.showerror("Error", "Selected family not found.")
        else:
            messagebox.showerror("Error", "Please select a meal plan.")

    def display_meal_plan_recipe(self, window, recipe):
        """Display the details of the current recipe in the meal plan."""
        # Clear previous details
        for widget in window.winfo_children():
            if isinstance(widget, tk.Text) or isinstance(widget, tk.Label):
                widget.destroy()

        # Title of the recipe
        title_label = tk.Label(window, text=f"{recipe['recipe_type']} {self.current_recipe_index+1}:  {recipe['title']}", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0,column=0,columnspan=3,pady=10)

        # Ingredients
        ingredients_label = tk.Label(window, text="Ingredients:", font=("Helvetica", 14))
        ingredients_label.grid(row=1,column=0,sticky="w")
        ingredients_list = tk.Text(window, height=5, width=50, wrap=tk.WORD)
        for ingredient in recipe['ingredients']:
            ingredients_list.insert(tk.END, f"{ingredient['quantity']} of {ingredient['item']}\n")
        ingredients_list.config(state=tk.DISABLED)  # Make it read-only
        ingredients_list.grid(row=2,column=0,columnspan=3,pady=10)

        # Instructions
        instructions_label = tk.Label(window, text="Instructions:", font=("Helvetica", 14))
        instructions_label.grid(row=3,column=0,sticky="w")
        instructions_list = tk.Text(window, height=10, width=50, wrap=tk.WORD)
        for step in recipe['instructions']:
            instructions_list.insert(tk.END, f"{step}\n")
        instructions_list.config(state=tk.DISABLED)  # Make it read-only
        instructions_list.grid(row=4,column=0,columnspan=3,pady=10)

    def show_previous_recipe(self, window):
        """Show the previous recipe in the meal plan."""
        if self.current_recipe_index > 0:
            self.current_recipe_index -= 1
            self.display_meal_plan_recipe(window, self.current_meal_plan['recipes'][self.current_recipe_index])

    def show_next_recipe(self, window):
        """Show the next recipe in the meal plan."""
        if self.current_recipe_index < len(self.current_meal_plan['recipes']) - 1:
            self.current_recipe_index += 1
            self.display_meal_plan_recipe(window, self.current_meal_plan['recipes'][self.current_recipe_index])

    def get_meal_plan(self):
        """Show the Meal Plan selection popup."""
        meal_plan_window = tk.Toplevel(self)
        meal_plan_window.title("Create Meal Plan")

        # Meal Type Dropdowns
        meal_type_label_1 = tk.Label(meal_plan_window, text="Select Meal Type 1:", font=("Helvetica", 12))
        meal_type_label_1.grid(row=0, column=0, padx=10, pady=10)

        self.meal_type_variable_1 = tk.StringVar()
        self.meal_type_dropdown_1 = ttk.Combobox(meal_plan_window, textvariable=self.meal_type_variable_1, state='readonly', font=("Helvetica", 12))
        self.meal_type_dropdown_1['values'] = ["Breakfast", "Lunch", "Dinner"]  # Default options
        self.meal_type_dropdown_1.set("Breakfast")  # Default to Breakfast
        self.meal_type_dropdown_1.grid(row=0, column=1, padx=10, pady=10)

        meal_type_label_2 = tk.Label(meal_plan_window, text="Select Meal Type 2:", font=("Helvetica", 12))
        meal_type_label_2.grid(row=1, column=0, padx=10, pady=10)

        self.meal_type_variable_2 = tk.StringVar()
        self.meal_type_dropdown_2 = ttk.Combobox(meal_plan_window, textvariable=self.meal_type_variable_2, state='readonly', font=("Helvetica", 12))
        self.meal_type_dropdown_2['values'] = ["Breakfast", "Lunch", "Dinner"]  # Default options
        self.meal_type_dropdown_2.set("Dinner")  # Default to Dinner
        self.meal_type_dropdown_2.grid(row=1, column=1, padx=10, pady=10)

        # Family Member Dropdown
        family_member_label = tk.Label(meal_plan_window, text="Select Family Member:", font=("Helvetica", 12))
        family_member_label.grid(row=2, column=0, padx=10, pady=10)

        self.family_member_variable_plan = tk.StringVar()
        self.family_member_dropdown_plan = ttk.Combobox(meal_plan_window, textvariable=self.family_member_variable_plan, state='readonly', font=("Helvetica", 12))
        self.family_member_dropdown_plan['values'] = ["All"] + [member['name'] for member in self.family_profiles[self.family_name_variable.get()]['members']]
        self.family_member_dropdown_plan.set("All")  # Default to All
        self.family_member_dropdown_plan.grid(row=2, column=1, padx=10, pady=10)

        # Meal Plan Keywords
        keywords_label = tk.Label(meal_plan_window, text="Meal Plan Keywords:", font=("Helvetica", 12))
        keywords_label.grid(row=3, column=0, padx=10, pady=10)

        self.keywords_entry = tk.Entry(meal_plan_window, font=("Helvetica", 12))
        self.keywords_entry.insert(0, "Low Carb")  # Default keyword
        self.keywords_entry.grid(row=3, column=1, padx=10, pady=10)

        # OK Button
        ok_button = tk.Button(meal_plan_window, text="OK", command=lambda: self.create_meal_plan(meal_plan_window), font=("Helvetica", 14))
        ok_button.grid(row=4, column=0, columnspan=2, pady=10)

    def get_grocery_list(self):
        """Gather ingredients for the selected recipe or meal plan and display the grocery list."""
        # Get the selected item from the listbox
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            selected_info = self.recipe_listbox.get(selected_index)
            # Extract the title from the selected entry
            title = selected_info.split()[0].strip()  # Assuming the title is the first word

            # Find the family name
            family_name = self.family_name_variable.get()

            if family_name in self.family_profiles:
                # Check if the selected item is a meal plan
                meal_plans = [recipe for recipe in self.family_profiles[family_name]['recipes'] if recipe['recipe_type'] == 'Meal Plan']
                meal_plan = next((mp for mp in meal_plans if mp['title'].startswith(title)), None)

                if meal_plan:
                    # Gather ingredients for all recipes in the meal plan
                    grocery_list = []
                    for recipe in meal_plan['recipes']:
                        for ingredient in recipe['ingredients']:
                            grocery_list.append(f"{ingredient['quantity']} of {ingredient['item']}")
                    
                    # Combine ingredients with the same units
                    grocery_list_dict = {}
                    for item in grocery_list:
                        quantity, ingredient_name = item.split(' ', 1)  # Split into quantity and ingredient name
                        unit = quantity.split()[-1]  # Get the unit from the quantity (e.g., "500g")
                        quantity_value = ' '.join(quantity.split()[:-1])  # Get the numeric part of the quantity
                        # Create a unique key for the ingredient based on name and unit
                        key = (ingredient_name.strip(), unit)
                        
                        if key in grocery_list_dict:
                            # Append to existing entry
                            grocery_list_dict[key] += f", {quantity_value}"
                        else:
                            grocery_list_dict[key] = quantity_value

                    # Create a popup window to display the grocery list
                    grocery_window = tk.Toplevel(self)
                    grocery_window.title("Grocery List")

                    # Grocery List Header
                    header_label = tk.Label(grocery_window, text="Grocery List", font=("Helvetica", 16, "bold"))
                    header_label.pack(pady=10)

                    # Display ingredients in a text area
                    grocery_text = tk.Text(grocery_window, height=10, width=40, wrap=tk.WORD)
                    for (ingredient, unit), quantity in grocery_list_dict.items():
                        grocery_text.insert(tk.END, f"{quantity} {unit} of {ingredient}\n")
                    grocery_text.config(state=tk.DISABLED)  # Make it read-only
                    grocery_text.pack(pady=5)

                    # Closing button
                    close_button = tk.Button(grocery_window, text="Close", command=grocery_window.destroy)
                    close_button.pack(pady=10)

                else:
                    # Check if the selected item is a recipe
                    recipes = self.family_profiles[family_name].get("recipes", [])
                    recipe = next((r for r in recipes if r['title'].startswith(title)), None)

                    if recipe:
                        # Prepare the grocery list for the selected recipe
                        grocery_list = []
                        for ingredient in recipe['ingredients']:
                            grocery_list.append(f"{ingredient['quantity']} of {ingredient['item']}")

                        # Create a popup window to display the grocery list
                        grocery_window = tk.Toplevel(self)
                        grocery_window.title("Grocery List")

                        # Grocery List Header
                        header_label = tk.Label(grocery_window, text="Grocery List", font=("Helvetica", 16, "bold"))
                        header_label.pack(pady=10)

                        # Display ingredients in a text area
                        grocery_text = tk.Text(grocery_window, height=10, width=40, wrap=tk.WORD)
                        for item in grocery_list:
                            grocery_text.insert(tk.END, item + "\n")
                        grocery_text.config(state=tk.DISABLED)  # Make it read-only
                        grocery_text.pack(pady=5)

                        # Closing button
                        close_button = tk.Button(grocery_window, text="Close", command=grocery_window.destroy)
                        close_button.pack(pady=10)
                    else:
                        messagebox.showerror("Error", "Recipe not found.")
            else:
                messagebox.showerror("Error", "Selected family not found.")
        else:
            messagebox.showerror("Error", "Please select a recipe or meal plan.")

    def load_profiles(self):
        """Load profiles from a JSON file."""
        if os.path.exists("profiles.json"):
            with open("profiles.json", "r") as f:
                profiles_data = json.load(f)
                self.family_profiles = profiles_data

    def save_profiles(self):
        """Save profiles to a JSON file."""
        profiles_data = self.family_profiles

        with open("profiles.json", "w") as f:
            json.dump(profiles_data, f, indent=4)

    def edit_profile(self):
        """Open the Edit Profile Screen for the selected family."""
        self.family_name = self.family_name_variable.get()
        self.last_family = self.family_name
        self.family_selected = 1

        if self.family_name in self.family_profiles:
            # Here we can call the edit profile method
            self.show_edit_profile_screen()  # Assuming you will implement this method
        else:
            messagebox.showerror("Error", "Please select a valid family.")

    def add_family(self):
        """Add a new family profile."""
        family_name = simpledialog.askstring("Add Family", "Enter family name:")
        if family_name not in self.family_profiles:
            self.family_profiles[family_name] = {
                "members": [],
                "kitchens": {},
                "saved_recipes": [],  # New key for saved recipes
                "recipes": self.get_default_recipes()  # Initialize with default recipes
            }
            self.save_profiles()  # Save the profiles
            self.update_family_dropdown()  # Update dropdowns with new family
            messagebox.showinfo("Success", f"Family '{family_name}' added.")
        else:
            messagebox.showerror("Error", "Family name is empty or already exists.")

    def remove_family(self):
        """Remove the selected family profile."""
        family_name = self.family_name_variable.get()
        if not family_name or family_name == "Family":
            messagebox.showerror("Error", "Please select a valid family to remove.")
            return

        # Ask for confirmation
        confirmation = messagebox.askyesno(
            "Confirm Removal", 
            f"Are you sure you want to remove the family '{family_name}'?"
        )

        if confirmation:
            # Remove the family from the profiles
            if family_name in self.family_profiles:
                del self.family_profiles[family_name]
                self.save_profiles()  # Save changes to the profiles
                messagebox.showinfo("Success", f"Family '{family_name}' has been removed.")
                self.update_family_dropdown()  # Update the dropdown after removal
                self.family_name_variable.set("Family")  # Reset the dropdown selection
            else:
                messagebox.showerror("Error", "Family not found in profiles.")

    def add_dietary_restriction(self,member_info):
        restriction = self.dietary_restrictions_dropdown.get()
        if restriction and restriction not in member_info['dietary_restrictions']:
            member_info['dietary_restrictions'].append(restriction)  # Add to member profile
            self.dietary_restrictions_dropdown.set('')  # Reset dropdown selection

    def add_custom_dietary_restriction(self, member_info):
        custom_restriction = self.custom_dietary_entry.get().strip()
        if custom_restriction and custom_restriction not in member_info['dietary_restrictions']:
            member_info['dietary_restrictions'].append(custom_restriction)  # Add to member profile
            self.custom_dietary_entry.delete(0, tk.END)  # Clear the entry

    def remove_dietary_restriction(self, member_info):
        """Remove selected dietary restriction from member's profile."""
        restriction = self.dietary_restrictions_dropdown.get()
        if restriction in member_info['dietary_restrictions']:
            member_info['dietary_restrictions'].remove(restriction)  # Remove from member profile
            self.dietary_restrictions_dropdown.set('')  # Reset dropdown selection

    def add_favorite_food(self, member_info):
        food = self.favorite_foods_variable.get()
        if food and food not in member_info['favorite_foods']:
            member_info['favorite_foods'].append(food)  # Add to member profile
            self.favorite_foods_variable.set('')  # Reset dropdown selection

    def add_custom_favorite_food(self,member_info):
        custom_food = self.custom_favorite_entry.get().strip()
        if custom_food and custom_food not in member_info['favorite_foods']:
            member_info['favorite_foods'].append(custom_food)  # Add to member profile
            self.custom_favorite_entry.delete(0, tk.END)  # Clear the entry

    def remove_favorite_food(self, member_info):
        """Remove selected favorite food from member's profile."""
        food = self.favorite_foods_dropdown.get()
        if food in member_info['favorite_foods']:
            member_info['favorite_foods'].remove(food)  # Remove from member profile
            self.favorite_foods_variable.set('')  # Reset dropdown selection

    def save_member(self, member_info,window):
        member_name = self.member_name_entry.get().strip()
        member_age = self.member_age_entry.get().strip()
    

        if member_name and member_age.isdigit():
            # Update the existing member's information
            member_info['name'] = member_name
            member_info['age'] = int(member_age)
            member_info['dietary_restrictions'] = member_info['dietary_restrictions']  # Keep existing restrictions
            member_info['favorite_foods'] = member_info['favorite_foods']  # Keep existing favorite foods

            self.save_profiles()  # Save changes to profiles
            messagebox.showinfo("Success", f"Member '{member_name}' updated.")
            window.destroy()  # Close the edit member window
        else:
            messagebox.showerror("Error", "Please enter a valid name and age.")
            
        self.populate_member_list()

    def add_member(self):
        """Add a new family member to the selected family."""
        member_name = simpledialog.askstring("Add Member", "Enter member name:")

        if member_name:
            if member_name not in self.family_profiles[self.family_name]["members"]:
                member_info = {
                "dietary_restrictions": [],
                "favorite_foods": [],
                "name": member_name,
                "age": ""
                }

                self.family_profiles[self.family_name]["members"].append(member_info)
                self.save_profiles()  # Save the profiles
                self.populate_member_list()  # Update listbox
                messagebox.showinfo("Success", f"{member_name}' added.")
            else:
                messagebox.showerror("Error", "Member has already been added.")
        else:
            messagebox.showerror("Error", "Member name is empty.")

    def edit_member(self):
        """Edit the selected family member."""
        family_name = self.family_name_variable.get()
        selected_member_index = self.member_listbox.curselection()  # Get the index of the selected member

        if selected_member_index:
            selected_member_info = self.member_listbox.get(selected_member_index)  # Get member info from the listbox
            member_name = selected_member_info.split()[0]  # Extract the member's name from the formatted string
            
            # Get the member's full details
            member_info = next((member for member in self.family_profiles[family_name]['members'] if member['name'] == member_name), None)

            if member_info:
                # Create a new top-level window for editing
                edit_member_window = tk.Toplevel(self)
                edit_member_window.title("Edit Member")

                # Name Entry
                tk.Label(edit_member_window, text="Member Name:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=10)
                self.member_name_entry = tk.Entry(edit_member_window, font=("Helvetica", 12))
                self.member_name_entry.insert(0, member_info['name'])  # Prepopulate name
                self.member_name_entry.grid(row=0, column=1, padx=10, pady=10)

                # Age Entry
                tk.Label(edit_member_window, text="Age:", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=10)
                self.member_age_entry = tk.Entry(edit_member_window, font=("Helvetica", 12))
                self.member_age_entry.insert(0, member_info['age'])  # Prepopulate age
                self.member_age_entry.grid(row=1, column=1, padx=10, pady=10)

                # Dietary Restrictions Dropdown
                tk.Label(edit_member_window, text="Dietary Restrictions:", font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=10)
                self.dietary_restrictions_dropdown = ttk.Combobox(edit_member_window, textvariable=self.dietary_restrictions_variable, state='readonly', font=("Helvetica", 12))
                self.dietary_restrictions_dropdown['values'] = ["All"] + member_info['dietary_restrictions'] + ["Dairy Free", "Gluten Free", "Vegitarian", "Vegan"]  # Prepopulate with the user's dietary restrictions
                self.dietary_restrictions_dropdown.set("All")  # Default to "All"
                self.dietary_restrictions_dropdown.grid(row=2, column=1, padx=10, pady=10)

                add_dietary_button = tk.Button(edit_member_window, text="+", command=lambda: self.add_dietary_restriction(member_info), font=("Helvetica", 12))
                add_dietary_button.grid(row=2, column=2, padx=10, pady=10)

                # Remove Dietary Restriction Button
                remove_dietary_button = tk.Button(edit_member_window, text="-", command=lambda: self.remove_dietary_restriction(member_info), font=("Helvetica", 12))
                remove_dietary_button.grid(row=2, column=3, padx=10, pady=10)

                # Custom Dietary Restriction Entry
                tk.Label(edit_member_window, text="Custom Dietary Restriction:", font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=10)
                self.custom_dietary_entry = tk.Entry(edit_member_window, font=("Helvetica", 12))
                self.custom_dietary_entry.grid(row=3, column=1, padx=10, pady=10)

                add_custom_dietary_button = tk.Button(edit_member_window, text="+", command=lambda: self.add_custom_dietary_restriction(member_info), font=("Helvetica", 12))
                add_custom_dietary_button.grid(row=3, column=2, padx=10, pady=10)

                # Favorite Foods Dropdown
                tk.Label(edit_member_window, text="Favorite Foods:", font=("Helvetica", 14)).grid(row=4, column=0, padx=10, pady=10)
                self.favorite_foods_dropdown = ttk.Combobox(edit_member_window, textvariable=self.favorite_foods_variable, state='readonly', font=("Helvetica", 12))
                self.favorite_foods_dropdown['values'] = ["All"] + member_info['favorite_foods'] # Prepopulate with the user's favorite foods
                self.favorite_foods_dropdown.set("All")  # Default to "All"
                self.favorite_foods_dropdown.grid(row=4, column=1, padx=10, pady=10)

                add_favorite_button = tk.Button(edit_member_window, text="+", command=lambda: self.add_favorite_food(member_info), font=("Helvetica", 12))
                add_favorite_button.grid(row=4, column=2, padx=10, pady=10)

                # Remove Favorite Food Button
                remove_favorite_button = tk.Button(edit_member_window, text="-", command=lambda: self.remove_favorite_food(member_info), font=("Helvetica", 12))
                remove_favorite_button.grid(row=4, column=3, padx=10, pady=10)

                # Custom Favorite Food Entry
                tk.Label(edit_member_window, text="Custom Favorite Food:", font=("Helvetica", 14)).grid(row=5, column=0, padx=10, pady=10)
                self.custom_favorite_entry = tk.Entry(edit_member_window, font=("Helvetica", 12))
                self.custom_favorite_entry.grid(row=5, column=1, padx=10, pady=10)

                add_custom_favorite_button = tk.Button(edit_member_window, text="+", command=lambda: self.add_custom_favorite_food(member_info), font=("Helvetica", 12))
                add_custom_favorite_button.grid(row=5, column=2, padx=10, pady=10)

                # Save Member Button
                save_member_button = tk.Button(edit_member_window, text="Save Member", command=lambda: self.save_member(member_info,edit_member_window), font=("Helvetica", 14))
                save_member_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    def remove_member(self):
        """Remove the selected family member."""
        family_name = self.family_name_variable.get()
        selected_member_index = self.member_listbox.curselection()  # Get the index of the selected member

        # Check if a member is selected
        if selected_member_index:
            selected_member_info = self.member_listbox.get(selected_member_index)  # Get member info from the listbox
            member_name = selected_member_info.split()[0]  # Extract the member's name from the formatted string

            # Ask for confirmation
            confirmation = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{member_name}'?")
            
            if confirmation:
                # Remove the member from the profiles
                self.family_profiles[family_name]['members'] = [
                    member for member in self.family_profiles[family_name]['members'] if member['name'] != member_name
                ]
                self.save_profiles()  # Save changes to the profiles
                self.populate_member_list()  # Refresh the member listbox
                messagebox.showinfo("Success", f"Member '{member_name}' has been removed.")
        else:
            messagebox.showerror("Error", "Please select a member to remove.")

    def update_family_dropdown(self):
        """Update the family dropdown with the names of available profiles."""
        self.family_dropdown['values'] = list(self.family_profiles.keys())

        if self.family_name_variable.get():
            self.family_dropdown.set(self.family_name_variable.get())

    def select_family(self):
        """Select the family from the dropdown and navigate to Main Menu."""
        self.family_name = self.family_name_variable.get()
        self.last_family = self.family_name
        self.family_selected = 1

        if self.family_name in self.family_profiles:
            self.show_main_menu_screen()  # Navigate to the main menu
        else:
            messagebox.showerror("Error", "Please select a valid family.")

# Initialize and run the application
if __name__ == "__main__":
    app = SmartKitchenAssistantApp()
    app.mainloop()
