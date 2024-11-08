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


## Profile

def load_profiles():
    """Load user profiles from the JSON file."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    """Save user profiles to the JSON file."""
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)

def create_profile(username):
    """Create a new user profile."""
    profiles = load_profiles()
    
    if username in profiles:
        print(f"Profile for {username} already exists.")
        return None
    
    profiles[username] = {
        'dietary_restrictions': [],
        'preferred_cuisine': [],
        'cooking_tools': [],
        'preferences': [],  # Key for specific food preferences
        'cooking_levels': [],  # Key for cooking skill levels
        'recipe_complexity': None,  # Key for complexity rating
        'dietary_preferences': []  # Key for dietary preferences
    }
    
    save_profiles(profiles)
    print(f"Profile for {username} created successfully.")
    return profiles[username]

def read_profile(username):
    """Read a user profile."""
    profiles = load_profiles()
    
    if username in profiles:
        return profiles[username]
    
    print(f"No profile found for {username}.")
    return None

# Function to handle profile selection and display recipes
def select_profile():
    profiles = load_profiles()
    if not profiles:
        messagebox.showinfo("Info", "No profiles found. Please create a new profile.")
        return
    
    profile_names = list(profiles.keys())
    selected_profile_name = simpledialog.askstring("Select Profile", "Available profiles:\n" + "\n".join(profile_names))

    if selected_profile_name in profiles:
        user_profile = profiles[selected_profile_name]
        messagebox.showinfo("Profile Selected", f"Profile '{selected_profile_name}' selected.")
        
        # Get recipe suggestions and provide cooking guidance
        recipe = get_recipe_suggestions(user_profile)
        if recipe:
            provide_cooking_guidance(recipe)
            collect_feedback(selected_profile_name, recipe['title'])
        else:
            messagebox.showinfo("Info", "No recipe found for the selected profile.")
    else:
        messagebox.showerror("Error", "Profile not found. Please check the username.")

def update_profile(username, dietary_restrictions=None, preferred_cuisine=None, cooking_tools=None):
    """Update an existing user profile."""
    profiles = load_profiles()
    
    if username not in profiles:
        print(f"No profile found for {username}.")
        return None
    
    if dietary_restrictions is not None:
        profiles[username]['dietary_restrictions'] = dietary_restrictions
    if preferred_cuisine is not None:
        profiles[username]['preferred_cuisine'] = preferred_cuisine
    if cooking_tools is not None:
        profiles[username]['cooking_tools'] = cooking_tools
    
    save_profiles(profiles)
    print(f"Profile for {username} updated successfully.")
    return profiles[username]

def add_profile_entry(username, key, value):
    """Add a key-value pair to an existing user profile."""
    profiles = load_profiles()
    
    if username not in profiles:
        print(f"No profile found for {username}.")
        return None
    
    profiles[username][key] = value
    save_profiles(profiles)
    print(f"Added '{key}: {value}' to profile for {username}.")
    return profiles[username]

def delete_profile(username):
    """Delete a user profile."""
    profiles = load_profiles()
    
    if username in profiles:
        del profiles[username]
        save_profiles(profiles)
        print(f"Profile for {username} deleted successfully.")
        return True
    
    print(f"No profile found for {username}.")
    return False

def update_profile_from_analysis(user_profile, analysis):
    """Update the user profile based on the feedback analysis."""
    # Example logic to parse analysis and update profile
    if "add preference" in analysis:
        new_preference = analysis.split("add preference: ")[1].strip()
        user_profile['preferences'].append(new_preference)
    if "increase cooking level" in analysis:
        user_profile['cooking_levels'].append("Intermediate")  # Example update
    # Continue for other potential updates
    
    save_profiles(user_profile)

## Assistant

def get_recipe_suggestions(user_profile):
    """Get personalized recipe suggestions based on user profile."""
    dietary_restrictions = user_profile.get('dietary_restrictions', [])
    preferred_cuisine = user_profile.get('preferred_cuisine', "")
    
    prompt = f"Suggest a recipe in {preferred_cuisine} cuisine for a {', '.join(dietary_restrictions)} meal. Include ingredients and steps."
    
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
        recipe_text = suggestions['choices'][0]['message']['content']
        
        # Parse the recipe text into structured format
        return parse_recipe(recipe_text)
        
    except Exception as e:
        append_text(f"Error fetching recipes: {e}")
        return None

def parse_recipe(recipe_text):
    """Parse the recipe text into a structured format."""
    lines = recipe_text.strip().split('\n')
    title = lines[0].strip()
    ingredients = []
    steps = []
    
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
            ingredients.append(line)
        elif section == 'steps':
            steps.append(line)
    
    return {
        'title': title,
        'ingredients': ingredients,
        'steps': steps
    }

def provide_cooking_guidance(recipe):
    """Provide step-by-step cooking guidance to the user."""
    append_text(f"Starting recipe: {recipe['title']}\n")
    append_text("Ingredients:")
    for ingredient in recipe['ingredients']:
        append_text(f"- {ingredient}")
    
    append_text("\nCooking Steps:")
    for index, step in enumerate(recipe['steps']):
        append_text(f"Step {index + 1}: {step}")
        # Wait for user input to proceed to the next step
        input("Press Enter to continue to the next step...")
    
    append_text("\nCooking complete! Enjoy your meal!")

## Feedback

def collect_feedback(username, recipe_title):
    """Collect feedback from the user after cooking."""
    rating = input(f"Please rate the recipe '{recipe_title}' (1-5): ")
    comments = input("Any comments about this recipe? (optional): ")

    feedback_entry = {
        'user': username,
        'recipe_title': recipe_title,
        'rating': rating,
        'comments': comments
    }
    
    feedback = load_feedback()
    feedback.append(feedback_entry)
    save_feedback(feedback)

    # Analyze feedback to update the user profile
    user_profile = read_profile(username)
    analysis = analyze_feedback(comments, user_profile)
    
    if analysis:
        print(f"Feedback Analysis: {analysis}")
        # Here you would parse the analysis and update the user profile accordingly
        # For example, if the analysis suggests adding a preference:
        # user_profile['preferences'].append(new_preference)
        # save_profiles(user_profile)
    
    print("Thank you for your feedback!")

def analyze_feedback(feedback, user_profile):
    """Analyze user feedback to update the user profile."""
    # Construct a prompt for the OpenAI API
    prompt = (
        f"Analyze the following feedback: '{feedback}'. "
        f"The user's current profile is: {user_profile}. "
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

def load_feedback():
    """Load user feedback from the JSON file."""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedback(feedback):
    """Save user feedback to the JSON file."""
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback, f, indent=4)

## GUI

def create_gui():
    global text_area  # Make the text_area global to access it in other functions
    root = tk.Tk()
    root.title("Smart Cooking Assistant")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    title_label = tk.Label(frame, text="Welcome to the Smart Cooking Assistant!", font=("Helvetica", 16))
    title_label.pack(pady=10)

    select_button = tk.Button(frame, text="Select Profile", command=select_profile)
    select_button.pack(pady=5)

    # Create a scrolled text area for displaying messages
    text_area = scrolledtext.ScrolledText(frame, width=50, height=15, wrap=tk.WORD)
    text_area.pack(pady=10)

    exit_button = tk.Button(frame, text="Exit", command=root.quit)
    exit_button.pack(pady=20)

    root.mainloop()

# Function to append text to the text area
def append_text(message):
    # Insert the message at the end of the text area
    text_area.insert(tk.END, message + "\n")
    # Scroll to the end of the text area
    text_area.see(tk.END)
# Example usage
if __name__ == "__main__":
    create_gui()
