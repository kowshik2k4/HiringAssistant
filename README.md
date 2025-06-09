# 💬 TalentScout Hiring Assistant
TalentScout Hiring Assistant is a smart, conversational AI-powered hiring assistant designed to streamline the initial technical screening process for candidates in tech roles. Built with Streamlit and integrated with LLMs (Large Language Models), this chatbot interacts with candidates, gathers their personal and professional details, and dynamically generates tailored technical questions based on their declared tech stack using Gemini 2.5 Flash

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hiringassistant-em49cabgydnjffvlygqwlp.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
# 🚀 Features
1. First list item
     - Collects key candidate details:
     - Full Name, Email, Phone Number
     - Experience, Desired Position, Current Location
     - Tech Stack
2. Generates tailored technical questions based on technologies listed
3. Maintains conversational flow and context
4. Fallback mechanism for invalid input
5. Clean UI using Streamlit with buttons and form validation

# 🛠️ Tech Stack & Architecture
## 🧰 Libraries Used
|Library	  |Purpose|
| ---  | ---  |
|streamlit|	      UI development and state management|
|re	|               Regex-based input validation|
|google.genai|      for generating questions about TechStack| 

**GEMINI 2.5 FLASH is used with API**
# App Flow
🔴In order to run the app on your device please ensure that u have a gemini api key.U can get one at [Get GEMINI API](https://ai.google.dev/gemini-api/docs/api-key)
* On launch, TalentScout welcomes you and prompts you to start the application.
* You will be asked to provide basic information like your name, email, phone number, years of experience, position you are applying for, location, and your tech stack.
* The chatbot provides a tip about typing exit words to quit the process gracefully.
* Based on your tech stack, TalentScout generates 3-5 tailored multiple-choice technical questions.
* Submit your answers to complete the assessment.
* At the end, your score and feedback will be displayed with next steps.

# Prompts Used
the tailored prompts used are available on prompts.py
