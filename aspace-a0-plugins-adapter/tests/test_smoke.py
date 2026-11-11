"""Smoke tests de l'adapter a0-plugins (D-N053 pas B).

Roules avec le venv du pas : `python -m pytest aspace-a0-plugins-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel reseau. La validation YAML
complete de l'index est celle de la suite amont
(scripts/test_index_release.py) ; le smoke verifie les constantes, les
comptages mesures par l'adapter et la coherence H-B6.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_a0_plugins_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:a0-plugins"
    assert adapter.LICENSE == "MIT"
    assert adapter.FORK == "Amdkn/a0-plugins"
    assert adapter.UPSTREAM_REPO == "agent0ai/a0-plugins"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "f73f767d0482accdf5b2ec53d137f916c22df3c9"


def test_validate_counts():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["plugin_dirs_total"] == 235
    assert v["plugin_names_resolved"] == 232
    assert v["indexed_plugins"] == 230
    assert v["index_yaml_present"] == 233
    assert v["legacy_plugin_yaml_only"] == ["a0-llmfallback", "agent0-terminal"]
    assert v["blocked_plugins"] == ["codex_provider", "discord"]
    assert v["generated_thumbnails"] == 87
    assert v["orphan_thumbnails"] == ["chat_organizer", "d2_audio"]
    assert v["local_thumbnails"] == 155
    assert v["plugins_without_any_thumbnail"] == []
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_validate_integrity():
    v = adapter.validate()
    assert v["index_yaml_invalid"] == []
    assert v["index_yaml_missing_keys"] == {}
    assert v["max_screenshots"] <= 5
    assert v["index_coherent"] is True


def test_triage_agent_zero_coherent():
    v = adapter.validate()
    assert v["abandoned_present"] == []
    assert v["surfaces_present"] == []


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp"):
        assert banned not in src, banned


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:a0-plugins"
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "MIT"
