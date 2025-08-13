import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sony FX6 Setup Checklist", page_icon="🎥", layout="centered")

# ---------- helpers ----------
def init_state():
    if "checked" not in st.session_state:
        st.session_state.checked = {}

def ck(key, label):
    st.session_state.checked[key] = st.checkbox(label, value=st.session_state.checked.get(key, False))

def header(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)

def section(title, items):
    with st.expander(title, expanded=False):
        for i, text in enumerate(items, start=1):
            ck(f"{title}:{i}", text)

def reset_all():
    st.session_state.checked = {}

def progress():
    vals = list(st.session_state.checked.values())
    done = sum(1 for v in vals if v)
    total = len(vals) if vals else 0
    return done, total, (done / total * 100 if total else 0)

# ---------- page ----------
init_state()
st.title("Sony FX6 – Intro Settings & Shoot-Day Checklist")
st.caption("MRTS 5830 Documentary Cinematography • Tap to tick items. Data stays in this browser tab.")

# quick controls
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔁 Reset All", help="Uncheck everything"):
        reset_all()
with c2:
    done, total, pct = progress()
    st.metric("Progress", f"{done}/{total}", f"{pct:.0f}%")
with c3:
    if st.button("📝 Export Report"):
        done, total, pct = progress()
        lines = ["Sony FX6 Setup Report",
                 f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                 f"Progress: {done}/{total} ({pct:.0f}%)", ""]
        for k, v in sorted(st.session_state.checked.items()):
            mark = "[x]" if v else "[ ]"
            lines.append(f"{mark} {k.split(':',1)[1]}")
        report = "\n".join(lines)
        st.download_button("Download .txt", report, file_name="fx6_setup_report.txt", mime="text/plain")

st.divider()

# 1. Initialize
section("1) Initialize (wipe previous users’ settings)", [
    "Menu (press & hold) → Maintenance → All Reset → Reset → Execute"
])

# 2. Base (Log) mode
section("2) Set Base for Log (Cine EI)", [
    "Menu → Project → Base Setting → Shooting Mode → Cine EI → Execute"
])

# 3. Color Gamut / Log & Monitor LUT", 
section("3) Color Gamut / Log & Monitor LUT", [
    "Menu → Project → Cine EI/Flex.ISO Set → S-Gamut3.Cine/S-Log3 (easier grading) "
    "or S-Gamut3/S-Log3 (wider gamut)",
    "Quick Menu → Monitoring (p.5) → VF → MLUT (enable Monitor LUT to view corrected image)"
])

# 4. Recording format
section("4) Recording Format", [
    "Menu → Project → Rec Format",
    "Frequency → 23.98",
    "Imager Scan Mode → FF (Full Frame)",
    "Codec → XAVC-I (4:2:2, 10-bit)",
    "Video Format → 4096×2160p → Execute (or 3840×2160p if desired)"
])

# 5. Shutter
section("5) Shutter", [
    "Menu → Shooting → Shutter → Shutter Speed On/Off → On",
    "Shutter Speed → 1/48"
])

# 6. Audio routing & XLR power
section("6) Audio Inputs & Channels", [
    "Menu → Audio → Audio Input → CH1 Input Select → INPUT 1",
    "Menu → Audio → Audio Input → CH2 Input Select → INPUT 2",
    "Menu → Audio → Audio Input → CH3 Input Select → Internal MIC (or OFF)",
    "Menu → Audio → Audio Input → CH4 Input Select → Internal MIC (or OFF)",
    "Verify side-panel XLR switches: MIC or MIC +48V as needed (phantom for shotguns/lavs)"
])

# 7. Timecode
section("7) Timecode", [
    "Menu → TC/Media → Timecode → Run → Free Run (double-system) or Rec Run (single-system)",
    "Menu → TC/Media → Timecode → Reset → Execute (set to 00:00:00:00)"
])

# 8. Format media
section("8) Format Media Cards", [
    "Menu → TC/Media → Format Media → Media A and/or Media B → Full Format → Execute"
])

# 9. White Balance
section("9) White Balance", [
    "Press the White Balance button (camera side)",
    "Use Multi-Dial to set Kelvin (3200K indoor tungsten / 5600K daylight / 4300K mixed) or custom WB"
])

# 10. Base ISO / EI workflow
section("10) Base ISO / EI", [
    "Menu → Shooting → ISO/Gain/EI → Base ISO → ISO 800",
    "Exit menu → Use H/M/L toggle to set EI = 800 (match EI to Base ISO for most conditions)"
])

# Autofocus tips
header("Autofocus (FX6)", "Face/Eye AF & object tracking (lens must support electronic AF).")
section("Autofocus – Engage / Disengage", [
    "Toggle Focus Auto switch (front of body) → AF tracking begins (eye AF on people).",
    "In Manual: tap LCD to focus where desired (tracking box appears).",
    "Disengage AF: rotate focus ring or toggle switch to Manual.",
    "Manual mode ‘Push Auto’ button gives a quick AF punch-in to peak focus."
])

# Lens note
st.info("⚠️ AF works only with lenses that communicate electronically with the camera. "
        "The Sony 28–135mm cinema zoom works great; there are two in the graduate equipment room.")

st.divider()
st.caption("Tip: Pin this tab on your phone and keep the page open; checkmarks persist while the tab stays active.")
