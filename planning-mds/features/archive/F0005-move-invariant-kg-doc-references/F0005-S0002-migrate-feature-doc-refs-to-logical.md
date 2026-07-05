# F0005-S0002 - Migrate Existing Feature-Doc References to Logical Form

## Story Header

**Story ID:** F0005-S0002
**Feature:** F0005 - Move-Invariant Knowledge-Graph Feature-Doc References
**Title:** Migrate existing feature-doc references to logical form
**Priority:** Critical
**Phase:** Platform Hardening

## User Story

**As a** knowledge-graph maintainer
**I want** every existing feature-folder reference rewritten from a physical path to the logical `F####/relative-path` form
**So that** the current graph stops carrying move-sensitive paths and archiving a feature no longer requires a repoint.

## Context & Background

With the dual-format resolver in place (S0001), the stored data can be flipped from physical to
logical without invalidating the graph. This is a one-time, mechanical rewrite scoped to
feature-folder references only: `canonical-nodes.yaml` (`source_docs`, `path`) and `code-index.yaml`
(`paths.docs.*`). References into stable roots are left exactly as they are.

The reference migration runs against `nebula-insurance-crm`, whose graph is green after F0038 — that
green state is the before/after baseline that proves the migration changed only the ref *form*, not
the graph's meaning.

## Acceptance Criteria

**Happy Path:**
- **Given** a physical ref `planning-mds/features/archive/F0038-.../README.md` in `canonical-nodes.yaml`
- **When** the migration runs
- **Then** it becomes `F0038/README.md`
- **And** a live-folder ref `planning-mds/features/F0017-.../F0017-S0001-...md` becomes `F0017/F0017-S0001-...md`
- **And** `validate.py` and `validate.py --check-drift` exit 0 both before and after, with no other change to graph semantics.

**Alternative Flows / Edge Cases:**
- Stable-root refs (`planning-mds/schemas|architecture|security|api/...`) are left byte-for-byte unchanged.
- `code-index.yaml` code-glob `node_bindings` are untouched (they are not doc refs).
- Re-running the migration is a no-op (idempotent).
- A `--check` dry-run lists every intended rewrite (old → new) and applies nothing.
- If any rewritten ref fails to resolve after migration, the run reports it and the migration is not
  considered complete.

## Interaction Contract

N/A — one-time maintenance script over planning data.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| `scripts/kg/migrate-doc-refs.py` (or equivalent) | Run migration | KG YAML doc-ref fields | Feature-folder refs rewritten to logical form | `git diff` shows only prefix rewrites; validators green | Maintainer, on a branch, reviewed |

## Data Requirements

**Transform:**
- `planning-mds/features/[archive/]F####-slug/REST` → `F####/REST` (feature-folder refs only).
- Applied to `canonical-nodes.yaml` `source_docs` + `path`, and `code-index.yaml` `paths.docs.*`.

**Validation Rules:**
- Only the `planning-mds/features/` prefix class is eligible; all other prefixes are ignored.
- YAML structure, ordering, and comments preserved as much as the writer allows; diff must be
  limited to the ref strings.
- Post-migration, every rewritten ref must resolve (via S0001 resolver) to an existing file.

## Dependencies

**Depends On:**
- F0005-S0001 — the resolver must accept logical refs before the data is flipped.

**Related Stories:**
- F0005-S0003 — enforcement locks in the migrated state.

## Business Rules

1. Meaning-preserving: the migration changes ref *form* only. The before/after graph must be
   semantically identical (same nodes, same docs, validators green).
2. Feature-scoped prefix only: never rewrite a stable-root path.
3. Idempotent and dry-runnable: safe to run twice; `--check` previews without writing.

## Out of Scope

- Resolver implementation (S0001).
- Rejecting future physical refs (S0003).
- Other product repos (per-repo rollout, tracked separately).

## Non-Functional Expectations

- Reliability: deterministic output; identical result on re-run.
- Auditability: dry-run diff reviewed before apply; `git diff` is the evidence.

## Questions & Assumptions

**Open Questions:**
- [ ] Do any current feature-doc refs point at a feature not present in `feature-mappings.yaml`? If
      so, backfill the mapping in the same change set (per `KNOWLEDGE-GRAPH.md` line 329).

**Assumptions (to be validated):**
- The `nebula-insurance-crm` graph is green immediately before migration (post-F0038 baseline holds).

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Migration script with `--check` dry-run
- [ ] All feature-folder refs in `canonical-nodes.yaml` and `code-index.yaml` migrated
- [ ] Stable-root refs and code-glob bindings unchanged (verified by diff)
- [ ] `validate.py` and `--check-drift` exit 0 before and after (baseline evidence captured)
- [ ] Idempotency test (second run is a no-op)
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
