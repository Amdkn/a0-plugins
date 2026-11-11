# A'Space adapter — a0-plugins

**Adresse :** `fiber:a0:a0-plugins` — D-N053 pas B (design Clara, design signé pas B D-B0..D-B3).
**Fork souverain :** `Amdkn/a0-plugins` (parent `agent0ai/a0-plugins`, branche `main`).
**Gel amont :** `d040c3fd8d7ca9486cabf2761cbcc51c47d9b7d8` (« Merge pull request #682 from TerminallyLazy/add/code-intelligence »).
**Bind Cordis Fiber (2L) :** `f73f767d0482accdf5b2ec53d137f916c22df3c9` — `aspace-plugin.json`, re-appliqué VERBATIM sur `main` au-dessus de l'adapter (F8 D2).
**Licence :** `MIT`.
**Version adapter :** 0.1.0 — contrat seul, patron D-N048 (dify / cordis) et pas A (chronos).

## Ce que fait l'adapter

a0-plugins est l'index communautaire des plugins Agent Zero : chaque dossier
de `plugins/` est une entrée `index.yaml` (title, description, github, tags,
screenshots) qui pointe vers le dépôt du plugin ; `generated/thumbnails/`
porte les thumbnails générées, `scripts/` la publication de l'index.

Surface : `validate()` (constate : gel, licence, comptage de l'index,
cohérence `generated/` vs `plugins/`, intégrité des `index.yaml`, cohérence
avec le tri agent-zero, zéro appel réseau), `doctor()` (liste de contrôles),
`describe()` (manifeste machine). **Aucun fichier amont touché, aucun appel
réseau, aucun poids monté dans le fork.**

Mesures au gel : 235 dossiers, 232 noms résolus, 230 indexés (suite amont :
« Verified complete index: 230 plugins »), 233 `index.yaml` valides,
87 thumbnails générées (2 orphelines constatées : `chat_organizer`,
`d2_audio`), 155 thumbnails locales, 0 plugin sans thumbnail, 0 des 3
abandonnés et 0 des 9 surfaces agent-zero dans l'index (H-B6).

## Confinement

Aucun confinement commercial : code et index MIT. Usage B2B autorisé par
la licence. L'index ne contient que des pointeurs ; aucun code de plugin
n'est monté dans le fork.

## Tests

```bash
python -m pytest aspace-a0-plugins-adapter/tests/test_smoke.py -v
```

Smoke : constantes (gel 40-hex, adresse fiber, licence), `validate()` vert
(comptages 235 / 232 / 230, intégrité, thumbnails), `doctor()` tout ok,
zéro import réseau dans l'adapter. La suite amont est celle du module au
gel (`scripts/test_index_release.py`, voir la fiche d'adaptation :
`a0-plugins-ADAPTATION.md`, évidence D-N053/b/a0-plugins/).
