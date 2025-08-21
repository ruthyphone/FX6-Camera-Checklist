# app.py
import streamlit as st
import runpy
from pathlib import Path
from itertools import chain

st.set_page_config(page_title="Camera Checklist", page_icon="✅", layout="centered")
st.title("🎬 Camera Checklist")

RELATIVE_CHECKLIST_PATH = "sonyfs6.py"
checklist_path = Path(__file__).parent / RELATIVE_CHECKLIST_PATH
if not checklist_path.exists():
    st.error(f"Checklist file not found at: {RELATIVE_CHECKLIST_PATH}")
    st.stop()

ns = runpy.run_path(str(checklist_path))
cat_map = ns.get("CATEGORY_MAP")
if not isinstance(cat_map, dict) or not cat_map:
    st.error("No CATEGORY_MAP found in sonyfs6.py (expected dict: category -> list of steps).")
    st.stop()

# Flatten once into a master list with category + step
flat = []
for cat, steps in cat_map.items():
    for s in steps:
        flat.append({"category": str(cat), "step": str(s), "done": False})

# Initialize session state once
if "items" not in st.session_state:
    st.session_state["items"] = flat

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

# Render grouped by category (expanders). Keys are the global indices (unique).
# Build: category -> list of (global_index, item)
by_cat = {}
for i, it in enumerate(st.session_state["items"]):
    by_cat.setdefault(it["category"], []).append((i, it))

for cat in cat_map.keys():  # keep original category order
    pairs = by_cat.get(cat, [])
    with st.expander(cat, expanded=False):
        for i, it in pairs:
            cols = st.columns([0.10, 0.90])
            with cols[0]:
                st.session_state["items"][i]["done"] = st.checkbox(
                    "", value=it["done"], key=f"done_{i}"
                )
            with cols[1]:
                st.write(it["step"])

st.caption("Tip: Keep this tab open; checkmarks persist while the tab stays active.")
