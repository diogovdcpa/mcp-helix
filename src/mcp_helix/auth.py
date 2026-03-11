from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Any

import httpx
import jwt


@dataclass
class TokenBundle:
    access_token: str
    tenant_id: str | None
    expires_at: float

    @property
    def is_valid(self) -> bool:
        return time.time() < self.expires_at


class TokenCache:
    def __init__(self) -> None:
        self._cache: dict[str, TokenBundle] = {}

    def get(self, key: str) -> TokenBundle | None:
        bundle = self._cache.get(key)
        if bundle and bundle.is_valid:
            return bundle
        if bundle:
            self._cache.pop(key, None)
        return None

    def set(self, key: str, access_token: str, expires_in: int, tenant_id: str | None) -> None:
        self._cache[key] = TokenBundle(
            access_token=access_token,
            tenant_id=tenant_id,
            expires_at=time.time() + max(expires_in - 300, 60),
        )


def extract_tenant_id(access_token: str) -> str | None:
    payload = jwt.decode(access_token, options={"verify_signature": False})
    tenant_id = payload.get("tenant_id") or payload.get("tenantId") or payload.get("tenant")
    return str(tenant_id) if tenant_id else None


async def fetch_access_token(
    *,
    client: httpx.AsyncClient,
    client_id: str,
    client_secret: str,
    token_endpoint: str,
    scope: str = "xdr.alr.r",
) -> dict[str, Any]:
    raw = f"{client_id}:{client_secret}".encode()
    auth_header = base64.b64encode(raw).decode()
    response = await client.post(
        token_endpoint,
        data={"grant_type": "client_credentials", "scope": scope},
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    response.raise_for_status()
    payload = response.json()
    if "access_token" not in payload:
        raise ValueError(f"Token response missing access_token: {payload}")
    return payload


async def fetch_customer_id(
    *,
    client: httpx.AsyncClient,
    api_base_url: str,
    api_key: str,
    access_token: str,
    tenant_id: str | None,
) -> str:
    headers = {
        "X-FeApi-Token": api_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    if tenant_id:
        headers["x-tenant-id"] = tenant_id

    response = await client.get(
        f"{api_base_url.rstrip('/')}/helix/api/v1/environment/",
        headers=headers,
    )
    response.raise_for_status()
    payload = response.json()

    customer_id = payload.get("environment", {}).get("customer_id")
    if not customer_id:
        raise ValueError(f"Could not discover customer_id from environment response: {payload}")
    return str(customer_id)
