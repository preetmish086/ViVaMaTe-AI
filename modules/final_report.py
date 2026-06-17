import streamlit as st
import plotly.graph_objects as go
import re


def show_final_report():

    st.header("📈 Final Performance Report")


    viva_history = st.session_state.get(
            "viva_history",
            []
        )


    presentation_metrics = st.session_state.get(
        "presentation_metrics",
        {}
    )   

    viva_score = 0
    if viva_history:

        scores = []

        for item in viva_history:

            evaluation = item["evaluation"]

            match = re.search(
                r'(\d+)\s*/\s*10',
                evaluation
            )

            if match:
                scores.append(
                    int(match.group(1))
                )

        if scores:
            viva_score = (
                sum(scores)
                / len(scores)
            ) * 10

        

    # ----------------------------
    # Presentation Score
    # ----------------------------

    duration = presentation_metrics.get(
        "duration",
        0
    )

    presentation_score = min(
        100,
        duration
    )

    # ----------------------------
    # Research Understanding
    # ----------------------------

    research_score = 90 if st.session_state.get(
        "paper_context"
    ) else 80

    # ----------------------------
    # Communication
    # ----------------------------

    communication_score = 75

    # ----------------------------
    # Overall
    # ----------------------------

    overall_score = round(
        (
            research_score * 0.4
            + viva_score * 0.3
            + presentation_score * 0.2
            + communication_score * 0.1
        ),
        2
    )

    # ----------------------------
    # Overall Assessment
    # ----------------------------

    if overall_score >= 85:
        st.success(
            "🏆 Excellent Presentation Readiness"
        )

    elif overall_score >= 70:
        st.info(
            "✅ Good Presentation Readiness"
        )

    elif overall_score >= 50:
        st.warning(
            "⚠ Moderate Preparation"
        )

    else:
        st.error(
            "❌ More Practice Recommended"
        )

    # ----------------------------
    # Metrics
    # ----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Research Understanding",
            f"{research_score}/100"
        )

    with col2:
        st.metric(
            "Viva Score",
            f"{viva_score}/100"
        )

    with col3:
        st.metric(
            "Overall Score",
            f"{overall_score}/100"
        )

    with col4:
        st.metric(
            "Presentation Score",
            f"{presentation_score}/100"
        )

    st.markdown("---")

    st.subheader("📊 Activity Summary")

    a1, a2 = st.columns(2)

    with a1:
        st.info(
            f"🎓 Viva Questions Answered: {len(viva_history)}"
        )

    with a2:
        st.info(
            f"🎤 Practice Duration: {round(duration,1)} sec"
        )

    st.subheader(
    "📋 Performance Breakdown"
    )

    st.progress(
        research_score / 100
    )
    st.caption(
        f"Research Understanding: {research_score}%"
    )

    st.progress(
        viva_score / 100
    )
    st.caption(
        f"Viva Performance: {round(viva_score,1)}%"
    )

    st.progress(
        presentation_score / 100
    )
    st.caption(
        f"Presentation Practice: {round(presentation_score,1)}%"
    )

    # ----------------------------
    # Radar Chart
    # ----------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=[
                research_score,
                viva_score,
                presentation_score,
                communication_score
            ],
            theta=[
                "Research",
                "Viva",
                "Presentation",
                "Communication"
            ],
            fill="toself"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------
    # Feedback
    # ----------------------------

    st.subheader("💪 Strengths")

    strengths = []

    if research_score > 80:
        strengths.append(
            "Strong understanding of the research paper and core concepts."
        )

    if viva_score > 50:
        strengths.append(
            "Demonstrated good performance during viva sessions."
        )

    if presentation_score > 50:
        strengths.append(
            "Maintained consistent presentation practice."
        )

    for s in strengths:
        st.success(s)

    st.subheader("📌 Improvements")

    improvements = []

    if viva_score < 70:
        improvements.append(
            "Attempt additional viva sessions to improve subject mastery."
        )

    if presentation_score < 70:
        improvements.append(
            "Increase presentation practice duration for stronger delivery."
        )

    if not improvements:
        improvements.append(
            "Excellent overall performance."
        )

    for i in improvements:
        st.warning(i)