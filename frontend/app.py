import streamlit as st

try:
    from frontend.about import render_about
    from frontend.footer import render_footer
except ModuleNotFoundError:  # pragma: no cover - supports direct script execution
    from about import render_about
    from footer import render_footer


def render_home() -> None:
    st.title("VisionIQ")
    st.caption("AI-powered business analytics for operations, service delivery, and performance intelligence")

    st.markdown(
        """
        <div style='background: linear-gradient(90deg, #0b5fff 0%, #6c63ff 100%); padding: 1.5rem; border-radius: 0.85rem; color: white;'>
            <h3 style='margin:0;'>Turn fragmented data into decisions that move the business</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Files processed", "120+", "This month")
    with col2:
        st.metric("Insights generated", "98%", "Actionable")
    with col3:
        st.metric("Business coverage", "12", "Capability packs")

    st.subheader("Operational overview")
    st.write(
        "VisionIQ brings structured semantic mapping, KPI measurement, and AI-guided insight generation together in a single analytics workflow."
    )

    st.markdown(
        """
    ### Platform capabilities
    - Excel and CSV data ingestion
    - Semantic canonical field mapping
    - Workflow execution planning and enrichment
    - KPI dashboards and operational insight summaries
    """
    )

    uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        st.success(f"File ready for analysis: {uploaded_file.name}")

    st.subheader("Recommended workflow")
    steps = [
        "Schema detection and file inspection",
        "Semantic normalization to canonical field names",
        "Execution plan and enrichment logic",
        "KPI, dashboard, and insight generation",
    ]
    for step in steps:
        st.markdown(f"- {step}")

    st.subheader("Core capability packs")
    pack_cols = st.columns(4)
    packs = [
        ("Incident", "Service and operational incident management"),
        ("Finance", "Budget, cost, and business performance analysis"),
        ("Attendance", "Workforce attendance and productivity patterns"),
        ("SAP PM", "Plant and maintenance performance monitoring"),
    ]
    for i, (title, description) in enumerate(packs):
        with pack_cols[i]:
            st.markdown(f"#### {title}\n{description}")


st.set_page_config(page_title="VisionIQ", page_icon="📊", layout="wide")

pages = ["Home", "About"]
selected_page = st.sidebar.radio("Navigation", pages, index=0)

if selected_page == "Home":
    render_home()
elif selected_page == "About":
    render_about()

render_footer()
