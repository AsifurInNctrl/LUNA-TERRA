"""LUNA-TERRA Streamlit entry point."""

import streamlit as st


st.set_page_config(
    page_title="LUNA-TERRA | Earth, Moon & Mars Analogs",
    page_icon="🌑",
    layout="wide",
)

st.title("LUNA-TERRA")
st.subheader("Earth analogs for Moon and Mars reference regions")
st.write(
    "LUNA-TERRA addresses the NASA Space Apps Challenge, **“Identify Earth "
    "Locations that Analog the Permanent Moon Base Locations and Mars.”** "
    "The project aims to identify purpose-specific environments on Earth that "
    "can be compared with selected reference regions on the Moon and Mars."
)

st.info(
    "**Development status:** data integration is under development. "
    "No satellite datasets have been integrated, and this prototype does not "
    "display observations, similarity scores, or candidate rankings."
)

st.markdown("### Project objective")
st.write(
    "LUNA-TERRA aims to identify purpose-specific terrestrial analog "
    "environments on Earth for selected lunar and Martian reference regions, "
    "including locations relevant to permanent Moon base planning. Potential "
    "comparison dimensions include terrain, geological, and environmental "
    "characteristics. Any claimed similarity must be supported by documented "
    "evidence, methods, and uncertainty. An Earth analog can inform a specific "
    "comparison, but it does not reproduce every condition on the Moon or Mars."
)

st.markdown("### Planned workflow")
st.markdown(
    "1. Select and document Earth datasets and the chosen Moon and Mars reference regions.\n"
    "2. Define reproducible terrain, geological, and environmental measurements.\n"
    "3. Implement an evidence-based comparison method after those choices are reviewed.\n"
    "4. Present any future findings with provenance, uncertainty, and analog limitations."
)

with st.expander("Data integration status"):
    st.write(
        "The `data/raw/` and `data/processed/` directories are scaffolded. "
        "They currently contain no scientific data. Source selection, licensing, "
        "coordinate conventions, resolution, and processing decisions remain to be documented."
    )

st.caption("NASA Space Apps Challenge 2026 project · Prototype scaffold")
