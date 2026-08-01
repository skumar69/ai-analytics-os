import streamlit as st

from backend.config.branding import COMPANY_NAME, PRODUCT_NAME, TAGLINE, COPYRIGHT, FOUNDER, WEBSITE


def render_about() -> None:
    st.title(PRODUCT_NAME)

    st.subheader("Designed and Architected by")
    st.write(f"**{FOUNDER}**")
    st.write("Founder & Chief Architect")

    st.markdown(
        f"""
    ### Vision
    AI That Understands Business

    ### Mission
    Transform Data into Decisions.

    ### Tagline
    {TAGLINE}

    ### Copyright
    {COPYRIGHT}

    ### Website
    {WEBSITE}
    """
    )

    st.info(
        f"{PRODUCT_NAME} is designed to turn messy operational data into structured insight, repeatable KPIs, and AI-assisted decision support."
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
