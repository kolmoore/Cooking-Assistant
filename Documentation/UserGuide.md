# User Guide for Smart Kitchen Assistant

Welcome to the **Smart Kitchen Assistant**! This application is designed to help families manage their recipes, dietary preferences, and meal planning efficiently. This user guide will provide you with an overview of the application’s features and instructions on how to use them.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Features](#features)
- [Navigating the Application](#navigating-the-application)
- [Managing Families](#managing-families)
- [Managing Recipes](#managing-recipes)
- [Creating Meal Plans](#creating-meal-plans)
- [Generating Grocery Lists](#generating-grocery-lists)
- [Editing Family Members](#editing-family-members)
- [Troubleshooting](#troubleshooting)
- [Frequently Asked Questions](#frequently-asked-questions)

## Introduction

The Smart Kitchen Assistant is a user-friendly application that allows families to store and organize their recipes, track dietary preferences, and create meal plans tailored to their needs.

## Getting Started

1. **Installation**: Follow the installation instructions in the `README.md` file to set up the application on your local machine.
2. **Open AI API**: For full functionality the user needs to order a project API key via https://platform.openai.com/account/api-keys.
3. **Launch the Application**: Run the application by executing the following command in your terminal: main.py

## Features

- **Family Management**: Add, edit, or remove family profiles and their members.
- **Recipe Management**: View, add, remove, and sort recipes based on various criteria.
- **Meal Planning**: Create customized meal plans based on family preferences.
- **Grocery List Generation**: Generate grocery lists based on selected recipes or meal plans.
- **Dietary Restrictions and Favorite Foods**: Manage dietary restrictions and favorite foods for each family member.

## Navigating the Application

Upon launching, you will see the welcome screen, which allows you to select a family or add a new one. Use the navigation buttons to access different sections of the application.

<img src="images/welcome_screen.png" alt="Welcome Screen" width="300" height="400">

## Managing Families

### Adding a Family

1. Click the **Add** button on the welcome screen.
2. Enter the family name in the prompt dialog and click **OK**.
3. The new family will be added to the list.

### Editing a Family

1. Select the family from the dropdown menu.
2. Click the **Edit** button to modify the family profile.
3. Make the necessary changes and save.

### Removing a Family

1. Select the family from the dropdown menu.
2. Click the **Remove** button and confirm the action.

### Selecting a family

1. Select the family from the dropdown menu.
2. Click the **Select** button to move to the **Main Menu**


### Main Menu

<img src="images/main_menu.png" alt="Main Menu" width="300" height="200">

## Managing Recipes

### Adding a Recipe

1. Navigate to the **Main Menu**.
2. Click the **Get Recipe** button to retrieve a recipe based on family preferences or manually add a recipe through the interface.
3. Fill in the recipe details and save.

### Viewing Recipes

1. In the **Main Menu**, the recipe list will display all available recipes.
2. Click on a recipe to view its details.

### Removing a Recipe

1. Select a recipe from the recipe list.
2. Click the **Remove Item** button to delete the recipe and confirm the action.

### Sorting Recipes

You can sort recipes by type, complexity, rating, and main ingredient using the dropdown menus in the **Main Menu**.

## Creating Meal Plans

1. Click the **Get Meal Plan** button in the **Main Menu**.
2. Select the meal types and family member preferences.
3. Click **OK** to generate a meal plan based on the provided criteria.

## Generating Grocery Lists

1. Select a recipe or meal plan from the recipe list.
2. Click the **Get Grocery List** button.
3. A new window will display the grocery list based on the selected item.


### Edit Member Screen

<img src="images/edit_users.png" alt="Edit Users" width="300" height="200">

## Editing Family Members

1. Click **Edit Family** on the **Main Menu** to navigate to the **Edit Family** screen.
2. Use the dropdown to select a family member.
3. Click **Edit Member** to modify their details.
4. Add dietary restrictions and favorite foods as needed.

## Troubleshooting

- **Application Does Not Start**: Ensure that all dependencies are installed (refer to `requirements.txt`).
- **API Key Issues**: Check your `.env` file to ensure the OpenAI API key is correctly set.

## Frequently Asked Questions

1. **Can I add multiple families?**
   - Yes, you can add as many families as needed.

2. **What happens if I remove a recipe?**
   - The recipe will be permanently deleted from the family profile.

3. **Is there a limit on the number of recipes or families?**
   - No, the application can handle multiple recipes and families as long as there is enough memory.

## Support

If you encounter any issues or have questions not covered in this guide, please reach out to the support team or check the project's GitHub repository for issues and updates.

### Instructions to Create the File:
1. Open a text editor (like Notepad, VS Code, or any Markdown editor).
2. Copy the above content.
3. Paste it into the editor.
4. Save the file as `USER_GUIDE.md` in your project directory.

This user guide provides a detailed overview of how to use the **Smart Kitchen Assistant** application, making it easier for users to navigate and utilize its features effectively. Feel free to modify or expand upon this guide as needed!