"""Load and transform the supplied PNS02 lunar vector datasets."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import shapefile
from pyproj import CRS, Transformer
from shapely import transform as shapely_transform
from shapely.geometry import shape

TARGET_IDS = {324, 325, 330, 335, 338}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT = REPOSITORY_ROOT / "data" / "demo" / "pns02"


def research_root() -> Path:
    """Resolve packaged demo data relative to repository; allow explicit override."""
    import os
    return Path(os.environ.get("LUNA_TERRA_RESEARCH_ROOT", DEFAULT_DATA_ROOT))


def _read_layer(folder: Path, name: str) -> tuple[list[dict[str, Any]], list[Any], CRS]:
    components = [folder / f"{name}{suffix}" for suffix in (".shp", ".shx", ".dbf", ".prj")]
    missing = [str(p) for p in components if not p.exists()]
    if missing:
        raise FileNotFoundError("Required shapefile components missing (.shp, .shx, .dbf, .prj): " + ", ".join(missing))
    shp_path = folder / f"{name}.shp"
    prj_path = folder / f"{name}.prj"
    crs = CRS.from_wkt(prj_path.read_text(encoding="utf-8"))
    reader = shapefile.Reader(str(shp_path), encoding="utf-8")
    fields = [f[0] for f in reader.fields[1:]]
    attrs, geoms = [], []
    try:
        for record in reader.iterShapeRecords():
            attrs.append(dict(zip(fields, list(record.record))))
            geoms.append(shape(record.shape.__geo_interface__))
    finally:
        reader.close()
    return attrs, geoms, crs


def _transform_geometries(geometries: list[Any], transformer: Transformer | None) -> list[Any]:
    """Project each geometry while preserving its dimensionality and source object."""
    if transformer is None:
        return list(geometries)
    return [shapely_transform(g, transformer.transform, include_z=g.has_z, interleaved=False)
            for g in geometries]


def load_pns02_data(root: Path | None = None) -> dict[str, Any]:
    """Load all source features and transform PSRs into exploration CRS."""
    root = Path(root or research_root())
    psr_dir, site_dir = root / "PSR_Volatile_Estimates", root / "Landing_Sites"
    psr_a, psr_g, psr_crs = _read_layer(psr_dir, "PSR_volatile_abundance_final")
    site_a, site_g, site_crs = _read_layer(site_dir, "LandingSites")
    area_a, area_g, area_crs = _read_layer(site_dir, "ExplorationArea_2km")
    if not site_crs.equals(area_crs):
        raise ValueError("LandingSites and ExplorationArea_2km CRS definitions differ")
    if psr_crs.equals(area_crs):
        psr_to_area = None
    else:
        if psr_crs.geodetic_crs is None or area_crs.geodetic_crs is None:
            raise ValueError("Could not verify lunar geodetic CRS for transformation")
        psr_to_area = Transformer.from_crs(psr_crs, area_crs, always_xy=True)
    psr_projected = _transform_geometries(psr_g, psr_to_area)
    if not all(g.is_valid for g in psr_projected + area_g):
        raise ValueError("Invalid source geometry found; refusing silent repair")
    return {"root": root, "psr_attrs": psr_a, "psr_geoms": psr_projected,
            "psr_source_records": list(range(1, len(psr_a) + 1)),
            "site_attrs": site_a, "site_geoms": site_g, "area_attrs": area_a,
            "area_geoms": area_g, "psr_crs": psr_crs, "display_crs": area_crs,
            "site_crs": site_crs, "transformed": psr_to_area is not None}


def candidates(data: dict[str, Any]) -> list[int]:
    return [i for i, a in enumerate(data["area_attrs"]) if str(a.get("Name", "")).strip() == "PNS02"]


def unique_candidate(data: dict[str, Any]) -> int:
    """Return the sole PNS02 exploration feature or explain missing/ambiguous matches."""
    matches = candidates(data)
    if not matches:
        raise ValueError("No exploration-area feature has Name=PNS02")
    if len(matches) > 1:
        raise ValueError(f"Found {len(matches)} exploration-area features named PNS02; select one explicitly")
    return matches[0]


def overlap_summary(data: dict[str, Any], area_index: int) -> list[dict[str, Any]]:
    area = data["area_geoms"][area_index]
    rows = []
    for record, attrs, geom in zip(data["psr_source_records"], data["psr_attrs"], data["psr_geoms"]):
        intersection = geom.intersection(area)
        if intersection.area > 0:
            rows.append({"source_record": record, "Id_1": attrs.get("Id_1"), "overlap_m2": intersection.area,
                         "psr_area_m2": geom.area,
                         "overlap_pct": 100 * intersection.area / geom.area if geom.area else 0})
    return rows


def viewport_bounds(geometry: Any, margin_fraction: float = 0.1) -> tuple[float, float, float, float]:
    """Return visualization-only (xmin, xmax, ymin, ymax) bounds with proportional margin."""
    if margin_fraction < 0:
        raise ValueError("margin_fraction must be non-negative")
    xmin, ymin, xmax, ymax = geometry.bounds
    width, height = xmax - xmin, ymax - ymin
    if width <= 0 or height <= 0:
        raise ValueError("Cannot calculate viewport for zero-width or zero-height geometry")
    return (xmin - width * margin_fraction, xmax + width * margin_fraction,
            ymin - height * margin_fraction, ymax + height * margin_fraction)


def pns02_site_candidates(data: dict[str, Any], area_index: int) -> list[int]:
    """Find named PNS02 points that lie within the selected PNS02 area geometry."""
    area = data["area_geoms"][area_index]
    return [i for i, (attrs, point) in enumerate(zip(data["site_attrs"], data["site_geoms"]))
            if str(attrs.get("Name", "")).strip() == "PNS02" and point.geom_type == "Point"
            and area.covers(point)]


def ordered_psr_records(data: dict[str, Any], area_index: int) -> list[int]:
    """Order indexes with PNS02-overlap records first, preserving source order."""
    overlapping = {row["source_record"] for row in overlap_summary(data, area_index)}
    return sorted(range(len(data["psr_attrs"])),
                  key=lambda i: (data["psr_source_records"][i] not in overlapping,
                                 data["psr_source_records"][i]))


def default_psr_record(data: dict[str, Any], area_index: int) -> int:
    """Return the first source-order overlapping PSR index for inspection only."""
    ordered = ordered_psr_records(data, area_index)
    if not ordered or data["psr_source_records"][ordered[0]] not in {
            row["source_record"] for row in overlap_summary(data, area_index)}:
        raise ValueError("No positive-area PSR overlap is available for default inspection")
    return ordered[0]


def default_selection_label(data: dict[str, Any], index: int) -> str:
    """Stable display label based on original source order and unchanged source ID."""
    return f"Record {data['psr_source_records'][index]} | Id_1={data['psr_attrs'][index].get('Id_1')}"
