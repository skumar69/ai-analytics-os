import streamlit as st

from backend.config.branding import (
    COMPANY_NAME,
    PRODUCT_NAME,
    TAGLINE,
    WEBSITE,
    COPYRIGHT,
    FOUNDER,
    VERSION_LABEL,
    PRODUCT_TYPE,
)

try:
    from frontend.about import render_about
    from frontend.footer import render_footer
except ModuleNotFoundError:  # pragma: no cover - supports direct script execution
    from about import render_about
    from footer import render_footer


st.set_page_config(page_title=PRODUCT_NAME, page_icon="📊", layout="wide")


def render_section_title(title: str, subtitle: str | None = None) -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def render_home() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top left, rgba(118, 92, 255, 0.18), transparent 30%),
                        radial-gradient(circle at top right, rgba(38, 180, 255, 0.18), transparent 30%),
                        linear-gradient(180deg, #081120 0%, #0d1526 52%, #0a1320 100%);
        }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        .hero-shell {
            padding: 2rem 1rem 2rem 1rem;
            border-radius: 28px;
            background: rgba(14, 21, 34, 0.7);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 20px 60px rgba(11,13,27,0.45);
            backdrop-filter: blur(14px);
        }
        .eyebrow {
            display: inline-block;
            background: rgba(117, 101, 255, 0.18);
            color: #d8d6ff;
            border: 1px solid rgba(170,154,255,0.25);
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            font-size: 0.72rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-weight: 700;
        }
        .hero-title {
            font-size: clamp(2.6rem, 5vw, 5rem);
            line-height: 0.98;
            font-weight: 800;
            color: white;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            color: rgba(224,232,255,0.8);
            font-size: 1.12rem;
            line-height: 1.7;
            max-width: 760px;
            margin-bottom: 1.6rem;
        }
        .hero-actions { margin-top: 1.5rem; }
        .primary-btn, .secondary-btn {
            display: inline-block;
            padding: 0.9rem 1.5rem;
            border-radius: 14px;
            text-decoration: none;
            font-weight: 700;
            margin-right: 0.7rem;
            margin-bottom: 0.7rem;
        }
        .primary-btn {
            background: linear-gradient(90deg, #4e7cff, #7d6bff);
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 16px 36px rgba(94,103,255,0.35);
        }
        .secondary-btn {
            color: #edf3ff;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.12);
        }
        .signal-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 1.15rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }
        .signal-label {
            color: rgba(208,220,255,0.72);
            font-size: 0.7rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .signal-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: white;
            margin-top: 0.35rem;
        }
        .network-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
        }
        .glass-card {
            border-radius: 18px;
            padding: 1rem;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            min-height: 140px;
        }
        .glass-card h4 {
            margin: 0 0 0.6rem 0;
            color: #eff4ff;
        }
        .glass-card p {
            margin: 0;
            color: rgba(224,232,255,0.76);
            line-height: 1.6;
        }
        .section-title {
            font-size: 2.2rem;
            color: white;
            font-weight: 800;
            margin-top: 2.4rem;
            margin-bottom: 0.35rem;
        }
        .section-subtitle {
            color: rgba(218,228,255,0.74);
            font-size: 1.02rem;
            margin-bottom: 1.2rem;
        }
        .logo-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.9rem;
            margin-top: 1rem;
        }
        .logo-pill {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            color: rgba(233,240,255,0.75);
            border-radius: 999px;
            padding: 0.75rem 1rem;
            font-weight: 600;
        }
        .feature-box {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.2rem;
            height: 100%;
        }
        .feature-box h4 { color: white; margin-bottom: 0.5rem; }
        .feature-box p { color: rgba(224,232,255,0.75); line-height: 1.7; }
        .price-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1.5rem;
            height: 100%;
        }
        .price-card .price {
            font-size: 2.4rem;
            font-weight: 800;
            color: white;
        }
        .price-card .price small {
            font-size: 0.9rem;
            color: rgba(224,232,255,0.7);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='hero-shell'>
            <div class='eyebrow'>VisionIQ OS</div>
            <div class='hero-title'>The AI Analytics Operating System</div>
            <div class='hero-subtitle'>Upload your business data once. VisionIQ OS automatically understands it, enriches it, builds semantic models, generates dashboards, explains insights, and recommends actions—all powered by AI.</div>
            <div class='hero-actions'>
                <a class='primary-btn' href='#start'>🚀 Start Free</a>
                <a class='secondary-btn' href='#demo'>▶ Watch Demo</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class='signal-card'>
              <div class='signal-label'>Records processed</div>
              <div class='signal-value'>1.2M+</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class='signal-card'>
              <div class='signal-label'>AI insight coverage</div>
              <div class='signal-value'>96%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class='signal-card'>
              <div class='signal-label'>Time to insight</div>
              <div class='signal-value'>3 min</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_title("Trusted Integrations", "Connect the systems your business already runs on.")
    st.markdown(
        """
        <div class='logo-row'>
          <div class='logo-pill'>Excel</div>
          <div class='logo-pill'>SAP</div>
          <div class='logo-pill'>SQL</div>
          <div class='logo-pill'>Salesforce</div>
          <div class='logo-pill'>Oracle</div>
          <div class='logo-pill'>Power BI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_section_title("AI Semantic Engine", "Automatically map structure, meaning, and business context.")
    col1, col2, col3 = st.columns(3)
    cards = [
        ("Schema Intelligence", "AI detects columns, relationships, and field intent across spreadsheets, systems, and exports."),
        ("Semantic Mapping", "Business terminology is normalized into a canonical model for KPI logic and reporting."),
        ("Actionable Guidance", "Insights are translated into recommendations, alerts, and next-best actions."),
    ]
    for item, container in zip(cards, (col1, col2, col3)):
        with container:
            title, text = item
            st.markdown(
                f"""
                <div class='glass-card'>
                    <h4>{title}</h4>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_title("Feature Highlights", "Designed to convert data into business decisions.")
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("Semantic Data Layer", "Transforms raw files into consistent, business-ready models."),
        ("AI Dashboarding", "Generates dynamic insights and KPI visualizations automatically."),
        ("Workflow Orchestration", "Executes enriched logic across schema, enrichment, and reporting stages."),
        ("Decision Copilot", "Recommends improvements, priorities, and next actions with context."),
    ]
    for item, container in zip(features, (col1, col2, col3, col4)):
        with container:
            title, text = item
            st.markdown(
                f"""
                <div class='feature-box'>
                    <h4>{title}</h4>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_title("Live Dashboard Preview", "Operational insight, in motion.")
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(
            """
            <div class='glass-card'>
                <h4>Executive Dashboard</h4>
                <p>Revenue trend · SLA performance · operational risk · issue aging · root cause summary</p>
            </div>
            <div class='glass-card' style='margin-top:1rem;'>
                <h4>AI Signal Feed</h4>
                <p>+18% faster resolution · 4 incidents require priority escalation · 3 cost anomalies detected</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class='glass-card'>
                <h4>Live KPI Cards</h4>
                <div class='network-grid'>
                    <div class='signal-card'><div class='signal-label'>MTTR</div><div class='signal-value'>4.7h</div></div>
                    <div class='signal-card'><div class='signal-label'>SLA</div><div class='signal-value'>94%</div></div>
                    <div class='signal-card'><div class='signal-label'>Cost</div><div class='signal-value'>$148k</div></div>
                    <div class='signal-card'><div class='signal-label'>Risk</div><div class='signal-value'>Low</div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_title("AI Agent Gallery", "Specialized agents working as one system.")
    col1, col2, col3 = st.columns(3)
    agents = [
        ("Schema Agent", "Detects table structure and data intent automatically."),
        ("Semantic Agent", "Maps raw data to a canonical business model."),
        ("Insight Agent", "Explains outliers, wins, losses, and anomalies."),
    ]
    for item, container in zip(agents, (col1, col2, col3)):
        with container:
            title, text = item
            st.markdown(
                f"""
                <div class='feature-box'>
                    <h4>{title}</h4>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_title("Customer Journey", "From raw data to AI-driven action.")
    col1, col2, col3, col4 = st.columns(4)
    stages = [
        ("1. Upload", "Bring in raw Excel, CSV, or system exports."),
        ("2. Understand", "AI analyzes structure, meaning, and business context."),
        ("3. Act", "Dashboards, insights, and recommendations are generated."),
        ("4. Improve", "Teams monitor outcomes and drive better decisions."),
    ]
    for item, container in zip(stages, (col1, col2, col3, col4)):
        with container:
            title, text = item
            st.markdown(
                f"""
                <div class='feature-box'>
                    <h4>{title}</h4>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_title("Pricing Preview", "Built for teams, ops leaders, and enterprise scale.")
    col1, col2, col3 = st.columns(3)
    plans = [
        ("Starter", "$49", "For small teams exploring AI analytics"),
        ("Growth", "$199", "For operational teams and business units"),
        ("Enterprise", "Custom", "For multi-team orchestration and advanced governance"),
    ]
    for item, container in zip(plans, (col1, col2, col3)):
        with container:
            title, price, text = item
            st.markdown(
                f"""
                <div class='price-card'>
                    <h4>{title}</h4>
                    <div class='price'>{price}<small>/mo</small></div>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin-top: 2rem;' />", unsafe_allow_html=True)


pages = ["Home", "About"]
selected_page = st.sidebar.radio("Navigation", pages, index=0)

if selected_page == "Home":
    render_home()
elif selected_page == "About":
    render_about()

render_footer()
