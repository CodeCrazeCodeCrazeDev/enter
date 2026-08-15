# ADR 008: Phase 1 Substrate Hardening & Core Reliability

## Status
Approved

## Context
Evolving toward a production-ready Autonomous Entrepreneurial Operating System (AEOS) requires a bulletproof, reliable, and thread-safe underlying substrate.
The current baseline implementation suffers from three critical vulnerabilities:
1. **SQLite Database Locks:** `SQLiteMemoryRepository` uses a single shared connection (`self._connection`) if in-memory, or opens new connections that are susceptible to multi-thread access errors (`sqlite3.ProgrammingError`) and database write-locks (`sqlite3.OperationalError: database is locked`) when multiple asynchronous agents write to semantic memory/KOS concurrently.
2. **In-Memory Trajectory Bloat:** `AReaLDataProxy` keeps all step traces in an in-memory dictionary. Under long-horizon execution and multi-loop trials, this leads to memory exhaustion and makes it impossible to retrieve trajectory histories across system restarts.
3. **Runaway Token Consumption:** The system relies on post-hoc rollback checks rather than active, real-time resource caps at the execution loop boundary, exposing the organization to unbounded API cost risk.

These vulnerabilities represent a critical bottleneck on our path toward AEOS hierarchical federated control, parallel candidate evaluations, and market-based bidding.

## Decision
We decide to execute **Phase 1: Substrate Hardening & Core Reliability** as the immediate, highest engineering ROI path.

Specifically, we will implement:
1. **Thread-Safe SQLite Repository Wrapper:**
   - Upgrade the internal connection management inside `SQLiteMemoryRepository` to use explicit re-entrant thread-locks for database write and read access.
   - Configure SQLite to use **Write-Ahead Logging (WAL)** mode (`PRAGMA journal_mode=WAL;`) and **NORMAL** synchronous commits (`PRAGMA synchronous=NORMAL;`), which dramatically improves concurrent read/write throughput and eliminates write-locks.
2. **Persistent SQL Trajectory Schema:**
   - Define a formal, indexed database table for trajectory step recordings inside a central database.
   - Refactor `AReaLDataProxy` to read and write traces directly to this persistent relational database instead of holding them in RAM.
3. **Active Resource Limits & Hard Caps:**
   - Integrate hard limits on token usage and latency directly within the core execution loops to act as real-time, non-bypassable circuit breakers.

## Alternatives Considered
- **Postgres/MySQL Database Migration:** Replaced in favor of WAL-enabled SQLite because SQLite offers zero-configuration, local-first offline compatibility, and maintains backward compatibility with the existing test runner.
- **AsyncIO Connection Pools (aiosqlite):** Replaced in favor of synchronous re-entrant thread-locks because a significant portion of the active database consumer code is synchronous, and a multi-threaded lock-guaranteed synchronous wrapper prevents breaking backward compatibility with existing synchronous test suites.

## Consequences
- **Pros:**
  - Prevents all multi-agent thread crashes and lock timeouts.
  - Keeps system memory completely flat during high-frequency, long-horizon trials.
  - Protects development and production budgets from runaway agent loops.
  - Completely backward compatible with all existing tests.
- **Cons:**
  - Synchronous thread-locking introduces minimal serialization latency, which is mitigated by fast WAL-mode throughput.
