"""Similarity comparison interfaces; no score or ranking method is defined."""


def compare_terrains(*args: object, **kwargs: object) -> None:
    """Placeholder for a future transparent analog-comparison method.

    A comparison method must be documented and validated before producing
    scores or rankings. This function intentionally produces neither.
    """
    raise NotImplementedError(
        "Terrain similarity is under development; no scoring method is defined."
    )
