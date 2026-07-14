"""Optional LLM integration with graceful, deterministic fallback.

AEAN engines call :meth:`LLMAdapter.complete` for creative text generation
(narratives, visual prompts). When an API key is configured the adapter routes
to a real provider; otherwise it falls back to a deterministic, offline
generator so the whole organism runs end-to-end with **zero external
dependencies or credentials**.

Configuration (all optional):
    AEAN_LLM_PROVIDER   one of {"openai", "anthropic", "simulation"}. Defaults
                        to auto-detection based on which API key is present.
    OPENAI_API_KEY      enables the OpenAI provider.
    ANTHROPIC_API_KEY   enables the Anthropic provider.
    AEAN_LLM_MODEL      overrides the default model name.
"""
from __future__ import annotations

import hashlib
import logging
import os
from typing import Optional

logger = logging.getLogger("aean.llm")


class LLMAdapter:
    """Routes text generation to a real provider or an offline simulator."""

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None) -> None:
        self.provider = (provider or os.getenv("AEAN_LLM_PROVIDER") or self._autodetect()).lower()
        self.model = model or os.getenv("AEAN_LLM_MODEL") or self._default_model()
        self._client = None
        if self.provider in ("openai", "anthropic"):
            self._client = self._build_client()
            if self._client is None:
                logger.warning("LLM provider %r requested but unavailable; using simulation.", self.provider)
                self.provider = "simulation"

    # ------------------------------------------------------------------
    @staticmethod
    def _autodetect() -> str:
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        if os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        return "simulation"

    def _default_model(self) -> str:
        return {
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-5-haiku-latest",
        }.get(self.provider, "simulation")

    def _build_client(self):  # pragma: no cover - exercised only with real keys
        try:
            if self.provider == "openai":
                from openai import OpenAI

                key = os.getenv("OPENAI_API_KEY")
                return OpenAI(api_key=key) if key else None
            if self.provider == "anthropic":
                import anthropic

                key = os.getenv("ANTHROPIC_API_KEY")
                return anthropic.Anthropic(api_key=key) if key else None
        except Exception as exc:  # pragma: no cover
            logger.warning("Failed to initialise %s client: %s", self.provider, exc)
        return None

    @property
    def is_live(self) -> bool:
        return self.provider in ("openai", "anthropic") and self._client is not None

    # ------------------------------------------------------------------
    def complete(self, prompt: str, *, system: str = "", max_tokens: int = 200, temperature: float = 0.7) -> str:
        """Return a completion for ``prompt``.

        Never raises on provider errors — falls back to the simulator so the
        flywheel keeps turning.
        """
        if self.is_live:
            try:
                return self._complete_live(prompt, system=system, max_tokens=max_tokens, temperature=temperature)
            except Exception as exc:  # pragma: no cover - network dependent
                logger.warning("Live LLM call failed (%s); falling back to simulation.", exc)
        return self._complete_simulation(prompt, system=system)

    def _complete_live(self, prompt: str, *, system: str, max_tokens: int, temperature: float) -> str:  # pragma: no cover
        if self.provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = self._client.chat.completions.create(
                model=self.model, messages=messages, max_tokens=max_tokens, temperature=temperature
            )
            return (resp.choices[0].message.content or "").strip()
        # anthropic
        resp = self._client.messages.create(
            model=self.model,
            system=system or None,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in resp.content if getattr(block, "type", None) == "text").strip()

    @staticmethod
    def _complete_simulation(prompt: str, *, system: str = "") -> str:
        """Deterministic offline generator.

        Produces stable, prompt-derived text so tests are reproducible while
        still feeling content-aware.
        """
        seed = hashlib.sha256((system + "|" + prompt).encode("utf-8")).hexdigest()
        tone = ["decisive", "aspirational", "urgent", "trusted", "contrarian"][int(seed[:2], 16) % 5]
        angle = ["outcome", "identity", "scarcity", "authority", "belonging"][int(seed[2:4], 16) % 5]
        # Pull the most salient token from the prompt as a subject anchor.
        words = [w.strip(".,:;\"'()").lower() for w in prompt.split() if len(w) > 4]
        subject = words[int(seed[4:6], 16) % len(words)] if words else "market"
        return f"[{tone}/{angle}] {subject.capitalize()} — {prompt.strip()[:80]}".strip()
