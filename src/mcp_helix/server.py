from __future__ import annotations

import logging
from typing import Any

from fastmcp import FastMCP

from .client import HelixClient
from .config import configure_logging
from .generated_tools import register_generated_tools


configure_logging()
logger = logging.getLogger(__name__)
client = HelixClient()
mcp = FastMCP("mcp-helix")


def _wrap_error(exc: Exception) -> dict[str, Any]:
    logger.exception("Tool execution failed")
    return {"status": "error", "error": str(exc)}


@mcp.tool()
async def get_environment(
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Return tenant environment details and resolve the active customer_id when needed."""
    try:
        return await client.get_environment(
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_alerts(
    customer_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    query: str | None = None,
    sort: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List alerts with optional filtering and pagination."""
    try:
        return await client.list_alerts(
            customer_id=customer_id,
            limit=limit,
            offset=offset,
            query=query,
            sort=sort,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_alert(
    alert_id: str,
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch a single alert by ID."""
    try:
        return await client.get_alert(
            alert_id=alert_id,
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_incidents(
    customer_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    query: str | None = None,
    sort: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List incidents with optional filtering and pagination."""
    try:
        return await client.list_incidents(
            customer_id=customer_id,
            limit=limit,
            offset=offset,
            query=query,
            sort=sort,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_incident(
    incident_id: str,
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch a single incident by ID."""
    try:
        return await client.get_incident(
            incident_id=incident_id,
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_events(
    customer_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    query: str | None = None,
    sort: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List events with optional filtering and pagination."""
    try:
        return await client.list_events(
            customer_id=customer_id,
            limit=limit,
            offset=offset,
            query=query,
            sort=sort,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_event(
    event_id: str,
    customer_id: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch a single event by ID."""
    try:
        return await client.get_event(
            event_id=event_id,
            customer_id=customer_id,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_indicators(
    customer_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    query: str | None = None,
    sort: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List indicators with optional filtering and pagination."""
    try:
        return await client.list_indicators(
            customer_id=customer_id,
            limit=limit,
            offset=offset,
            query=query,
            sort=sort,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_indicator(
    indicator_id: str,
    customer_id: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch a single indicator by ID."""
    try:
        return await client.get_indicator(
            indicator_id=indicator_id,
            customer_id=customer_id,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_cases(
    customer_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    query: str | None = None,
    sort: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List cases with optional filtering and pagination."""
    try:
        return await client.list_cases(
            customer_id=customer_id,
            limit=limit,
            offset=offset,
            query=query,
            sort=sort,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_case(
    case_id: str,
    customer_id: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch a single case by ID."""
    try:
        return await client.get_case(
            case_id=case_id,
            customer_id=customer_id,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def create_case(
    case_data: dict[str, Any],
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Create a case using the provided JSON object."""
    try:
        return await client.create_case(
            case_data=case_data,
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_detections(
    customer_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    query: str | None = None,
    sort: str | None = None,
    fields: str | None = None,
    includes: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List detections with optional filtering and pagination."""
    try:
        return await client.list_detections(
            customer_id=customer_id,
            limit=limit,
            offset=offset,
            query=query,
            sort=sort,
            fields=fields,
            includes=includes,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_users(
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch users from the v1 users endpoint."""
    try:
        return await client.get_users(
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def list_users(
    customer_id: str | None = None,
    id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """List users from the v3 users endpoint."""
    try:
        return await client.list_users(
            customer_id=customer_id,
            id=id,
            limit=limit,
            offset=offset,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_tags(
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch available tags."""
    try:
        return await client.get_tags(
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def get_stats(
    customer_id: str | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
) -> dict[str, Any]:
    """Fetch tenant statistics."""
    try:
        return await client.get_stats(
            customer_id=customer_id,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
        )
    except Exception as exc:
        return _wrap_error(exc)


@mcp.tool()
async def helix_request(
    method: str,
    endpoint: str,
    customer_id: str | None = None,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | list[Any] | None = None,
    base_url: str = "",
    client_id: str = "",
    client_secret: str = "",
    api_key: str = "",
    token_endpoint: str = "",
    scope: str = "xdr.alr.r",
    raw_path: bool = False,
) -> dict[str, Any]:
    """Execute a generic Trellix Helix API request for endpoints not yet wrapped as dedicated tools."""
    try:
        return await client.request(
            method=method,
            endpoint=endpoint,
            customer_id=customer_id,
            params=params,
            body=body,
            api_base_url=base_url or None,
            client_id=client_id or None,
            client_secret=client_secret or None,
            api_key=api_key or None,
            token_endpoint=token_endpoint or None,
            scope=scope,
            raw_path=raw_path,
        )
    except Exception as exc:
        return _wrap_error(exc)


def main() -> None:
    logger.info("Starting mcp-helix in stdio mode")
    mcp.run()


register_generated_tools(mcp, client, _wrap_error)


if __name__ == "__main__":
    main()
