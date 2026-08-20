from __future__ import annotations

from typing import Protocol


class Translator(Protocol):
    """Interface for any model that proposes a CIR object from source text."""

    def translate(self, source_text: str, *, seed: int | None = None) -> dict:
        ...
