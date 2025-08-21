# app.py
import streamlit as st
import runpy
from pathlib import Path

import uuid

# Always have a list to work with
if "items" not in st.session_state:
    st.session_state["items"] = []   # each item: {"text": "...", "done": False, "category": "..."}

# Ensure each item has a permanent unique id (uid)
for it in st.session_state["items"]:
    if isinstance(it, dict) and "uid" not in it:
        it["uid"] = uuid.uuid4().hex


if "items" not in st.session_state:
    st.session_state["items"] = []  # list of dicts like {"text": "...", "category": "..."}


st.set_page_config(page_title="Camera Checklist", page_icon="✅", layout="centered")
st.title("🎬 Camera Checklist")

# 👉 CHANGE THIS to match where your file sits in the repo:
RELATIVE_CHECKLIST_PATH = "sonyfs6.py"  # e.g. "checklist/SonyFS6.py" if it's in a folder

checklist_path = Path(__file__).parent / RELATIVE_CHECKLIST_PATH
if not checklist_path.exists():
    st.error(f"Checklist file not found at: {RELATIVE_CHECKLIST_PATH}")
    st.stop()

# Run the checklist file and capture any variables it defines
ns = runpy.run_path(str(checklist_path))

# Accept common list variable names if you structured it already
raw = ns.get("CHECKLIST") or ns.get("STEPS") or ns.get("ITEMS")

# Fallback: if your file is just text, use each non-empty line as a step
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
            "category": str(x.get("category", "")),
        }
    # list/tuple -> dict
    try:
        step = str(x[0])
        done = bool(x[1]) if len(x) > 1 else False
        notes = str(x[2]) if len(x) > 2 else ""
        return {"step": step, "done": done, "notes": notes}
    except Exception:
        return {"step": str(x), "done": False, "notes": ""}

if "items" not in st.session_state:
    st.session_state["items"] = [norm(i) for i in raw]

# Controls
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Reset all"):
        for it in st.session_state["items"]: it["done"] = False
with c2:
    if st.button("Mark all done"):
        for it in st.session_state["items"]: it["done"] = True
with c3:
    # simple ordering so unfinished float to top
    if st.button("Sort (undone first)"):
        st.session_state["items"].sort(key=lambda i: i["done"])

st.divider()
# st.subheader("Steps")

# Optional category filter if your items have "category"
# cats = sorted({i.get("category","") for i in st.session_state["items"] if i.get("category","")})
# view = st.session_state["items"] if not cats else [
#    i for i in st.session_state["items"]
#]

#start fix

st.subheader("Steps")

items = st.session_state["items"]  # <-- the actual list we’re iterating

# Build category list (tolerate items that might not be dicts yet)
cats = sorted({i.get("category", "") for i in items if isinstance(i, dict)})
cats = [c for c in cats if c]  # drop empty strings

# Optional: filter selector only if we have categories
if cats:
    chosen = st.selectbox("Filter by category", ["All"] + cats, index=0)
    view = items if chosen == "All" else [i for i in items if isinstance(i, dict) and i.get("category") == chosen]
else:
    view = items

items = st.session_state["items"]
index_by_uid = {it["uid"]: idx for idx, it in enumerate(items) if isinstance(it, dict) and "uid" in it}

# Render steps (works if each item is {"text": "...", ...}; falls back to str(item))
# Assume you already computed `view` (the list you want to display), e.g. filtered by category.
# Each element of `view` is one of the dicts from st.session_state["items"].

for view_pos, item in enumerate(view):
    if not isinstance(item, dict):
        st.write(f"{view_pos+1}. {str(item)}")
        continue

    uid = item.get("uid")
    if not uid:
        # Safety: create if missing, then update the index map
        uid = uuid.uuid4().hex
        item["uid"] = uid
        index_by_uid[uid] = len(st.session_state["items"]) - 1  # best-effort; adjust if you ever append here

    # Use uid-based keys so they are truly unique across the app
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        checked = st.checkbox(
            label="", 
            value=bool(item.get("done", False)), 
            key=f"done_{uid}"
        )
    with col2:
        text_val = item.get("text", "")
        st.write(text_val if text_val else "(no text)")

    # Write the checkbox state back to the master list using uid→index mapping
    master_idx = index_by_uid[uid]
    st.session_state["items"][master_idx]["done"] = checked

# end fix

for i, item in enumerate(view):
    idx = st.session_state["items"].index(item)
    col_a, col_b = st.columns([0.12, 0.88])
    with col_a:
        st.session_state["items"][idx]["done"] = st.checkbox("", value=item["done"], key=f"done_{idx}")
    with col_b:
        st.write(f"**{item['step']}**")
        st.session_state["items"][idx]["notes"] = st.text_input("Notes", value=item.get("notes",""), key=f"notes_{idx}", label_visibility="collapsed")

st.divider()
new = st.text_input("Add a new step")
if st.button("Add") and new.strip():
    st.session_state["items"].append({"step": new.strip(), "done": False, "notes": ""})
    st.rerun()
