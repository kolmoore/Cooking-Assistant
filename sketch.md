# Smart Cooking Assistant

## Who would be the users? Are there secondary stakeholders?

- Anyone who likes to cook at home and wants to try more advanced recipes but doesn’t know how.
- Anyone who would like a cooking assistant who learns from their interactions and improves over time

## What is the task? What problem would it (help to) solve?

- The task is to guide a user through cooking a meal.  
- The assistant can take a suggestion for a recipe or it can suggest a recipe to the user.
- The recipe selection and tools used will be automatically optimized based on learned knowledge about the user.
- This learned knowledge will be in the form of a profile that includes information about the users’ preferences, cooking skills, and available ingredients and tools.

## What is the primary interaction? Is there an interaction loop?

- The user will initially interact with the assistant by asking for help.
- The user should confirm that they want the assistant to remember them.
- If the user wants to be remembered, the assistant must ask for the user’s name or get it somewhere else in the UI like a drop-down menu.
- If the user is new and requesting a recipe suggestion, the assistant will ask a few general questions about preferences, to make a more tailored response.  
- After preferences are agreed upon, the assistant must validate that the user has the required ingredients and tools available.
- If the memory feature is active and the user validates that they have an ingredient or tool, the assistant should remember that and not ask to validate this again.
- The assistant could also remember certain ingredients for future recipes, such as custom spice mixes.

## What kind of user interfaces could you use? 

- Initial prototypes would use a GUI to be run on a laptop.
- Must have a way to converse with the assistant and allow for the assistant to display various pieces of information relating to the recipe plan.
- Would like to incorporate the ability to input speech and read the instructions to the user to imitate a conversation.

## What data would be used (input), how would you get it and how is it processed/analyzed?

- The data we use is the user’s input.  
 - Whatever they say or type in will be used to create a profile of that user.  
- There will be a workflow dedicated to creating and controlling these profiles.
- There will be a check to determine if a user’s input should drive a change in the user’s profile and a trigger when an update is needed. 
 - The information in the profile still needs to be determined and investigated. (What structure leads to the best UX)

## What are the results and how are they presented? 

- The results of developing the profile are presented in a personalized experience when working through a recipe. 

### The profile can help optimize the following:
 - Tools available
 - Ingredients available
 - Previous recipes made
 - Special Ingredient preferences
 - Regional preferences


## Seeing how helpful of a profile we can quickly create with the help of LLMs is a primary part of what this project looks to explore.  
