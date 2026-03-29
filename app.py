import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Persist owner/pet/task model in Streamlit session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, pets=[], available_hours=4)

# Keep consistent owner name as input updates (optional update behavior)
if st.session_state.owner.name != owner_name:
    st.session_state.owner.name = owner_name

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

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

    # Ensure current pet exists in Owner object and persist in session
    owner = st.session_state.owner
    current_pet = next((p for p in owner.pets if p.name == pet_name), None)
    if current_pet is None:
        current_pet = Pet(breed=species, name=pet_name, tasks=[])
        owner.pets.append(current_pet)

    priority_map = {"high": 1, "medium": 2, "low": 3}
    task_obj = Task(
        description=task_title,
        duration=int(duration),
        due_time=datetime.now(),
        priority=priority_map.get(priority, 3),
    )
    current_pet.add_task(task_obj)
    st.session_state.owner = owner

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    if not owner.pets:
        st.warning("No pets or tasks found yet. Add a task to create a pet and schedule.")
    else:
        scheduler = Scheduler(all_tasks=owner.get_all_tasks(), owner=owner)
        schedule = scheduler.get_schedule()

        st.success("Schedule generated from current Owner state")
        for task in schedule:
            st.write(
                f"{task.due_time.strftime('%I:%M %p')} - {task.description} | priority: {task.priority} | pet: "
                f"{next((p.name for p in owner.pets if task in p.tasks), 'unknown')}"
            )

    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
