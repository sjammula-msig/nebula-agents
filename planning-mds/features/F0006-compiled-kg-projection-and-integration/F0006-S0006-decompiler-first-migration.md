# F0006-S0006 - Decompiler-First Migration with Round-Trip Proof

## Story Header

**Story ID:** F0006-S0006
**Feature:** F0006 - Compiled Knowledge-Graph Projection and Governed Integration
**Title:** Decompiler-first migration with round-trip proof
**Priority:** Critical
**Phase:** Platform Hardening (Feature Phase B)

## User Story

**As a** framework maintainer cutting the reference graph over to the shard model
**I want** a mechanical decompiler that explodes the current monolithic graph into `kg-source/` shards, with proof that compiling those shards reproduces the pre-migration graph byte-identically
**So that** the migration cannot silently lose or alter graph semantics, requires no hand-transcription of ~550 nodes, and is a single revert away from rollback.

## Context & Background

The safe migration direction is decompile-first (review amendment #2): rather than hand-authoring
shards and hoping they compile to something equivalent, `decompile.py` mechanically partitions the
existing (already canonicalized, post-merge-train) `canonical-nodes.yaml`,
`feature-mappings.yaml`, `code-index.yaml`, plus `solution-ontology.yaml` into per-concept shards —
rewriting physical feature-doc refs to logical `F####/...` form (absorbing F0005-S0002's migration)
— and the cutover gate is `compile(decompile(graph)) == graph`.

Hard precondition: **the merge train is complete** (Phase A exit — 7 PRs as of 2026-07-05, plus
any that arrive before the train finishes). The migration rewrites exactly the files every open PR
touches; migrating with open contributor PRs invalidates them all.

## Acceptance Criteria

**Happy Path:**
- **Given** the post-train, canonicalized reference graph (validators green)
- **When** `decompile.py` runs, then `compile.py` runs on its output
- **Then** the compiled projections are byte-identical to the pre-migration files, every shard
  passes S0004 validation, `validate.py` stays green across the migration, and the reproducibility
  check (`validate.py --check-reproducible`) is green on the compiled result.

**Logical-ref migration:**
- **Given** a canonical node with physical refs into a live feature folder and an archived one
- **When** decompilation rewrites doc refs
- **Then** both become `F####/rel-path` form, resolving (per S0005) to the same physical files as
  before — including the F0038 archive paths that previously needed hand-repointing.

**Alternative Flows / Edge Cases:**
- `--check` dry-run reports the intended shard partition and ref rewrites without writing.
- Idempotency: decompiling twice produces identical shards.
- Unpartitionable content (node kind with no directory home, orphan mapping entry, ref to a
  feature absent from mappings) → loud failure listing every instance; nothing written. Resolve by
  fixing the source graph first (pre-existing drift is fixed in the graph, not paperied over in
  shards).
- Stable-root refs are not rewritten (byte-preserved through the round trip).
- `solution-ontology.yaml` moves to `kg-source/ontology/` content-identical (home change only).
- Cutover mechanics: one migration commit (tagged) containing shards + unchanged projections +
  the switch of authoring truth; rollback = revert that commit.

## Interaction Contract

N/A — migration CLI; no interactive surface.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| `scripts/kg/decompile.py` | Run (`--check` first) | `planning-mds/kg-source/**` (new files only) | Shard tree, or dry-run report, or loud failure with no writes | Idempotent re-run; round-trip diff empty | Maintainer, once per repo; kept for future repo adoptions |

## Data Requirements

**Inputs:** the four curated/monolithic files; feature-mappings for ref rewriting; S0004 schema.
**Outputs:** populated `kg-source/**`; migration report (shard count per directory, refs rewritten,
anomalies).

**Validation Rules:**
- Round-trip byte-identity is the cutover gate — no manual "close enough."
- Every emitted shard passes S0004 validation.
- Node/mapping/binding counts reconcile exactly (nothing dropped, nothing invented).

## Dependencies

**Depends On:** F0006-S0004 (shard contract), F0006-S0005 (compiler + `--check`), Phase A complete
(merge train landed — hard precondition).
**Related Stories:** F0006-S0008 (reproducibility check flips blocking after this lands).

## Business Rules

1. No shard is hand-authored during migration; the decompiler is the only writer.
2. Pre-existing graph drift discovered during decompilation is fixed in the monolith first (as its
   own reviewed commit), then re-decompiled — the migration never launders errors into shards.
3. After cutover, the monolithic files are generated outputs; the decompiler is retired from the
   repo's normal flow (kept for adopting other repos).

## Out of Scope

- CI enforcement flips (S0008). Tracker generation (S0007). Other product repos (each adopts
  later with the same tool).

## Non-Functional Expectations

- Full decompile + compile + diff cycle in under a minute on the reference graph.

## Questions & Assumptions

**Open Questions:**
- [ ] Shard filename convention for nodes with long IDs (proposal: the ID's kebab body, which is
      already filesystem-safe by the S0004 ID grammar).

**Assumptions (to be validated):**
- Post-canonicalization (S0001), byte-identity through the round trip is achievable because both
  decompiler and compiler share the canonical serializer.

## Definition of Done

- [ ] Acceptance criteria met; round-trip byte-identity proven and recorded in evidence
- [ ] Dry-run, idempotency, anomaly-failure, and count-reconciliation tests
- [ ] Migration executed on `nebula-insurance-crm` (tagged cutover commit)
- [ ] Migration report archived with the feature evidence
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
