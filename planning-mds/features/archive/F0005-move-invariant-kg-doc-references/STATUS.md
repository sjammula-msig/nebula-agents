# F0005 - Move-Invariant Knowledge-Graph Feature-Doc References - Status

**Overall Status:** Superseded by F0006 (2026-07-04) — no stories will be executed under this feature
**Last Updated:** 2026-07-04

## Story Checklist

| Story | Title | Status |
|-------|-------|--------|
| F0005-S0001 | Feature-doc reference resolver (dual-format, fail-loud) | [ ] Not Started |
| F0005-S0002 | Migrate existing feature-doc references to logical form | [ ] Not Started |
| F0005-S0003 | Enforce logical-only feature-doc references | [ ] Not Started |
| F0005-S0004 | Reconcile framework contract, prompt, and KG docs | [ ] Not Started |

## Reference-Implementation Progress (product repo `scripts/kg/`)

- [ ] `resolve_doc_ref()` implemented (logical + stable-root physical, fail-loud)
- [ ] Wired into `validate.py` existence check
- [ ] Wired into `validate.py` coverage-freshness (`build_coverage_report`)
- [ ] Wired into `lookup.py` display and `eval.py` aggregation
- [ ] Migration script with `--check` dry-run
- [ ] Existing refs migrated (`canonical-nodes.yaml`, `code-index.yaml`)
- [ ] Enforcement rule rejects physical `planning-mds/features/...` doc refs
- [ ] Green baseline before/after: `validate.py` and `--check-drift` exit 0

## Framework-Contract Progress (`nebula-agents`)

- [ ] `agents/actions/feature.md` G7/G8/ownership/forbidden/exit-validation reconciled
- [ ] `agents/templates/prompts/evidence-contract/feature-operator-friendly.md` lines 87/103/117/118/120 reconciled
- [ ] `agents/docs/KNOWLEDGE-GRAPH.md` logical-ref format documented
- [ ] `agents/templates/feature-assembly-plan-template.md` + `kg-reconciliation-template.md` examples updated

## Cross-Cutting

- [ ] Resolver unit tests (live feature, archived feature, unmapped, missing file, stable-root passthrough)
- [ ] Migration idempotency test
- [ ] Enforcement-rule test (physical feature path rejected)
- [ ] Archive-a-feature dry-run proves single `feature-mappings.yaml` edit keeps graph green
- [ ] Story validator passes
- [ ] Tracker validator passes
- [ ] README and getting-started docs updated

## Required Signoff Roles (Set in Planning)

| Role | Required | Why Required | Set By | Date |
|------|----------|--------------|--------|------|
| Quality Engineer | Yes | Validates resolver behavior, migration idempotency, enforcement rule, and green before/after baseline. | Architect | 2026-07-02 |
| Code Reviewer | Yes | Reviews resolver correctness, fail-loud semantics, and migration safety. | Architect | 2026-07-02 |
| Architect | Yes | Owns the semantic-graph contract; confirms the logical-ref schema and the G7/G8 reconciliation. | Architect | 2026-07-02 |
| Security Reviewer | No | No auth, secret, or external surface; pure path resolution over local planning docs. | Architect | 2026-07-02 |
| DevOps | No | No deployment or runtime-container surface. | Architect | 2026-07-02 |

## Story Signoff Provenance

Complete this before moving `Overall Status` to `Done` or `Archived`.

| Story | Role | Reviewer | Verdict | Evidence | Date | Notes |
|-------|------|----------|---------|----------|------|-------|
| F0005-S0001 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0001 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0001 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0002 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0002 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0003 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0003 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0004 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0005-S0004 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |

## Deferred Non-Blocking Follow-ups

| Follow-up | Why deferred | Tracking link | Owner |
|-----------|--------------|---------------|-------|
| Roll resolver + migration to other product repos | Each repo adopts the knowledge graph independently | TBD | Framework maintainer |

## Closeout Summary

| Field | Value |
|-------|-------|
| Implementation completed | TBD |
| Closeout review date | TBD |
| Total stories | 4 |
| Stories completed | 0 / 4 |
| Test count (unit + integration) | TBD |
| Defects found during review | TBD |
| Defects fixed before closeout | TBD |
| Residual risks | TBD |

## Tracker Sync Checklist

- [ ] `planning-mds/features/REGISTRY.md` status/path aligned
- [ ] `planning-mds/features/ROADMAP.md` section aligned
- [ ] `planning-mds/features/STORY-INDEX.md` regenerated or updated
- [ ] `planning-mds/BLUEPRINT.md` feature/story status links aligned
- [ ] Every required signoff role has story-level `PASS` entries with reviewer, date, and evidence
