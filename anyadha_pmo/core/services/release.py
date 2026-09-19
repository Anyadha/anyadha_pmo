"""Release and deployment metadata helpers.

These helpers intentionally contain no database mutation. Deployment remains
an explicit operator action through the normal Frappe migration process.
"""
from __future__ import annotations

APP_NAME = "anyadha_pmo"
RELEASE_LINE = "2.1.x"
WAVE = "Wave 7 - Enterprise Hardening & Production Readiness"


def release_metadata() -> dict[str, str]:
    return {"app": APP_NAME, "release_line": RELEASE_LINE, "wave": WAVE}
