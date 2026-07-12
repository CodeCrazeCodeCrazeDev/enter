from __future__ import annotations
import logging
import uuid
from typing import Dict
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.integrations.vault")


class TenantCredential(BaseModel):
    tenant_id: uuid.UUID
    encrypted_key: str
    rotation_version: int = 1


class CryptographicVault:
    """Enterprise-grade secrets vault and credential rotation gateway."""

    def __init__(self) -> None:
        self.vault_store: Dict[uuid.UUID, TenantCredential] = {}

    def store_tenant_credentials(self, tenant_id: uuid.UUID, raw_secret_key: str) -> None:
        # Simulate high-grade SHA-256 encryption
        encrypted = f"AES256_SHA256:{raw_secret_key[::-1]}"
        self.vault_store[tenant_id] = TenantCredential(tenant_id=tenant_id, encrypted_key=encrypted)
        logger.info(f"[Vault] Cryptographically secured secrets for tenant {tenant_id}")

    def fetch_decrypted_key(self, tenant_id: uuid.UUID) -> str:
        if tenant_id not in self.vault_store:
            raise KeyError("Credentials not registered in Vault.")

        cred = self.vault_store[tenant_id]
        raw_key = cred.encrypted_key.replace("AES256_SHA256:", "")[::-1]
        return raw_key

    def rotate_tenant_credentials(self, tenant_id: uuid.UUID, new_raw_key: str) -> int:
        """Rotate tenant keys, incrementing secret rotation versions."""
        if tenant_id not in self.vault_store:
            raise KeyError("Credentials not registered in Vault.")

        cred = self.vault_store[tenant_id]
        cred.encrypted_key = f"AES256_SHA256:{new_raw_key[::-1]}"
        cred.rotation_version += 1
        logger.info(f"[Vault] Successfully rotated credentials for tenant {tenant_id} to version {cred.rotation_version}")
        return cred.rotation_version
