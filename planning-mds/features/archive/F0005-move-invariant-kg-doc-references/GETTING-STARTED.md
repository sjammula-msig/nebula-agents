# F0005 - Getting Started

This feature has two homes:

- **Reference implementation** (code + data): a product repo's `scripts/kg/` and
  `planning-mds/knowledge-graph/`. First target: `nebula-insurance-crm`.
- **Contract** (docs): this repo, `nebula-agents` — `agents/actions/feature.md`, the feature
  operator prompt, and `agents/docs/KNOWLEDGE-GRAPH.md`.

## Key files (product repo)

| File | Role |
|------|------|
| `scripts/kg/kg_common.py` | Resolver home candidate (`resolve_doc_ref`) |
| `scripts/kg/validate.py` | Existence check (`validate_path_exists`) + coverage freshness (`build_coverage_report`) |
| `scripts/kg/lookup.py` | Echoes `source_docs` for operators |
| `scripts/kg/eval.py` | Aggregates declared docs |
| `planning-mds/knowledge-graph/canonical-nodes.yaml` | `source_docs`/`path` → migrate to logical |
| `planning-mds/knowledge-graph/code-index.yaml` | `paths.docs.*` → migrate to logical |
| `planning-mds/knowledge-graph/feature-mappings.yaml` | `features:` `id → path` — the resolver's source of truth |

## Verify the graph

```bash
# from the product repo root
python3 scripts/kg/validate.py               # basic integrity incl. doc-path existence
python3 scripts/kg/validate.py --check-drift  # drift check
```

Both must exit 0 before and after the migration. The `nebula-insurance-crm` graph is currently
green (post-F0038) and is the migration baseline.

## Logical-ref format

`F####/relative-path-within-the-feature-folder`, e.g. `F0038/README.md`,
`F0038/F0038-S0002-day-at-a-glance-shell-and-zone-dispatch.md`. The resolver joins it with the
feature's `path:` from `feature-mappings.yaml`. Stable-root refs (`planning-mds/schemas/...`,
`.../architecture/...`, `.../security/...`, `.../api/...`) stay physical and are not migrated.

## Prove the payoff

Archive a completed feature by editing only its `path:` line in `feature-mappings.yaml`
(`features/F####-...` → `features/archive/F####-...`) and moving the folder. `validate.py` and
`--check-drift` must stay green with no edit to `canonical-nodes.yaml` or `code-index.yaml`.
