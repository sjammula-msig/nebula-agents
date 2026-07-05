# F0006-S0003 - Integrator Role and `integrate` Action

## Story Header

**Story ID:** F0006-S0003
**Feature:** F0006 - Compiled Knowledge-Graph Projection and Governed Integration
**Title:** Integrator role and `integrate` action
**Priority:** Critical
**Phase:** Platform Hardening (Feature Phase A)

## User Story

**As a** maintainer on a personal GitHub account (no merge queue, no bot accounts)
**I want** a dedicated integrator agent — with a persona, an `integrate` action, agent-map wiring, and an evidence contract — that I run serially at merge time
**So that** integration has a sanctioned owner: sources merge semantically, projections regenerate unconditionally, validation gates the merge, every run leaves auditable evidence, and no role ever needs an off-book edit again.

## Context & Background

The framework assigns per-feature ownership (PM = WHAT, architect = HOW) but no role owns
"reconcile with a mainline that moved": F0038's closeout needed an off-book PM repoint, and PR #47's
conflict resolution had no sanctioned owner. GitHub-side fixes (merge queue, bot ownership of
generated files) are unavailable on a personal account — and unnecessary: one maintainer running
one agent serially provides the same serialization, and the agent being the sole writer of
generated files on the mainline provides the same ownership.

The integrator is deliberately **mechanical**. It converges provable equivalences, recompiles,
validates, and reports — it never makes semantic decisions. That hard boundary is what makes it
safe to run routinely and what keeps architect/PM authority intact.

Its first production runs are the 5-PR merge train in `nebula-insurance-crm`
(#47 → #51 → #50/#48/#49; #51 stacks on #47). Pre-compiler, "recompile" means: `merge3.py` the
curated trio (S0001) + tracker rows (S0002), then regenerate all derived outputs
(`symbols.py`, `decisions.py`, `--write-coverage-report`, `generate-story-index.py`).

## Acceptance Criteria

**Happy Path:**
- **Given** a contributor branch with clean code merge and independent KG/tracker additions
- **When** the maintainer runs the `integrate` action against it
- **Then** the agent merges sources (git + merge3), regenerates every generated output
  unconditionally, runs full validation green, writes an integration evidence run, and leaves a
  prepared merge commit for the maintainer to push — having modified **no** source-authored file.

**Bounce path:**
- **Given** a branch whose committed generated outputs don't match regeneration from its own
  sources (Phase A: derived files stale relative to curated files; Phase B: reproducibility fail)
- **When** the integrator verifies the branch
- **Then** it stops before merging, emits a bounce report telling the contributor exactly what to
  regenerate, and the evidence run records the bounce. The integrator does not fix the branch.

**Conflict-routing path:**
- **Given** merge3 reports a `DivergentUpdate` on a `capability:` node
- **When** the integration runs
- **Then** the run halts with the conflict report addressed to the **architect**, the evidence run
  records it, and nothing is merged. (PM-owned kinds route to the PM identically.)

**Alternative Flows / Edge Cases:**
- Textually clean git merge of generated files → still regenerated (never trusted); test proves a
  poisoned "clean" merge is overwritten by regeneration.
- Stacked PR (#51 ⊇ #47): after #47 lands, integrating #51 replays only the delta.
- Validation failure *after* a clean semantic merge (e.g. orphaned binding) → halt, evidence, route.
- Evidence runs are append-only with unique run IDs; a re-run after a bounce is a **new** run.
- The integrator never pushes to the mainline; the prepared merge is the maintainer's to push.
- Code conflicts are surfaced as ordinary git conflicts for the maintainer/contributor — the
  integrator does not resolve code.

## Interaction Contract

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| `agents/actions/integrate.md` via operator prompt | Maintainer starts an integration run naming the source branch/PR | Local merge worktree only | Prepared merge commit + evidence run, or halt report | Evidence run dir persists; re-run creates a new run | Maintainer-invoked only; serial (one run at a time) |

## Data Requirements

**Agent registration (`agents/agent-map.yaml`):**
- `integrator`: reads everything; writes limited to generated outputs
  (`{PRODUCT_ROOT}/planning-mds/knowledge-graph/**` generated files, `STORY-INDEX.md`, tracker
  generated-table regions), merge-worktree state, and its evidence run dir. Explicit non-writes:
  `kg-source/**`, `features/**` docs, code.

**Integration evidence run contents:**
- Inputs (PR/branch, merge base, mainline SHA), merge3/tracker reports (JSON), regeneration
  command log, validator outputs, bounce/conflict reports, prepared-merge SHA, operator identity,
  timestamps (evidence only — never in committed projections).

**Validation Rules:**
- A run that modifies any source-authored file must abort and self-report (contract violation).
- Every halt names the owning role and the exact records/fields at issue.

## Dependencies

**Depends On:** F0006-S0001 (merge3), F0006-S0002 (tracker merge).
**Related Stories:** F0006-S0008 (CI mirrors the branch-reproducibility check), F0006-S0009
(contract docs describe this role), F0005-derived duties absorbed via Phase B stories.

## Business Rules

1. **Serial by construction:** one integration run at a time; the maintainer is the serializer.
2. **Sole writer:** on the mainline, only integrator runs (or explicit maintainer override) may
   change generated files.
3. **Never edits sources:** any source change needed = semantic collision = route to owner
   (architect: nodes/bindings/policies/ontology; PM: features/trackers; co-sign: exclusions).
4. **Unconditional regeneration:** clean git merges of generated files are never trusted.
5. **Bounce, don't fix:** contributor branches stay contributor-owned.
6. **Evidence always:** merged, bounced, or halted — every run leaves an append-only record.

## Out of Scope

- The compiler and reproducibility CI (Phase B) — the integrator's Phase B upgrades land with them.
- Automating the maintainer's push. Multi-repo orchestration. Code-conflict resolution.

## Non-Functional Expectations

- A no-conflict integration completes in minutes; the agent's context stays within one run.
- Deterministic: re-running a bounced integration after the fix produces the same merge result.

## Questions & Assumptions

**Open Questions:**
- [ ] Model tier for the integrator in `agent-map.yaml`: the work is mechanical (tool invocation +
      report assembly) — a standard tier may suffice; decide during implementation.
- [ ] Evidence home in the product repo (mirror the feature evidence-run layout vs a dedicated
      `integration-runs/` root).

**Assumptions (to be validated):**
- The five open PRs' code merges stay clean (verified for #47 and by overlap scan for the rest at
  review time; re-verify at each integration).

## Definition of Done

- [ ] `agents/integrator/SKILL.md`, `agents/actions/integrate.md`,
      `agents/templates/prompts/evidence-contract/integrate-operator-friendly.md`, integration
      evidence template, `agent-map.yaml` registration, `actions/README.md` + `ROUTER.md` routing
- [ ] Acceptance criteria met including the poisoned-clean-merge test and a full dry run on PR #47
- [ ] The 5-PR merge train executed: 5 merges, 5 evidence runs, mainline green after each
      (tracked as the feature's Phase-A exit in `STATUS.md`)
- [ ] Contract-violation self-abort test (attempted source edit aborts the run)
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
