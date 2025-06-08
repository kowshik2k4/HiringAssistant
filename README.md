# 💬 TalentScout Hiring Assistant
TalentScout Hiring Assistant is a smart, conversational AI-powered hiring assistant designed to streamline the initial technical screening process for candidates in tech roles. Built with Streamlit and integrated with LLMs (Large Language Models), this chatbot interacts with candidates, gathers their personal and professional details, and dynamically generates tailored technical questions based on their declared tech stack using Gemini 2.5 Flash

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hiringassistant-yjyph2rqgq9vpx8tzdmxyg.streamlit.app/)

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
## GEMINI 2.5 FLASH is used with API
