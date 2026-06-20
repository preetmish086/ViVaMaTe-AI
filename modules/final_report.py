import streamlit as st
import plotly.graph_objects as go
import re
import json
import os

def show_final_report():

    if st.button("🔄 Refresh Report"):
        st.rerun()

    st.header("📈 Final Performance Report")


    viva_history = st.session_state.get(
            "viva_history",
            []
        )


    presentation_metrics = {}

    if os.path.exists("results.json"):

        with open("results.json","r") as f:

            presentation_metrics = json.load(f)           

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

    presentation_score = presentation_metrics.get(
        "confidence_score",
        0
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

    communication_score = presentation_metrics.get(
        "engagement_score",
        75
    )

    # ----------------------------
    # Overall
    # ----------------------------

    if len(viva_history) == 0:

        overall_score = (
            research_score * 0.5
            + presentation_score * 0.3
            + communication_score * 0.2
        )

    else:

        overall_score = (
            research_score * 0.35
            + viva_score * 0.25
            + presentation_score * 0.25
            + communication_score * 0.15
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

        if len(viva_history) == 0:

            st.metric(
                "Viva Score",
                "Not Attempted"
            )

        else:

            st.metric(
                "Viva Score",
                f"{round(viva_score,1)}/100"
            )

    with col3:
        st.metric(
            "Overall Score",
            f"{round(overall_score,1)}/100"
        )

    with col4:
        st.metric(
            "Presentation Score",
            f"{presentation_score}/100"
        )

    st.markdown("---")

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
        height=400,
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
    # Feedback
    # ----------------------------


    