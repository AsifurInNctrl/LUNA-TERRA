"""Data loading helpers for explicitly supplied tabular files.

Source-specific loading, validation, and provenance tracking are still under
development. This module does not fetch remote data.
"""

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Read a local CSV file without implying scientific validation.

    Callers are responsible for verifying source, license, schema, units,
    coordinate reference system, and preprocessing before analysis.
    """
    return pd.read_csv(path)
