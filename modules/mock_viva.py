import streamlit as st
from llm.client import chat

PERSONAS = [
    "Professor",
    "Industry Expert",
    "Interviewer",
    "Skeptic",
    "Student"
]

def show_mock_viva():

    if st.session_state.paper_context is None:
        st.warning("Upload a paper first.")
        return
    
    if "viva_history" not in st.session_state:
        st.session_state.viva_history = []

    if "viva_evaluation" not in st.session_state:
        st.session_state.viva_evaluation = None

    st.header("🎓 Mock Viva")

    persona = st.selectbox(
        "Choose Examiner Persona",
        PERSONAS
    )

    if "viva_question" not in st.session_state:
        st.session_state.viva_question = None

    if st.button("Generate Viva Question"):

        paper_text = st.session_state.paper_context["full_text"][:10000]

        prompt = f"""
You are acting as a {persona}.

Based on the following research paper, ask ONE realistic viva question.

Paper:
{paper_text}

Return only the question.
"""

        question = chat(
            system_prompt="You are an experienced viva examiner.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        st.session_state.viva_question = question

    if st.session_state.viva_question:

        st.markdown("### 🎤 Viva Question")

        st.success(
            st.session_state.viva_question
        )

        st.caption(
            "Future AI voice playback will read this question aloud."
        )

        if "answer_transcript" not in st.session_state:
            st.session_state.answer_transcript = ""

        answer = st.text_area(
            "📝 Answer Transcript",
            value=st.session_state.answer_transcript,
            height=150
        )

        if st.button("Evaluate Answer"):

            evaluation_prompt = f"""
Question:
{st.session_state.viva_question}

Student Answer:
{answer}

Evaluate the answer.

Provide:

1. Score out of 10
2. Strengths
3. Weaknesses
4. Suggested Better Answer

Use markdown.
"""

            evaluation = chat(
                system_prompt="You are a strict academic evaluator.",
                messages=[
                    {
                        "role": "user",
                        "content": evaluation_prompt
                    }
                ]
            )
            if "viva_history" not in st.session_state:
                st.session_state.viva_history = []

            st.session_state.viva_history.append({
                "persona": persona,
                "question": st.session_state.viva_question,
                "answer": answer,
                "evaluation": evaluation
            })
            st.markdown(evaluation)
            with st.expander("📜 Previous Viva Attempts"):

                if "viva_history" in st.session_state:

                    for viva in reversed(st.session_state.viva_history):

                        st.markdown(viva["evaluation"])
                        st.divider()