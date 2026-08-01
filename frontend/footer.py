import streamlit as st

from backend.config.branding import COMPANY_NAME, PRODUCT_NAME, COPYRIGHT, FOUNDER, WEBSITE


def render_footer() -> None:
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #e6e6e6; color: #555;'>
            <div><strong>{PRODUCT_NAME}</strong></div>
            <div>Designed and Architected by</div>
            <div><strong>{FOUNDER}</strong></div>
            <div>Founder & Chief Architect</div>
            <div>{COPYRIGHT}</div>
            <div>{WEBSITE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
