# F0006-S0004 - `kg-source/` Shard Schema, Layout, and Ownership

## Story Header

**Story ID:** F0006-S0004
**Feature:** F0006 - Compiled Knowledge-Graph Projection and Governed Integration
**Title:** `kg-source/` shard schema, layout, and ownership
**Priority:** Critical
**Phase:** Platform Hardening (Feature Phase B)

## User Story

**As a** contributor (human or role agent) adding a feature's graph facts
**I want** a documented shard layer — one concept per small file, typed by directory, each directory owned by exactly one role — with a validated schema
**So that** independent features touch disjoint files (naturally mergeable), every shard has an unambiguous owner for conflict routing, and the compiler has a stable input contract.

## Context & Background

This story is the specification half of Phase B: the shard schema and ownership map must be agreed
before the compiler (S0005) or the migration (S0006) is built against them. It also settles the
classification questions earlier drafts left open: `solution-ontology.yaml` is curated source and
rehomes to `kg-source/ontology/` (keeping its embedded architect/PM ownership matrix authoritative
for its sections); `decisions-index.yaml` is confirmed generated. It records the `depends_on`
decision: the feature shard is the **single home** for feature dependencies; ROADMAP's dependency
mentions become projections.

Layout (per PRD §3): `nodes/{entities,capabilities,workflows,endpoints}/`, `features/`,
`bindings/`, `policies/`, `exclusions/`, `ontology/`. Semantic-ID strategy per PRD §4 (no sequence
numbers except REGISTRY-governed `F####`; no GUIDs for concepts). Logical doc refs per PRD §5.

## Acceptance Criteria

**Happy Path:**
- **Given** the schema spec and a new capability with its binding and owning feature
- **When** a contributor authors three shards (node, binding, feature) following the spec
- **Then** each file passes shard validation (id, kind/directory agreement, owner resolvable,
  logical doc refs only, references well-formed) and the schema documents every field they needed.

**Alternative Flows / Edge Cases:**
- A shard whose `kind` disagrees with its directory fails validation.
- A shard with a physical `planning-mds/features/...` doc ref fails with the logical-form hint.
- A shard file containing two top-level concepts fails ("one concept per file") unless the
  directory's spec explicitly allows a scoped bundle (e.g. an endpoint group).
- Ownership map covers every directory; a file outside mapped directories fails.
- The spec defines ID grammar per kind (`capability:kebab-case`, `entity:kebab-case`,
  `endpoint:resource-action`, `adr:NNN`, `schema:name`, `feature:F####`).
- Cross-shard references (`affects`, `governed_by`, `uses_schema`) are declared by ID only —
  resolution is the compiler's job, so shards never embed paths to other shards.

## Interaction Contract

N/A — specification + validation rules; no interactive surface.

| Surface / Entry Point | User Action | Editable State | Save / Mutation Result | Reload / Persistence Evidence | Roles / Status Constraints |
|-----------------------|-------------|----------------|-------------------------|-------------------------------|----------------------------|
| Shard files under `planning-mds/kg-source/**` | Author/edit a shard | The shard | Validated by compiler/`validate.py` | Deterministic re-validation | Directory owner role only |

## Data Requirements

**Deliverables:**
- Schema spec document (product repo `planning-mds/kg-source/README.md` + JSON Schemas per kind
  under `planning-mds/schemas/kg-source/`).
- Ownership map: directory → primary owner (+ co-sign), encoded both in docs and in
  `agents/agent-map.yaml` write scopes:
    - Primary architect: `nodes/`, `bindings/`, `policies/`, `ontology/`
    - Primary PM: `features/`
    - Co-sign: `exclusions/` (PM + architect), `ontology/` (+ PM per its embedded matrix),
      `policies/` (+ security where applicable)
  Co-sign is encoded as a secondary approver on the primary owner's scope, not a second write scope.

**Validation Rules:**
- Every shard: parseable YAML, required `id`, kind/directory agreement, single owner.
- Referential fields ID-only; doc refs logical-only; binding globs syntactically valid.

## Dependencies

**Depends On:** F0006-S0003 (routing table consumes the ownership map; Phase A complete).
**Related Stories:** F0006-S0005 (compiler consumes this contract), F0006-S0006 (migration emits
shards in this shape), F0006-S0009 (agent-map/docs encode the ownership).

## Business Rules

1. One concept (or one explicitly-allowed scoped bundle) per file.
2. Every directory has exactly one **primary owner role** (the conflict-routing target). Three
   directories additionally require **co-sign** on the relevant files/sections, which the
   compiler/validator records but does not auto-resolve:
   - `exclusions/` — PM + architect (symmetric: either-side change needs both).
   - `ontology/` — architect primary; PM co-sign on the sections its embedded ownership matrix
     assigns to PM.
   - `policies/` — architect primary; security co-sign where applicable (e.g. `authorization-*.yaml`).
3. Feature shards are the single home for feature `path`, `status`, and `depends_on`.
4. No shard may reference another shard by file path — IDs only.

## Out of Scope

- The compiler itself (S0005), populating the shards (S0006), tracker projection fields' rendering
  (S0007).

## Non-Functional Expectations

- Schema validation errors are actionable (name the file, field, rule, and fix).

## Questions & Assumptions

**Open Questions:**
- [x] Whether `policies/` needs security-role co-sign for authorization rules — **decided: yes**,
      security co-sign on `authorization-*.yaml` (per PRD §2 "security co-sign where applicable";
      encoded in the co-sign column of Business Rule 2).

**Assumptions (to be validated):**
- The current graph's node kinds map cleanly onto the four `nodes/` subdirectories (verify against
  the real `canonical-nodes.yaml` kind census during S0006).

## Definition of Done

- [ ] Schema spec + JSON Schemas reviewed and landed
- [ ] Ownership map encoded in docs and `agent-map.yaml`
- [ ] Shard validation implemented (standalone or in `validate.py`) with tests for every edge case
      above
- [ ] `depends_on` single-home decision recorded (here and in KNOWLEDGE-GRAPH.md via S0009)
- [ ] Story filename matches `Story ID` prefix
- [ ] Story index regenerated or updated

## Review Provenance

Story-level signoff provenance is recorded in the parent feature `STATUS.md`.
