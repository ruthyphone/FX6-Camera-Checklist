# sonyfs6.py
# Data-only file for app.py to consume

CHECKLIST = [
    # 1) Initialize
    "Menu (press & hold) → Maintenance → All Reset → Reset → Execute",

    # 2) Set Base for Log (Cine EI)
    "Menu → Project → Base Setting → Shooting Mode → Cine EI → Execute",

    # 3) Color Gamut / Log & Monitor LUT
    "Menu → Project → Cine EI/Flex.ISO Set → S-Gamut3.Cine/S-Log3 (easier grading) or S-Gamut3/S-Log3 (wider gamut)",
    "Quick Menu → Monitoring (p.5) → VF → MLUT (enable Monitor LUT to view corrected image)",

    # 4) Recording Format
    "Menu → Project → Rec Format",
    "Frequency → 23.98",
    "Imager Scan Mode → FF (Full Frame)",
    "Codec → XAVC-I (4:2:2, 10-bit)",
    "Video Format → 4096×2160p → Execute (or 3840×2160p if desired)",

    # 5) Shutter
    "Menu → Shooting → Shutter → Shutter Speed On/Off → On",
    "Shutter Speed → 1/48",

    # 6) Audio Inputs & Channels
    "Menu → Audio → Audio Input → CH1 Input Select → INPUT 1",
    "Menu → Audio → Audio Input → CH2 Input Select → INPUT 2",
    "Menu → Audio → Audio Input → CH3 Input Select → Internal MIC (or OFF)",
    "Menu → Audio → Audio Input → CH4 Input Select → Internal MIC (or OFF)",
    "Verify side-panel XLR switches: MIC or MIC +48V as needed (phantom for shotguns/lavs)",

    # 7) Timecode
    "Menu → TC/Media → Timecode → Run → Free Run (double-system) or Rec Run (single-system)",
    "Menu → TC/Media → Timecode → Reset → Execute (set to 00:00:00:00)",

    # 8) Format Media Cards
    "Menu → TC/Media → Format Media → Media A and/or Media B → Full Format → Execute",

    # 9) White Balance
    "Press the White Balance button (camera side)",
    "Use Multi-Dial to set Kelvin (3200K indoor tungsten / 5600K daylight / 4300K mixed) or custom WB",

    # 10) Base ISO / EI
    "Menu → Shooting → ISO/Gain/EI → Base ISO → ISO 800",
    "Exit menu → Use H/M/L toggle to set EI = 800 (match EI to Base ISO for most conditions)",

    # Autofocus
    "Autofocus: Toggle Focus Auto switch (front of body) to engage tracking (Eye AF on people)",
    "Manual focus: tap LCD to focus where desired (tracking box appears)",
    "Disengage AF: rotate focus ring or toggle switch to Manual",
    "Manual mode: ‘Push Auto’ button gives a quick AF punch-in to peak focus",

    # Tip
    "Tip: AF works only with lenses that communicate electronically (e.g., Sony 28–135mm cinema zoom)"
]
