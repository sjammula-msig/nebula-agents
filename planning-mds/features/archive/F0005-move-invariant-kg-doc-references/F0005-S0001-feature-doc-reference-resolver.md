# F0005-S0001 - Feature-Doc Reference Resolver (Dual-Format, Fail-Loud)

## Story Header

**Story ID:** F0005-S0001
**Feature:** F0005 - Move-Invariant Knowledge-Graph Feature-Doc References
**Title:** Feature-doc reference resolver (dual-format, fail-loud)
**Priority:** Critical
**Phase:** Platform Hardening

## User Story

**As a** knowledge-graph maintainer
**I want** a resolver that turns a logical `F####/relative-path` reference into the current physical path via `feature-mappings.yaml`
**So that** graph nodes can reference feature docs without embedding a move-sensitive path, and validation can still confirm the underlying file exists.

## Context & Background

This is the enabling capability for F0005. Before any data is migrated, the KG scripts must be able
to *read* a logical reference and resolve it. The resolver must be dual-format: it resolves logical
feature-doc refs through the mappings, and passes stable-root physical paths (`schemas/`,
`architecture/`, `security/`, `api/`) through unchanged. Shipping the resolver first — while the data
is still physical — keeps the graph valid at every step of the migration (S0002).

The resolver plugs into exactly three scripts and four call sites (see PRD "Where it plugs in").

## Acceptance Criteria

**Happy Path:**
- **Given** `feature-mappings.yaml` maps `feature:F0038 → planning-mds/features/archive/F0038-...`
- **When** the resolver is asked to resolve `F0038/README.md`
- **Then** it returns `planning-mds/features/archive/F0038-.../README.md`
- **And** the same ref resolves to the live path when the mapping still points at the non-archived folder — the ref itself is unchanged across the move.

**Stable-root passthrough:**
- **Given** a reference `planning-mds/schemas/neuron-zone-payload.schema.json`
- **When** the resolver processes it
- **Then** it returns the path unchanged (not treated as a logical ref, not rewritten).

**Alternative Flows / Edge Cases:**
- A logical ref for a feature id absent from `feature-mappings.yaml` fails loudly:
  `Unmapped feature <F####> for doc ref <ref>` — never silently skipped or treated as existing.
- A logical ref that resolves to a non-existent file fails with the resolved physical path in the message.
- A malformed ref (matches `F####/` prefix but empty relative part) is rejected.
- `validate.py` existence checks, `build_coverage_report` freshness, `lookup.py` output, and
  `eval.py` aggregation all route feature-doc refs through the resolver.
- With the graph still fully physical (pre-migration), `validate.py` and `--check-drift` remain green
  (dual-format keeps legacy physical feature-doc paths working during the transition).

## Interaction Contract

N/A — internal library function and script wiring; no interactive surface.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| `scripts/kg/validate.py` | Run validation | None (read-only) | None | Re-running yields identical result on unchanged graph | Maintainer / CI |

## Data Requirements

**Resolver inputs:**
- `ref`: a doc reference string (logical `F####/rel` or physical path).
- `feature_mappings`: loaded `features:` section (`id → path`).

**Resolver output:**
- A physical repo-relative path, or a raised/collected validation error.

**Validation Rules:**
- Logical form matches `^F\d{4}/.+$`.
- Feature id must exist in mappings; otherwise loud failure.
- Non-logical refs are returned verbatim (stable-root physical paths).
- The resolver performs no writes and no network I/O.

## Dependencies

**Depends On:**
- None (first story; operates on the current physical graph).

**Related Stories:**
- F0005-S0002 — migration relies on this resolver to validate the new logical form.
- F0005-S0003 — enforcement builds on the resolver's logical/physical distinction.

## Business Rules

1. Dual-format during transition: physical feature-doc paths must keep validating until S0002
   completes, so the graph is never left invalid mid-change.
2. Fail-loud: an unresolvable reference is an error, never a pass. Silent skips reintroduce the
   drift this feature exists to remove.
3. Stable-root paths are out of scope for resolution and must pass through byte-for-byte.

## Out of Scope

- Rewriting any existing references (that is S0002).
- Forbidding physical feature-doc paths (that is S0003).
- Contract/doc edits (that is S0004).

## Non-Functional Expectations

- Performance: resolution is an in-memory dictionary lookup; no measurable validation slowdown.
- Reliability: identical result on repeated runs over an unchanged graph.

## Questions & Assumptions

**Open Questions:**
- [ ] Resolver home: `kg_common.py` (shared) vs a small new module. Prefer `kg_common.py` so all
      three scripts import one implementation.

**Assumptions (to be validated):**
- All three consumer scripts load `feature-mappings.yaml` already (or can cheaply).

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Edge cases handled (unmapped, missing file, malformed, stable-root passthrough)
- [ ] Wired into all four call sites (`validate.py` ×2, `lookup.py`, `eval.py`)
- [ ] Unit tests cover live, archived, unmapped, missing-file, malformed, and passthrough cases
- [ ] `validate.py` and `--check-drift` green on the still-physical graph
- [ ] Documentation updated (resolver behavior noted in KG docs draft)
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
