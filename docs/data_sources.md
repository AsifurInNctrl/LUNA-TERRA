# Data sources and provenance

> Status: provenance template. No scientific datasets are currently integrated.
> `docs/research_basis.md` names provisional candidate products and catalog
> collections; those proposals are not evidence of AOI coverage, downloaded
> files, or integrated data.

Create one entry per dataset and retain enough information to retrieve the exact
source version. Do not store raw satellite data in Git; see `.gitignore`.

## Dataset record

- Dataset title and identifier:
- Provider and landing-page URL:
- Version, release, or access date:
- License and usage conditions:
- Sensor or instrument (if applicable):
- Product identifier and processing level (distinguish at-sensor radiance,
  surface reflectance, surface temperature, and derived products):
- Body (Earth, Moon, or Mars), region, and spatial/temporal coverage:
- Role in the comparison (Earth analog candidate or selected planetary reference region):
- Native resolution, coordinate reference system, and units:
- File formats and required bands/variables:
- Quality flags and filtering decisions:
- Local storage location (raw files belong under `data/raw/`):
- Checksums or other integrity identifiers:
- Citation and acknowledgement text:
- Known gaps or caveats:

## ASTER product note

Do not label ASTER L1T as surface reflectance. NASA identifies AST_L1T as
precision terrain-corrected, registered at-sensor radiance. AST_07 and AST_07XT
are separate surface-reflectance products; AST_08 is a surface kinetic
temperature product. Confirm the exact product, access route, version, bands,
and AOI coverage before selecting one. [NASA ASTER product definitions](https://asterweb.jpl.nasa.gov/data_products.asp)
