import streamlit as st
from llm.client import chat

PAPER_TEXT_LIMIT = 12000


def _paper_text():
    return st.session_state.paper_context["full_text"][:PAPER_TEXT_LIMIT]


def _generate_material(prompt):
    return chat(
        system_prompt="You are an expert research presentation coach.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


def show_presentation_generator():

    if st.session_state.paper_context is None:
        st.warning("Upload a paper first.")
        return

    st.header("📊 Presentation Generator")


    st.markdown(
        """
        <style>
            .stTabs [data-baseweb="tab-list"] {
                display: flex;
                width: 100%;
            }

            .stTabs [data-baseweb="tab"] {
                flex: 1 1 0;
                justify-content: center;
                text-align: center;
            }

            .stTabs [data-baseweb="tab"] p {
                width: 100%;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    summaries_tab, outline_tab, questions_tab = st.tabs([
        "Generate Summaries",
        "Generate Slide Deck Outline",
        "Generate Takeaways & Viva Questions"
    ])

    with summaries_tab:
        generate_summaries = st.button(
            "Generate Summaries",
            use_container_width=True
        )

        if generate_summaries:

            with st.spinner("Generating summaries..."):

                text = _paper_text()

                prompt = f"""
You are a research presentation expert.

Research Paper:
{text}

Generate:

1. Two minute summary

2. Five minute summary

Return in clean markdown with heading structure.
"""

                st.session_state.generated_summary = _generate_material(prompt)

        if st.session_state.generated_summary:
            st.markdown(st.session_state.generated_summary)

    with outline_tab:
        slide_count = st.slider(
            "Number of Slides",
            5,
            10,
            8
        )
        generate_outline = st.button(
            "Generate Slide Deck Outline",
            use_container_width=True
        )

        if generate_outline:

            with st.spinner("Generating slide deck outline..."):

                text = _paper_text()

                prompt = f"""
You are a research presentation expert.

Research Paper:
{text}

Generate a Slide-by-Slide Presentation Structure.

IMPORTANT:

Generate EXACTLY {slide_count} slides.

Use this format:

Slide 1:
Title:
Bullet Points:
Speaker Notes:

Slide 2:
Title:
Bullet Points:
Speaker Notes:

Slide 3:
...

Continue sequentially until Slide {slide_count}.

The last slide MUST be Slide {slide_count}.

Do not stop before Slide {slide_count}.

Return in clean markdown with large headings.
"""

                st.session_state.generated_outline = _generate_material(prompt)

        if st.session_state.generated_outline:
            st.markdown(st.session_state.generated_outline)

    with questions_tab:
        generate_questions = st.button(
            "Generate Takeaways & Viva Questions",
            use_container_width=True
        )

        if generate_questions:

            with st.spinner("Generating takeaways and viva questions..."):

                text = _paper_text()

                prompt = f"""
You are a research presentation expert.

Research Paper:
{text}

Generate:

1. Key takeaways

2. Ten likely viva questions

Return in clean markdown with large headings.
"""

                st.session_state.generated_questions = _generate_material(prompt)

        if st.session_state.generated_questions:
            st.markdown(st.session_state.generated_questions)
