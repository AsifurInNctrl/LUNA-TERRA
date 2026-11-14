# LUNA-TERRA

LUNA-TERRA is an early-stage project for the 2026 NASA Space Apps Challenge,
**“Identify Earth Locations that Analog the Permanent Moon Base Locations and
Mars.”** The research basis proposes purpose-specific Earth analog environments
for selected lunar and Martian reference regions. Its provisional primary
references are PNS02 in the Peak Near Shackleton region on the Moon and Jezero
Crater on Mars; CR05 (Connecting Ridge) is a provisional secondary lunar case.
Atacama salars, Haughton Impact Crater, Lake Bonney/McMurdo Dry Valleys, Lonar
Crater, and Rio Tinto are proposed Earth benchmark environments. These are
research selections, not verified analog results. Potential comparison
dimensions include terrain, geological, and environmental characteristics.

Any similarity claim must be evidence-based, with sources, methods, and
uncertainty documented. An Earth analog may inform a specific purpose, but it
does not reproduce every condition on the Moon or Mars.

**This repository is a scaffold. Data integration is under development.** It
contains no downloaded or integrated scientific datasets, analyzed
observations, model outputs, similarity scores, or candidate rankings. The
named regions and benchmarks remain provisional; exact AOIs, dataset
availability, processing, and validation have not been finalized. The proposed
workflow is a roadmap:
raster processing, STAC discovery, terrain analysis, and similarity scoring
are not implemented. No composite score is currently proposed for the MVP.

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
docs/research_basis.md     Preliminary literature review and research roadmap
assets/screenshots/        Project screenshots
```

Raw satellite data must not be committed. The `.gitignore` keeps both data
directories out of version control while preserving their `.gitkeep` markers.
Do not put secrets in the repository.

## Scientific documentation

Use `docs/research_basis.md` as a preliminary plan, not as a dataset inventory
or a report of LUNA-TERRA findings. Complete the templates in `docs/` before
presenting quantitative results. Record source identifiers, licenses, exact
AOIs, processing steps, measurement definitions, uncertainty, validation, and
known limitations. Do not interpret placeholder code as a validated scientific
method.
