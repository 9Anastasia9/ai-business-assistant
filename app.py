import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Business Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Business Assistant")
st.caption("Smart lead management and AI-powered business workflow assistant")

# Initialize data
if "leads" not in st.session_state:
    st.session_state.leads = []

# Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Leads", len(st.session_state.leads))

with col2:
    hot_leads = sum(
        1 for lead in st.session_state.leads
        if lead["priority"] == "Hot"
    )
    st.metric("Hot Leads", hot_leads)

with col3:
    st.metric("AI Status", "Ready")

st.divider()

st.subheader("➕ Add New Lead")

with st.form("lead_form"):
    name = st.text_input("Customer name")
    email = st.text_input("Email")
    company = st.text_input("Company")

    priority = st.selectbox(
        "Lead priority",
        ["Hot", "Warm", "Cold"]
    )

    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Add Lead")

    if submitted:
        if name and email:
            st.session_state.leads.append(
                {
                    "name": name,
                    "email": email,
                    "company": company,
                    "priority": priority,
                    "notes": notes,
                    "created": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }
            )

            st.success(f"Lead {name} added successfully!")
        else:
            st.warning("Name and email are required.")

st.divider()

st.subheader("📋 Lead Pipeline")

if not st.session_state.leads:
    st.info("No leads yet. Add your first lead above.")
else:
    for lead in reversed(st.session_state.leads):
        with st.expander(
            f"{lead['priority']} | {lead['name']} | {lead['company']}"
        ):
            st.write(f"**Email:** {lead['email']}")
            st.write(f"**Priority:** {lead['priority']}")
            st.write(f"**Created:** {lead['created']}")
            st.write(f"**Notes:** {lead['notes']}")
