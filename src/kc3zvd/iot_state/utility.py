from __future__ import annotations


def normalize(content: str) -> str:
    return content.lower().replace(" ", "_")