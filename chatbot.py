import google.generativeai as genai
import streamlit as st
import json
from prompts import mcq_generation_prompt

# Configure Gemini with Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load Gemini Pro model
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
def clean_gemini_response(response_text: str) -> str:
    # Remove markdown code fences like ```json or ```
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        # Remove the first line with ```
        cleaned = "\n".join(cleaned.split("\n")[1:])
    if cleaned.endswith("```"):
        # Remove last line with ```
        cleaned = "\n".join(cleaned.split("\n")[:-1])
    return cleaned.strip()

def call_gemini(prompt: str, temperature: float = 0.7) -> str:
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

def generate_mcq_questions(tech_stack: str, experience: str):
    prompt = mcq_generation_prompt(tech_stack, experience)
    response_text = call_gemini(prompt)

    # st.write("=== Raw Gemini output ===")
    # st.text(response_text)

    cleaned_text = clean_gemini_response(response_text)

    try:
        questions = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse generated questions JSON: {e}")
        questions = []
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        questions = []

    return questions


def evaluate_mcq_answer(question: dict, selected_option: str):
    correct_answer = question.get("answer", "")
    is_correct = selected_option.strip() == correct_answer.strip()
    st.write(is_correct)
    if is_correct:
        feedback = "✅ Correct! Great job."
    else:
        feedback = f"❌ Incorrect. The correct answer is: {correct_answer}."
    return is_correct, feedback
