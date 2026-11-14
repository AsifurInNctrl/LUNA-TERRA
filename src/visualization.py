"""Visualization helpers for data supplied by a future integrated workflow."""

import pandas as pd
import plotly.express as px


def coordinate_figure(
    records: pd.DataFrame,
    *,
    latitude_column: str,
    longitude_column: str,
):
    """Create a map from caller-supplied coordinates, without sample data."""
    required = {latitude_column, longitude_column}
    missing = required.difference(records.columns)
    if missing:
        raise ValueError(f"Missing coordinate columns: {', '.join(sorted(missing))}")

    return px.scatter_map(
        records,
        lat=latitude_column,
        lon=longitude_column,
        zoom=1,
    )
