# F0006-S0007 - Tracker Generation from Feature Shards

## Story Header

**Story ID:** F0006-S0007
**Feature:** F0006 - Compiled Knowledge-Graph Projection and Governed Integration
**Title:** Tracker generation from feature shards
**Priority:** High
**Phase:** Platform Hardening (Feature Phase B)

## User Story

**As a** PM keeping REGISTRY, ROADMAP, and the story index synchronized
**I want** the feature tables in `REGISTRY.md` and `ROADMAP.md` generated from feature shards (as `STORY-INDEX.md` already is from story files)
**So that** feature status/path/dependency truth lives in exactly one place (the feature shard), tracker tables can never conflict or drift, and the S0002 table-merge machinery retires to a transition-only role.

## Context & Background

Review amendment #3: the original compiled-projection draft generated only STORY-INDEX, leaving
REGISTRY/ROADMAP — 2 of PR #47's 7 conflicts — hand-maintained forever. This story completes the
projection model for trackers. The feature shard (S0004) is already the single home for `path`,
`status`, and `depends_on`; this story renders those facts into the tracker tables.

Trackers are *partially* generated: the generator owns fenced table regions
(`<!-- generated:begin ... -->` / `<!-- generated:end -->`); surrounding prose (purpose, update
rules, notes, numbering rules) stays PM-authored. Fields the tables need beyond current shard
schema (phase, "Why Now", validation gate, archive dates) extend the feature shard schema — they
are feature facts, so the shard is their correct home.

## Acceptance Criteria

**Happy Path:**
- **Given** feature shards for all features with status/phase/dates/sequencing fields
- **When** the tracker generator runs (standalone or via `compile.py`)
- **Then** REGISTRY's Active/Planned/Retired/Archived tables and ROADMAP's Now/Next/Later/Completed
  tables are rendered inside their fenced regions, ordered by the per-table sort rules (archived:
  date desc, ID-desc tiebreak), prose outside regions byte-untouched.

**Cutover parity:**
- **Given** the hand-maintained tracker state on cutover day
- **When** generated output is diffed against it
- **Then** discrepancies are enumerated, reconciled once (shards fixed, or table corrected) with PM
  review, and the post-reconcile diff is empty.

**Alternative Flows / Edge Cases:**
- `Next Available Feature Number` derives as max(existing IDs) + 1.
- A feature shard with no roadmap-section field fails generation loudly (every feature must be
  placed, matching ROADMAP's completeness rule).
- Retired/superseded features render with `Superseded By` from the shard's supersession field.
- Hand-edits inside a fenced region are detected by the S0008 reproducibility check.
- `STORY-INDEX.md` generation is unchanged (already shipped); this story only adds it to the
  compile driver's invocation list.
- BLUEPRINT.md's feature-plan list: evaluated for the same fenced-region treatment; if deferred,
  the decision and rationale are recorded (it is a tracker per TRACKER-GOVERNANCE.md).

## Interaction Contract

N/A — generator CLI; no interactive surface.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| tracker generator (via `compile.py`) | Run compile | Fenced table regions only | Regions re-rendered deterministically | Re-run zero-diff on unchanged shards | Any branch owner; integrator at merge |

## Data Requirements

**Inputs:** `kg-source/features/**` (extended schema), story files (for story index), fenced-region
markers in tracker files.
**Outputs:** re-rendered table regions in `REGISTRY.md` / `ROADMAP.md`.

**Validation Rules:**
- Generator writes only between markers; missing/duplicated markers → loud failure.
- Deterministic rendering (stable column widths/escaping) so re-runs are zero-diff.
- Every feature shard appears in exactly one REGISTRY status table and one ROADMAP section.

## Dependencies

**Depends On:** F0006-S0004 (+ shard schema extension), F0006-S0005 (compile driver),
F0006-S0006 (shards populated).
**Related Stories:** F0006-S0002 (retires to transition/non-generated tables),
F0006-S0008 (enforces region integrity), F0006-S0009 (TRACKER-GOVERNANCE update).

## Business Rules

1. Feature facts live in the shard; tables are views. A table edit that changes a fact is the
   wrong move — edit the shard.
2. PM owns feature shards and tracker prose; the integrator regenerates regions at merge.
3. Sort order is always recomputed, never merged.

## Out of Scope

- Story file content, STATUS.md files (remain authored), evidence trackers, this repo's
  (`nebula-agents`) own trackers until it adopts the shard model itself.

## Non-Functional Expectations

- Zero-diff regeneration on unchanged shards; sub-second runtime.

## Questions & Assumptions

**Open Questions:**
- [ ] Include BLUEPRINT.md feature-plan list in scope now or defer (see edge case; needs PM call).

**Assumptions (to be validated):**
- Fenced-region markers are acceptable in tracker files consumed by existing validators
  (`validate-trackers.py` tolerance to HTML comments — verify).

## Definition of Done

- [ ] Acceptance criteria met including cutover parity reconciliation with PM signoff
- [ ] Feature-shard schema extension reviewed (S0004 spec updated)
- [ ] Region-integrity, ordering, counter, and zero-diff tests
- [ ] `compile.py` driver invokes tracker generation; integrator flow picks it up automatically
- [ ] TRACKER-GOVERNANCE.md implications handed to S0009
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
