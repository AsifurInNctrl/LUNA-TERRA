"""Build the small, standalone NASA Site07 demo package from downloaded source GeoTIFFs."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from src.nasa_site07 import EXPECTED_SOURCE_SHA256, process_site07


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", required=True, type=Path, help="Path to NASA *_surf.tif source")
    parser.add_argument("--slope", required=True, type=Path, help="Path to NASA *_slp.tif source")
    parser.add_argument("--output", type=Path, default=Path("data/demo/nasa_site07"))
    parser.add_argument("--download-date", default="2026-11-15")
    args = parser.parse_args()
    result = process_site07(args.surface, args.slope, args.output, args.download_date,
                            expected_source_sha256=EXPECTED_SOURCE_SHA256)
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["provenance"]["processing_script_sha256"] = script_hash
    result["provenance"]["processor_module_sha256"] = hashlib.sha256(
        Path(__file__).parents[1].joinpath("src", "nasa_site07.py").read_bytes()).hexdigest()
    (args.output / "summary.json").write_text(__import__("json").dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote standalone NASA Site07 derivatives to {args.output.resolve()}")
    print(f"Surface valid pixels: {result['elevation']['valid_pixel_count']:,}; slope valid pixels: {result['slope']['valid_pixel_count']:,}")


if __name__ == "__main__":
    main()
