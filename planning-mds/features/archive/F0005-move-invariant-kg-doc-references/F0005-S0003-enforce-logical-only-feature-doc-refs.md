# F0005-S0003 - Enforce Logical-Only Feature-Doc References

## Story Header

**Story ID:** F0005-S0003
**Feature:** F0005 - Move-Invariant Knowledge-Graph Feature-Doc References
**Title:** Enforce logical-only feature-doc references
**Priority:** High
**Phase:** Platform Hardening

## User Story

**As a** knowledge-graph maintainer
**I want** validation to reject any new physical `planning-mds/features/...` path in a doc-reference field
**So that** the stale-path class cannot regress after the migration — future authors are forced into the move-invariant logical form.

## Context & Background

S0001 makes logical refs resolvable and S0002 migrates existing data. Without enforcement, an
architect could add a new physical feature-doc path at the next `G7` and quietly reintroduce the
drift. This story adds a validator rule that makes a physical feature-folder path in a doc-reference
field a hard error, keeping the invariant durable. The rule is deliberately narrow: it targets only
the `planning-mds/features/` prefix in doc-reference fields, so stable-root paths and code-glob
bindings are unaffected.

## Acceptance Criteria

**Happy Path:**
- **Given** a `canonical-nodes.yaml` node whose `source_docs` contains `planning-mds/features/F0040-.../PRD.md`
- **When** `validate.py` runs
- **Then** it fails with a clear message naming the node, the field, and the offending path, and
  instructing the author to use the `F0040/PRD.md` logical form.

**Alternative Flows / Edge Cases:**
- A logical ref (`F0040/PRD.md`) passes.
- A stable-root physical path (`planning-mds/schemas/...`) passes (not a feature-folder path).
- A `code-index.yaml` code-glob binding (e.g. `neuron/app/**`) passes (not a doc-reference field).
- The rule fires for both `archive/` and non-archive feature-folder prefixes.
- The post-S0002 migrated graph passes the new rule with zero violations.

## Interaction Contract

N/A — validator rule; no interactive surface.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| `scripts/kg/validate.py` | Run validation | None | None | Violations reported deterministically | Maintainer / CI gate |

## Data Requirements

**Rule scope:**
- Fields: `canonical-nodes.yaml` `source_docs` + `path`, `code-index.yaml` `paths.docs.*`.
- Trigger: value begins with `planning-mds/features/` (with or without `archive/`).

**Validation Rules:**
- Violation is an error (not a warning) with node id, field, and offending value.
- Message names the expected logical form.
- No false positives on stable-root paths or code-glob bindings.

## Dependencies

**Depends On:**
- F0005-S0002 — the graph must already be migrated, or the rule would fail the whole graph.

**Related Stories:**
- F0005-S0001 — reuses the resolver's logical/physical classification.

## Business Rules

1. Narrow trigger: only `planning-mds/features/` in doc-reference fields; never code-glob bindings
   or stable-root paths.
2. Hard failure: a physical feature-doc path is an error, so CI blocks regressions.
3. Actionable message: every violation tells the author the exact logical replacement.

## Out of Scope

- Auto-fixing violations (authors fix by using the logical form; S0002 handles the bulk one-time pass).
- Contract/doc wording (S0004).

## Non-Functional Expectations

- Reliability: deterministic pass/fail; zero violations on the migrated baseline.
- Clarity: a new maintainer can fix a violation from the message alone.

## Questions & Assumptions

**Open Questions:**
- [ ] Should the rule also warn on a logical ref whose relative part looks like it escaped the
      feature folder (e.g. contains `../`)? Likely yes — reject path traversal in the relative part.

**Assumptions (to be validated):**
- After S0002, no legitimate doc-reference field needs a physical feature-folder path.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Rule rejects physical feature-doc paths in the named fields; passes logical, stable-root, and code-glob
- [ ] Migrated baseline reports zero violations
- [ ] Test covers violation, logical pass, stable-root pass, code-glob pass, archive + non-archive prefixes
- [ ] Documentation updated
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
