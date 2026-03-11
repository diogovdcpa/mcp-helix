from __future__ import annotations

from dataclasses import dataclass
from inspect import Parameter, Signature
from typing import Any, Callable

from fastmcp import FastMCP

from .client import HelixClient


@dataclass(frozen=True)
class ToolSpec:
    name: str
    method: str
    endpoint_template: str
    path_params: tuple[str, ...] = ()
    raw_path: bool = False


COMMON_SIGNATURE_PARAMS = (
    Parameter("customer_id", Parameter.POSITIONAL_OR_KEYWORD, default=None, annotation=str | None),
    Parameter("params", Parameter.POSITIONAL_OR_KEYWORD, default=None, annotation=dict[str, Any] | None),
    Parameter(
        "payload",
        Parameter.POSITIONAL_OR_KEYWORD,
        default=None,
        annotation=dict[str, Any] | list[Any] | None,
    ),
    Parameter("base_url", Parameter.POSITIONAL_OR_KEYWORD, default="", annotation=str),
    Parameter("client_id", Parameter.POSITIONAL_OR_KEYWORD, default="", annotation=str),
    Parameter("client_secret", Parameter.POSITIONAL_OR_KEYWORD, default="", annotation=str),
    Parameter("api_key", Parameter.POSITIONAL_OR_KEYWORD, default="", annotation=str),
    Parameter("token_endpoint", Parameter.POSITIONAL_OR_KEYWORD, default="", annotation=str),
    Parameter("scope", Parameter.POSITIONAL_OR_KEYWORD, default="xdr.alr.r", annotation=str),
)


GENERATED_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec(name="get_alert_v3", method="GET", endpoint_template="/api/v3/alerts/{alert_id}", path_params=("alert_id",)),
    ToolSpec(name="suppress_alerts", method="POST", endpoint_template="/api/v1/alerts/suppress"),
    ToolSpec(name="unsuppress_alerts", method="POST", endpoint_template="/api/v1/alerts/unsuppress"),
    ToolSpec(name="get_alert_overview", method="GET", endpoint_template="/api/v1/alerts/overview/"),
    ToolSpec(name="get_alert_stats", method="GET", endpoint_template="/api/v1/alertStats/"),
    ToolSpec(name="get_alert_types", method="GET", endpoint_template="/api/v1/alertTypes/"),
    ToolSpec(name="list_alert_suppressions", method="GET", endpoint_template="/api/v1/alertSuppressions/"),
    ToolSpec(name="create_alert_suppression", method="POST", endpoint_template="/api/v1/alertSuppressions/"),
    ToolSpec(
        name="delete_alert_suppression",
        method="DELETE",
        endpoint_template="/api/v1/alertSuppressions/{suppression_id}/",
        path_params=("suppression_id",),
    ),
    ToolSpec(name="list_white_lists", method="GET", endpoint_template="/api/v1/whiteLists/"),
    ToolSpec(name="create_white_list", method="POST", endpoint_template="/api/v1/whiteLists/"),
    ToolSpec(name="get_white_list", method="GET", endpoint_template="/api/v1/whiteLists/{whitelist_id}/", path_params=("whitelist_id",)),
    ToolSpec(name="update_white_list", method="PUT", endpoint_template="/api/v1/whiteLists/{whitelist_id}/", path_params=("whitelist_id",)),
    ToolSpec(name="delete_white_list", method="DELETE", endpoint_template="/api/v1/whiteLists/{whitelist_id}/", path_params=("whitelist_id",)),
    ToolSpec(name="create_search", method="POST", endpoint_template="/api/v1/search/"),
    ToolSpec(name="get_search_archive", method="GET", endpoint_template="/api/v1/search/archive/{search_id}", path_params=("search_id",)),
    ToolSpec(
        name="get_search_archive_results",
        method="GET",
        endpoint_template="/api/v1/search/archive/{search_id}/results",
        path_params=("search_id",),
    ),
    ToolSpec(
        name="cancel_search_archive",
        method="POST",
        endpoint_template="/api/v1/search/archive/{search_id}/cancel",
        path_params=("search_id",),
    ),
    ToolSpec(name="get_search_fields", method="GET", endpoint_template="/api/v1/search/fields/"),
    ToolSpec(
        name="get_authorized_users",
        method="GET",
        endpoint_template="/api/v1/{model_name}/authorized/users/",
        path_params=("model_name",),
    ),
    ToolSpec(name="get_api_schema", method="GET", endpoint_template="/api/schema/", raw_path=True),
    ToolSpec(name="get_analytics_modules", method="GET", endpoint_template="/api/v1/analytics/modules/"),
    ToolSpec(name="get_analytics_trainings", method="GET", endpoint_template="/api/v1/analytics/trainings/"),
    ToolSpec(name="update_analytics_trainings_flag", method="PUT", endpoint_template="/api/v1/analytics/trainings/flag/"),
    ToolSpec(
        name="create_incident_from_alert",
        method="POST",
        endpoint_template="/api/v1/createIncidentFromAlert/{alert_id}/",
        path_params=("alert_id",),
    ),
    ToolSpec(name="list_export_alerts", method="GET", endpoint_template="/api/v1/export/alerts/"),
    ToolSpec(name="delete_export_alerts", method="DELETE", endpoint_template="/api/v1/export/alerts/"),
    ToolSpec(name="list_export_incidents", method="GET", endpoint_template="/api/v1/export/incidents/"),
    ToolSpec(name="delete_export_incidents", method="DELETE", endpoint_template="/api/v1/export/incidents/"),
    ToolSpec(name="get_export_incident", method="GET", endpoint_template="/api/v1/export/incidents/{export_id}/", path_params=("export_id",)),
    ToolSpec(name="delete_export_incident", method="DELETE", endpoint_template="/api/v1/export/incidents/{export_id}/", path_params=("export_id",)),
    ToolSpec(name="list_export_indicators", method="GET", endpoint_template="/api/v1/export/indicators/"),
    ToolSpec(name="get_export_indicator", method="GET", endpoint_template="/api/v1/export/indicators/{export_id}/", path_params=("export_id",)),
    ToolSpec(name="get_export_rule", method="GET", endpoint_template="/api/v1/exportRule/"),
    ToolSpec(name="list_export_rule_packs", method="GET", endpoint_template="/api/v1/exportRulePack/"),
    ToolSpec(name="create_export_rule_pack", method="POST", endpoint_template="/api/v1/exportRulePack/"),
    ToolSpec(name="get_export_rule_pack", method="GET", endpoint_template="/api/v1/exportRulePack/{rule_pack_id}/", path_params=("rule_pack_id",)),
    ToolSpec(name="list_export_search_lists", method="GET", endpoint_template="/api/v1/exportSearchList/"),
    ToolSpec(name="create_export_search_list", method="POST", endpoint_template="/api/v1/exportSearchList/"),
    ToolSpec(name="delete_export_search_list", method="DELETE", endpoint_template="/api/v1/exportSearchList/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="get_export_search_list", method="GET", endpoint_template="/api/v1/exportSearchList/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="update_export_search_list", method="PUT", endpoint_template="/api/v1/exportSearchList/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="get_file_analysis", method="GET", endpoint_template="/api/v1/file-analysis/{file_id}/", path_params=("file_id",)),
    ToolSpec(name="import_rule", method="POST", endpoint_template="/api/v1/import/rule/"),
    ToolSpec(name="import_rule_pack", method="POST", endpoint_template="/api/v1/importRulePack/"),
    ToolSpec(name="import_rule_pack_from_org", method="POST", endpoint_template="/api/v1/importRulePackFromOrg/"),
    ToolSpec(name="import_rule_packs", method="POST", endpoint_template="/api/v1/importRulePacks/"),
    ToolSpec(name="list_import_search_lists", method="GET", endpoint_template="/api/v1/importSearchList/"),
    ToolSpec(name="create_import_search_list", method="POST", endpoint_template="/api/v1/importSearchList/"),
    ToolSpec(name="delete_import_search_list", method="DELETE", endpoint_template="/api/v1/importSearchList/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="get_import_search_list", method="GET", endpoint_template="/api/v1/importSearchList/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="update_import_search_list", method="PUT", endpoint_template="/api/v1/importSearchList/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="get_incident_stats", method="GET", endpoint_template="/api/v1/incidentStats/"),
    ToolSpec(name="list_notices", method="GET", endpoint_template="/api/v1/notices/"),
    ToolSpec(name="create_notice", method="POST", endpoint_template="/api/v1/notices/"),
    ToolSpec(name="delete_notice", method="DELETE", endpoint_template="/api/v1/notices/{notice_id}/", path_params=("notice_id",)),
    ToolSpec(name="get_notice", method="GET", endpoint_template="/api/v1/notices/{notice_id}/", path_params=("notice_id",)),
    ToolSpec(name="update_notice", method="PUT", endpoint_template="/api/v1/notices/{notice_id}/", path_params=("notice_id",)),
    ToolSpec(name="list_pcap_jobs", method="GET", endpoint_template="/api/v1/pcap/jobs/"),
    ToolSpec(name="create_pcap_job", method="POST", endpoint_template="/api/v1/pcap/jobs/"),
    ToolSpec(name="delete_pcap_job", method="DELETE", endpoint_template="/api/v1/pcap/jobs/{job_id}/", path_params=("job_id",)),
    ToolSpec(name="get_pcap_job", method="GET", endpoint_template="/api/v1/pcap/jobs/{job_id}/", path_params=("job_id",)),
    ToolSpec(name="update_pcap_job", method="PUT", endpoint_template="/api/v1/pcap/jobs/{job_id}/", path_params=("job_id",)),
    ToolSpec(name="get_pcap_job_export", method="GET", endpoint_template="/api/v1/pcap/jobs/{job_id}/export/", path_params=("job_id",)),
    ToolSpec(name="get_pcap_job_transcript", method="GET", endpoint_template="/api/v1/pcap/jobs/{job_id}/transcript/", path_params=("job_id",)),
    ToolSpec(name="list_pcap_sensors", method="GET", endpoint_template="/api/v1/pcap/sensors/"),
    ToolSpec(name="create_pcap_sensor", method="POST", endpoint_template="/api/v1/pcap/sensors/"),
    ToolSpec(name="delete_pcap_sensor", method="DELETE", endpoint_template="/api/v1/pcap/sensors/{sensor_id}/", path_params=("sensor_id",)),
    ToolSpec(name="get_pcap_sensor", method="GET", endpoint_template="/api/v1/pcap/sensors/{sensor_id}/", path_params=("sensor_id",)),
    ToolSpec(name="update_pcap_sensor", method="PUT", endpoint_template="/api/v1/pcap/sensors/{sensor_id}/", path_params=("sensor_id",)),
    ToolSpec(name="list_rule_packs", method="GET", endpoint_template="/api/v1/rulepacks/"),
    ToolSpec(name="create_rule_pack", method="POST", endpoint_template="/api/v1/rulepacks/"),
    ToolSpec(name="delete_rule_pack", method="DELETE", endpoint_template="/api/v1/rulepacks/{rule_pack_id}/", path_params=("rule_pack_id",)),
    ToolSpec(name="get_rule_pack", method="GET", endpoint_template="/api/v1/rulepacks/{rule_pack_id}/", path_params=("rule_pack_id",)),
    ToolSpec(name="update_rule_pack", method="PUT", endpoint_template="/api/v1/rulepacks/{rule_pack_id}/", path_params=("rule_pack_id",)),
    ToolSpec(name="disable_rule_pack", method="PUT", endpoint_template="/api/v1/rulepacks/{rule_pack_id}/disable/", path_params=("rule_pack_id",)),
    ToolSpec(name="enable_rule_pack", method="PUT", endpoint_template="/api/v1/rulepacks/{rule_pack_id}/enable/", path_params=("rule_pack_id",)),
    ToolSpec(name="list_rules", method="GET", endpoint_template="/api/v1/rules/"),
    ToolSpec(name="create_rule", method="POST", endpoint_template="/api/v1/rules/"),
    ToolSpec(name="delete_rule", method="DELETE", endpoint_template="/api/v1/rules/{rule_id}/", path_params=("rule_id",)),
    ToolSpec(name="get_rule", method="GET", endpoint_template="/api/v1/rules/{rule_id}/", path_params=("rule_id",)),
    ToolSpec(name="update_rule", method="PUT", endpoint_template="/api/v1/rules/{rule_id}/", path_params=("rule_id",)),
    ToolSpec(name="list_scheduled_searches", method="GET", endpoint_template="/api/v1/scheduledSearch/"),
    ToolSpec(name="create_scheduled_search", method="POST", endpoint_template="/api/v1/scheduledSearch/"),
    ToolSpec(name="delete_scheduled_search", method="DELETE", endpoint_template="/api/v1/scheduledSearch/{search_id}/", path_params=("search_id",)),
    ToolSpec(name="get_scheduled_search", method="GET", endpoint_template="/api/v1/scheduledSearch/{search_id}/", path_params=("search_id",)),
    ToolSpec(name="update_scheduled_search", method="PUT", endpoint_template="/api/v1/scheduledSearch/{search_id}/", path_params=("search_id",)),
    ToolSpec(name="list_scheduled_search_jobs", method="GET", endpoint_template="/api/v1/scheduledSearch/{search_id}/jobs/", path_params=("search_id",)),
    ToolSpec(name="create_scheduled_search_job", method="POST", endpoint_template="/api/v1/scheduledSearch/{search_id}/jobs/", path_params=("search_id",)),
    ToolSpec(name="delete_scheduled_search_job", method="DELETE", endpoint_template="/api/v1/scheduledSearch/{search_id}/jobs/{job_id}/", path_params=("search_id", "job_id")),
    ToolSpec(name="get_scheduled_search_job", method="GET", endpoint_template="/api/v1/scheduledSearch/{search_id}/jobs/{job_id}/", path_params=("search_id", "job_id")),
    ToolSpec(name="update_scheduled_search_job", method="PUT", endpoint_template="/api/v1/scheduledSearch/{search_id}/jobs/{job_id}/", path_params=("search_id", "job_id")),
    ToolSpec(name="get_search", method="GET", endpoint_template="/api/v1/search/{search_id}/", path_params=("search_id",)),
    ToolSpec(name="list_search_favorites", method="GET", endpoint_template="/api/v1/searchFavorites/"),
    ToolSpec(name="create_search_favorite", method="POST", endpoint_template="/api/v1/searchFavorites/"),
    ToolSpec(name="delete_search_favorite", method="DELETE", endpoint_template="/api/v1/searchFavorites/{favorite_id}/", path_params=("favorite_id",)),
    ToolSpec(name="get_search_favorite", method="GET", endpoint_template="/api/v1/searchFavorites/{favorite_id}/", path_params=("favorite_id",)),
    ToolSpec(name="update_search_favorite", method="PUT", endpoint_template="/api/v1/searchFavorites/{favorite_id}/", path_params=("favorite_id",)),
    ToolSpec(name="list_search_histories", method="GET", endpoint_template="/api/v1/searchHistorys/"),
    ToolSpec(name="create_search_history", method="POST", endpoint_template="/api/v1/searchHistorys/"),
    ToolSpec(name="delete_search_history", method="DELETE", endpoint_template="/api/v1/searchHistorys/{history_id}/", path_params=("history_id",)),
    ToolSpec(name="get_search_history", method="GET", endpoint_template="/api/v1/searchHistorys/{history_id}/", path_params=("history_id",)),
    ToolSpec(name="update_search_history", method="PUT", endpoint_template="/api/v1/searchHistorys/{history_id}/", path_params=("history_id",)),
    ToolSpec(name="list_search_lists", method="GET", endpoint_template="/api/v1/searchLists/"),
    ToolSpec(name="create_search_list", method="POST", endpoint_template="/api/v1/searchLists/"),
    ToolSpec(name="delete_search_list", method="DELETE", endpoint_template="/api/v1/searchLists/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="get_search_list", method="GET", endpoint_template="/api/v1/searchLists/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="update_search_list", method="PUT", endpoint_template="/api/v1/searchLists/{search_list_id}/", path_params=("search_list_id",)),
    ToolSpec(name="list_settings", method="GET", endpoint_template="/api/v1/settings/"),
    ToolSpec(name="create_setting", method="POST", endpoint_template="/api/v1/settings/"),
    ToolSpec(name="delete_setting", method="DELETE", endpoint_template="/api/v1/settings/{setting_id}/", path_params=("setting_id",)),
    ToolSpec(name="get_setting", method="GET", endpoint_template="/api/v1/settings/{setting_id}/", path_params=("setting_id",)),
    ToolSpec(name="update_setting", method="PUT", endpoint_template="/api/v1/settings/{setting_id}/", path_params=("setting_id",)),
    ToolSpec(name="list_tables", method="GET", endpoint_template="/api/v1/tables/"),
    ToolSpec(name="delete_table", method="DELETE", endpoint_template="/api/v1/tables/{table_id}/", path_params=("table_id",)),
    ToolSpec(name="get_taxonomy", method="GET", endpoint_template="/api/v1/taxonomy/"),
    ToolSpec(name="validate_mql", method="POST", endpoint_template="/api/v1/validate/mql/"),
    ToolSpec(name="list_app_devices", method="GET", endpoint_template="/api/v3/app/{app}/devices/{device_id}/", path_params=("app", "device_id")),
    ToolSpec(name="create_app_device", method="POST", endpoint_template="/api/v3/app/{app}/devices/{device_id}/", path_params=("app", "device_id")),
    ToolSpec(name="get_app_device", method="GET", endpoint_template="/api/v3/app/{app}/devices/{device_id}/{item_id}/", path_params=("app", "device_id", "item_id")),
    ToolSpec(name="update_app_device", method="PUT", endpoint_template="/api/v3/app/{app}/devices/{device_id}/{item_id}/", path_params=("app", "device_id", "item_id")),
    ToolSpec(name="delete_app_device", method="DELETE", endpoint_template="/api/v3/app/{app}/devices/{device_id}/{item_id}/delete/", path_params=("app", "device_id", "item_id")),
    ToolSpec(name="get_appliances", method="GET", endpoint_template="/api/v3/appliances/"),
    ToolSpec(name="get_appliance", method="GET", endpoint_template="/api/v3/appliances/{appliance_id}/", path_params=("appliance_id",)),
    ToolSpec(name="export_appliances", method="GET", endpoint_template="/api/v3/appliances/export/"),
    ToolSpec(name="get_appliances_health", method="GET", endpoint_template="/api/v3/appliances/health/"),
    ToolSpec(name="get_appliances_timeline", method="GET", endpoint_template="/api/v3/appliances/timeline/"),
    ToolSpec(name="list_artifact_indicator_groups", method="GET", endpoint_template="/api/v3/artifact-indicator-groups/"),
    ToolSpec(name="get_artifact_indicator_group", method="GET", endpoint_template="/api/v3/artifact-indicator-groups/{group_id}/", path_params=("group_id",)),
    ToolSpec(name="create_asset_tag", method="POST", endpoint_template="/api/v3/asset_tags/"),
    ToolSpec(name="get_asset_id", method="GET", endpoint_template="/api/v3/assetid{asset_id}/", path_params=("asset_id",)),
    ToolSpec(name="get_assets", method="GET", endpoint_template="/api/v3/assets/"),
    ToolSpec(name="get_asset", method="GET", endpoint_template="/api/v3/assets/{asset_id}/", path_params=("asset_id",)),
    ToolSpec(name="get_ast_alerts", method="GET", endpoint_template="/api/v3/ast/alerts/"),
    ToolSpec(name="create_batch_actions", method="POST", endpoint_template="/api/v3/batch/actions/"),
    ToolSpec(name="get_campaign_populate", method="GET", endpoint_template="/api/v3/campaign/populate/campaign-data/"),
    ToolSpec(name="purge_campaign_data", method="DELETE", endpoint_template="/api/v3/campaign/purge/campaign-data/"),
    ToolSpec(name="update_case", method="PUT", endpoint_template="/api/v3/cases/{case_id}/", path_params=("case_id",)),
    ToolSpec(name="delete_case", method="DELETE", endpoint_template="/api/v3/cases/{case_id}/", path_params=("case_id",)),
    ToolSpec(name="create_case_from_alert", method="POST", endpoint_template="/api/v3/alerts/{alert_id}/cases/", path_params=("alert_id",)),
    ToolSpec(name="list_correlation_groups", method="GET", endpoint_template="/api/v3/correlationgroups/"),
    ToolSpec(name="create_correlation_group", method="POST", endpoint_template="/api/v3/correlationgroups/"),
    ToolSpec(name="get_correlation_group", method="GET", endpoint_template="/api/v3/correlationgroups/{group_id}/", path_params=("group_id",)),
    ToolSpec(name="update_correlation_group", method="PUT", endpoint_template="/api/v3/correlationgroups/{group_id}/", path_params=("group_id",)),
    ToolSpec(name="list_correlations", method="GET", endpoint_template="/api/v3/correlations/"),
    ToolSpec(name="get_custom_org_settings", method="GET", endpoint_template="/api/v3/custom-organization-settings/"),
    ToolSpec(name="list_device_groups", method="GET", endpoint_template="/api/v3/device-groups/"),
    ToolSpec(name="create_device_group_action", method="POST", endpoint_template="/api/v3/device-groups/{group_id}/actions/", path_params=("group_id",)),
    ToolSpec(name="list_domains", method="GET", endpoint_template="/api/v3/domains/"),
    ToolSpec(name="get_etp", method="GET", endpoint_template="/api/v3/etp/"),
    ToolSpec(name="get_fields", method="GET", endpoint_template="/api/v3/fields/"),
    ToolSpec(name="list_group_actions", method="GET", endpoint_template="/api/v3/group-actions/"),
    ToolSpec(name="list_intel_feeds", method="GET", endpoint_template="/api/v3/intel-feeds/"),
    ToolSpec(name="get_intel_feed_status", method="GET", endpoint_template="/api/v3/intel-feeds/{feed_id}/status/", path_params=("feed_id",)),
    ToolSpec(name="get_intel_propagation", method="GET", endpoint_template="/api/v3/intel-propagation/"),
    ToolSpec(name="list_intel_signatures", method="GET", endpoint_template="/api/v3/intel-signatures/"),
    ToolSpec(name="get_intel", method="GET", endpoint_template="/api/v3/intel/{intel_id}/", path_params=("intel_id",)),
    ToolSpec(name="list_intels", method="GET", endpoint_template="/api/v3/intels/"),
    ToolSpec(name="list_lists", method="GET", endpoint_template="/api/v3/lists/"),
    ToolSpec(name="get_metrics", method="GET", endpoint_template="/api/v3/metrics/"),
    ToolSpec(name="replay_correlations", method="POST", endpoint_template="/api/v3/replay-correlations/"),
    ToolSpec(name="list_senders", method="GET", endpoint_template="/api/v3/senders/"),
    ToolSpec(name="list_sensors", method="GET", endpoint_template="/api/v3/sensors/"),
    ToolSpec(name="get_sensor", method="GET", endpoint_template="/api/v3/sensors/{sensor_id}/", path_params=("sensor_id",)),
    ToolSpec(name="get_sensors_status", method="GET", endpoint_template="/api/v3/sensors/status/"),
    ToolSpec(name="get_sources", method="GET", endpoint_template="/api/v3/sources/"),
    ToolSpec(name="get_task_status", method="GET", endpoint_template="/api/v3/tasks/status/{task_id}/", path_params=("task_id",)),
    ToolSpec(name="get_unity", method="GET", endpoint_template="/api/v3/unity/{faude_url_path}/", path_params=("faude_url_path",)),
    ToolSpec(name="create_unity", method="POST", endpoint_template="/api/v3/unity/{faude_url_path}/", path_params=("faude_url_path",)),
    ToolSpec(name="get_user_challenge_query", method="GET", endpoint_template="/api/v3/user/challenge-query/"),
    ToolSpec(name="get_user_chat", method="GET", endpoint_template="/api/v3/user/chat/"),
)


def _build_signature(spec: ToolSpec) -> Signature:
    path_parameters = [
        Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        for name in spec.path_params
    ]
    return Signature(
        parameters=[*path_parameters, *COMMON_SIGNATURE_PARAMS],
        return_annotation=dict[str, Any],
    )


def _make_tool(
    spec: ToolSpec,
    client: HelixClient,
    wrap_error: Callable[[Exception], dict[str, Any]],
) -> Callable[..., Any]:
    async def _tool(**kwargs: Any) -> dict[str, Any]:
        try:
            path_values = {name: kwargs[name] for name in spec.path_params}
            endpoint = spec.endpoint_template.format(**path_values)
            return await client.request(
                method=spec.method,
                endpoint=endpoint,
                customer_id=kwargs.get("customer_id"),
                params=kwargs.get("params"),
                body=kwargs.get("payload"),
                api_base_url=kwargs.get("base_url") or None,
                client_id=kwargs.get("client_id") or None,
                client_secret=kwargs.get("client_secret") or None,
                api_key=kwargs.get("api_key") or None,
                token_endpoint=kwargs.get("token_endpoint") or None,
                scope=kwargs.get("scope", "xdr.alr.r"),
                raw_path=spec.raw_path,
            )
        except Exception as exc:
            return wrap_error(exc)

    _tool.__name__ = spec.name
    _tool.__doc__ = (
        f"Auto-generated Trellix Helix wrapper for "
        f"{spec.method} {spec.endpoint_template}. "
        f"Use `params` for query parameters and `payload` for request bodies."
    )
    _tool.__signature__ = _build_signature(spec)
    annotations: dict[str, Any] = {
        name: str for name in spec.path_params
    }
    annotations.update(
        {
            "customer_id": str | None,
            "params": dict[str, Any] | None,
            "payload": dict[str, Any] | list[Any] | None,
            "base_url": str,
            "client_id": str,
            "client_secret": str,
            "api_key": str,
            "token_endpoint": str,
            "scope": str,
            "return": dict[str, Any],
        }
    )
    _tool.__annotations__ = annotations
    return _tool


def register_generated_tools(
    mcp: FastMCP,
    client: HelixClient,
    wrap_error: Callable[[Exception], dict[str, Any]],
) -> None:
    for spec in GENERATED_SPECS:
        mcp.tool()(_make_tool(spec, client, wrap_error))
