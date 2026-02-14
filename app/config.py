"""Central configuration for JWT Playground scenarios.

This keeps lab secrets and algorithm choices in one place so they can be
reasoned about and (if needed) overridden more easily.

Nothing in here is suitable for production use – it is intentionally
simplified for teaching.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JwtConfig:
    secret: str
    algorithm: str
    lifetime_seconds: int


LAB_JWT = JwtConfig(
    secret="jwt-playground-secret",
    algorithm="HS256",
    lifetime_seconds=600,
)

INSECURE_JWT = JwtConfig(
    secret="do-not-use-this-in-production",
    algorithm="HS256",
    lifetime_seconds=600,
)
