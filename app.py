import streamlit as st
from pawpal_system import Task, Pet, Owner
from scheduler import Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("Your daily pet care planner.")

st.divider()

# --- Owner + Pet Info ---
st.subheader("Owner & Pet Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=120)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

st.divider()

# --- Task Input ---
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
    if st.button("Clear all tasks"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule Generation ---
st.subheader("Daily Schedule")

if st.button("Generate schedule", type="primary"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, available_minutes=int(available_minutes))
        pet = Pet(name=pet_name, species=species)
        tasks = [
            Task(title=t["title"], duration_minutes=t["duration_minutes"], priority=t["priority"])
            for t in st.session_state.tasks
        ]

        plan = Scheduler().generate_plan(owner, tasks)

        st.success(
            f"Scheduled {len(plan.scheduled)} of {len(tasks)} tasks "
            f"({plan.total_minutes} / {available_minutes} min used)"
        )

        if plan.scheduled:
            st.markdown("#### Scheduled Tasks")
            st.table([
                {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
                for t in plan.scheduled
            ])

        if plan.skipped:
            st.markdown("#### Skipped Tasks")
            st.table([
                {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
                for t in plan.skipped
            ])

        st.markdown("#### Reasoning")
        for reason in plan.reasoning:
            st.markdown(f"- {reason}")
