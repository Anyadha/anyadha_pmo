"""Common KPI/KRI/KCI metric calculations for the PMO reporting layer."""

from __future__ import annotations


def achievement_percent(actual: float | None, target: float | None, direction: str = "Higher is Better") -> float | None:
    """Return achievement percentage using the KPI's declared direction."""
    if actual is None or target in (None, 0):
        return None
    actual = float(actual)
    target = float(target)
    if direction == "Lower is Better":
        if actual == 0:
            return 100.0
        return round((target / actual) * 100, 2)
    return round((actual / target) * 100, 2)


def threshold_status(current: float | None, threshold: float | None, direction: str = "Higher is Worse") -> str:
    """Classify a threshold metric. Missing values remain unclassified."""
    if current is None or threshold is None:
        return "Amber"
    current, threshold = float(current), float(threshold)
    if direction == "Lower is Worse":
        return "Red" if current <= threshold else "Green"
    return "Red" if current >= threshold else "Green"
