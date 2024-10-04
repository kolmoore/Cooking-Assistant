import json
import requests
import os
from dotenv import load_dotenv

# Define the path for the user profiles JSON file
PROFILE_FILE = 'profiles/user_profiles.json'

# Load environment variables from .env file
load_dotenv()

# Your OpenAI API key
API_KEY = os.getenv('OPENAI_API_KEY')
# Ensure the profiles directory exists
os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)

## Profile Management

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

def create_profile(username, dietary_restrictions, preferred_cuisine, cooking_tools):
    """Create a new user profile."""
    profiles = load_profiles()
    
    if username in profiles:
        print(f"Profile for {username} already exists.")
        return None
    
    profiles[username] = {
        'dietary_restrictions': dietary_restrictions,
        'preferred_cuisine': preferred_cuisine,
        'cooking_tools': cooking_tools
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

## ChatGPT Management

def get_recipe_suggestions(user_profile):
    """Get personalized recipe suggestions based on user profile."""
    dietary_restrictions = user_profile.get('dietary_restrictions', [])
    preferred_cuisine = user_profile.get('preferred_cuisine', "")
    
    prompt = f"Suggest some recipes for a {', '.join(dietary_restrictions)} meal in {preferred_cuisine} cuisine."
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'model': 'gpt-3.5-turbo',  # or 'gpt-4' if you have access
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 100,  # Adjust the number of tokens based on your needs
    }
    
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        suggestions = response.json()
        recipes = suggestions['choices'][0]['message']['content']
        return recipes
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Create a profile for testing
    create_profile("Sarah", ["vegan"], "Mediterranean", ["slow cooker", "blender"])
    
    # Fetch the profile
    user_profile = read_profile("Sarah")
    
    # Get recipe suggestions
    recipes = get_recipe_suggestions(user_profile)
    print(f"Recipe Suggestions for {user_profile['preferred_cuisine']} cuisine: {recipes}")
