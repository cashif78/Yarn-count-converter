# app.py
import streamlit as st
import numpy as np

CONST_NE_TEX = 590.5  # used for Ne <-> Tex conversions

UNIT_KEYS = {
    "Tex": "tex",
    "Denier (den)": "denier",
    "Decitex (dtex)": "dtex",
    "Metric (Nm)": "nm",
    "English cotton (Ne)": "ne",
}

def to_tex(value: float, unit_key: str):
    """Convert input value (in unit_key) to Tex."""
    if value is None:
        return None
    if unit_key == "Tex":
        return float(value)
    if unit_key == "Denier (den)":
        return float(value) / 9.0
    if unit_key == "Decitex (dtex)":
        return float(value) / 10.0
    if unit_key == "Metric (Nm)":
        if value == 0:
            return None
        return 1000.0 / float(value)
    if unit_key == "English cotton (Ne)":
        if value == 0:
            return None
        return CONST_NE_TEX / float(value)
    return None

def from_tex(tex_val: float):
    """Return dict of conversions from tex to other units."""
    if tex_val is None:
        return {}
    tex = float(tex_val)
    result = {
        "Tex": tex,
        "Denier (den)": tex * 9.0,
        "Decitex (dtex)": tex * 10.0,
        "Metric (Nm)": (1000.0 / tex) if tex != 0 else None,
        "English cotton (Ne)": (CONST_NE_TEX / tex) if tex != 0 else None,
    }
    return result

def fmt(v):
    if v is None:
        return "—"
    # Use sensible rounding: show up to 6 significant digits
    if abs(v) >= 100:
        return f"{v:,.2f}"
    return f"{v:.6g}"

st.set_page_config(page_title="Yarn Count Converter", layout="centered")
st.title("Yarn Count Converter")
st.write("Convert between Tex, Denier, Dtex, Metric (Nm), and English cotton count (Ne).")

col1, col2 = st.columns([1, 1])
with col1:
    value = st.number_input("Input value", value=20.0, format="%.6g")
with col2:
    from_unit = st.selectbox("From unit", list(UNIT_KEYS.keys()))

targets = st.multiselect("Show conversions to (leave empty to show all)", list(UNIT_KEYS.keys()))
if len(targets) == 0:
    targets = list(UNIT_KEYS.keys())

if st.button("Convert") or st.session_state.get("__run__", True):
    tex = to_tex(value, from_unit)
    conv = from_tex(tex)
    st.markdown("### Results")
    rows = []
    for u in targets:
        rows.append((u, fmt(conv.get(u))))
    # nice table
    st.table({ "Unit": [r[0] for r in rows], "Value": [r[1] for r in rows] })

st.markdown("**Notes:**")
st.markdown(
    "- Tex = grams per 1000 m; Denier = grams per 9000 m (Denier = Tex × 9)."
)
st.markdown("- Metric Nm = 1000 / Tex.  English cotton Ne = 590.5 / Tex.")
