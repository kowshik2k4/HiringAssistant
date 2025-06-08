import streamlit as st
import re
from chatbot import generate_mcq_questions, evaluate_mcq_answer


st.set_page_config(page_title="TalentScout Hiring Assistant")
st.title("🤖 TalentScout - Hiring Assistant")
# --- Sticky Footer ---
st.markdown(
    """
    <hr style="margin-top: 3em;">
    <div style='text-align: center; font-size: 0.9em; color: #999;'>
        © 2025 TalentScout AI. All rights reserved. | Built with ❤️ using Streamlit and Gemini AI.|Sai Kowsik Tukuntla
    </div>
    """,
    unsafe_allow_html=True
)
fields = ["name", "email", "phone", "experience", "position", "location", "tech_stack"]
questions_text = {
    "name": "What is your full name?",
    "email": "What is your email address?",
    "phone": "What is your phone number?",
    "experience": "How many years of experience do you have?",
    "position": "What position are you applying for?",
    "location": "Where are you currently located?",
    "tech_stack": "Please list your tech stack (languages, frameworks, tools)."
}

# Initialize session state variables
if "started" not in st.session_state:
    st.session_state.started = False
if "current_field_index" not in st.session_state:
    st.session_state.current_field_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "input_value" not in st.session_state:
    st.session_state.input_value = ""
if "questions_ready" not in st.session_state:
    st.session_state.questions_ready = False
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "q_answers" not in st.session_state:
    st.session_state.q_answers = []
if "q_feedback" not in st.session_state:
    st.session_state.q_feedback = []
if "q_correct" not in st.session_state:
    st.session_state.q_correct = []

def start_app():
    st.session_state.started = True

def is_valid(field, value):
    if field == "name":
        return bool(re.match(r"^[A-Za-z\s]+$", value.strip()))
    elif field == "email":
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value.strip()))
    elif field == "phone":
        return bool(re.match(r"^\d{10,15}$", value.strip()))
    elif field == "experience":
        try:
            return float(value) >= 0
        except:
            return False
    elif field in ["position", "location", "tech_stack"]:
        return len(value.strip()) > 0
    return False

def categorize_experience(exp_str):
    try:
        years = float(exp_str)
    except ValueError:
        return "Intern / Fresher"

    if years < 1:
        return "Intern / Fresher"
    elif years < 3:
        return "Junior"
    elif years < 6:
        return "Mid-level"
    elif years < 10:
        return "Senior"
    else:
        return "Expert / Lead"

def handle_submission():
    idx = st.session_state.current_field_index
    field = fields[idx]
    val = st.session_state.input_value.strip()

    if is_valid(field, val):
        st.session_state.answers[field] = val
        st.session_state.current_field_index += 1
        st.session_state.input_value = ""
    else:
        st.error(f"Invalid input for {field}. Please try again.")

def handle_answer_submission():
    q_index = st.session_state.q_index
    selected_option = st.session_state.get(f"option_{q_index}")

    if selected_option is None:
        st.warning("Please select an answer before submitting.")
        return

    question = st.session_state.tech_questions[q_index]
    is_correct, feedback = evaluate_mcq_answer(question, selected_option)
    st.write(is_correct)
    st.session_state.q_answers.append(selected_option)
    st.session_state.q_correct.append(is_correct)
    st.session_state.q_feedback.append(feedback)
    st.session_state.q_index += 1
    st.rerun()
    
# --- Start Screen ---
if not st.session_state.started:
    st.markdown("""
        <div style='text-align: center; margin-top: 3em;'>
            <h2>👋 Welcome to <span style='color:#4CAF50'>TalentScout</span>!</h2>
            <p style='font-size: 18px;'>I'm your AI Hiring Assistant. Click below to begin.</p>
        </div>
    """, unsafe_allow_html=True)
    cols = st.columns(7)
    with cols[3]:
        st.button("Start", on_click=start_app)
    st.stop()

# --- Collect user info ---
st.markdown("<h3 style='text-align: center; margin-top: 2em;'>📝 Tell us about yourself</h3>", unsafe_allow_html=True)

idx = st.session_state.current_field_index

for i in range(idx):
    field = fields[i]
    st.markdown(f"<b>{questions_text[field]}</b>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: green;'>{st.session_state.answers[field]}</span>", unsafe_allow_html=True)

if idx < len(fields):
    field = fields[idx]
    st.markdown(f"<b>{questions_text[field]}</b>", unsafe_allow_html=True)
    st.text_input("Your Answer", key="input_value")
    cols = st.columns(7)
    with cols[6]:
        st.button("Submit", on_click=handle_submission)
    st.stop()

# --- Generate questions once user data is collected ---
if not st.session_state.questions_ready:
    tech_stack = st.session_state.answers["tech_stack"]
    experience = categorize_experience(st.session_state.answers["experience"])

    st.session_state.tech_questions = generate_mcq_questions(tech_stack, experience)
    if len(st.session_state.tech_questions) == 0:
        st.error("Failed to generate questions. Please restart the app.")
        st.stop()

    st.session_state.questions_ready = True
    st.rerun()
# --- Question & Answer Phase ---
# # --- Collect user info ---
# st.markdown("<h3 style='text-align: center;'>Tell us about yourself!</h3>", unsafe_allow_html=True)
# idx = st.session_state.current_field_index

# for i in range(idx):
#     field = fields[i]
#     st.markdown(f"**{questions_text[field]}**")
#     st.markdown(f"`{st.session_state.answers[field]}`")

# if idx < len(fields):
#     field = fields[idx]
#     st.markdown(f"**{questions_text[field]}**")
#     st.text_input("Your Answer", key="input_value")
#     cols = st.columns(7)
#     with cols[6]:
#         st.button("Submit", on_click=handle_submission)
#     st.stop()



# --- Question & Answer Phase ---
q_index = st.session_state.q_index
tech_questions = st.session_state.tech_questions

if q_index < len(tech_questions):
    question = tech_questions[q_index]

    st.markdown(f"### 🧠 Technical Question {q_index + 1}")
    st.markdown(f"**{question['question']}**")

    selected_option = st.radio(
        "Choose your answer:",
        question["options"],
        key=f"option_{q_index}"
    )

    if st.button("Submit Answer"):
        handle_answer_submission()

else:
# --- Completion / Score Summary ---
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>🎉 You’ve completed the technical round!</h3>", unsafe_allow_html=True)

    total_score = sum(10 for is_correct in st.session_state.q_correct if is_correct)
    percentage = total_score * 2

    st.markdown(f"### Your Total Score: {total_score} / {50} ({percentage:.2f}%)")

    if percentage >= 90:
        st.success("✅ Excellent! Our recruiting team will follow up with you shortly.")
    elif percentage >= 60:
        st.info("👍 Good effort! Keep growing — we'll keep your profile in view.")
    else:
        st.warning("Thanks for trying! Stay updated on our careers page for future roles.")
# # --- Start Screen ---
# if not st.session_state.started:
#     st.markdown("<h3 style='text-align: center;'>👋 Welcome to TalentScout!</h3>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center;'>I'm your AI Hiring Assistant. Click below to begin.</p>", unsafe_allow_html=True)
#     cols = st.columns(7)
#     with cols[3]:
#         st.button("Start", on_click=start_app)
#     st.stop()


    
    
#     total_score = 0
#     max_score_per_question = 10
#     num_questions = len(tech_questions)
#     st.write(num_questions)
#     for is_correct in st.session_state.q_correct:
#         #st.write(is_correct)
#         if is_correct:
#             total_score += 10
    
#     percentage = (total_score *2) 
    
#    
    
#     if percentage > 90:
#         st.success("✅ Thank you! Our recruting team will follow up with you shortly.")
#     else:
#         st.info("We appreciate your effort! Follow our carrers website for any upcoming jobs.")

    
