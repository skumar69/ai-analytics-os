import streamlit as st


def render_about() -> None:
    st.title("VisionIQ™")

    st.subheader("Designed and Architected by")
    st.write("**Sanjeev Kumar**")
    st.write("Founder & Chief Architect")

    st.markdown(
        """
    ### Vision
    AI That Understands Business

    ### Mission
    Transform Data into Decisions.

    ### Copyright
    © 2026 All Rights Reserved.
    """
    )

    st.info(
        "VisionIQ is designed to turn messy operational data into structured insight, repeatable KPIs, and AI-assisted decision support."
    )

    st.markdown(
        """
    ### What the platform does
    - Reads operational and Excel-based data sources
    - Normalizes schema and semantic names
    - Applies execution plans and enrichment logic
    - Produces KPI-driven dashboards and insight summaries
    """
    )
