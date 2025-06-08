def intro_prompt():
    return (
        "👋 Hello! I'm your virtual assistant from **TalentScout**.\n\n"
        "I'm here to help you with the initial screening process. "
        "We'll go step-by-step to collect your basic info and then ask you some technical questions based on your tech stack.\n\n"
        "You can type **'exit'** at any time to stop. Ready to begin?"
    )

def mcq_generation_prompt(tech_stack_str, experience):
    return f"""
You are an expert technical interviewer.

Generate 5 multiple-choice questions based on the following list of technologies: {tech_stack_str}.
Generate only a JSON array; no extra text or feedback.
Difficulty should be based on {experience}.
Requirements:
- The 5 questions together must cover every technology in the list at least once.
- Each question must have 4 answer options.
- Exactly one option per question is the correct answer.
- Format your response as a JSON array of 5 objects with these keys:
  - "question": the question text
  - "options": an array of 4 answer options
  - "answer_index": the zero-based index of the correct option
  - "answer": the correct answer text (must match one of the options)

Example output:
[
  {{
    "question": "Sample question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer_index": 2,
    "answer": "Option C"
  }},
  ...
]
"""

def evaluation_prompt(question, answer):
    return (
        f"You are a senior technical interviewer.\n\n"
        f"Question: {question}\n"
        f"Candidate's Answer: {answer}\n\n"
        f"Evaluate the answer:\n"
        f"1. Score (0–10)\n"
        f"2. Short feedback on strengths or what’s missing.\n\n"
        f"Format:\n"
        f"Score: <number>\nFeedback: <1-2 lines>"
    )
