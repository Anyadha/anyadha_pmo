"""Production-safe data quality helpers for PMO records."""
from __future__ import annotations

from typing import Iterable


def missing_required_values(doc, fieldnames: Iterable[str]) -> list[str]:
    """Return required fieldnames that are empty on a document."""
    return [field for field in fieldnames if not doc.get(field)]


def non_negative_issues(doc, fieldnames: Iterable[str]) -> list[str]:
    """Return numeric fieldnames containing negative values."""
    issues = []
    for field in fieldnames:
        value = doc.get(field)
        if value is not None and value != "" and float(value) < 0:
            issues.append(field)
    return issues
