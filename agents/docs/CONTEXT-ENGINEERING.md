# Context Engineering

The framework-level reference for how agents keep their working context lean
and relevant: what gets loaded, when, in what form, and how it survives a long
session. This doc names the **strategy**; the mechanisms live in the docs it
links and are not restated here.

Most of the framework's retrieval machinery — the knowledge graph, role
scoping, `.agentignore`, the evidence cold-archive — exists to serve context
engineering. Naming the strategy makes those pieces legible as one discipline
instead of unrelated tools.

## The Four Moves

Context engineering here is organized around four moves. Every retrieval tool
in the framework serves at least one of them.

| Move | Goal | Primary mechanisms |
|------|------|--------------------|
| **Select** | Load only what is relevant | KG query layer, ROUTER, `.agentignore` |
| **Compress** | Fewest tokens per unit of context | tiered lookup, field projection, symbol granularity |
| **Write** | Persist context outside the window | `workstate.py`, KG-DECISION markers, STATUS.md |
| **Isolate** | Partition context by responsibility | per-role scopes, `{PRODUCT_ROOT}` split, sub-agents |

## Select — retrieve only what is relevant

The core discipline: **query an index, do not read the repo.**

| Practice | Tool / contract | Reference |
|----------|-----------------|-----------|
| Route before any code search | `hint.py <path>` (replaces blind grep) | KNOWLEDGE-GRAPH.md |
| Materialize a feature/file slice | `lookup.py` / `blast.py` — joins at query time; **raw yamls never enter context** | KNOWLEDGE-GRAPH.md |
| Follow the load order | `retrieval_contract` in `solution-ontology.yaml`: ontology → canonical-nodes → only the matching feature entry → one hop → raw files only when linked/changed/needed | KNOWLEDGE-GRAPH.md |
| Load only task-matched references | consult `ROUTER.md` before opening any `agents/<role>/references/` file | ROUTER.md |
| Skip cold archives | honor `{PRODUCT_ROOT}/.agentignore`; treat `planning-mds/operations/**` as cold — start from the evidence README + `latest-run.json` | AGENTIGNORE.md |

## Compress — fewest tokens per unit of context

| Practice | Tool / contract | Reference |
|----------|-----------------|-----------|
| Pull the minimum, expand on demand | `lookup.py F#### --tier 1/2/3/4` depth, `--fields ids/summaries/full` verbosity | KNOWLEDGE-GRAPH.md |
| Honor the minimal context contract | `minimum_prompt_block` in `solution-ontology.yaml` | KNOWLEDGE-GRAPH.md |
| Point at spans, not whole files | symbol + line-range results from `blast.py` / `lookup.py`; `diff-impact.py` maps a diff to symbols | KNOWLEDGE-GRAPH.md |
| Treat the KG as starting context | KG is a retrieval aid, not the answer — open raw artifacts only on conflict or verification (source precedence: raw wins) | KNOWLEDGE-GRAPH.md |

**Cache tiers.** Order what's loaded by volatility so the model pays cache *reads*
(≈0.1× input) rather than *writes* (≈1.25×) for stable material. Put a stable
prefix — system prompt, active `SKILL.md`, `ROUTER`, framework docs,
`SOLUTION-PATTERNS.md` — ahead of a volatile tail (current instruction, retrieval
results, latest tool output), and keep that prefix byte-stable (no per-turn
timestamps or ids inside it). A cache write only pays off when it's re-read before
it expires, so cache the re-read preamble and leave one-shot reads as plain input.
Reset context at task boundaries (e.g. between planning phases) so the cached
prefix doesn't grow unbounded — per-turn cost scales with context size.

## Write — persist context outside the window

The long-horizon resilience layer: externalize state so a session can recover
after compaction instead of re-deriving it.

| Practice | Tool / contract | Reference |
|----------|-----------------|-----------|
| Externalize session state | `workstate.py init` (role, scope, run-id); `dump --compact` to recover after compaction | KNOWLEDGE-GRAPH.md |
| Filter stale context | record decisions with `--supersedes`; read `dump --current-view` | KNOWLEDGE-GRAPH.md |
| Make context climbs explicit | `workstate.py escalate` records *why* raw artifacts were opened — governed expansion, not silent ballooning | KNOWLEDGE-GRAPH.md |
| Persist rationale at the edit site | inline `// KG-DECISION:` markers, harvested into `decisions-index.yaml` | KNOWLEDGE-GRAPH.md |
| Query current state, not history | `STATUS.md` rows are append-only audit; resolve "current" via the documented semantics | AGENT-USE.md |

## Isolate — partition context by responsibility

| Practice | Tool / contract | Reference |
|----------|-----------------|-----------|
| Scope each role's reads/writes | per-role read/write surfaces (backend → `engine/**`, frontend → `experience/**`, …) | AGENT-USE.md |
| Separate framework from product | `{PRODUCT_ROOT}` placeholder keeps `agents/**` context out of product context | AGENT-USE.md |
| Exclude outright | `{PRODUCT_ROOT}/.agentignore` removes paths from agent attention | AGENTIGNORE.md |
| Delegate to bounded sub-tasks | action orchestration runs agents within their declared scope | actions/README.md |

## Measurement — what makes it managed, not vibes

Context efficiency is observed, not assumed.

- `kg_common.estimate_tokens()` + `emit_telemetry()` stamp token estimates and a
  `--run-id` on every retrieval.
- `eval.py --since <ref>` scores retrieval quality against historical telemetry.
- Run/command telemetry is captured per the evidence contract in `AGENT-OPS.md`.

If a retrieval pattern starts costing more tokens or returning worse slices, the
telemetry shows it before it becomes habit.

## Known gaps — discipline, not enforcement

These are deliberate honesty about where the strategy relies on agents
following it rather than being forced:

- **No hard context budget.** The agent chooses the tier; nothing caps total
  context or forces tier-1-first. Convention, not a ceiling.
- **The write layer depends on the agent calling `workstate.py`.** Skip it and
  post-compaction recovery degrades to re-derivation.
- **Quality gating is partial.** Low-confidence / `ambiguous` edges *halt*
  action (good), but there is no automatic "you have loaded too much, compress"
  trigger.

A planned KG-retrieval MCP server strengthens **select + compress** by moving
the joins server-side, so only the compact structured slice ever reaches the
model — but it changes the delivery channel, not this strategy.

## Cross-References

- `agents/docs/KNOWLEDGE-GRAPH.md` — the KG query layer, `workstate.py`,
  retrieval contract, and tiering that serve Select / Compress / Write.
- `agents/docs/AGENT-USE.md` — session setup, per-role scopes, and prompt
  clauses that serve Isolate.
- `agents/docs/AGENTIGNORE.md` — `.agentignore` and cold-archive retrieval
  semantics.
- `agents/docs/AGENT-OPS.md` — the telemetry/evidence contract behind
  Measurement.
- `agents/ROUTER.md` — task-to-reference routing (Select for the reference
  corpus).
