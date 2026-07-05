# F0005-S0004 - Reconcile Framework Contract, Prompt, and KG Docs

## Story Header

**Story ID:** F0005-S0004
**Feature:** F0005 - Move-Invariant Knowledge-Graph Feature-Doc References
**Title:** Reconcile framework contract, prompt, and KG docs
**Priority:** High
**Phase:** Platform Hardening

## User Story

**As a** framework maintainer
**I want** the feature action, the operator prompt, and the KG docs updated to describe move-invariant references
**So that** the contract matches the shipped behavior — no phantom PM repoint step, and the "PM does not author the semantic graph" rule is finally true.

## Context & Background

Once the reference implementation (S0001–S0003) is green, the `nebula-agents` contract must be
reconciled. Today the contract is internally inconsistent: `KNOWLEDGE-GRAPH.md` line 294 already says
archiving is a single `feature-mappings.yaml` `path:` edit, while `feature.md` / the operator prompt
imply a path-sensitive coverage re-stale and the PM in practice repoints `canonical-nodes.yaml`
(which the same prompt forbids at line 118). F0005 removes the repoint entirely; the contract should
say so. These are wording changes — a step is removed, not added.

## Acceptance Criteria

**Happy Path:**
- **Given** the reference implementation is green
- **When** the contract surfaces are updated
- **Then** they describe feature-doc refs as logical/move-invariant, the only archive-time path edit
  is `feature-mappings.yaml`, and no step tells any role to repoint `canonical-nodes.yaml` /
  `code-index.yaml`.

**Specific edits:**
- `agents/actions/feature.md`:
  - G7 framing (Step 7 intro; gate-table row ~line 175): "binds **code** paths only (stable across
    the archive move)" → code globs *and* logical doc-refs are move-invariant; only
    `feature-mappings.yaml` carries the physical path.
  - Step 7 point 6 and the Forbidden bullet (~line 99): the coverage-ordering reason becomes "before
    the `feature-mappings.yaml` path update," not "before the archive move."
  - Step 8 (points 3–6): the PM's only path edit is the `feature-mappings.yaml` `path:` value; remove
    any implication of repointing the semantic graph.
  - Exit Validation step 9: coverage rationale reworded to reference the mappings update.
- `agents/templates/prompts/evidence-contract/feature-operator-friendly.md`:
  - Line 87 (G7 parenthetical), line 103 (defer-coverage reason), line 117 (feature-mappings as the
    sole path edit), line 120 (coverage rationale) reworded.
  - Line 118 ("Do NOT author `code-index.yaml` / `canonical-nodes.yaml` here") left in force and now
    consistent with reality.
- `agents/docs/KNOWLEDGE-GRAPH.md`: document the logical-ref format in the schema description
  (around line 122); confirm line 294 (single `path:` edit on archive) still holds.
- `agents/templates/feature-assembly-plan-template.md` and
  `agents/templates/kg-reconciliation-template.md`: any `source_docs` examples shown in logical form.

**Alternative Flows / Edge Cases:**
- `python3 agents/scripts/validate_templates.py` passes after edits.
- No new gate or step is introduced; the net line count of closeout steps does not grow.
- Cross-references between the three docs stay consistent (no doc still describes a repoint).

## Interaction Contract

N/A — documentation/contract edits.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| `agents/actions/feature.md`, operator prompt, `KNOWLEDGE-GRAPH.md`, templates | Edit docs | Markdown contract text | Contract describes move-invariant refs | `validate_templates.py` passes; review diff | Framework maintainer / Architect |

## Data Requirements

N/A — prose/contract content. The only structured artifact is the logical-ref grammar, documented in
`KNOWLEDGE-GRAPH.md`.

## Dependencies

**Depends On:**
- F0005-S0001, S0002, S0003 — the contract must describe shipped, green behavior, so it lands after
  the reference implementation.

**Related Stories:**
- None downstream.

## Business Rules

1. Describe shipped behavior only: no contract edit lands before the reference implementation is green.
2. Removal, not addition: the change deletes the phantom repoint and simplifies wording; it must not
   add a gate or step.
3. Consistency: after this story, no framework doc describes a PM repoint of the semantic graph.

## Out of Scope

- Any code or data change (S0001–S0003).
- Rolling the contract's reference implementation to additional product repos.

## Non-Functional Expectations

- Clarity: an operator reading only the prompt understands that archiving edits `feature-mappings.yaml`
  and nothing else in the graph.
- Consistency: `feature.md`, the operator prompt, and `KNOWLEDGE-GRAPH.md` agree.

## Questions & Assumptions

**Open Questions:**
- [ ] Should `kg-reconciliation-template.md` gain an explicit "feature-doc refs are logical" checkbox
      so each `G7` run affirms it?

**Assumptions (to be validated):**
- The reference implementation lands in at least one product repo before this story closes.

## Definition of Done

- [ ] Acceptance criteria met
- [ ] `feature.md`, operator prompt, `KNOWLEDGE-GRAPH.md`, and the two templates updated
- [ ] No framework doc still describes a PM repoint of `canonical-nodes.yaml` / `code-index.yaml`
- [ ] `validate_templates.py` passes
- [ ] Documentation cross-references consistent
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
