import streamlit as st
from llm.client import chat

def show_presentation_generator():

    if st.session_state.paper_context is None:
        st.warning("Upload a paper first.")
        return

    st.header("📊 Presentation Generator")

    slide_count = st.slider(
        "Number of Slides",
        5,
        15,
        8
    )

    if st.button("Generate Presentation Material"):

        with st.spinner("Generating..."):

            text = st.session_state.paper_context["full_text"][:12000]

            prompt = f"""
You are a research presentation expert.

Research Paper:
{text}

Generate:

1. Two minute summary

2. Five minute summary

3. Slide-by-Slide Presentation Structure

For each slide provide:

- Slide Number
- Slide Title
- Bullet Points
- Speaker Notes

Create exactly {slide_count} slides.

4. Key takeaways

5. Ten likely viva questions

Return in clean markdown with large headings.
"""

            response = chat(
                system_prompt="You are an expert research presentation coach.",
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )

            st.session_state.generated_summary = response

    if st.session_state.generated_summary:
        st.markdown(
            st.session_state.generated_summary
        )