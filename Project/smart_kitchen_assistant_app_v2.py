import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, scrolledtext
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Your OpenAI API key
API_KEY = os.getenv('OPENAI_API_KEY')


class SmartKitchenAssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Kitchen Assistant")

        # Create main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0,column=0,padx=10, pady=10)

        # Initialize Variables

        self.family_name_variable = tk.StringVar()
        self.meal_type_variable = tk.StringVar()
        self.meal_complexity_variable = tk.StringVar()
        self.family_member_variable = tk.StringVar()
        self.kitchen_name_variable = tk.StringVar()

        # Main App Title
        self.app_label = tk.Label(self.main_frame, text="Smart Kitchen Assistant", font=("Helvetica", 14))
        self.app_label.grid(row=0,column=0,columnspan=3,pady=10)

        ## Main Menu Frame

        self.main_menu_frame = tk.Frame(self.main_frame, relief= 'sunken', borderwidth=2)
        self.main_menu_frame.grid(row=1,column=0, padx=10, pady=10)

        self.app_label = tk.Label(self.main_menu_frame, text="Main Menu", font=("Helvetica", 12, "bold"))
        self.app_label.grid(row=0,column=0,columnspan=2,pady=10)

        # Family Profile Dropdown
        self.family_name_label = tk.Label(self.main_menu_frame, text="Select Family:", font=("Helvetica", 12))
        self.family_name_label.grid(row=1,column=0,padx=10, pady=10)
        

        self.family_name_dropdown = ttk.Combobox(self.main_menu_frame, textvariable=self.family_name_variable, state='readonly')
        self.family_name_dropdown.bind("<<ComboboxSelected>>", self.update_family_members)
        self.family_name_dropdown.grid(row=1,column=1,padx=10, pady=10)

        # Meal Type Dropdown
        self.meal_type_label = tk.Label(self.main_menu_frame, text="Select Meal Type:", font=("Helvetica", 12))
        self.meal_type_label.grid(row=2,column=0,padx=10, pady=10)

        self.meal_type_dropdown = ttk.Combobox(self.main_menu_frame, textvariable=self.meal_type_variable)
        self.meal_type_dropdown['values'] = ("Weekday Dinner", "Weekend Dinner", "Thanksgiving", "Birthday", "Football Game")
        self.meal_type_dropdown.grid(row=2,column=1,padx=10, pady=10)

        # Meal Complexity Dropdown
        self.meal_complexity_label = tk.Label(self.main_menu_frame, text="Select Meal Complexity:", font=("Helvetica", 12))
        self.meal_complexity_label.grid(row=3,column=0,padx=10, pady=10)

        self.meal_complexity_dropdown = ttk.Combobox(self.main_menu_frame, textvariable=self.meal_complexity_variable)
        self.meal_complexity_dropdown['values'] = ("Make it Easy", "Challenge Me", "Cook to Impress")
        self.meal_complexity_dropdown.grid(row=3,column=1,padx=10, pady=10)


        self.family_summary_label = tk.Label(self.main_menu_frame, text="Family Summary:", font=("Helvetica", 12))
        self.family_summary_label.grid(row=4,column=0,padx=10, pady=10)
        self.family_summary_text = scrolledtext.ScrolledText(self.main_menu_frame, width=40, height=1, wrap=tk.WORD)
        self.family_summary_text.grid(row=5,column=0,columnspan=2,padx=10, pady=10)

        self.previous_meals_label = tk.Label(self.main_menu_frame, text="Previous Meals:", font=("Helvetica", 12))
        self.previous_meals_label.grid(row=6,column=0,padx=10, pady=10)
        self.previous_meals_text = scrolledtext.ScrolledText(self.main_menu_frame, width=40, height=1, wrap=tk.WORD)
        self.previous_meals_text.grid(row=7,column=0,columnspan=2,padx=10, pady=10)

        # Main Menu Buttons

        self.mm_button_frame = tk.Frame(self.main_menu_frame, relief='ridge',borderwidth=2)
        self.mm_button_frame.grid(row=8,column=0,columnspan=3, padx=10,pady=10)

        self.get_recipe_button = tk.Button(self.mm_button_frame, text="Get Recipe", command=self.get_recipe)
        self.get_recipe_button.grid(row=0, column=0, padx=15, pady=10)

        self.get_meal_plan_button = tk.Button(self.mm_button_frame, text="Get Meal Plan", command=self.get_meal_plan)
        self.get_meal_plan_button.grid(row=0, column=1, padx=15, pady=10)

        self.get_grocery_list_button = tk.Button(self.mm_button_frame, text="Get Grocery List", command=self.get_meal_plan)
        self.get_grocery_list_button.grid(row=0, column=2, padx=15, pady=10)


        ## Profile Frame
        
        self.profile_frame = tk.Frame(self.main_frame, relief= 'sunken', borderwidth=2, width=100,height=300)
        self.profile_frame.grid(row=1,column=1,padx=10,pady=10)

        self.app_label = tk.Label(self.profile_frame, text="Profile Menu", font=("Helvetica", 12, "bold"))
        self.app_label.grid(row=0,column=0,columnspan=2,pady=10)

        # Family Profile Dropdown
        self.prof_family_name_label = tk.Label(self.profile_frame, text="Select Family:", font=("Helvetica", 12))
        self.prof_family_name_label.grid(row=1,column=0,padx=10, pady=10)
        
        self.prof_family_name_dropdown = ttk.Combobox(self.profile_frame, textvariable=self.family_name_variable, state='readonly')
        self.prof_family_name_dropdown.bind("<<ComboboxSelected>>", self.update_family_members)
        self.prof_family_name_dropdown.grid(row=1,column=1,padx=10, pady=10)

        # Family Member Dropdown
        self.family_member_label = tk.Label(self.profile_frame, text="Family Member:", font=("Helvetica", 12))
        self.family_member_label.grid(row=2,column=0,padx=10, pady=10)

        self.family_member_dropdown = ttk.Combobox(self.profile_frame, textvariable=self.family_member_variable, state='readonly')
        self.family_member_dropdown.bind("<<ComboboxSelected>>", self.update_member_info)
        self.family_member_dropdown.grid(row=2,column=1,padx=10, pady=10)

        # Editable Text Boxes for Family Member Info
        self.age_label = tk.Label(self.profile_frame, text="Member Age:", font=("Helvetica", 12))
        self.age_label.grid(row=3,column=0,padx=10, pady=5)
        self.age_entry = tk.Entry(self.profile_frame)
        self.age_entry.grid(row=3,column=1,padx=10,pady=10)

        self.favorite_foods_label = tk.Label(self.profile_frame, text="Favorite Foods:", font=("Helvetica", 12))
        self.favorite_foods_label.grid(row=4,column=0,padx=10, pady=10)
        self.favorite_foods_text = scrolledtext.ScrolledText(self.profile_frame, width=40, height=2, wrap=tk.WORD)
        self.favorite_foods_text.grid(row=5,column=0,columnspan=2,padx=10, pady=10)

        self.dietary_restrictions_label = tk.Label(self.profile_frame, text="Dietary Restrictions:", font=("Helvetica", 12))
        self.dietary_restrictions_label.grid(row=6,column=0,padx=10, pady=10)
        self.dietary_restrictions_text = scrolledtext.ScrolledText(self.profile_frame, width=40, height=1, wrap=tk.WORD)
        self.dietary_restrictions_text.grid(row=7,column=0,columnspan=2,padx=10, pady=10)

        # Profile Menu Buttons

        self.profile_button_frame = tk.Frame(self.profile_frame, relief='ridge',borderwidth=2)
        self.profile_button_frame.grid(row=8,column=0,columnspan=2,pady=10)


        self.add_family_button = tk.Button(self.profile_button_frame, text="Add Family", command=self.add_family)
        self.add_family_button.grid(row=0, column=0, padx=15, pady=10)

        self.add_member_button = tk.Button(self.profile_button_frame, text="Add Member", command=self.add_member)
        self.add_member_button.grid(row=0, column=1, padx=15, pady=10)

        self.update_profile_button = tk.Button(self.profile_button_frame, text="Save Profile", command=self.save_profile)
        self.update_profile_button.grid(row=0, column=2, padx=15, pady=10)



        ## Kitchen Menu
        
        self.kitchen_frame = tk.Frame(self.main_frame, relief= 'sunken', borderwidth=2, width=100,height=300)
        self.kitchen_frame.grid(row=1,column=2,padx=10,pady=10)

        self.app_label = tk.Label(self.kitchen_frame, text="Kitchen Menu", font=("Helvetica", 12,"bold"))
        self.app_label.grid(row=0,column=0,columnspan=2,pady=10)

        # Family Profile Dropdown
        self.kit_family_name_label = tk.Label(self.kitchen_frame, text="Select Family:", font=("Helvetica", 12))
        self.kit_family_name_label.grid(row=1,column=0,padx=10, pady=10)
        
        self.kit_family_name_dropdown = ttk.Combobox(self.kitchen_frame, textvariable=self.family_name_variable, state='readonly')
        self.kit_family_name_dropdown.bind("<<ComboboxSelected>>", self.update_family_members)
        self.kit_family_name_dropdown.grid(row=1,column=1,padx=10, pady=10)

        # Kitchen Selection Dropdown
        self.kitchen_name_label = tk.Label(self.kitchen_frame, text="Select Kitchen:", font=("Helvetica", 12))
        self.kitchen_name_label.grid(row=2,column=0,padx=10, pady=10)
        
        self.kitchen_name_dropdown = ttk.Combobox(self.kitchen_frame, textvariable=self.kitchen_name_variable, state='readonly')
        self.kitchen_name_dropdown.bind("<<ComboboxSelected>>", self.update_kitchen_info)
        self.kitchen_name_dropdown.grid(row=2,column=1,padx=10, pady=10)

        self.kitchen_location_label = tk.Label(self.kitchen_frame, text="Kitchen Location:", font=("Helvetica", 12))
        self.kitchen_location_label.grid(row=3,column=0,padx=10, pady=5)
        self.kitchen_location_entry = tk.Entry(self.kitchen_frame)
        self.kitchen_location_entry.grid(row=3,column=1,padx=10,pady=10)

        self.tools_available_label = tk.Label(self.kitchen_frame, text="Tools Available:", font=("Helvetica", 12))
        self.tools_available_label.grid(row=4,column=0,padx=10, pady=10)
        self.tools_available_text = scrolledtext.ScrolledText(self.kitchen_frame, width=40, height=1, wrap=tk.WORD)
        self.tools_available_text.grid(row=5,column=0,columnspan=2,padx=10, pady=10)

        self.ingredients_available_label = tk.Label(self.kitchen_frame, text="Ingredients Available:", font=("Helvetica", 12))
        self.ingredients_available_label.grid(row=6,column=0,padx=10, pady=10)
        self.ingredients_available_text = scrolledtext.ScrolledText(self.kitchen_frame, width=40, height=1, wrap=tk.WORD)
        self.ingredients_available_text.grid(row=7,column=0,columnspan=2,padx=10, pady=10)


        # Kitchen Buttons

        self.kitchen_button_frame = tk.Frame(self.kitchen_frame, relief='ridge',borderwidth=2)
        self.kitchen_button_frame.grid(row=8,column=0,columnspan=2,pady=10)


        self.add_kitchen_button = tk.Button(self.kitchen_button_frame, text="Add Kitchen", command=self.add_kitchen)
        self.add_kitchen_button.grid(row=0, column=0, padx=15, pady=10)

        self.save_kitchen_button = tk.Button(self.kitchen_button_frame, text="Save Kitchen", command=self.save_profile)
        self.save_kitchen_button.grid(row=0, column=2, padx=15, pady=10)


        # Profile storage
        #self.profiles = {
        #    "kitchen": {}
        #}

        # Additional storage for multiple profiles
        self.family_profiles = {
        }

        # Load profiles on startup
        self.load_profiles()
        self.update_family_dropdown()
        self.update_kitchen_dropdown()

    def add_family(self):
        """Add a new family profile."""
        family_name = simpledialog.askstring("Add Family", "Enter family name:")
        if family_name not in self.family_profiles:
            self.family_profiles[family_name] = {
                "number_of_members": 0,
                "members": [],
                "kitchens": {
                    "kitchen_name": {
                        "location": "",
                        "tools_available": [],
                        "ingredients_available": []
                    }
                }
            }
            self.update_family_dropdown()
            self.update_kitchen_dropdown()
            self.family_name_variable.set(family_name)  # Automatically select the new family
        else:
            messagebox.showerror("Error", "Family name is empty or already exists.")

    def add_kitchen(self):
        """Add a new kitchen profile."""
        kitchen_name = simpledialog.askstring("Add Kitchen", "Enter Kitchen Name:")
        family_name = self.family_name_variable.get()

        if kitchen_name and family_name:
            # Check if the family has a kitchens dictionary; if not, create one
            if "kitchens" not in self.family_profiles[family_name]:
                self.family_profiles[family_name]["kitchens"] = {}

            # Add the new kitchen if it doesn't already exist
            if kitchen_name not in self.family_profiles[family_name]["kitchens"]:
                self.family_profiles[family_name]["kitchens"][kitchen_name] = {
                    "location": "",
                    "tools_available": [],
                    "ingredients_available": []
                }

                self.kitchen_name_variable.set(kitchen_name)            
                self.update_kitchen_info(family_name)  # Update kitchen info based on the selected family
                self.update_kitchen_dropdown()  # Update the dropdown with the new kitchen name

            else:
                messagebox.showerror("Error", "Kitchen name already exists.")
        else:
            messagebox.showerror("Error", "Please enter a kitchen name and select a family.")

        self.family_name_variable.set(family_name)  # Keep the selected family name
        self.kitchen_name_variable.set(kitchen_name)  # Keep the selected family name

    def add_member(self):
        """Add a new member to the currently selected family."""
        family_name = self.family_name_variable.get()
        if not family_name:
            messagebox.showerror("Error", "Please select a family first.")
            return

        member_name = simpledialog.askstring("Add Member", "Enter member's name:")
        if member_name:
            # Retrieve the current family information
            family_info = self.family_profiles[family_name]
            # Add the new member with default values
            family_info['members'].append({
                "name": member_name,
                "age": 0,  # Default age
                "dietary_restrictions": [],
                "favorite_foods": []
            })
            family_info['number_of_members'] += 1
            
            # Update the family member dropdown
            self.update_family_members(None)  # Refresh the member dropdown
            self.family_member_variable.set(member_name)  # Automatically select the new member
        else:
            messagebox.showerror("Error", "Member name cannot be empty.")

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

    def update_kitchen_dropdown(self):
        """Update the family dropdown with the names of available profiles."""
        if self.family_name_variable.get():
            family_name = self.family_name_variable.get()
            self.kitchen_name_dropdown['values'] = list(self.family_profiles[family_name]["kitchens"].keys())
            self.kitchen_name_dropdown.set('')  # Clear the selection

    def update_family_dropdown(self):
        """Update the family dropdown with the names of available profiles."""
        self.family_name_dropdown['values'] = list(self.family_profiles.keys())
        self.family_name_dropdown.set('')  # Clear the selection
        self.prof_family_name_dropdown['values'] = list(self.family_profiles.keys())
        self.prof_family_name_dropdown.set('')
        self.kit_family_name_dropdown['values'] = list(self.family_profiles.keys())
        self.kit_family_name_dropdown.set('')

    def update_family_members(self, event):
        """Update the family member dropdown based on selected family."""
        family_name = self.family_name_variable.get()
        if family_name in self.family_profiles:
            members = [member['name'] for member in self.family_profiles[family_name]['members']]
            self.family_member_dropdown['values'] = members
            self.family_member_dropdown.set('')  # Clear the selection
            self.clear_member_info()  # Clear any existing member info
            self.update_kitchen_info(None)
            self.update_kitchen_dropdown()
        else:
            self.family_member_dropdown['values'] = []

    def update_kitchen_info(self, event):
        """Update the kitchen editable text boxes based on the selected family."""
        if self.kitchen_name_variable.get():
            kitchen_name = self.kitchen_name_variable.get() 
            if self.family_name_variable.get():
                family_name = self.family_name_variable.get() 
                kitchen_info = self.family_profiles[family_name]["kitchens"][kitchen_name]
                self.kitchen_location_entry.delete(0, tk.END)
                self.kitchen_location_entry.insert(0, kitchen_info['location'])
                self.tools_available_text.delete(1.0, tk.END)
                self.tools_available_text.insert(tk.INSERT, ', '.join(kitchen_info['tools_available']))
                self.ingredients_available_text.delete(1.0, tk.END)
                self.ingredients_available_text.insert(tk.INSERT, ', '.join(kitchen_info['ingredients_available']))
            else:
                messagebox.showerror("Error", "Select a family the kitchen is for first.")

            self.kitchen_name_variable.set(kitchen_name)

    def update_member_info(self, event):
        """Update the editable text boxes with the selected family member's information."""
        family_name = self.family_name_variable.get()
        member_name = self.family_member_variable.get()

        if family_name and member_name:
            member_info = next((member for member in self.family_profiles[family_name]['members'] if member['name'] == member_name), None)
            if member_info:
                self.age_entry.delete(0, tk.END)
                self.age_entry.insert(0, member_info['age'])
                self.dietary_restrictions_text.delete(1.0, tk.END)
                self.dietary_restrictions_text.insert(tk.INSERT, ', '.join(member_info['dietary_restrictions']))

                self.favorite_foods_text.delete(1.0, tk.END)
                self.favorite_foods_text.insert(tk.INSERT, ', '.join(member_info['favorite_foods']))
        else:
            self.clear_member_info()

    def clear_member_info(self):
        """Clear the editable text boxes for member information."""
        self.age_entry.delete(0, tk.END)
        self.dietary_restrictions_text.delete(1.0, tk.END)
        self.favorite_foods_text.delete(1.0, tk.END)

    def clear_kitchen_info(self):
        """Clear the editable text boxes for kitchen information."""
        self.kitchen_location_entry.delete(0, tk.END)
        self.tools_available_text.delete(0, tk.END)
        self.ingredients_available_text.delete(0, tk.END)        

    def save_profile(self):
        """Save the changes made in the text boxes to the relevant profile data."""
        family_name = self.family_name_variable.get()
        member_name = self.family_member_variable.get()
        kitchen_name = self.kitchen_name_variable.get()

        if family_name:

            if member_name:
                member_info = next((member for member in self.family_profiles[family_name]['members'] if member['name'] == member_name), None)
                if member_info:
                    # Update member information
                    member_info['age'] = int(self.age_entry.get()) if self.age_entry.get() else member_info['age']
                    member_info['dietary_restrictions'] = self.dietary_restrictions_text.get(1.0, tk.END).strip().split(',') if self.dietary_restrictions_text.get(1.0, tk.END).strip() else []
                    member_info['favorite_foods'] = self.favorite_foods_text.get(1.0, tk.END).strip().split(',') if self.favorite_foods_text.get(1.0, tk.END).strip() else []
                               
                    # Save profiles to file
                    self.save_profiles()
                    messagebox.showinfo("Success", "Profile updated successfully!")

            # Save kitchen profile changes
            self.family_profiles[family_name]["kitchens"][kitchen_name]["location"] = self.kitchen_location_entry.get() if self.kitchen_location_entry else []
            self.family_profiles[family_name]["kitchens"][kitchen_name]["tools_available"] = self.tools_available_text.get(1.0, tk.END).strip().split(',') if self.tools_available_text.get(1.0, tk.END).strip() else []
            self.family_profiles[family_name]["kitchens"][kitchen_name]["ingredients_available"] = self.ingredients_available_text.get(1.0, tk.END).strip().split(',') if self.ingredients_available_text.get(1.0, tk.END).strip() else []

        else:
            messagebox.showerror("Error", "Please select a family.")

    def get_meal_plan(self):
        # Placeholder for the get meal plan functionality
        print("Get Meal Plan button clicked")

    def get_recipe(self):
        """Get recipe based on family member preferences and selected meal type."""
        family_name = self.family_name_variable.get()
        member_name = self.family_member_variable.get()
        meal_type = self.meal_type_variable.get()
        complexity = self.meal_complexity_variable.get()

        if family_name and member_name and meal_type and complexity:
            # Get member's favorite foods and dietary restrictions
            member_info = next((member for member in self.family_profiles[family_name]['members'] if member['name'] == member_name), None)
            if member_info:
                favorite_foods = ', '.join(member_info['favorite_foods'])
                dietary_restrictions = ', '.join(member_info['dietary_restrictions'])

                # Construct the prompt for the recipe request
                prompt = (f"Please provide a recipe for {meal_type} that is "
                        f"{complexity} and considers {member_name}'s favorite foods: {favorite_foods}. "
                        f"Also, take into account any dietary restrictions: {dietary_restrictions}.")

                # Simulate receiving a recipe response
                recipe_response = self.request_recipe_from_api(prompt)
                self.display_recipe(recipe_response)
            else:
                messagebox.showerror("Error", "Member information not found.")
        else:
            messagebox.showerror("Error", "Please select a family, member, meal type, and complexity.")

    def request_recipe_from_api(self, prompt):
        """Request a recipe from the OpenAI API using the provided prompt."""
        api_url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",  # Use the API_KEY variable
            "Content-Type": "application/json"
        }

        # Construct the request payload
        data = {
            "model": "gpt-4",  # Specify the model you want to use
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,  # Adjust as necessary to get complete recipes
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
            return self.parse_recipe_response(recipe_text)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None  # Return None in case of an error

    def parse_recipe_response(self, response_text):
        """Parse the recipe response text into a structured format."""
        # This is a simple parser; you may want to enhance it based on how you format prompts
        lines = response_text.strip().split('\n')
        title = lines[0]  # Assuming the first line is the title
        ingredients = []
        instructions = []

        # Simple logic to separate ingredients and instructions
        in_ingredients = True
        for line in lines[1:]:
            if line.lower().startswith("ingredients:"):
                in_ingredients = True
                continue
            elif line.lower().startswith("instructions:"):
                in_ingredients = False
                continue

            if in_ingredients:
                ingredients.append(line.strip())
            else:
                instructions.append(line.strip())

        return {
            "title": title,
            "ingredients": ingredients,
            "instructions": '\n'.join(instructions),
            "servings": "4",  # Placeholder; adjust based on your needs
            "prep_time": "10 minutes",  # Placeholder; adjust based on your needs
            "cook_time": "15 minutes"  # Placeholder; adjust based on your needs
        }

    def display_recipe(self, recipe):
        """Display the recipe in a new frame."""
        # Create a new window for the recipe
        recipe_window = tk.Toplevel(self)
        recipe_window.title("Recipe Details")

        # Recipe Title
        title_label = tk.Label(recipe_window, text=recipe['title'], font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Ingredients
        ingredients_label = tk.Label(recipe_window, text="Ingredients:", font=("Helvetica", 14))
        ingredients_label.pack(anchor="w")
        ingredients_text = tk.Text(recipe_window, height=5, width=50, wrap=tk.WORD)
        ingredients_text.insert(tk.END, '\n'.join(recipe['ingredients']))
        ingredients_text.config(state=tk.DISABLED)  # Make it read-only
        ingredients_text.pack(pady=5)

        # Instructions
        instructions_label = tk.Label(recipe_window, text="Instructions:", font=("Helvetica", 14))
        instructions_label.pack(anchor="w")
        instructions_text = tk.Text(recipe_window, height=10, width=50, wrap=tk.WORD)
        instructions_text.insert(tk.END, recipe['instructions'])
        instructions_text.config(state=tk.DISABLED)  # Make it read-only
        instructions_text.pack(pady=5)

        # Serving Information
        serving_info_label = tk.Label(recipe_window, text=f"Servings: {recipe['servings']}, Prep Time: {recipe['prep_time']}, Cook Time: {recipe['cook_time']}", font=("Helvetica", 12))
        serving_info_label.pack(pady=10)

# Initialize and run the application
if __name__ == "__main__":
    app = SmartKitchenAssistantApp()
    app.mainloop()
