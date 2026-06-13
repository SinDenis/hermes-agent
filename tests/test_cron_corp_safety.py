from cron.scheduler import _resolve_cron_disabled_toolsets
from toolsets import CORP_DANGEROUS_TOOLSETS

def test_cron_denylist_contains_all_dangerous_toolsets():
    disabled = set(_resolve_cron_disabled_toolsets({}))
    missing = set(CORP_DANGEROUS_TOOLSETS) - disabled
    assert not missing, f"cron denylist missing dangerous toolsets: {missing}"
    # plus the always-disabled interactive/recursive ones
    assert {"cronjob", "messaging", "clarify"} <= disabled

def test_cron_denylist_layers_user_disabled():
    disabled = set(_resolve_cron_disabled_toolsets({"agent": {"disabled_toolsets": ["spotify"]}}))
    assert "spotify" in disabled
    assert "terminal" in disabled  # corp dangerous still present
