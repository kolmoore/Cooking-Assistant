import json
import requests
import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from dotenv import load_dotenv

# Define the path for the user profiles JSON file
PROFILE_FILE = 'profiles/user_profiles.json'
FEEDBACK_FILE = 'feedback/user_feedback.json'

# Ensure the profiles directory exists
os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

# Load environment variables from .env file
load_dotenv()
# Your OpenAI API key
API_KEY = os.getenv('OPENAI_API_KEY')

## GUI
class Cooking_Assistant_App(tk.Tk):
    def __init__(self):
        super().__init__()

        
        self.title("Smart Cooking Assistant")

        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        self.title_label = tk.Label(self.frame, text="Welcome to the Smart Cooking Assistant!", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(padx=10,pady=10)

        # Label to display the current profile
        self.profile_label = tk.Label(self.control_frame, text="Current Profile: None", font=("Helvetica", 12))
        self.profile_label.grid(row=0,column=0,pady=5)

        self.select_button = tk.Button(self.control_frame, text="Select Profile", command=self.select_profile)
        self.select_button.grid(row=0,column=1,pady=5)

        self.create_button = tk.Button(self.control_frame, text="Create Profile", command=self.create_profile)
        self.create_button.grid(row=0,column=2,pady=5)

        self.view_button = tk.Button(self.control_frame, text="View Profiles", command=self.view_profiles_gui)
        self.view_button.grid(row=0,column=3,pady=5)

        self.update_button = tk.Button(self.control_frame, text="Update Profile", command=self.update_profile_gui)
        self.update_button.grid(row=0,column=4,pady=5)

        # Create a scrolled text area for displaying messages
        self.text_area = scrolledtext.ScrolledText(self.frame, width=50, height=15, wrap=tk.WORD)
        self.text_area.pack(pady=10)

        # Create an editable text area for user input
        self.input_text = tk.Text(self.frame, width=50, height=3, wrap=tk.WORD)
        self.input_text.pack(pady=5)

        # Create a submit button
        self.submit_button = tk.Button(self.frame, text="Submit Response", command=self.submit_response)
        self.submit_button.pack(pady=5)

        self.exit_button = tk.Button(self.frame, text="Exit", command=self.quit)
        self.exit_button.pack(pady=20)

    def append_text(self, message):
        # Insert the message at the end of the text area
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def clear_text(self):
        # Insert the message at the end of the text area
        self.text_area.config(text=())

    def wait_for_response(self):
        self.response_submitted = False

        while not self.response_submitted:
            t = 0
            if t > 100000:
                self.append_text("Waiting on user input")
                t += 1
    
    def submit_response(self):
        """Handle the submission of user input."""
        user_input = self.input_text.get("1.0", tk.END).strip()  # Get input from the text box
        if user_input:
            self.append_text(f"\nYou: {user_input}\n")  # Display user input in the scrolled text area
            self.input_text.delete("1.0", tk.END)  # Clear the text box
            # Process the input based on the current context
            match self.current_operation:
                case 'select_profile':
                    self.username = user_input
                    self.append_text(f"Hello {self.username}!  It's a pleasure to assist you today!")
                case 'profile_dr':
                    self.profiles[self.username]['dietary_restrictions'] = user_input
                    self.save_profiles()
                    self.append_text(f"Dietary Restrictions for '{self.username}' updated successfully.")
                case 'profile_ff':
                    self.profiles[self.username]['favorite_food'] = user_input
                    self.save_profiles()
                    self.append_text(f"Favorite Food for '{self.username}' updated successfully.")
                case 'profile_pt':
                    self.profiles[self.username]['preferred_tools'] = user_input
                    self.save_profiles()
                    self.append_text(f"Preferred Tools for '{self.username}' updated successfully.")
                case 'profile_pi':
                    self.profiles[self.username]['preferred_ingredients'] = user_input
                    self.save_profiles()
                    self.append_text(f"Preferred Ingredients for '{self.username}' updated successfully.")
                case 'profile_sl':
                    self.profiles[self.username][''] = user_input
                    self.save_profiles()
                    self.append_text(f"Skill Level for '{self.username}' updated successfully.")
                case 'profile_rc':
                    self.profiles[self.username]['recipe_complexity'] = user_input
                    self.save_profiles()
                    self.append_text(f"Recipe Complexity for '{self.username}' updated successfully.")
                case 'update_profile':
                    match user_input:
                        case '1':
                            self.update_dietrestrict()
                        case '2':
                            self.update_favorite_food()
                        case '3':
                            self.update_preferred_tools()
                        case '4':
                            self.update_prefered_ingredients()
                        case '5':
                            self.update_cooking_skill_level()
                        case '6':
                            self.update_recipe_complexity()
                    

        self.response_submitted = True


    ## Profile

    def load_profiles(self):
        """Load user profiles from the JSON file."""
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, 'r') as f:
                return json.load(f)
        return {}

    def create_profile(self):
        """Open a dialog to create a new user profile."""
        if self.username is None:
            self.append_text("Please Enter A Username")
            self.current_operation = 'create_profile'
            return
        
        
        if self.username in self.profiles:
            self.append_text(f"Profile for {self.username} already exists.")
            return None  
        
        self.save_profiles()
        self.append_text(f"Profile for {self.username} created successfully.")

    def view_profiles_gui(self):
        """Open a dialog to view existing profiles."""
        profiles = self.load_profiles()
        if not profiles:
            self.append_text("No profiles found.")
            return
        
        profile_info = "\n".join([f"{name}:\n {details}" for name, details in profiles.items()])
        self.append_text("User Profiles: \n" + profile_info)

    def update_profile_gui(self):

        if self.username:
            self.profiles = self.load_profiles()
            if self.username not in self.profiles:
                self.profiles[self.username] = {
                    'dietary_restrictions': [],
                    'favorite_foods': [],
                    'preferred_tools': [],
                    'preferred_ingredients': [],  # Key for specific food preferences
                    'skill_level': [],  # Key for cooking skill levels
                    'recipe_complexity': None,  # Key for complexity rating
                    }
                return
            
            self.append_text(f"What would you like to update?\n1 = Diet Resrictions \n2 = Favorite Foods \n3 = Preferred Tools \n4 = Preferred Ingredients \n5 = Cooking Skill Level \n6 = Recipe Complexity")
            self.current_operation = 'update_profile' 

    def update_dietrestrict(self):
            """Open a dialog to enter new user Dietary Restrictions."""
            self.append_text(f"Hello {self.username}! Do you have any dietary restrictions we should know about?\n  Please enter multiple items seperated by a comma or press cancel to skip")
            self.current_operation = 'profile_dr'  # Set the current operation context
        
    def update_favorite_food(self):
            """Open a dialog to enter new user Preferred Cuisine."""
            self.append_text("What is your favortie food?  Press cancel to skip")
            self.current_operation = 'profile_ff'  # Set the current operation context

    def update_preferred_tools(self):
            """Open a dialog to enter new user Cooking Tools."""
            self.append_text("Are there any types of cooking tools that you'd like to add to your prefered tools?\n Please enter multiple items seperated by a comma or press cancel to skip")
            self.current_operation = 'profile_pt'  # Set the current operation context  

    def update_prefered_ingredients(self):
            """Open a dialog to enter preferences."""
            self.append_text("Are there any specific ingredients that you prefer?\n Please enter multiple items seperated by a comma or press cancel to skip")
            self.current_operation = 'profile_pi'  # Set the current operation context  

    def update_cooking_skill_level(self):
            """Open a dialog to enter preferences."""
            self.append_text("What would you say your skill level is?  Press cancel to skip")
            self.current_operation = 'profile_sl'  # Set the current operation context  

            self.save_profiles()
            self.append_text(f"Skill Level for '{self.username}' updated successfully.")

    def update_recipe_complexity(self):
            """Open a dialog to enter preferences."""
            self.append_text("How complex of a recipe are you looking to make? Press cancel to skip")
            self.current_operation = 'profile_ct'  # Set the current operation context  

            self.save_profiles()
            self.append_text(f"Preferred Recipe Complexity for '{self.username}' updated successfully.")
    
    def save_profiles(self):
        """Save user profiles to the JSON file."""
        with open(PROFILE_FILE, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def read_profile(self):
        """Read a user profile."""
        profiles = self.load_profiles()
        
        if self.username in profiles:
            return profiles[self.username]
        
        self.append_text(f"No profile found for {self.username}.")
        return None

    def select_profile(self):
        """Allow the user to select an existing profile."""
        self.profiles = self.load_profiles()
        if not self.profiles:
            self.append_text("No profiles found. Please create a new profile.")
            self.current_operation = 'create_profile'
            return
        
        profile_names = list(self.profiles.keys())
        self.append_text("Available profiles\n" + "\n".join(profile_names))

        """Open a dialog to create a new user profile."""
        self.append_text("Enter username to select profile:")
        self.current_operation = 'select_profile'  # Set the current operation context


    def find_recipe(self):

        if self.username in self.profiles:
            self.user_profile = self.profiles[self.username]
            self.append_text(f"Profile '{self.username}' selected.")
            self.profile_label.config(text=f"Current Profile: {self.username}")  # Update the label to show the current profile
            
            self.append_text(f"Finding Recipe suggestion for '{self.username}'.")
            # Get recipe suggestions and provide cooking guidance
            self.recipe = self.get_recipe_suggestions()
            if self.recipe:
                self.provide_cooking_guidance()
                self.collect_feedback()
            else:
                self.append_text("Info", "No recipe found for the selected profile.")
        else:
            self.append_text("Error", "Profile not found. Please check the username.")

    def add_profile_entry(self):
        """Add a key-value pair to an existing user profile."""
        profiles = self.load_profiles()
        
        if self.username not in profiles:
            self.append_text(f"No profile found for {self.username}.")
            return None
        
        profiles[self.username][self.key] = self.value
        self.save_profiles(profiles)
        print(f"Added '{self.key}: {self.value}' to profile for {self.username}.")
        return profiles[self.username]

    def delete_profile(self):
        """Delete a user profile."""
        self.profiles = self.load_profiles()
        
        if self.username in self.profiles:
            del self.profiles[self.username]
            self.save_profiles(self.profiles)
            self.append_text(f"Profile for {self.username} deleted successfully.")
            return True
        
        self.append_text(f"No profile found for {self.username}.")
        return False

    ## Assistant

    def get_recipe_suggestions(self):
        """Get personalized recipe suggestions based on user profile."""
        self.dietary_restrictions = self.user_profile.get('dietary_restrictions', [])
        self.preferred_cuisine = self.user_profile.get('preferred_cuisine', "")
        
        prompt = f"Suggest a recipe in {self.preferred_cuisine} cuisine for a {', '.join(self.dietary_restrictions)} meal. Include ingredients and steps."
        
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'model': 'gpt-3.5-turbo',  # or 'gpt-4' if you have access
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 200,  # Adjust the number of tokens based on your needs
        }
        
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses
            suggestions = response.json()
            self.recipe_text = suggestions['choices'][0]['message']['content']
            
            # Parse the recipe text into structured format
            return self.parse_recipe()
            
        except Exception as e:
            self.append_text(f"Error fetching recipes: {e}")
            return None

    def parse_recipe(self):
        """Parse the recipe text into a structured format."""
        lines = self.recipe_text.strip().split('\n')
        self.recipe_title = lines[0].strip()
        self.recipe_ingredients = []
        self.recipe_steps = []
        
        # Assuming a simple format: first line is title, then ingredients, then steps
        section = 'ingredients'
        for line in lines[1:]:
            line = line.strip()
            if line.lower() == 'steps:':
                section = 'steps'
                continue
            elif line.lower() == 'ingredients:':
                continue
            
            if section == 'ingredients':
                self.recipe_ingredients.append(line)
            elif section == 'steps':
                self.recipe_steps.append(line)
        
        return {
            'title': self.recipe_title,
            'ingredients': self.recipe_ingredients,
            'steps': self.recipe_steps
        }

    def provide_cooking_guidance(self):
        """Provide step-by-step cooking guidance to the user."""
        self.append_text(f"Starting recipe: {self.recipe['title']}\n")
        self.append_text("Ingredients:")
        for ingredient in self.recipe['ingredients']:
            self.append_text(f"- {ingredient}")
        
        self.append_text("\nCooking Steps:")
        for index, step in enumerate(self.recipe['steps']):
            self.append_text(f"Step {index + 1}: {step}")
            # Wait for user input to proceed to the next step
            self.ppend_text("Press Enter to continue to the next step...")
        
        self.append_text("\nCooking complete! Enjoy your meal!")

    ## Feedback

    def collect_feedback(self):
        """Collect feedback from the user after cooking."""
        rating = input(f"Please rate the recipe '{self.recipe_title}' (1-5): ")
        comments = input("Any comments about this recipe? (optional): ")

        feedback_entry = {
            'user': self.username,
            'recipe_title': self.recipe_title,
            'rating': rating,
            'comments': comments
        }
        
        self.feedback = self.load_feedback()
        self.feedback.append(feedback_entry)
        self.save_feedback()

        # Analyze feedback to update the user profile
        self.user_profile = self.read_profile()
        self.analysis = self.analyze_feedback()
        
        if self.analysis:
            print(f"Feedback Analysis: {self.analysis}")
            # Here you would parse the analysis and update the user profile accordingly
            # For example, if the analysis suggests adding a preference:
            # user_profile['preferences'].append(new_preference)
            # save_profiles(user_profile)
        
        print("Thank you for your feedback!")

    def analyze_feedback(self):
        """Analyze user feedback to update the user profile."""
        # Construct a prompt for the OpenAI API
        prompt = (
            f"Analyze the following feedback: '{self.feedback}'. "
            f"The user's current profile is: {self.user_profile}. "
            f"Suggest any updates to the user's profile based on the feedback."
        )

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            'model': 'gpt-3.5-turbo',  # or 'gpt-4' if you have access
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150,
        }

        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses
            suggestions = response.json()
            analysis = suggestions['choices'][0]['message']['content']
            return analysis  # This will include suggested updates to the profile
        except Exception as e:
            print(f"Error analyzing feedback: {e}")
            return None

    def load_feedback(self):
        """Load user feedback from the JSON file."""
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_feedback(self):
        """Save user feedback to the JSON file."""
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(self.feedback, f, indent=4)

# Initialize and run the application
if __name__ == "__main__":
    app = Cooking_Assistant_App()
    app.mainloop()