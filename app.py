import streamlit as st
from datetime import datetime
from lead_scoring import analyze_lead

st.set_page_config(
    page_title="AI Business Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Business Assistant")
st.caption(
    "Smart lead management, scoring and business workflow assistant"
)

# Initialize data
if "leads" not in st.session_state:
    st.session_state.leads = []

# Dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Leads", len(st.session_state.leads))

with col2:
    hot_leads = sum(
        1
        for lead in st.session_state.leads
        if lead["priority"] == "HOT"
    )
    st.metric("Hot Leads", hot_leads)

with col3:
    if st.session_state.leads:
        average_score = sum(
            lead["score"] for lead in st.session_state.leads
        ) / len(st.session_state.leads)

        st.metric("Average Score", f"{average_score:.0f}/100")
    else:
        st.metric("Average Score", "0/100")

with col4:
    st.metric("System Status", "Ready")

st.divider()

st.subheader("➕ Add & Analyze Lead")

with st.form("lead_form"):
    name = st.text_input("Customer name")
    email = st.text_input("Email")
    company = st.text_input("Company")

    budget = st.number_input(
        "Estimated budget (€)",
        min_value=0,
        step=500,
    )

    urgency = st.selectbox(
        "Purchase urgency",
        [
            "Immediate",
            "This week",
            "This month",
            "Just exploring",
        ],
    )

    interest_level = st.selectbox(
        "Interest level",
        ["High", "Medium", "Low"],
    )

    notes = st.text_area("Notes")

    submitted = st.form_submit_button(
        "Analyze & Add Lead"
    )

    if submitted:
        if name and email:
            analysis = analyze_lead(
                budget,
                urgency,
                interest_level,
            )

            new_lead = {
                "name": name,
                "email": email,
                "company": company,
                "budget": budget,
                "urgency": urgency,
                "interest_level": interest_level,
                "notes": notes,
                "score": analysis["score"],
                "priority": analysis["priority"],
                "recommended_action": analysis[
                    "recommended_action"
                ],
                "created": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
            }

            st.session_state.leads.append(new_lead)

            st.success(
                f"{name} analyzed successfully — "
                f"Score: {analysis['score']}/100 | "
                f"Priority: {analysis['priority']}"
            )

        else:
            st.warning(
                "Customer name and email are required."
            )

st.divider()

st.subheader("📋 Lead Pipeline")

if not st.session_state.leads:
    st.info(
        "No leads yet. Add and analyze your first lead above."
    )

else:
    sorted_leads = sorted(
        st.session_state.leads,
        key=lambda lead: lead["score"],
        reverse=True,
    )

    for lead in sorted_leads:
        with st.expander(
            f"{lead['priority']} | "
            f"{lead['score']}/100 | "
            f"{lead['name']} | "
            f"{lead['company']}"
        ):
            st.write(f"**Email:** {lead['email']}")
            st.write(
                f"**Estimated budget:** €{lead['budget']:,.0f}"
            )
            st.write(f"**Urgency:** {lead['urgency']}")
            st.write(
                f"**Interest:** {lead['interest_level']}"
            )
            st.write(
                f"**Priority:** {lead['priority']}"
            )
            st.write(
                f"**Lead score:** {lead['score']}/100"
            )

            st.progress(lead["score"] / 100)

            st.write("**Recommended next action:**")
            st.info(lead["recommended_action"])

            if lead["notes"]:
                st.write(f"**Notes:** {lead['notes']}")

            st.caption(
                f"Created: {lead['created']}"
            )
