# app.py
import streamlit as st
import runpy
from pathlib import Path

st.set_page_config(page_title="Camera Checklist", page_icon="✅", layout="centered")
st.title("🎬 Camera Checklist")

# 👉 If your checklist lives elsewhere, change this path accordingly.
RELATIVE_CHECKLIST_PATH = "sonyfs6.py"

checklist_path = Path(__file__).parent / RELATIVE_CHECKLIST_PATH
if not checklist_path.exists():
    st.error(f"Checklist file not found at: {RELATIVE_CHECKLIST_PATH}")
    st.stop()

# Run the checklist file and capture any variables it defines
ns = runpy.run_path(str(checklist_path))

# Accept common variable names
raw = ns.get("CHECKLIST") or ns.get("STEPS") or ns.get("ITEMS")

# Fallback: treat each non-empty line as a step (ignore comments/triple-quoted blocks)
if raw is None:
    lines = checklist_path.read_text(encoding="utf-8").splitlines()
    raw = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith(('#', "'''", '"""'))]

def norm(x):
    # string -> dict
    if isinstance(x, str):
        return {"step": x, "done": False, "notes": ""}
    # dict -> dict (ensure keys)
    if isinstance(x, dict):
        return {
            "step": str(x.get("step", "")),
            "done": bool(x.get("done", False)),
            "notes": str(x.get("notes", "")),
        }
    # list/tuple -> dict
    try:
        step = str(x[0])
        done = bool(x[1]) if len(x) > 1 else False
        notes = str(x[2]) if len(x) > 2 else ""
        return {"step": step, "done": done, "notes": notes}
    except Exception:
        return {"step": str(x), "done": False, "notes": ""}

# Initialize session items once from the source file
if "items" not in st.session_state:
    st.session_state["items"] = [norm(i) for i in raw]

# Controls
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Reset all"):
        for it in st.session_state["items"]:
            it["done"] = False
with c2:
    if st.button("Mark all done"):
        for it in st.session_state["items"]:
            it["done"] = True
with c3:
    if st.button("Sort (undone first)"):
        st.session_state["items"].sort(key=lambda i: i["done"])

st.divider()
st.subheader("Steps")

# Render list (single pass -> no duplicate keys)
for i, item in enumerate(st.session_state["items"]):
    col_a, col_b = st.columns([0.12, 0.88])
    with col_a:
        st.session_state["items"][i]["done"] = st.checkbox(
            "", value=item.get("done", False), key=f"done_{i}"
        )
    with col_b:
        st.write(f"**{item.get('step', '')}**")
        st.session_state["items"][i]["notes"] = st.text_input(
            "Notes", value=item.get("notes", ""), key=f"notes_{i}", label_visibility="collapsed"
        )

st.divider()
new = st.text_input("Add a new step")
if st.button("Add") and new.strip():
    st.session_state["items"].append({"step": new.strip(), "done": False, "notes": ""})
    st.rerun()
