"""Load and transform the supplied PNS02 lunar vector datasets."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import shapefile
from pyproj import CRS, Transformer
from shapely.geometry import shape
from shapely.ops import transform

TARGET_IDS = {324, 325, 330, 335, 338}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT = REPOSITORY_ROOT / "data" / "demo" / "pns02"


def research_root() -> Path:
    """Resolve packaged demo data relative to repository; allow explicit override."""
    import os
    return Path(os.environ.get("LUNA_TERRA_RESEARCH_ROOT", DEFAULT_DATA_ROOT))


def _read_layer(folder: Path, name: str) -> tuple[list[dict[str, Any]], list[Any], CRS]:
    shp_path = folder / f"{name}.shp"
    prj_path = folder / f"{name}.prj"
    missing = [str(p) for p in (shp_path, prj_path) if not p.exists()]
    if missing:
        raise FileNotFoundError("Required shapefile components missing: " + ", ".join(missing))
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
    psr_projected = [transform(psr_to_area.transform, g) if psr_to_area else g for g in psr_g]
    if not all(g.is_valid for g in psr_projected + area_g):
        raise ValueError("Invalid source geometry found; refusing silent repair")
    return {"root": root, "psr_attrs": psr_a, "psr_geoms": psr_projected,
            "site_attrs": site_a, "site_geoms": site_g, "area_attrs": area_a,
            "area_geoms": area_g, "psr_crs": psr_crs, "display_crs": area_crs,
            "site_crs": site_crs, "transformed": psr_to_area is not None}


def candidates(data: dict[str, Any]) -> list[int]:
    return [i for i, a in enumerate(data["area_attrs"]) if str(a.get("Name", "")).strip() == "PNS02"]


def overlap_summary(data: dict[str, Any], area_index: int) -> list[dict[str, Any]]:
    area = data["area_geoms"][area_index]
    rows = []
    for attrs, geom in zip(data["psr_attrs"], data["psr_geoms"]):
        intersection = geom.intersection(area)
        if intersection.area > 0:
            rows.append({"Id_1": attrs.get("Id_1"), "overlap_m2": intersection.area,
                         "psr_area_m2": geom.area,
                         "overlap_pct": 100 * intersection.area / geom.area if geom.area else 0})
    return rows
