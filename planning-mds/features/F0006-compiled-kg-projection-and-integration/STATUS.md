# F0006 - Compiled Knowledge-Graph Projection and Governed Integration - Status

**Overall Status:** Draft
**Last Updated:** 2026-07-04

## Story Checklist

| Story | Title | Phase | Status |
|-------|-------|-------|--------|
| F0006-S0001 | Three-way semantic KG merge tool (`merge3.py`) | A | [ ] Not Started |
| F0006-S0002 | Tracker-table three-way merge (REGISTRY/ROADMAP rows) | A | [ ] Not Started |
| F0006-S0003 | Integrator role and `integrate` action | A | [ ] Not Started |
| F0006-S0004 | `kg-source/` shard schema, layout, and ownership | B | [ ] Not Started |
| F0006-S0005 | Deterministic KG compiler with logical doc refs | B | [ ] Not Started |
| F0006-S0006 | Decompiler-first migration with round-trip proof | B | [ ] Not Started |
| F0006-S0007 | Tracker generation from feature shards | B | [ ] Not Started |
| F0006-S0008 | Reproducibility CI, enforcement, and git policy | B | [ ] Not Started |
| F0006-S0009 | Framework contract, roles, and docs reconciliation | B | [ ] Not Started |

## Phase-A Exit (merge-train) Progress

- [ ] `merge3.py` replays the PR #47 resolution: re-serialization hunks converge to zero conflicts
- [ ] Known PR #47 real deltas surface as typed items (F0038 archive repoints, `excluded_features` regression, stale F0038 `status`)
- [ ] Integrator dry-run on PR #47 emits a complete integration evidence run
- [ ] PR #47 merged via integrator
- [ ] PR #51 merged via integrator (stacked on #47 — delta replay)
- [ ] PRs #50 / #48 / #49 merged via integrator
- [ ] Mainline green after each merge (`validate.py`, orphan check, story-index zero-diff)

## Reference-Implementation Progress (product repo `scripts/kg/`)

- [ ] Canonical serializer in `kg_common.py` (+ one-time no-semantic-change canonicalization commit, ID-level-diff verified)
- [ ] `merge3.py`: record merge, field rules, taxonomy, all-or-nothing output, conflict report
- [ ] Tracker-row merge for REGISTRY/ROADMAP feature tables
- [ ] `compile.py` deterministic (double-compile byte-identical; no committed timestamps)
- [ ] Logical-ref resolver wired into `validate.py` / `lookup.py` / `eval.py` call sites
- [ ] `decompile.py` with `--check`; round-trip `compile(decompile(graph))` byte-identical
- [ ] `kg-source/**` populated; `solution-ontology.yaml` rehomed under `kg-source/ontology/`
- [ ] Tracker generator owns fenced REGISTRY/ROADMAP table regions
- [ ] `validate.py --check-reproducible` + new rules (physical-path ban, alias ledger, glob overlap, archived⇒no-stale-path)
- [ ] `.gitattributes` (linguist-generated + merge driver) and CI workflow (warn → blocking)

## Framework-Contract Progress (`nebula-agents`)

- [ ] `agents/integrator/SKILL.md` persona (duties, hard boundary, routing)
- [ ] `agents/agent-map.yaml`: integrator registered; Phase-B shard write scopes for architect/PM
- [ ] `agents/actions/integrate.md` + `actions/README.md` + `ROUTER.md` routing
- [ ] Integration evidence template + `integrate-operator-friendly.md` prompt
- [ ] `agents/actions/feature.md` G7/G8 reconciled (no off-book repoint narrative)
- [ ] `feature-operator-friendly.md` prompt reconciled
- [ ] `agents/docs/KNOWLEDGE-GRAPH.md` / `ORCHESTRATION-CONTRACT.md` / `MANUAL-ORCHESTRATION-RUNBOOK.md` updated
- [ ] Templates updated: `kg-reconciliation`, `feature-assembly-plan`, `tracker-governance`, `feature-registry`, `ci-gates`

## Cross-Cutting

- [ ] merge3 unit tests: converge-identical, one-side, field-recurse, ordered-list conflict, delete-vs-update, orphan edge, unique violation, all-or-nothing
- [ ] Determinism tests: double-compile, cross-machine byte-identical
- [ ] Migration idempotency + round-trip test
- [ ] Reproducibility-check red test (synthetic hand-edit) and green test
- [ ] Archive-a-feature dry-run: one feature-shard edit keeps graph + trackers green
- [ ] Story validator passes; tracker validator passes
- [ ] README / getting-started updated

## Required Signoff Roles (Set in Planning)

| Role | Required | Why Required | Set By | Date |
|------|----------|--------------|--------|------|
| Architect | Yes | Owns merge semantics, shard schema, ontology classification, and the ownership-boundary changes; this feature redefines the KG contract. | Architect | 2026-07-04 |
| Quality Engineer | Yes | Validates merge determinism, round-trip proof, taxonomy coverage, and the PR #47 replay evidence. | Architect | 2026-07-04 |
| Code Reviewer | Yes | Reviews merge3/compile/decompile correctness, all-or-nothing semantics, and canonical-serializer safety. | Architect | 2026-07-04 |
| DevOps | Yes | CI reproducibility workflow, `.gitattributes` merge driver, branch-protection changes. | Architect | 2026-07-04 |
| Security Reviewer | No | No auth, secret, or external surface; local planning-doc tooling only. | Architect | 2026-07-04 |

## Story Signoff Provenance

Complete this before moving `Overall Status` to `Done` or `Archived`.

| Story | Role | Reviewer | Verdict | Evidence | Date | Notes |
|-------|------|----------|---------|----------|------|-------|
| F0006-S0001 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0001 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0001 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0002 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0002 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0003 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0003 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0004 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0005 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0005 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0005 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0006 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0006 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0007 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0008 | DevOps | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0008 | Quality Engineer | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0009 | Architect | TBD | TBD | TBD | TBD | Pending implementation |
| F0006-S0009 | Code Reviewer | TBD | TBD | TBD | TBD | Pending implementation |

## Deferred Non-Blocking Follow-ups

| Follow-up | Why deferred | Tracking link | Owner |
|-----------|--------------|---------------|-------|
| Roll compiler + shard migration to other product repos | Each repo adopts independently after the reference implementation is proven | TBD | Framework maintainer |
| Re-evaluate OmniGraph (or similar) if live multi-agent graph writes are ever needed | Out of scope; serial integrator suffices at current scale | TBD | Architect |
| Central `F####` reservation tooling for contributors | Process rule suffices now (REGISTRY reservation before branching) | TBD | PM |

## Closeout Summary

| Field | Value |
|-------|-------|
| Implementation completed | TBD |
| Closeout review date | TBD |
| Total stories | 9 |
| Stories completed | 0 / 9 |
| Test count (unit + integration) | TBD |
| Defects found during review | TBD |
| Defects fixed before closeout | TBD |
| Residual risks | TBD |

## Tracker Sync Checklist

- [ ] `planning-mds/features/REGISTRY.md` status/path aligned (incl. F0005 superseded record)
- [ ] `planning-mds/features/ROADMAP.md` section aligned
- [ ] `planning-mds/features/STORY-INDEX.md` regenerated or updated
- [ ] `planning-mds/BLUEPRINT.md` feature/story status links aligned
- [ ] Every required signoff role has story-level `PASS` entries with reviewer, date, and evidence
