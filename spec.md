# Project Summary
The **Smart Cooking Assistant** is an AI-powered application designed to guide users through meal preparation while personalizing their cooking experience. The assistant adapts to each user’s preferences, skill level, and available kitchen tools, using an intelligent profiling system that evolves based on interactions. This project aims to create a tool that not only provides recipes but also enhances the user’s culinary skills by offering tailored suggestions, step-by-step guidance, and dynamic optimization of recipe plans. Whether the user is a novice cook, a parent managing dietary restrictions, or a caregiver navigating complex nutrition needs, the assistant learns and grows with each interaction to deliver an increasingly personalized experience.

Key to the assistant’s functionality is the creation of detailed user profiles. These profiles store information about food preferences, available ingredients, and kitchen tools, and are continuously updated through feedback during and after the cooking process. By leveraging the OpenAI ChatGPT API, the system uses machine learning models to analyze user inputs (both text and voice), extracting insights that further refine the profile. This allows the assistant to suggest recipes and tools that suit the user’s specific needs. The assistant can also connect with external apps, such as grocery trackers, to update profiles based on ingredient availability and provide real-time recipe suggestions based on what’s in the pantry.

The initial prototype will feature a desktop-based graphical user interface (GUI) with text and speech input capabilities. Users will interact with the assistant conversationally, and while voice recognition is a long-term goal, it may be omitted in early versions. The assistant will display recipe instructions, ingredient lists, and other relevant data, all while maintaining a smooth, guided user experience. The prototype will rely on Python dicts stored as JSON files for profile management, although further research into scalable data storage (e.g., databases) is planned as the project progresses.

In addition to the OpenAI API for natural language processing, future versions may incorporate APIs for voice recognition and ingredient tracking. As the assistant grows, the focus will be on refining how user feedback is handled and how the assistant dynamically updates profiles in real time, ensuring that each cooking experience is optimized for the individual.

This project explores the boundaries of AI in daily life, particularly in the kitchen, where personalization can have a significant impact on user satisfaction and cooking efficiency. The ultimate goal is to create a system that not only improves the cooking process but also enhances the user’s confidence and knowledge over time.

# Task Vignettes

## 1)	User Recipe Selection and Cooking Assistance
### Vignette: 
John is a novice cook looking to prepare dinner for his family. He opens the Smart Cooking Assistant on his laptop and is greeted by a friendly prompt asking how he would like to proceed. John asks for recipe suggestions, and the assistant replies with a few personalized options based on his profile, which includes his family’s dietary preferences (vegetarian) and the ingredients available in his pantry. John selects a "Vegetable Stir-Fry" recipe from the suggestions.
  
The assistant verifies that John has all the required ingredients and tools, cross-referencing the grocery list and tools stored in his profile. After confirming he has everything, the assistant walks John through the steps, pausing after each one to ensure he’s ready to continue. The assistant also provides additional context when John asks for clarification on how to properly dice vegetables, utilizing video or image instructions. Throughout the process, the assistant notes John’s feedback on each step, improving the profile for future recipe recommendations.
  
### Technical Details:
#### Input: 
- The user requests a recipe suggestion via voice or text. Inputs are passed to the OpenAI ChatGPT API to generate responses.
#### Profile Access: 
- The system retrieves user profile data (dietary preferences, ingredient availability, and cooking skills) to personalize recipe suggestions.
#### External Data: 
- The system checks the user’s ingredient inventory by accessing linked grocery tracking apps or stored profile data.
#### User Interface: 
- The GUI displays recipe options with the ability to select and confirm ingredients. After selection, a step-by-step guide is displayed. The assistant also provides an option to replay or elaborate on any specific step.
#### Voice Interaction: 
- Basic voice interaction for receiving user commands and asking clarifying questions (optional for early prototypes).
#### Data Flow: 
- User interaction data is collected and stored in the profile, refining future interactions and recipe suggestions.
#### Feedback Loop: 
- User feedback after completing steps is analyzed by the LLM to further optimize future experiences.


## 2)	Profile Creation and Personalization
### Vignette: 
Sarah is a new user of the Smart Cooking Assistant and needs to set up her profile. Upon launching the assistant, she is asked if she would like the assistant to remember her preferences. Sarah confirms, and the assistant asks a few key questions to personalize her profile: "Do you have any dietary restrictions?", "Which cuisine do you prefer?", and "Which cooking tools do you use frequently?" 

Sarah inputs that she is vegan, loves Mediterranean cuisine, and has a slow cooker, blender, and basic kitchen tools.
The assistant uses Sarah’s answers to create her initial profile, which will be refined over time based on her cooking behavior and additional feedback. Sarah can also integrate her grocery app with the assistant, allowing it to track her pantry items and recommend recipes accordingly. Once the profile is created, Sarah can immediately start receiving personalized recipe suggestions.

### Technical Details:
#### Input: 
- Initial user responses to questions about dietary restrictions, cuisine preferences, and kitchen tools.
#### Profile Creation: 
- A user profile is created, with key preferences stored in a JSON file (or later in a database). Each user has a unique profile that evolves based on interactions.
#### External Integration: 
- The assistant connects with third-party apps (e.g., grocery trackers) to sync data on ingredient availability.
#### Data Flow: 
- Data is stored locally or on the cloud depending on user preference. Profile updates happen automatically when Sarah provides feedback or makes changes to her preferences.
#### User Interface: 
- The profile setup is guided via a clean, user-friendly GUI with text and optional voice interaction.


## 3)	Ingredient Substitution and Alternative Suggestions
### Vignette: 
Emma is preparing a recipe for lasagna when the Smart Cooking Assistant informs her that she is missing one key ingredient: ricotta cheese. The assistant suggests several substitutions based on the ingredients Emma has in her pantry, such as cottage cheese or a tofu-based alternative. It also offers to adjust the recipe slightly to accommodate the substitution. Emma selects the cottage cheese option, and the assistant seamlessly updates the instructions.

### Technical Details:
#### Input: 
- Missing ingredient triggers the assistant to suggest alternatives.
#### Data Handling: 
- The assistant accesses the user’s pantry data, retrieves ingredient substitutions from a pre-defined database and suggests alternatives.
#### User Interaction: 
- Emma selects an alternative via the smart display or verbally.
#### Output: 
- The recipe is dynamically updated with the new ingredient.


## 4)	Cooking Progress Reminders and Timers
### Vignette: 
David is making a slow-cooked stew using the assistant, and after prepping the ingredients, he starts the cooking process. The assistant reminds him to check on the stew every 30 minutes and provides updates on the remaining cooking time. When it’s time to add the vegetables, the assistant alerts him via voice and updates the progress on the screen.

### Technical Details:
#### Input: 
- Cooking start triggers reminders.
#### Data Handling: 
- Timer data is managed locally or on the cloud, with notifications linked to each cooking step.
#### User Interaction: 
- Verbal or text feedback acknowledges the alert and moves forward with the cooking process.
#### Output: 
- Verbal reminders, and visual updates on the screen.


## 5)	Post-Meal Feedback and Profile Update
### Vignette: 
After completing the meal, Lisa provides feedback to the assistant on how it went. She rates the recipe and answers a few follow-up questions about the cooking process—whether she found it easy or if there were confusing steps. The assistant uses this feedback to further refine Lisa’s profile, noting her preference for faster, easier recipes and reducing the complexity of future recipe suggestions.

### Technical Details:
#### Input: 
- User feedback through verbal or text input, rating system.
#### Data Handling: 
- The assistant processes feedback and updates the user profile accordingly.
#### User Interaction: 
- Post-cooking feedback, and recipe rating on the display or through voice.
#### Output: 
- An updated profile that adjusts future recommendations.

![Block Diagram of Cooking Assistant](Cooking Assistant Block Diagram.png)
  
