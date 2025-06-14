import streamlit as st
import re
from chatbot import generate_mcq_questions, evaluate_mcq_answer

# --- Page Config ---
st.set_page_config(page_title="TalentScout Hiring Assistant")
st.title("🤖 TalentScout - Hiring Assistant")

# --- Initialize Session State ---
# Setting default values for persistent state across reruns
for key, default in {
    "hide_footer": False,
    "started": False,
    "current_field_index": 0,
    "answers": {},
    "input_value": "",
    "questions_ready": False,
    "tech_questions": [],
    "q_index": 0,
    "q_answers": [],
    "q_feedback": [],
    "q_correct": [],
    "fallback_message": "",
    "exit_tip_shown": False  # Track if the exit instruction tip has been shown
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Exit Keywords ---
EXIT_KEYWORDS = {"exit", "quit", "bye", "close", "stop"}

# --- Functions ---

# Begin the application and hide footer
def start_app():
    st.session_state.started = True
    st.session_state.hide_footer = True
    st.session_state.fallback_message = ""

# Validate user inputs based on the field type
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

# Categorize candidates based on experience
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

# End the conversation if an exit word is detected
def handle_exit_check(input_text):
    if input_text.lower() in EXIT_KEYWORDS:
        st.info("👋 Thank you for visiting TalentScout! If you want to apply later, just come back anytime.")
        st.stop()

# Handle form field submission
def handle_submission():
    val = st.session_state.input_value.strip()
    handle_exit_check(val)
    idx = st.session_state.current_field_index
    field = fields[idx]
    if is_valid(field, val):
        st.session_state.answers[field] = val
        st.session_state.current_field_index += 1
        st.session_state.input_value = ""
        st.session_state.fallback_message = ""
    else:
        st.session_state.fallback_message = f"⚠️ Please enter a valid {field.replace('_', ' ')}."

# Handle answer submission during quiz phase
def handle_answer_submission():
    q_index = st.session_state.q_index
    selected_option = st.session_state.get(f"option_{q_index}")
    if selected_option is None:
        st.warning("Please select an answer before submitting.")
        return
    handle_exit_check(selected_option)
    question = st.session_state.tech_questions[q_index]
    is_correct, feedback = evaluate_mcq_answer(question, selected_option)
    st.session_state.q_answers.append(selected_option)
    st.session_state.q_correct.append(is_correct)
    st.session_state.q_feedback.append(feedback)
    st.session_state.q_index += 1
    st.session_state.fallback_message = ""

# Display sticky footer
def show_footer():
    st.markdown(
        """
        <style>
        .block-container { padding-bottom: 100px !important; }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0e1117;
            text-align: center;
            padding: 10px;
            font-size: 0.9em;
            color: #f9f9f9;
            border-top: 1px solid #e6e6e6;
            z-index: 100;
        }
        </style>
        <div class="footer">
            © 2025 TalentScout AI. All rights reserved | Built with ❤️ using Streamlit and Gemini AI | Sai Kowsik Tukuntla
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Field Setup ---
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

# --- Intro Page ---
if not st.session_state.started:
    st.markdown("""
        <div style='text-align: center; margin-top: 3em; animation: fadeIn 2s;'>
            <h2>👋 Welcome to <span style='color:#4CAF50'>TalentScout</span>!</h2>
            <p style='font-size: 18px;'>I'm your AI Hiring Assistant. Click below to begin your journey.</p>
        </div>
        <style>@keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }</style>
    """, unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[2]:
        st.button("Apply for a Job", on_click=start_app, use_container_width=True)
    if not st.session_state.hide_footer:
        show_footer()
    st.stop()

# --- Form Section ---
idx = st.session_state.current_field_index
st.markdown("<h3 style='text-align: center; margin-top: 2em;'>📝 Tell us about yourself</h3>", unsafe_allow_html=True)
progress_ratio = min((idx + 1) / len(fields), 1.0)
st.progress(progress_ratio, text=f"Step {min(idx+1, len(fields))} of {len(fields)}")

# Display previous answers for context
for i in range(idx):
    field = fields[i]
    st.markdown(f"<b>{questions_text[field]}</b>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: green;'>{st.session_state.answers[field]}</span>", unsafe_allow_html=True)

# Display current question
if idx < len(fields):
    field = fields[idx]
    st.markdown(f"<b>{questions_text[field]}</b>", unsafe_allow_html=True)

    # Show exit tip only once
    if not st.session_state.exit_tip_shown:
        st.info("💡 You can type 'exit', 'quit', or 'bye' anytime to end the application.")
        st.session_state.exit_tip_shown = True

    st.text_input("Your Answer", key="input_value")
    st.button("Submit", on_click=handle_submission)
    if st.session_state.fallback_message:
        st.warning(st.session_state.fallback_message)
    st.stop()

# --- Generate Technical Questions ---
if not st.session_state.questions_ready:
    tech_stack = st.session_state.answers["tech_stack"]
    experience = categorize_experience(st.session_state.answers["experience"])

    st.session_state.tech_questions = generate_mcq_questions(tech_stack, experience)
    if len(st.session_state.tech_questions) == 0:
        st.error("Failed to generate questions. Please restart the app.")
        st.stop()

    st.session_state.questions_ready = True
    st.rerun()

# --- Quiz Section ---
q_index = st.session_state.q_index
tech_questions = st.session_state.tech_questions

if q_index < len(tech_questions):
    question = tech_questions[q_index]
    st.markdown(f"### 🧠 Technical Question {q_index + 1}")
    st.progress((q_index + 1) / len(tech_questions), text=f"Question {q_index+1} of {len(tech_questions)}")
    st.markdown(f"**{question['question']}**")
    st.radio("Choose your answer:", question["options"], key=f"option_{q_index}")
    st.button("Submit Answer", on_click=handle_answer_submission)
    if st.session_state.fallback_message:
        st.warning(st.session_state.fallback_message)
else:
    # --- Final Score ---
    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>🎉 You’ve completed the technical round!</h3>", unsafe_allow_html=True)
    total_score = sum(10 for is_correct in st.session_state.q_correct if is_correct)
    percentage = total_score * 2

    st.markdown(f"### Your Total Score: {total_score} / 50 ({percentage:.2f}%)")

    if percentage >= 90:
        st.success("✅ Excellent! Our recruiting team will follow up with you shortly.")
        st.balloons()
    elif percentage >= 60:
        st.info("👍 Good effort! Keep growing — we'll keep your profile in view.")
    else:
        st.warning("Thanks for trying! Stay updated on our careers page for future roles.")

# --- Footer ---
if not st.session_state.hide_footer:
    show_footer()
