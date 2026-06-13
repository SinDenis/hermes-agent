from hermes_cli.tools_config import _get_platform_tools
from toolsets import CORP_DANGEROUS_TOOLSETS, resolve_toolset

# Individual tool names that must never reach a Time session.
DANGEROUS = {"terminal", "process", "write_file", "patch",
             "execute_code", "computer_use", "browser_navigate",
             "ha_call_service", "delegate_task", "kanban_create"}

def test_time_platform_strips_dangerous_even_if_misconfigured():
    # Even if an admin wrongly grants the coding toolset to Time:
    config = {"platform_toolsets": {"time": ["coding"]}}
    tools = _get_platform_tools(config, "time")
    leaked = tools & DANGEROUS
    assert not leaked, f"Time leaked dangerous tools: {leaked}"
    # Also no dangerous toolset NAMES survive:
    assert not (tools & set(CORP_DANGEROUS_TOOLSETS))

def test_time_keeps_safe_tools_when_corp_safe_configured():
    config = {"platform_toolsets": {"time": ["corp_safe"]}}
    tools = _get_platform_tools(config, "time")
    # _get_platform_tools returns a mix of toolset NAMES and individual tool
    # names. For a composite like corp_safe, the safe toolset keys are
    # recovered by the reverse-mapping loop, so "web" (not "web_search") and
    # "memory" are the expected values in the returned set.
    assert "web" in tools  # web toolset key (web_search + web_extract)
    assert "memory" in tools
    assert not (tools & DANGEROUS)

def test_non_time_platform_unaffected():
    # The hard-deny is Time-only: a non-restricted platform with the same
    # config still gets terminal.
    config = {"platform_toolsets": {"slack": ["coding"]}}
    tools = _get_platform_tools(config, "slack")
    assert "terminal" in tools, "non-time platform must NOT be hard-denied"
