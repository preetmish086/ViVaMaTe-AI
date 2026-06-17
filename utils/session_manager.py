import streamlit as st

def initialize_session():

    defaults = {
        "paper_context": None,

        "generated_summary": None,
        "generated_outline": None,
        "generated_questions": None,

        "presentation_metrics": {},

        "viva_results": {},

        "final_report": {}
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value