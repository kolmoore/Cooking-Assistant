# Smart Kitchen Assistant

The **Smart Kitchen Assistant** is a user-friendly application designed to help families manage their recipes, dietary preferences, and meal planning. With this app, users can easily store and retrieve family profiles, add or edit family members, and create customized meal plans tailored to their preferences.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Family Management**: Add, edit, or remove families and their members.
- **Recipe Management**: View, add, remove, and sort recipes based on type, complexity, rating, and main ingredient.
- **Meal Planning**: Create and view meal plans tailored to the family's dietary preferences and favorite foods.
- **Grocery List Generation**: Generate grocery lists based on selected recipes or meal plans.
- **Dietary Restrictions and Favorite Foods**: Manage dietary restrictions and favorite foods for each family member.

## Technology Stack

The Smart Kitchen Assistant is built using the following technologies:

- **Python**: The main programming language used for the application.
- **Tkinter**: A standard GUI toolkit for building the user interface.
- **Requests**: A library for making HTTP requests to the OpenAI API for recipe generation.
- **JSON**: Used for storing family profiles and recipes.
- **dotenv**: For loading environment variables from a `.env` file.

## Installation

To set up the Smart Kitchen Assistant on your local machine, follow these steps:

1. **Clone the repository**:
   git clone https://github.com/yourusername/smart-kitchen-assistant.git
   cd smart-kitchen-assistant

2. **Create a virtual environment (optional but recommended)**:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages**:
   pip install -r requirements.txt

4. **Create a `.env` file** in the root directory and add your OpenAI API key:
   OPENAI_API_KEY=your_api_key_here

5. **Run the application**:
   main.py


## Usage

1. Launch the application. The welcome screen will appear, prompting you to select a family or add a new one.
2. Navigate to the main menu to manage recipes and family members.
3. Use the buttons to add or edit family members, view or manage recipes, and create meal plans.
4. Generate grocery lists based on selected recipes or meal plans.

## Contributing

We welcome contributions to improve the Smart Kitchen Assistant! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.


### Instructions to Create the File:
1. Open a text editor (like Notepad, VS Code, or any Markdown editor).
2. Copy the above content.
3. Paste it into the editor.
4. Save the file as `README.md` in your project directory.
