# LUNA-TERRA

LUNA-TERRA is an early-stage project for the 2026 NASA Space Apps Challenge,
**“Identify Earth Locations that Analog the Permanent Moon Base Locations and
Mars.”** It aims to identify purpose-specific terrestrial analog environments
on Earth for selected reference regions on the Moon and Mars, including
locations relevant to permanent Moon base planning. Potential comparison
dimensions include terrain, geological, and environmental characteristics.

Any similarity claim must be evidence-based, with sources, methods, and
uncertainty documented. An Earth analog may inform a specific purpose, but it
does not reproduce every condition on the Moon or Mars.

**This repository is a scaffold. Data integration is under development.** It
contains no scientific observations, model outputs, similarity scores, or
candidate rankings. Earth dataset selection, the Moon and Mars reference
regions, comparison methodology, and validation decisions have not yet been
established.

## Run locally

The listed direct dependencies are pinned to versions found installed in the
project environment. No packages were installed while creating this scaffold.

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Install dependencies separately when you are ready to set up another
environment:

```powershell
python -m pip install -r requirements.txt
```

## Repository layout

```text
app.py                     Streamlit prototype
src/                       Data and analysis module scaffolds
data/raw/                  Local source data; ignored by Git
data/processed/            Local derived data; ignored by Git
docs/methodology.md         Methodology record template
docs/data_sources.md       Data provenance template
docs/limitations.md        Limitations record template
assets/screenshots/        Project screenshots
```

Raw satellite data must not be committed. The `.gitignore` keeps both data
directories out of version control while preserving their `.gitkeep` markers.
Do not put secrets in the repository.

## Scientific documentation

Complete the templates in `docs/` before presenting quantitative results.
Record source identifiers, licenses, processing steps, measurement definitions,
uncertainty, validation, and known limitations. Do not interpret placeholder
code as a validated scientific method.
