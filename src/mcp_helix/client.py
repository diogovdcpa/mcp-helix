from __future__ import annotations

from typing import Any

import httpx

from .auth import TokenCache, extract_tenant_id, fetch_access_token, fetch_customer_id
from .config import Settings, get_settings


class HelixClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._token_cache = TokenCache()
        self._customer_id_cache: dict[str, str] = {}

    def _resolve_credentials(
        self,
        *,
        client_id: str | None,
        client_secret: str | None,
        api_key: str | None,
        token_endpoint: str | None,
        api_base_url: str | None,
    ) -> dict[str, str]:
        resolved = {
            "client_id": (client_id or self.settings.client_id).strip(),
            "client_secret": (client_secret or self.settings.client_secret).strip(),
            "api_key": (api_key or self.settings.api_key).strip(),
            "token_endpoint": (token_endpoint or self.settings.token_endpoint).strip(),
            "api_base_url": (api_base_url or self.settings.api_base_url).strip().rstrip("/"),
        }
        missing = [key for key, value in resolved.items() if not value]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        return resolved

    async def _get_access_context(
        self,
        *,
        client_id: str,
        client_secret: str,
        api_key: str,
        token_endpoint: str,
        api_base_url: str,
        customer_id: str | None,
        scope: str,
    ) -> tuple[str, str | None, str]:
        cache_key = f"{client_id}:{token_endpoint}:{scope}"
        bundle = self._token_cache.get(cache_key)

        async with httpx.AsyncClient(timeout=self.settings.timeout_seconds) as http:
            if not bundle:
                token_payload = await fetch_access_token(
                    client=http,
                    client_id=client_id,
                    client_secret=client_secret,
                    token_endpoint=token_endpoint,
                    scope=scope,
                )
                access_token = str(token_payload["access_token"])
                tenant_id = extract_tenant_id(access_token)
                self._token_cache.set(
                    cache_key,
                    access_token,
                    int(token_payload.get("expires_in", 3600)),
                    tenant_id,
                )
                bundle = self._token_cache.get(cache_key)
                if not bundle:
                    raise RuntimeError("Token cache failed to store access token")

            resolved_customer_id = customer_id
            if not resolved_customer_id:
                customer_key = f"{client_id}:{bundle.tenant_id or ''}:{api_base_url}"
                resolved_customer_id = self._customer_id_cache.get(customer_key)
                if not resolved_customer_id:
                    resolved_customer_id = await fetch_customer_id(
                        client=http,
                        api_base_url=api_base_url,
                        api_key=api_key,
                        access_token=bundle.access_token,
                        tenant_id=bundle.tenant_id,
                    )
                    self._customer_id_cache[customer_key] = resolved_customer_id

        return bundle.access_token, bundle.tenant_id, resolved_customer_id

    async def request(
        self,
        *,
        method: str,
        endpoint: str,
        customer_id: str | None = None,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | list[Any] | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        api_key: str | None = None,
        token_endpoint: str | None = None,
        api_base_url: str | None = None,
        scope: str = "xdr.alr.r",
        raw_path: bool = False,
    ) -> dict[str, Any]:
        creds = self._resolve_credentials(
            client_id=client_id,
            client_secret=client_secret,
            api_key=api_key,
            token_endpoint=token_endpoint,
            api_base_url=api_base_url,
        )
        access_token, tenant_id, resolved_customer_id = await self._get_access_context(
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            api_key=creds["api_key"],
            token_endpoint=creds["token_endpoint"],
            api_base_url=creds["api_base_url"],
            customer_id=customer_id,
            scope=scope,
        )

        headers = {
            "X-FeApi-Token": creds["api_key"],
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if tenant_id:
            headers["x-tenant-id"] = tenant_id

        clean_endpoint = endpoint if raw_path else endpoint.lstrip("/")
        if raw_path:
            url = f"{creds['api_base_url']}/{clean_endpoint.lstrip('/')}"
        else:
            url = (
                f"{creds['api_base_url']}/helix/id/"
                f"{resolved_customer_id}/{clean_endpoint}"
            )

        async with httpx.AsyncClient(timeout=self.settings.timeout_seconds) as http:
            response = await http.request(
                method.upper(),
                url,
                headers=headers,
                params=params,
                json=body,
            )
            response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return {"status": "success", "status_code": response.status_code}

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        return {
            "status": "success",
            "status_code": response.status_code,
            "content_type": content_type,
            "text": response.text,
        }

    @staticmethod
    def _list_params(**kwargs: Any) -> dict[str, Any] | None:
        params = {key: value for key, value in kwargs.items() if value is not None}
        return params or None

    async def get_environment(self, **kwargs: Any) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="helix/api/v1/environment/",
            raw_path=True,
            **kwargs,
        )

    async def list_alerts(
        self,
        *,
        customer_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
        sort: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v1/alerts/",
            customer_id=customer_id,
            params=self._list_params(
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
                fields=fields,
                includes=includes,
            ),
            **kwargs,
        )

    async def get_alert(self, *, alert_id: str, customer_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint=f"api/v1/alerts/{alert_id}/",
            customer_id=customer_id,
            **kwargs,
        )

    async def list_incidents(
        self,
        *,
        customer_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
        sort: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v1/incidents/",
            customer_id=customer_id,
            params=self._list_params(
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
                fields=fields,
                includes=includes,
            ),
            **kwargs,
        )

    async def get_incident(
        self,
        *,
        incident_id: str,
        customer_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint=f"api/v1/incidents/{incident_id}/",
            customer_id=customer_id,
            **kwargs,
        )

    async def list_events(
        self,
        *,
        customer_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
        sort: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v1/events/",
            customer_id=customer_id,
            params=self._list_params(
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
                fields=fields,
                includes=includes,
            ),
            **kwargs,
        )

    async def get_event(
        self,
        *,
        event_id: str,
        customer_id: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint=f"api/v1/events/{event_id}/",
            customer_id=customer_id,
            params=self._list_params(fields=fields, includes=includes),
            **kwargs,
        )

    async def list_indicators(
        self,
        *,
        customer_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
        sort: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v1/indicators/",
            customer_id=customer_id,
            params=self._list_params(
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
                fields=fields,
                includes=includes,
            ),
            **kwargs,
        )

    async def get_indicator(
        self,
        *,
        indicator_id: str,
        customer_id: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint=f"api/v1/indicators/{indicator_id}/",
            customer_id=customer_id,
            params=self._list_params(fields=fields, includes=includes),
            **kwargs,
        )

    async def list_cases(
        self,
        *,
        customer_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
        sort: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v3/cases/",
            customer_id=customer_id,
            params=self._list_params(
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
                fields=fields,
                includes=includes,
            ),
            **kwargs,
        )

    async def get_case(
        self,
        *,
        case_id: str,
        customer_id: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint=f"api/v3/cases/{case_id}/",
            customer_id=customer_id,
            params=self._list_params(fields=fields, includes=includes),
            **kwargs,
        )

    async def create_case(
        self,
        *,
        case_data: dict[str, Any],
        customer_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="POST",
            endpoint="api/v3/cases/",
            customer_id=customer_id,
            body=case_data,
            **kwargs,
        )

    async def list_detections(
        self,
        *,
        customer_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
        sort: str | None = None,
        fields: str | None = None,
        includes: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v3/detections/",
            customer_id=customer_id,
            params=self._list_params(
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
                fields=fields,
                includes=includes,
            ),
            **kwargs,
        )

    async def get_users(self, *, customer_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v1/users/",
            customer_id=customer_id,
            **kwargs,
        )

    async def list_users(
        self,
        *,
        customer_id: str | None = None,
        id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v3/users/",
            customer_id=customer_id,
            params=self._list_params(id=id, limit=limit, offset=offset),
            **kwargs,
        )

    async def get_tags(self, *, customer_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v3/tags/",
            customer_id=customer_id,
            **kwargs,
        )

    async def get_stats(self, *, customer_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        return await self.request(
            method="GET",
            endpoint="api/v1/stats/",
            customer_id=customer_id,
            **kwargs,
        )
