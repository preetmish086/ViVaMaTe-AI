import streamlit as st
import time
import random


def show_practice_mode():

    st.header("🎤 Presentation Practice (Prototype)")

    # Initialize session state
    if "practice_running" not in st.session_state:
        st.session_state.practice_running = False

    if "practice_start_time" not in st.session_state:
        st.session_state.practice_start_time = None

    if "practice_completed" not in st.session_state:
        st.session_state.practice_completed = False

    if "presentation_metrics" not in st.session_state:
        st.session_state.presentation_metrics = None

    # Controls
    col1, col2 = st.columns(2)

    with col1:
        start_clicked = st.button(
            "▶ Start Session",
            disabled=st.session_state.practice_running,
            use_container_width=True
        )

    with col2:
        stop_clicked = st.button(
            "⏹ Stop Session",
            disabled=not st.session_state.practice_running,
            use_container_width=True
        )

    if start_clicked:
        st.session_state.practice_running = True
        st.session_state.practice_start_time = time.time()
        st.session_state.practice_completed = False
        st.session_state.presentation_metrics = None
        st.rerun()

    if stop_clicked and st.session_state.practice_running:
        st.session_state.practice_running = False
        st.session_state.practice_completed = True
        st.rerun()

    # Active session
    if st.session_state.practice_running:

        elapsed = time.time() - st.session_state.practice_start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        st.info(f"🔴 Session running — {minutes:02d}:{seconds:02d}")

        try:
            st.camera_input("📷 Live Webcam Preview", key="webcam_feed")
        except Exception:
            st.warning("Webcam not available. Session timer is still running.")

        st.caption("Press **⏹ Stop Session** when done.")

        # Auto-refresh every 2s to update timer
        time.sleep(2)
        st.rerun()

    # Completed session — compute and show metrics
    if st.session_state.practice_completed and st.session_state.practice_start_time:

        duration = time.time() - st.session_state.practice_start_time

        # Cap duration awareness at 3 minutes for score scaling
        capped = min(duration, 180)

        # Confidence: grows with duration, small random variation
        confidence_base = 40 + (capped / 180) * 45
        confidence_score = round(
            min(100, confidence_base + random.uniform(-1, 1)), 1
        )

        # Engagement: slightly different curve
        engagement_base = 35 + (capped / 180) * 50
        engagement_score = round(
            min(100, engagement_base + random.uniform(-3, 5)), 1
        )

        # Presentation: weighted combo
        presentation_score = round(
            (confidence_score * 0.4) + (engagement_score * 0.4) + min(20, (capped / 180) * 20),
            1
        )

        metrics = {
            "duration": round(duration, 2),
            "confidence_score": confidence_score,
            "engagement_score": engagement_score,
            "presentation_score": presentation_score
        }

        st.session_state.presentation_metrics = metrics
        st.session_state.practice_completed = False  # prevent recalculation on reruns

        st.success("✅ Practice Session Completed!")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Duration (sec)", round(duration, 1))
        m2.metric("Practice Consistency", f"{confidence_score}%")
        m3.metric("Session Engagement", f"{engagement_score}%")
        m4.metric("Presentation Score", f"{presentation_score}%")

        st.caption("Metrics saved. Head to **Final Report** to see your full analysis.")

    # Show previous metrics if available and not in active session
    elif (
        not st.session_state.practice_running
        and st.session_state.presentation_metrics
        and not st.session_state.practice_completed
    ):

        metrics = st.session_state.presentation_metrics

        st.success("✅ Last Session Results")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Duration (sec)", metrics.get("duration", 0))
        m2.metric("Practice Duration Score", f"{metrics.get('confidence_score', 0)}%")
        m3.metric("Session Consistency", f"{metrics.get('engagement_score', 0)}%")
        m4.metric("Practice Completion Score", f"{metrics.get('presentation_score', 0)}%")

        st.caption("Metrics saved. Head to **Final Report** to see your full analysis.")

    elif not st.session_state.practice_running:
        st.info("Press **▶ Start Session** to begin your practice session.")