🟣 AI Code Explainer
Project Title: AI Code Explainer using Gemini 1.5 Flash
Name: Bezawada Haritha
1. Introduction
The AI Code Explainer is a web-based application designed to provide quick and concise explanations for code snippets across various programming languages. Leveraging the power of Google's Gemini 1.5 Flash generative AI model, this tool aims to enhance code comprehension by offering immediate, high-level summaries of code functionality. The application features a clean, intuitive user interface built with Streamlit, styled with a distinct purple theme.

2. Features
Brief Code Explanations: Provides a single, very short sentence describing the overall main purpose of a given code snippet.

Detailed Code Explanations: Offers a comprehensive, easy-to-understand, step-by-step breakdown of the code's functionality and logical flow.

Multi-Language Support: Capable of explaining code written in Python, C, C++, Java, JavaScript, Go, Rust, SQL, HTML/CSS/JS, with an auto-detect option.

Intuitive Web Interface: Built using Streamlit for a simple and responsive user experience.

Aesthetic Design: Features a custom purple color scheme with subtle AI-themed background patterns for an engaging visual appeal.

Powered by Gemini 1.5 Flash: Utilizes a fast and powerful generative AI model for efficient and accurate explanations.

3. Technologies Used
Python 3.9+: The core programming language for the application.

Streamlit: For building the interactive web user interface.

Requests Library: For making HTTP API calls to the Gemini 1.5 Flash model.

Google Gemini 1.5 Flash API: The generative AI model responsible for generating code explanations.

4. Setup and Local Installation
Follow these steps to set up and run the AI Code Explainer on your local machine.

4.1. Prerequisites
Python 3.9 or higher installed on your system.

pip (Python package installer), which usually comes with Python.

An active internet connection to access the Gemini 1.5 Flash API.

4.2. Clone the Repository
First, clone this GitHub repository to your local machine:

git clone https://github.com/YourUsername/AI-Code-Explainer.git
cd AI-Code-Explainer

(Replace https://github.com/YourUsername/AI-Code-Explainer.git with your actual GitHub repository URL)

4.3. Set Up a Python Virtual Environment (Recommended)
It's best practice to use a virtual environment to manage project dependencies.

python -m venv venv

4.4. Activate the Virtual Environment
On Windows (Command Prompt):

.\venv\Scripts\activate

On Windows (PowerShell):

.\venv\Scripts\Activate.ps1

On macOS/Linux:

source venv/bin/activate

4.5. Install Dependencies
Install the required Python libraries using pip:

pip install -r requirements.txt

4.6. API Key Configuration
This project uses the Google Gemini 1.5 Flash API for AI capabilities.

IMPORTANT NOTE FOR EVALUATORS:
When this project is run within the designated Canvas environment, the GEMINI_API_KEY is automatically provided by the system at runtime. You do not need to set it manually.

For local development outside the Canvas environment:
You would typically set your Gemini API key as an environment variable named GEMINI_API_KEY before running the application.

On Linux/macOS:

export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

On Windows (Command Prompt):

set GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

On Windows (PowerShell):

$env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

(Replace YOUR_ACTUAL_GEMINI_API_KEY_HERE with your actual Gemini API key obtained from Google AI Studio or Google Cloud Console.)

The app.py code is designed to check for this environment variable.

4.7. Run the Application
With the virtual environment activated and dependencies installed, run the Streamlit application:

streamlit run app.py

Your web browser should automatically open to http://localhost:8501 (or a similar local address) where you can interact with the AI Code Explainer.

5. Usage
Paste your code into the provided text area.

Select the programming language from the dropdown menu (or leave it as "Auto-detect").

Choose the explanation style ("Brief" or "Detailed") using the radio buttons.

Click the "Explain Code" button.

The explanation (brief or detailed, as chosen) of your code's main purpose will appear in the styled output box.

6. Project Structure
ai_code_explainer/
├── venv/                   # Python virtual environment (ignored by Git)
├── .gitignore              # Specifies files/folders to ignore in Git
├── app.py                  # Main Streamlit application code
└── requirements.txt        # Lists Python dependencies

7. Future Enhancements
Code Refactoring/Optimization Suggestions: Add functionality to suggest improvements to the provided code.

Error Identification/Debugging: Integrate features to help identify potential errors or suggest debugging approaches.

Multi-Modal Input: Explore explaining code from images (e.g., screenshots) using multimodal capabilities.

Interactive Code Playground: Allow users to edit and run code directly within the application.

User Feedback Loop: Implement a system for users to rate explanations, enabling continuous model improvement.

