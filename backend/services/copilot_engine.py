"""
VisionIQ AI Copilot Engine — Sprint 6
Pattern-matches maintenance questions and answers using real analytics data.
No external LLM required: all insights come from the built-in analytics engines.
"""

import re
from services.data_service import has_data
from services.sap_intelligence import (
    calculate_asset_health_scores,
    pm_compliance_by_plant,
    planner_group_performance,
    work_order_sla,
    repeat_failure_analysis,
    mttr_trend,
)
from services.pm_analytics import (
    calculate_mttr,
    calculate_mtbf,
    calculate_pm_compliance,
    calculate_backlog,
    calculate_top_failed_equipment,
    calculate_failure_frequency,
)
from services.kpi_engine import get_dashboard_kpis


# ---------------------------------------------------------------------------
# Intent patterns (order matters — first match wins)
# ---------------------------------------------------------------------------

_INTENTS = [
    ("risk",        r"risk|critical|danger|worst|most critical|at risk"),
    ("health",      r"health score|asset health|equipment health|healthiest|weakest"),
    ("top_failure", r"fail(ed|ure|ing)?s?|breakdown|broke down|most fail|chronic"),
    ("backlog",     r"backlog|overdue|pending|outstanding|open order"),
    ("sla",         r"sla|past due|over \d+ days?|deadline"),
    ("mttr",        r"mttr|mean time to repair|repair time|how long.*repair"),
    ("mtbf",        r"mtbf|mean time between|time between fail|reliability index"),
    ("compliance",  r"pm compliance|preventive maintenance|compliance|pm rate"),
    ("planner",     r"planner|planner group|planner performance|who.*most backlog"),
    ("kpi",         r"kpi|summary|overview|dashboard|how many|how is|status"),
    ("trend",       r"trend|getting better|improving|worse|over time|monthly"),
    ("recommend",   r"recommend|suggest|what should|what to do|action|next step"),
    ("help",        r"help|what can you|what do you|show me|list|available"),
]

_RISK_LABELS = {"Red": "🔴 Critical", "Amber": "🟡 Amber", "Green": "🟢 Healthy"}


def _intent(question: str) -> str:
    q = question.lower()
    for intent, pattern in _INTENTS:
        if re.search(pattern, q):
            return intent
    return "unknown"


# ---------------------------------------------------------------------------
# Answer builders
# ---------------------------------------------------------------------------

def _answer_risk() -> dict:
    health = calculate_asset_health_scores()
    if not health:
        return _no_data("equipment risk assessment")

    critical = [h for h in health if h["risk_level"] == "Red"]
    amber    = [h for h in health if h["risk_level"] == "Amber"]

    if not critical and not amber:
        return {
            "answer": "All equipment is currently in healthy (Green) status. No critical assets detected.",
            "related_assets": [h["equipment"] for h in health[:3]],
            "recommendations": ["Continue current PM schedule.", "Monitor health trends monthly."],
        }

    worst = health[0]
    lines = [f"**{worst['equipment']}** is at the highest risk with a health score of **{worst['health_score']}/100** ({_RISK_LABELS[worst['risk_level']]})."]

    if critical:
        lines.append(f"\n{len(critical)} asset(s) are in Critical status:")
        for h in critical[:5]:
            d = h["details"]
            lines.append(f"  • {h['equipment']}: score {h['health_score']}, {d.get('failure_count', 0)} failures, {d.get('open_orders', 0)} open orders")

    if amber:
        lines.append(f"\n{len(amber)} asset(s) are in Amber (warning) status.")

    recs = [
        f"Schedule immediate inspection for {worst['equipment']}.",
        "Review PM strategy for all Critical assets.",
        "Prioritize spare parts procurement for high-risk equipment.",
    ]

    return {
        "answer": "\n".join(lines),
        "related_assets": [h["equipment"] for h in health[:5]],
        "recommendations": recs,
    }


def _answer_health() -> dict:
    health = calculate_asset_health_scores()
    if not health:
        return _no_data("equipment health scores")

    lines = ["**Equipment Health Scores** (worst first):\n"]
    for h in health[:8]:
        bar = "█" * (h["health_score"] // 10) + "░" * (10 - h["health_score"] // 10)
        lines.append(f"  {_RISK_LABELS[h['risk_level']]} **{h['equipment']}** [{bar}] {h['health_score']}/100")

    fleet_avg = round(sum(h["health_score"] for h in health) / len(health))
    lines.append(f"\n**Fleet Average Health: {fleet_avg}/100**")

    return {
        "answer": "\n".join(lines),
        "related_assets": [h["equipment"] for h in health[:5]],
        "recommendations": [
            f"Improve health of {health[0]['equipment']} — currently the weakest asset.",
            "Target fleet average above 70 for good reliability.",
        ],
    }


def _answer_top_failures() -> dict:
    failures = calculate_top_failed_equipment(10)
    if not failures:
        return _no_data("failure frequency data")

    repeat = repeat_failure_analysis(min_failures=3)

    lines = ["**Top Failed Equipment:**\n"]
    for i, f in enumerate(failures[:7], 1):
        lines.append(f"  {i}. **{f['equipment']}** — {f['failures']} failures")

    if repeat:
        lines.append(f"\n**Chronic failures** (≥3 occurrences): {', '.join(r['equipment'] for r in repeat[:3])}")

    return {
        "answer": "\n".join(lines),
        "related_assets": [f["equipment"] for f in failures[:5]],
        "recommendations": [
            f"Investigate root cause of failures on {failures[0]['equipment']}.",
            "Consider redesign or enhanced PM for top 3 assets.",
            "Review spare parts availability for high-failure equipment.",
        ],
    }


def _answer_backlog() -> dict:
    backlog = calculate_backlog()
    if backlog.get("source") == "demo":
        return _demo_response("backlog")

    total = backlog.get("total_backlog", 0)
    by_plant = backlog.get("by_plant", [])

    if total == 0:
        return {
            "answer": "No open work order backlog detected. All orders are in a completed or closed status.",
            "related_assets": [],
            "recommendations": ["Maintain current closure rate.", "Monitor for new notifications."],
        }

    lines = [f"There are **{total} open work orders** in the backlog.\n"]

    if by_plant:
        lines.append("**Backlog by Plant:**")
        for p in by_plant[:5]:
            lines.append(f"  • Plant {p['plant']}: {p['count']} orders")

    planner = planner_group_performance()
    if planner:
        worst_planner = planner[0]
        lines.append(f"\n**Planner {worst_planner['planner_group']}** has the highest backlog ({worst_planner['backlog']} orders, {worst_planner['compliance_pct']}% compliance).")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            f"Prioritize {by_plant[0]['plant']} — highest backlog plant." if by_plant else "Review all open orders.",
            "Set daily closure targets per planner group.",
            "Escalate orders older than 30 days.",
        ],
    }


def _answer_sla() -> dict:
    sla = work_order_sla(30)
    if sla.get("source") == "demo":
        return _demo_response("SLA compliance")

    overdue = sla.get("overdue_count", 0)
    on_time = sla.get("on_time_count", 0)
    total   = overdue + on_time
    pct     = round((overdue / total) * 100) if total else 0

    if overdue == 0:
        return {
            "answer": "All open work orders are within the 30-day SLA. No overdue orders detected.",
            "related_assets": [],
            "recommendations": ["Maintain current response times.", "Consider tightening SLA to 21 days."],
        }

    lines = [
        f"**{overdue} work orders are past the 30-day SLA** ({pct}% of open orders).",
        f"{on_time} orders are on time.",
    ]
    by_priority = sla.get("overdue_by_priority", [])
    if by_priority:
        lines.append("\nOverdue by priority:")
        for p in by_priority:
            lines.append(f"  • {p['priority']}: {p['count']} orders")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            "Immediately address overdue Critical and High priority orders.",
            "Set automated SLA alerts at 21 days.",
            f"Review workload for planner groups with overdue orders.",
        ],
    }


def _answer_mttr() -> dict:
    mttr = calculate_mttr()
    trend = mttr_trend()

    if mttr.get("source") == "demo":
        return _demo_response("MTTR")

    days = mttr.get("mttr_days")
    lines = [f"**Mean Time To Repair (MTTR): {days} days** (based on {mttr.get('sample_size', 0)} work orders)."]

    if trend and len(trend) >= 2:
        first = trend[0]["mttr_days"]
        last  = trend[-1]["mttr_days"]
        direction = "improving ↓" if last < first else "worsening ↑"
        lines.append(f"\nMTTR is **{direction}** — from {first}d ({trend[0]['period']}) to {last}d ({trend[-1]['period']}).")

    benchmark = 3.0
    if days and days > benchmark:
        lines.append(f"\nMTTR is above the **{benchmark}-day benchmark**. Investigate repair process bottlenecks.")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            "Pre-stage spare parts to reduce repair time.",
            "Review technician skill gaps for high-MTTR equipment types.",
            "Target MTTR below 3 days for critical assets.",
        ],
    }


def _answer_mtbf() -> dict:
    mtbf = calculate_mtbf()

    if mtbf.get("source") == "demo":
        return _demo_response("MTBF")

    days = mtbf.get("mtbf_days")
    lines = [f"**Mean Time Between Failures (MTBF): {days} days** (based on {mtbf.get('sample_size', 0)} failure intervals)."]

    if days:
        if days < 14:
            lines.append("\n⚠️ MTBF is very low — equipment is failing very frequently. Immediate reliability improvement is needed.")
        elif days < 30:
            lines.append("\nMTBF is below 30 days — reliability needs improvement.")
        else:
            lines.append(f"\nMTBF of {days} days indicates reasonable reliability. Target is above 60 days.")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            "Increase PM frequency for equipment with MTBF < 30 days.",
            "Analyze failure root causes to extend intervals.",
            "Review lubrication and inspection schedules.",
        ],
    }


def _answer_compliance() -> dict:
    compliance = calculate_pm_compliance()
    by_plant   = pm_compliance_by_plant()

    if compliance.get("source") == "demo":
        return _demo_response("PM compliance")

    pct  = compliance.get("compliance_pct", 0)
    lines = [f"**Overall PM Compliance: {pct}%** ({compliance.get('completed', 0)} completed of {compliance.get('total', 0)} total orders)."]

    if by_plant:
        worst = by_plant[0]
        best  = by_plant[-1]
        lines.append(f"\n**Worst plant:** Plant {worst['plant']} at {worst['compliance_pct']}%")
        lines.append(f"**Best plant:** Plant {best['plant']} at {best['compliance_pct']}%")

    recs = []
    if pct < 70:
        recs.append("PM compliance is critically low — escalate to plant management.")
    elif pct < 85:
        recs.append("PM compliance needs improvement — target 90%.")
    else:
        recs.append("PM compliance is good — maintain current schedule.")

    if by_plant and by_plant[0]["compliance_pct"] < 70:
        recs.append(f"Focus on Plant {by_plant[0]['plant']} — immediate intervention needed.")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": recs,
    }


def _answer_planner() -> dict:
    planners = planner_group_performance()

    if not planners:
        return _no_data("planner group data")

    lines = ["**Planner Group Performance:**\n"]
    for p in planners:
        lines.append(f"  • **{p['planner_group']}**: {p['compliance_pct']}% compliance, {p['backlog']} backlog, {p['total']} total orders")

    worst = planners[0]
    best  = planners[-1]
    lines.append(f"\n**Needs attention:** {worst['planner_group']} ({worst['compliance_pct']}% compliance)")
    lines.append(f"**Best performer:** {best['planner_group']} ({best['compliance_pct']}% compliance)")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            f"Review workload distribution for {worst['planner_group']}.",
            "Set weekly backlog targets per planner group.",
            f"Share {best['planner_group']} best practices across the team.",
        ],
    }


def _answer_kpi() -> dict:
    kpis = get_dashboard_kpis()
    lines = [
        "**VisionIQ Dashboard Summary:**\n",
        f"  📋 Work Orders: **{kpis.get('work_orders', '—')}**",
        f"  🔔 Notifications: **{kpis.get('notifications', '—')}**",
        f"  🏭 Plants: **{kpis.get('plants', '—')}**",
        f"  ⚙️ Equipment: **{kpis.get('equipment', '—')}**",
        f"  💚 Asset Health: **{kpis.get('asset_health', '—')}%**",
    ]

    if has_data():
        health = calculate_asset_health_scores()
        red    = sum(1 for h in health if h["risk_level"] == "Red")
        if red:
            lines.append(f"\n⚠️ **{red} Critical asset(s)** require immediate attention.")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            "Review the Reliability Dashboard for detailed KPI analysis.",
            "Upload updated SAP PM data to refresh all metrics.",
        ],
    }


def _answer_trend() -> dict:
    trend = mttr_trend()
    if not trend:
        return _no_data("MTTR trend data")

    lines = ["**MTTR Trend (Mean Time To Repair by period):**\n"]
    for t in trend:
        lines.append(f"  • {t['period']}: {t['mttr_days']} days")

    if len(trend) >= 2:
        direction = "⬇️ improving" if trend[-1]["mttr_days"] < trend[0]["mttr_days"] else "⬆️ worsening"
        lines.append(f"\nOverall trend: **{direction}**")

    return {
        "answer": "\n".join(lines),
        "related_assets": [],
        "recommendations": [
            "Plot MTTR against PM compliance to identify correlation.",
            "Target month-over-month MTTR reduction of 5%.",
        ],
    }


def _answer_recommend() -> dict:
    health   = calculate_asset_health_scores()
    backlog  = calculate_backlog()
    failures = calculate_top_failed_equipment(5)
    compliance = calculate_pm_compliance()

    recs = []

    if health:
        critical = [h for h in health if h["risk_level"] == "Red"]
        if critical:
            recs.append(f"🔴 **Immediate:** Inspect {critical[0]['equipment']} — highest risk asset (score: {critical[0]['health_score']}).")

    if failures:
        recs.append(f"🔧 **Short-term:** Investigate root cause of repeated failures on {failures[0]['equipment']} ({failures[0]['failures']} failures).")

    bl = backlog.get("total_backlog", 0)
    if bl > 10:
        recs.append(f"📋 **This week:** Reduce work order backlog of {bl} open orders.")

    pct = compliance.get("compliance_pct", 100)
    if pct < 80:
        recs.append(f"📅 **Schedule:** PM compliance is at {pct}% — target 90% by month end.")

    recs.append("📊 **Monthly:** Review Reliability Analytics dashboard with your maintenance team.")

    answer = "**VisionIQ Maintenance Recommendations:**\n\n" + "\n\n".join(recs) if recs else "All maintenance metrics are within acceptable ranges. Continue current PM strategy."

    return {
        "answer": answer,
        "related_assets": [h["equipment"] for h in health[:3]] if health else [],
        "recommendations": recs[:3] if recs else [],
    }


def _answer_help() -> dict:
    return {
        "answer": (
            "**VisionIQ AI Copilot** — I can answer questions using your SAP PM data:\n\n"
            "  🔴 **Risk & Health**\n"
            "  • Which equipment is at highest risk?\n"
            "  • Show asset health scores\n\n"
            "  🔧 **Failures & Reliability**\n"
            "  • Which equipment failed the most?\n"
            "  • What is the MTTR / MTBF?\n"
            "  • Show repeat failures\n\n"
            "  📋 **Backlog & Compliance**\n"
            "  • Show overdue work orders\n"
            "  • What is PM compliance?\n"
            "  • Which planner has the most backlog?\n\n"
            "  📊 **Overview & Actions**\n"
            "  • Give me a dashboard summary\n"
            "  • What should I do this week?\n"
            "  • Show me the MTTR trend\n"
        ),
        "related_assets": [],
        "recommendations": ["Try asking: 'Which equipment is at highest risk?'"],
    }


def _no_data(topic: str) -> dict:
    return {
        "answer": f"No {topic} data is available yet. Please upload a SAP PM Excel file (IW38, IW39, or similar) to enable this analysis.",
        "related_assets": [],
        "recommendations": ["Go to Dashboard and upload a SAP PM Excel file.", "Supported formats: IW38, IW39, IW28, IP24."],
    }


def _demo_response(topic: str) -> dict:
    return {
        "answer": f"Showing **demo {topic} data** (no file uploaded yet). Upload a real SAP PM Excel to see live analysis.",
        "related_assets": [],
        "recommendations": ["Upload a SAP PM Excel file to get real answers."],
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def ask(question: str) -> dict:
    if not question or not question.strip():
        return {"answer": "Please ask a question about your SAP PM data.", "related_assets": [], "recommendations": []}

    intent = _intent(question.strip())

    handlers = {
        "risk":        _answer_risk,
        "health":      _answer_health,
        "top_failure": _answer_top_failures,
        "backlog":     _answer_backlog,
        "sla":         _answer_sla,
        "mttr":        _answer_mttr,
        "mtbf":        _answer_mtbf,
        "compliance":  _answer_compliance,
        "planner":     _answer_planner,
        "kpi":         _answer_kpi,
        "trend":       _answer_trend,
        "recommend":   _answer_recommend,
        "help":        _answer_help,
    }

    handler = handlers.get(intent)
    if handler:
        result = handler()
    else:
        result = {
            "answer": f"I understood your question but don't have a specific handler for it yet. Try asking about: risk, failures, backlog, MTTR, MTBF, PM compliance, or recommendations.",
            "related_assets": [],
            "recommendations": ["Type 'help' to see all supported questions."],
        }

    result["intent"] = intent
    result["question"] = question
    return result
