# F0005 - Move-Invariant Knowledge-Graph Feature-Doc References PRD

## Feature Header

**Feature ID:** F0005
**Feature Name:** Move-Invariant Knowledge-Graph Feature-Doc References
**Priority:** High
**Phase:** Platform Hardening
**Status:** Draft

## Feature Statement

**As a** framework maintainer running governed feature actions
**I want** knowledge-graph nodes to reference feature docs by a move-invariant logical name instead of a physical path
**So that** archiving a completed feature at closeout requires exactly one `feature-mappings.yaml` edit and never leaves the graph pointing at stale paths — without the Product Manager having to edit architect-owned graph files.

## Business Objective

- **Goal:** Eliminate the stale-feature-doc-path class of knowledge-graph drift at feature closeout.
- **Metric:** Number of hand-edits to `canonical-nodes.yaml` / `code-index.yaml` required to archive a feature.
- **Baseline:** Today the PM must repoint every feature-doc path inside `canonical-nodes.yaml` (and, silently, `code-index.yaml`) after the `G8` archive move — an off-book edit of architect-owned files that the contract forbids. F0038 needed this (`pm-closeout.md` line 60).
- **Target:** Archiving a feature is a single `path:` edit in `feature-mappings.yaml`. Zero KG binding edits. `validate.py` and `--check-drift` stay green across the move with no repoint step.

## Problem Statement

- **Current State:** `canonical-nodes.yaml` `source_docs`/`path` and `code-index.yaml`
  `paths.docs.*` embed physical feature-doc paths (`planning-mds/features/F####-slug/...`).
  `validate.py` runs `validate_path_exists` on those (`scripts/kg/validate.py:1075`, `:1077`), and
  `coverage-report.yaml` freshness is derived from them (`:247`). At `G8` the PM moves the feature
  folder to `archive/`, invalidating every embedded path. Because the contract (feature.md:98,
  operator-prompt line 118) forbids the PM from editing the architect-owned graph, and the
  architect's `G7` reconciliation runs *before* the move, no role can cleanly repoint after it.
- **Desired State:** Feature-doc references are logical (`F####/relative-path`) and never contain a
  move-sensitive prefix. The physical folder location lives in one place — `feature-mappings.yaml`,
  which the PM already owns and already updates on archive (`agents/docs/KNOWLEDGE-GRAPH.md`
  line 294). A resolver joins logical ref + mapping at read time.
- **Impact:** Removes a standing ownership contradiction, deletes a fragile manual closeout step,
  makes the "architect owns the semantic graph; PM only verifies it" contract actually true, and
  makes the `G7` "binds move-stable references" claim accurate.

## Scope & Boundaries

**In Scope:**
- A logical reference format for feature-folder docs: `F####/relative-path-within-feature-folder`.
- A resolver that maps a logical ref to the current physical path via `feature-mappings.yaml`.
- Wiring the resolver into the three consuming scripts: `validate.py` (existence + coverage
  freshness), `lookup.py` (display/output), `eval.py` (declared-doc aggregation).
- Fail-loud validation when a logical ref cannot resolve (unknown feature id, feature not in
  mappings, or file missing after resolution).
- One-time migration of existing feature-folder refs (~220 in `canonical-nodes.yaml`, ~44 in
  `code-index.yaml`) from physical to logical form, verified against a green baseline.
- A validator rule that forbids new physical feature-folder paths in doc-reference fields.
- Framework-contract reconciliation in `nebula-agents`: `feature.md`, the feature operator prompt,
  `KNOWLEDGE-GRAPH.md`, and the affected templates.

**Out of Scope:**
- References into stable roots (`schemas/`, `architecture/`, `security/`, `api/`) — these never
  move and stay as physical paths.
- Code-glob `node_bindings` in `code-index.yaml` (already move-stable; unchanged).
- Re-modeling `feature-mappings.yaml` itself (it already carries `id → path`; F0005 reuses it).
- Changing gate ordering or introducing any new gate.
- Migrating product repos that have no populated knowledge graph yet.

## Acceptance Criteria Overview

- [ ] A documented logical-ref format exists for feature-folder docs.
- [ ] The resolver returns the correct physical path for a logical ref given `feature-mappings.yaml`,
      for both live and archived features, with no change to the ref across the move.
- [ ] An unresolvable logical ref (unknown/unmapped feature, or missing file) fails `validate.py`
      loudly with an actionable message — it is never silently skipped.
- [ ] Refs into stable roots continue to validate as physical paths unchanged.
- [ ] All existing feature-folder refs are migrated to logical form; `validate.py` and
      `--check-drift` are green before and after with an otherwise-identical graph.
- [ ] A physical `planning-mds/features/...` path in a doc-reference field is rejected by validation.
- [ ] Archiving a feature (the reference `nebula-insurance-crm` graph) requires editing only the
      `path:` line in `feature-mappings.yaml`; no KG binding file is touched and the graph stays green.
- [ ] `feature.md`, the feature operator prompt, and `KNOWLEDGE-GRAPH.md` no longer describe a PM
      repoint of the semantic graph, and the "PM does not author canonical-nodes/code-index" rule is
      consistent with the shipped behavior.

## Design & Mechanism

### Logical reference format

A feature-folder doc reference is written as `{FEATURE_ID}/{path-relative-to-feature-folder}`:

```yaml
# before (physical — breaks on the G8 archive move):
source_docs:
  - planning-mds/features/archive/F0038-neuron-day-at-a-glance-shell/README.md
# after (logical — move-invariant):
source_docs:
  - F0038/README.md
```

The relative portion (`README.md`, `F0038-S0002-....md`, `feature-assembly-plan.md`) is stable —
only the folder *prefix* moves on archive, and that prefix is no longer stored in the node.

### Resolver

```
resolve_doc_ref(ref):
    if ref matches ^F\d{4}/ :                       # logical feature-doc ref
        feature_id, rel = ref.split('/', 1)
        folder = feature_mappings.path_for(feature_id)   # e.g. planning-mds/features/archive/F0038-...
        if folder is None: FAIL "unmapped feature <feature_id> for doc ref <ref>"
        return folder + '/' + rel
    else:                                            # stable-root physical path (schemas/, api/, ...)
        return ref                                   # unchanged
```

`feature_mappings.path_for` reads the `features:` section of `feature-mappings.yaml`
(`id: feature:F#### / path: ...`). On archive, the PM updates that one `path:` value; every logical
ref that references the feature automatically resolves to the new location. The resolver is a pure
lookup — no writes, no I/O beyond the already-loaded mappings.

### Where it plugs in (three call sites, product repo `scripts/kg/`)

| Script | Site | Change |
|--------|------|--------|
| `validate.py` | `validate_path_exists` on `source_docs`/`path` (`:1075`, `:1077`) | Resolve first, then check existence; fail loud on unresolvable ref |
| `validate.py` | `build_coverage_report` freshness (`:247`) | Resolve logical refs before `stat` for `last_modified` |
| `lookup.py` | `source_docs` echo (`:118-119`) | Resolve for display so operators get an openable path |
| `eval.py` | declared-docs aggregation (`:148`) | Resolve before aggregating |

### Hybrid, not wholesale

Only feature-folder refs change form. In `canonical-nodes.yaml` today: ~220 feature-folder refs
(move) vs ~480 stable-root refs (`architecture/` ~226, `security/` ~160, `api/` ~94 — never move).
The resolver's `else` branch passes stable-root physical paths through untouched.

## Data Requirements

**Logical-ref grammar:**
- `^F\d{4}/.+$` — feature id, `/`, then a path relative to the feature folder.
- Applies only in doc-reference fields: `canonical-nodes.yaml` `source_docs` and `path`,
  `code-index.yaml` `paths.docs.*`.

**Resolution rules:**
- The feature id must exist in the `features:` section of `feature-mappings.yaml`.
- Resolution result must be an existing file at validation time (else loud failure).
- A ref that is not a logical feature-doc ref is treated as a physical path and validated as-is.
- Stable-root refs (`planning-mds/{schemas,architecture,security,api}/...`) must NOT be rewritten.

**Migration rules:**
- Rewrite `planning-mds/features/[archive/]F####-slug/REST` → `F####/REST` for feature-folder refs only.
- Idempotent; a dry-run/`--check` mode reports intended rewrites without applying them.
- Verify `validate.py` and `validate.py --check-drift` exit 0 before and after.

## Role-Based Ownership

| Role | Responsibility | Notes |
|------|----------------|-------|
| Architect | Authors logical feature-doc refs in `canonical-nodes.yaml` / `code-index.yaml` at `G7` | Refs are move-invariant; no post-move edit needed |
| Product Manager | Owns the single `path:` value per feature in `feature-mappings.yaml` | The only edit required on archive |
| Framework maintainer | Owns the resolver, migration, and contract/doc reconciliation | Reference implementation in the product repo |

## Success Criteria

- Archiving a feature never produces a `Missing path` validation error.
- The PM performs zero edits to `canonical-nodes.yaml` / `code-index.yaml` during closeout.
- The logical ref for a doc is identical before and after that doc's feature is archived.
- No regression on stable-root references or code-glob bindings.

## Risks & Assumptions

- **Risk:** `feature-mappings.yaml` becomes a hard resolve-time dependency for feature-doc paths.
  **Mitigation:** validation fails loudly on unmapped features; `KNOWLEDGE-GRAPH.md` line 329 already
  documents the "feature not yet in mappings → fall back to file reads / backfill the mapping"
  path, so the unmapped case has a defined behavior.
- **Risk:** Migration silently corrupts refs. **Mitigation:** dry-run mode + green-baseline
  before/after diff on the `nebula-insurance-crm` graph (currently green after F0038).
- **Risk:** A stable-root path is accidentally rewritten to logical form. **Mitigation:** migration
  scopes strictly to the `planning-mds/features/` prefix; enforcement rule only targets that prefix.
- **Assumption:** Every feature whose docs are referenced by a canonical node is (or will be)
  present in `feature-mappings.yaml` — consistent with the existing coverage model.
- **Assumption:** The relative path of a doc within its feature folder is stable across the archive
  move (only the folder prefix changes). True for the current archive convention.

## Dependencies

- Product-repo knowledge-graph tooling: `scripts/kg/{validate,lookup,eval}.py`,
  `scripts/kg/kg_common.py` (resolver home candidate).
- `feature-mappings.yaml` `features:` section as the id→path source of truth.
- Framework contract surfaces in `nebula-agents`: `agents/actions/feature.md`,
  `agents/templates/prompts/evidence-contract/feature-operator-friendly.md`,
  `agents/docs/KNOWLEDGE-GRAPH.md`, `agents/templates/feature-assembly-plan-template.md`,
  `agents/templates/kg-reconciliation-template.md`.
- A green reference graph to migrate and validate against (`nebula-insurance-crm`, post-F0038).

## Related Stories

- [F0005-S0001](./F0005-S0001-feature-doc-reference-resolver.md) - Feature-doc reference resolver (dual-format, fail-loud)
- [F0005-S0002](./F0005-S0002-migrate-feature-doc-refs-to-logical.md) - Migrate existing feature-doc references to logical form
- [F0005-S0003](./F0005-S0003-enforce-logical-only-feature-doc-refs.md) - Enforce logical-only feature-doc references
- [F0005-S0004](./F0005-S0004-reconcile-framework-contract-and-docs.md) - Reconcile framework contract, prompt, and KG docs

## Rollout & Enablement

- Land S0001–S0003 in one product repo (`nebula-insurance-crm`) first as the reference
  implementation; keep the dual-format resolver so the graph is valid mid-migration.
- Ship S0004 (contract/prompt/docs) once the reference implementation is green so the contract
  never describes unshipped behavior.
- Roll the resolver + migration to other product repos as they adopt the knowledge graph; each is an
  independent application of the same S0001–S0003 steps (tracked per repo, not in this feature).
