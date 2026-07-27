"""Deterministic identity generation for AI-EOS.

Ensures that experiment UUIDs, venture cell namespaces, and signatures are reproducible
and traceable across walk-forward testing.
"""

from __future__ import annotations
import hashlib
import uuid


class DeterministicIdentityGenerator:
    """Utility for generating deterministic and traceable UUIDs and hashes."""

    @staticmethod
    def generate_uuid_from_seed(seed_string: str) -> uuid.UUID:
        """Generate a deterministic UUID v5 from a seed string namespace."""
        dns_namespace = uuid.NAMESPACE_DNS
        return uuid.uuid5(dns_namespace, seed_string)

    @staticmethod
    def compute_sha256(payload: str) -> str:
        """Compute the SHA-256 hash of a string payload."""
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
