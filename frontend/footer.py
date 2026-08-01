import streamlit as st


def render_footer() -> None:
    st.markdown(
        """
        <div style='text-align: center; margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #e6e6e6; color: #555;'>
            <div><strong>VisionIQ™</strong></div>
            <div>Designed and Architected by</div>
            <div><strong>Sanjeev Kumar</strong></div>
            <div>Founder & Chief Architect</div>
            <div>© 2026 All Rights Reserved.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
