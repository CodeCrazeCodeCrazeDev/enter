"""Shared text-processing helpers."""

from __future__ import annotations

_BRACKET_PAIRS = {")": "(", "}": "{", "]": "["}


def is_balanced_brackets(text: str) -> bool:
    """Return ``True`` if all round/curly/square brackets in ``text`` are balanced.

    A string is balanced when every closing bracket matches the most recently
    opened bracket of the same kind and no bracket is left unclosed.
    """
    stack: list[str] = []
    for char in text:
        if char in _BRACKET_PAIRS.values():
            stack.append(char)
        elif char in _BRACKET_PAIRS:
            if not stack or stack[-1] != _BRACKET_PAIRS[char]:
                return False
            stack.pop()
    return not stack
