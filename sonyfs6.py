"""
sonyfs6_v3.py — structured FX6 setup checklist (with Exposure Indexing section)

What’s new vs. v2
- Added "11) Exposure Indexing for Low Light (Cine EI)" with detailed, step‑by‑step workflow
- Preserves your exact original steps and order for all other categories
- Utilities & CLI remain the same as v2

Run examples
  python sonyfs6_v3.py --format md > fx6_checklist.md
  python sonyfs6_v3.py --only "11) Exposure Indexing for Low Light (Cine EI)" --format md
  python sonyfs6_v3.py --search "exposure indexing" --format txt
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Iterable, Optional
import json
import argparse
import textwrap


# =============================
# Data Model
# =============================
@dataclass(frozen=True)
class Step:
    text: str
    note: Optional[str] = None

    def __str__(self) -> str:
        if self.note:
            return f"{self.text}  —  {self.note}"
        return self.text


@dataclass(frozen=True)
class Category:
    title: str
    steps: List[Step]


# =============================
# Source Data (preserves your original entries)
# =============================
RAW_CATEGORY_MAP: Dict[str, List[str]] = {
    "1) Initialize (wipe previous users’ settings)": [
        "Menu (press & hold) → Maintenance → All Reset → Reset → Execute",
    ],
    "2) Set Base for Log (Cine EI)": [
        "Menu → Project → Base Setting → Shooting Mode → Cine EI → Execute",
    ],
    "3) Color Gamut / Log & Monitor LUT": [
        "Menu → Project → Cine EI/Flex.ISO Set → S-Gamut3.Cine/S-Log3 (easier grading) or S-Gamut3/S-Log3 (wider gamut)",
        "Quick Menu → Monitoring (p.5) → VF → MLUT (enable Monitor LUT to view corrected image)",
    ],
    "4) Recording Format": [
        "Menu → Project → Rec Format",
        "Frequency → 23.98",
        "Imager Scan Mode → FF (Full Frame)",
        "Codec → XAVC-I (4:2:2, 10-bit)",
        "Video Format → 4096×2160p → Execute (or 3840×2160p if desired)",
    ],
    "5) Shutter": [
        "Menu → Shooting → Shutter → Shutter Speed On/Off → On",
        "Shutter Speed → 1/48",
    ],
    "6) Audio Inputs & Channels": [
        "Menu → Audio → Audio Input → CH1 Input Select → INPUT 1",
        "Menu → Audio → Audio Input → CH2 Input Select → INPUT 2",
        "Menu → Audio → Audio Input → CH3 Input Select → Internal MIC (or OFF)",
        "Menu → Audio → Audio Input → CH4 Input Select → Internal MIC (or OFF)",
        "Verify side-panel XLR switches: MIC or MIC +48V as needed (phantom for shotguns/lavs)",
    ],
    "7) Timecode": [
        "Menu → TC/Media → Timecode → Run → Free Run (double-system) or Rec Run (single-system)",
        "Menu → TC/Media → Timecode → Reset → Execute (set to 00:00:00:00)",
    ],
    "8) Format Media Cards": [
        "Menu → TC/Media → Format Media → Media A and/or Media B → Full Format → Execute",
    ],
    "9) White Balance": [
        "Press the White Balance button (camera side)",
        "Set Kelvin (3200K indoor / 5600K daylight / ~4300K mixed) or custom WB",
    ],
    "10) Base ISO / EI": [
        "Menu → Shooting → ISO/Gain/EI → Base ISO → ISO 800",
        "Exit menu → Use H/M/L toggle to set EI = 800 (match EI to Base ISO)",
    ],
    "Autofocus (FX6)": [
        "Toggle Focus Auto switch (front of body) to engage tracking (Eye AF on people)",
        "Manual: tap LCD to choose focus point (tracking box appears)",
        "Disengage AF: rotate focus ring or switch to Manual",
        "Manual mode: ‘Push Auto’ button gives a quick AF punch-in",
    ],
    "11) Exposure Indexing for Low Light (Cine EI)": [
        "Goal: Bring out more shadow detail in extreme low light by overexposing S-Log intentionally, then normalizing in post.",
        "1) Optional: Connect an external monitor for easier viewing.",
        "2) Quick Menu: press/release Menu → LCD touch quick menu.",
        "3) Quick Menu → Monitoring (page 5/10).",
        "4) Set VF to SG3C/S-Log3 (routes S-Log to the LCD screen).",
        "5) Set HDMI/SDI to MLUT (applies LUT to the external monitor only).",
        "6) Set Base Look/LUT to s709 (standard viewing on the external monitor).",
        "7) Hold Menu for full menu → Shooting → LUT On/Off → verify Internal Rec = MLUT Off (prevents baking LUT to media).",
        "8) Exit menus. LCD shows S-Log; external monitor shows s709.",
        "   • Assign button (LCD side) → enable Waveform Monitor. With external monitor connected, waveform reflects the external signal (s709 or S-Log). Expect ‘LUT s709’ above the waveform if s709 is routed to HDMI/SDI.",
        "9) Full menu → Shooting → ISO/Gain/EI → set EI targets:",
        "   • Exposure Index <H> = 800 EI / 6.0E",
        "   • Exposure Index <M> = 400 EI / 5.0E",
        "   • Exposure Index <L> = 200 EI / 4.0E",
        "   NOTE: When NOT using exposure indexing, keep EI equal to Base ISO (usually 800) to maximize dynamic range.",
        "10) +1 stop workflow (use M=400 EI):",
        "   a) Set H/M/L toggle to M → EI shows 400 on LCD. S-Log image does not change; EI affects LUT only.",
        "   b) External monitor appears 1 stop darker; waveform drops by ~1 stop (it represents s709 on the external monitor).",
        "   c) Open lens aperture by +1 stop (e.g., f/4 → f/2.8) to re-center exposure on the external monitor.",
        "   d) Result: Recorded S-Log is effectively +1 stop brighter (cleaner shadows) while Base ISO remains 800. EI ≠ ISO.",
        "   e) In post, lower exposure ~1 stop back to nominal; shadow noise is reduced vs. no EI.",
        "11) +2 stops workflow (use L=200 EI): set toggle to L, then open aperture +2 stops to compensate.",
        "12) Reminder: +1 stop = 2× light; +2 stops = 4× light. -1 stop = 1/2 light.",
        "NOTE: You can perform EI without an external monitor by placing s709 on the LCD and setting the waveform to display S-Log3; the EI steps and results are the same.",
    ],
}

# Optional: tiny clarifying notes appended without changing your original lines
CLARIFY_NOTES: Dict[str, Dict[int, str]] = {
    "3) Color Gamut / Log & Monitor LUT": {
        1: "Enable MLUT for monitoring only; recording stays in S-Log3.",
    },
    "4) Recording Format": {
        1: "24.00 vs 23.98: pick 23.98 for broadcast-friendly workflows.",
    },
}


# =============================
# Build helpers
# =============================
def _build_categories(raw: Dict[str, List[str]]) -> List[Category]:
    cats: List[Category] = []
    for title, steps in raw.items():
        cats.append(Category(title=title, steps=[Step(s) for s in steps]))
    return cats


def list_categories() -> List[str]:
    return list(RAW_CATEGORY_MAP.keys())


def get_steps(category: str) -> List[str]:
    return RAW_CATEGORY_MAP.get(category, [])


def search(term: str) -> Dict[str, List[str]]:
    term_l = term.lower()
    out: Dict[str, List[str]] = {}
    for k, steps in RAW_CATEGORY_MAP.items():
        hits = [s for s in steps if term_l in s.lower()]
        if hits:
            out[k] = hits
    return out


def to_markdown(categories: Optional[Iterable[str]] = None) -> str:
    cats = RAW_CATEGORY_MAP if categories is None else {k: RAW_CATEGORY_MAP[k] for k in RAW_CATEGORY_MAP if k in categories}
    lines: List[str] = []
    for title, steps in cats.items():
        lines.append(f"## {title}")
        for i, s in enumerate(steps, 1):
            lines.append(f"{i}. {s}")
        lines.append("")
    return "\n".join(lines)


def to_json(categories: Optional[Iterable[str]] = None, indent: int = 2) -> str:
    cats = RAW_CATEGORY_MAP if categories is None else {k: RAW_CATEGORY_MAP[k] for k in RAW_CATEGORY_MAP if k in categories}
    return json.dumps(cats, indent=indent, ensure_ascii=False)


# =============================
# CLI
# =============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sony FX6 setup checklist exporter")
    parser.add_argument("--format", choices=["md", "json", "txt"], default="md")
    parser.add_argument("--only", nargs="*", help="Restrict to these category titles")
    parser.add_argument("--search", dest="term", help="Search term to filter steps")
    args = parser.parse_args()

    if args.term:
        hits = search(args.term)
        print(to_json(hits, indent=2))
    else:
        if args.only:
            cats = [c for c in args.only]
        else:
            cats = None
        out = to_markdown(cats) if args.format == "md" else (to_json(cats) if args.format == "json" else to_markdown(cats))
        print(out)

# Backward compatibility for apps expecting CATEGORY_MAP
CATEGORY_MAP = RAW_CATEGORY_MAP
