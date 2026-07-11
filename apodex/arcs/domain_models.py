from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Tenant(SQLModel, table=True):
    """Tenant model for absolute cryptographic separation of workspaces."""

    __tablename__: str = "arcs_tenants"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    api_key_hash: str
    status: str = "active"  # active, suspended
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Customer(SQLModel, table=True):
    """Customer model representing accounts within a tenant."""

    __tablename__: str = "arcs_customers"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(foreign_key="arcs_tenants.id")
    email: str
    kyc_status: str = "pending"  # pending, verified, rejected
    currency: str = "USD"
    balance_cents: int = 0
    status: str = "active"  # active, suspended, canceled
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Product(SQLModel, table=True):
    """Product or service offered by a tenant."""

    __tablename__: str = "arcs_products"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(foreign_key="arcs_tenants.id")
    name: str
    description: str
    pricing_type: str = "recurring"  # recurring, one_time, usage_based
    amount_cents: int
    currency: str = "USD"
    status: str = "draft"  # draft, active, retired
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Invoice(SQLModel, table=True):
    """Invoice representing billing states."""

    __tablename__: str = "arcs_invoices"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="arcs_customers.id")
    tenant_id: uuid.UUID = Field(foreign_key="arcs_tenants.id")
    amount_cents: int
    currency: str = "USD"
    status: str = "draft"  # draft, pending, paid, unpaid, suspended
    due_at: datetime
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LedgerEntry(SQLModel, table=True):
    """Double-entry ledger record for accounting validation."""

    __tablename__: str = "arcs_ledger_entries"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(foreign_key="arcs_tenants.id")
    entry_group_id: uuid.UUID = Field(default_factory=uuid.uuid4)  # groups credit and debit together
    account_code: str  # ASSETS.CASH, REVENUE.SAAS, EXPENSES.MARKETING, etc.
    debit_cents: int = 0
    credit_cents: int = 0
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
