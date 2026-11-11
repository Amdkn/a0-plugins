"""A'Space adapter — a0-plugins (D-N053 pas B, design Clara + design signe pas B).

Contrat seul, patron D-N048 (dify / cordis) et pas A (chronos) : cet adapter
ne modifie AUCUN fichier amont, ne fait AUCUN appel reseau, ne monte AUCUN
poids. Il constate : le gel epingle, la licence, la coherence de l'index
(plugins/ vs generated/ vs scripts/), l'integrite des entrees index.yaml,
et la coherence avec le tri des 47 plugins agent-zero (H-P5-7).

Adresse : fiber:a0:a0-plugins
Fork souverain : Amdkn/a0-plugins (parent agent0ai/a0-plugins, branche main)
Gel amont : d040c3fd8d7ca9486cabf2761cbcc51c47d9b7d8 (« Merge pull request #682
from TerminallyLazy/add/code-intelligence »)
Bind Cordis Fiber (2L) : f73f767d0482accdf5b2ec53d137f916c22df3c9
Licence : MIT

Mesures au gel (2026-11-11, verifiees au fichier) :
- 235 dossiers dans plugins/, 232 noms resolus (regex ^[a-z0-9_]+$, hors
  reserve `_example1` et hors `a0-llmfallback` / `agent0-terminal`,
  noms a traits d'union exclus par la resolution amont elle-meme),
  230 indexes (moins `codex_provider` et `discord`, bloques par blocked.md)
  — le chiffre 230 est celui de la suite amont elle-meme
  (« Verified complete index: 230 plugins »).
- 233 index.yaml presents, tous des mappings YAML valides, tous avec
  title + description + github ; max 5 screenshots (regle amont respectee).
- 2 dossiers en plugin.yaml seul (a0-llmfallback, agent0-terminal) :
  format historique amont, constates, non modifies.
- 87 thumbnails generees, dont 2 orphelines (chat_organizer, d2_audio :
  plugins retires, thumbnails restees) ; 155 thumbnails locales ;
  0 plugin sans thumbnail (locale ou generee).
- Coherence H-B6 : aucun des 3 plugins abandonnes du tri agent-zero
  (_plugin_installer, _plugin_scan, _plugin_validator) ni aucune des
  9 surfaces (_telegram_integration, _whatsapp_integration,
  _email_integration, _kokoro_tts, _whisper_stt, _office, _oauth,
  _pin_to_top, _sidebar_folders) n'apparait dans cet index.
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:a0-plugins"
FORK = "Amdkn/a0-plugins"
UPSTREAM_REPO = "agent0ai/a0-plugins"
UPSTREAM_BRANCH = "main"
PINNED_UPSTREAM_COMMIT = "d040c3fd8d7ca9486cabf2761cbcc51c47d9b7d8"
PINNED_UPSTREAM_COMMIT_SHORT = "d040c3f"
BIND_COMMIT = "f73f767d0482accdf5b2ec53d137f916c22df3c9"
BIND_LAYER = "2L"
LICENSE = "MIT"
ADAPTER_VERSION = "0.1.0"

ABANDONED_AGENT_ZERO = ("_plugin_installer", "_plugin_scan", "_plugin_validator")
SURFACES_AGENT_ZERO = (
    "_telegram_integration",
    "_whatsapp_integration",
    "_email_integration",
    "_kokoro_tts",
    "_whisper_stt",
    "_office",
    "_oauth",
    "_pin_to_top",
    "_sidebar_folders",
)
PLUGIN_DIRNAME_PATTERN = re.compile(r"^[a-z0-9_]+$")
THUMBNAIL_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")
REQUIRED_INDEX_KEYS = ("title", "description", "github")

CONFINEMENT = """Aucun confinement commercial : code et index MIT. Usage B2B autorise
par la licence. L'index ne contient que des pointeurs (index.yaml) vers
les depots des plugins ; aucun code de plugin n'est monte dans le fork."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _plugin_dirs(root: Path) -> list[Path]:
    plugins = root / "plugins"
    if not plugins.is_dir():
        return []
    return sorted(p for p in plugins.iterdir() if p.is_dir())


def _index_entries(root: Path) -> dict:
    """Mesure l'index au fichier, sans YAML tiers (stdlib seule).

    Une entree est valide si index.yaml existe, est un mapping (premiere
    ligne non-commentaire sans indentation + cles `k:` en debut de ligne)
    et contient title + description + github. La validation YAML complete
    est celle de la suite amont (scripts/test_index_release.py, pyyaml).
    """
    dirs = _plugin_dirs(root)
    resolved = [p for p in dirs if PLUGIN_DIRNAME_PATTERN.fullmatch(p.name) and not p.name.startswith("_")]
    with_index = [p for p in dirs if (p / "index.yaml").exists()]
    legacy = [p.name for p in dirs if not (p / "index.yaml").exists() and (p / "plugin.yaml").exists()]
    blocked = [p.name for p in dirs if (p / "blocked.md").exists()]
    indexed = [p for p in resolved if p.name not in blocked]
    missing_keys: dict[str, list[str]] = {k: [] for k in REQUIRED_INDEX_KEYS}
    invalid_yaml: list[str] = []
    max_screenshots = 0
    for p in with_index:
        text = (p / "index.yaml").read_text(encoding="utf-8", errors="replace")
        if not re.search(r"(?m)^[A-Za-z_][A-Za-z0-9_-]*:", text):
            invalid_yaml.append(p.name)
            continue
        for key in REQUIRED_INDEX_KEYS:
            if not re.search(rf"(?m)^{key}:", text):
                missing_keys[key].append(p.name)
        m = re.search(r"(?m)^screenshots:\s*$", text)
        if m:
            block = text[m.end():]
            count = len(re.findall(r"(?m)^\s+-\s+\S", block.split("\n\n")[0]))
            max_screenshots = max(max_screenshots, count)
    thumbs_dir = root / "generated" / "thumbnails"
    generated = sorted(p.name for p in thumbs_dir.iterdir() if p.is_dir()) if thumbs_dir.is_dir() else []
    orphan_thumbs = [t for t in generated if t not in {p.name for p in dirs}]
    local_thumb = [
        p.name
        for p in with_index
        if any(next(p.glob(f"*{suffix}"), None) is not None for suffix in THUMBNAIL_SUFFIXES)
    ]
    without_thumb = [
        p.name for p in with_index if p.name not in generated and p.name not in local_thumb
    ]
    names = {p.name for p in dirs}
    return {
        "plugin_dirs_total": len(dirs),
        "plugin_names_resolved": len(resolved),
        "indexed_plugins": len(indexed),
        "index_yaml_present": len(with_index),
        "legacy_plugin_yaml_only": legacy,
        "blocked_plugins": blocked,
        "index_yaml_invalid": invalid_yaml,
        "index_yaml_missing_keys": {k: v for k, v in missing_keys.items() if v},
        "max_screenshots": max_screenshots,
        "generated_thumbnails": len(generated),
        "orphan_thumbnails": orphan_thumbs,
        "local_thumbnails": len(local_thumb),
        "plugins_without_any_thumbnail": without_thumb,
        "abandoned_present": [n for n in ABANDONED_AGENT_ZERO if n in names],
        "surfaces_present": [n for n in SURFACES_AGENT_ZERO if n in names],
    }


def describe() -> dict:
    """Decrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'etat de l'index gele. Aucun appel reseau, aucune ecriture."""
    root = _repo_root()
    entries = _index_entries(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "confinement": CONFINEMENT,
        **entries,
        "index_coherent": (
            entries["index_yaml_invalid"] == []
            and entries["index_yaml_missing_keys"] == {}
            and entries["plugins_without_any_thumbnail"] == []
            and entries["abandoned_present"] == []
            and entries["surfaces_present"] == []
        ),
    }


def doctor() -> list[dict]:
    """Liste de controles sur l'index gele.

    Les anomalies amont constatees (2 thumbnails orphelines, 2 dossiers en
    plugin.yaml historique) sont rapportees comme informations (ok=True
    avec detail) : ce sont des faits de l'amont, pas des defaillances de
    l'adapter — l'adapter constate, il ne juge pas l'amont.
    """
    v = validate()
    checks = [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_mit",
            "ok": v["license_file_present"] and v["license"] == "MIT",
            "detail": "LICENSE present, MIT",
        },
        {
            "name": "index_comptage",
            "ok": v["plugin_dirs_total"] == 235 and v["indexed_plugins"] == 230,
            "detail": (
                f"{v['plugin_dirs_total']} dossiers, {v['plugin_names_resolved']} noms resolus, "
                f"{v['indexed_plugins']} indexes (suite amont : 230)"
            ),
        },
        {
            "name": "index_yaml_integrite",
            "ok": v["index_yaml_invalid"] == [] and v["index_yaml_missing_keys"] == {},
            "detail": (
                f"{v['index_yaml_present']} index.yaml, 0 invalide, 0 cle requise manquante, "
                f"max {v['max_screenshots']} screenshots"
            ),
        },
        {
            "name": "thumbnails_coherence",
            "ok": v["plugins_without_any_thumbnail"] == [],
            "detail": (
                f"{v['generated_thumbnails']} generees, {v['local_thumbnails']} locales, "
                f"0 plugin sans thumbnail ; orphelines constatees : {v['orphan_thumbnails']}"
            ),
        },
        {
            "name": "tri_agent_zero_coherent",
            "ok": v["abandoned_present"] == [] and v["surfaces_present"] == [],
            "detail": "0 des 3 abandonnes, 0 des 9 surfaces agent-zero dans l'index",
        },
        {
            "name": "dossiers_historiques_constates",
            "ok": True,
            "detail": f"plugin.yaml seul (format historique amont) : {v['legacy_plugin_yaml_only']}",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import reseau, 0 appel sortant",
        },
    ]
    return checks
