# Lessons — iep-kernel-engineer

Curated implementation playbook for `@intentsolutions/core` kernel changes. Patterns and non-obvious gates that have bitten kernel changes. Operator-appended; the agent does not self-edit.

## Python parity — the `models.py` wrapper idiom (NEVER edit `_generated/`)

- Generated Pydantic comes from `datamodel-code-generator`; fix parity in a `models.py` subclass wrapper (the `GateResultV1` precedent), never by editing `_generated/*.py` (erased on next codegen).
- **Optional-not-nullable** (field NOT in schema `required`, no `null` branch): wrapper `field: T = None  # type: ignore[assignment]` — annotation excludes None, so absence is allowed but explicit `null` is rejected. (origin: iec#57)
- **Required-but-nullable** (field IN `required`, `oneOf[T,null]`): wrapper `field: T | None` with NO default — key required, value nullable. The generated `T | None = None` wrongly makes the key omittable. (origin: Gemini HIGH iec#59)
- Cross-field invariants → a `@model_validator(mode="after")` on the wrapper. Mirror the JSON-Schema `if/then` and the Zod `superRefine` exactly.
- Verify in a throwaway venv: `python3 -m venv /tmp/v && /tmp/v/bin/pip install -q -e . pytest && /tmp/v/bin/python -m pytest tests/test_parity.py -q`. Remove the venv after. The Python parity/codegen gates run in `.github/workflows/python.yml`, NOT in local `pnpm run check`.

## Hash alphabet convention

- **Entities** use bare `sha256` (64-hex) for content-addressing — align entity hashes to `SkillSnapshot.combined_sha`. **In-toto predicates** use `sha256:`-prefixed (matches `gate-result/v1`). This split is deliberate; keep entity hashes bare and predicate hashes prefixed. A reference and its same-layer referent must share one alphabet (the D3 fix).

## Three-layer enforcement pattern

- JSON-Schema: `allOf` with `if/then` blocks (handle both branches, e.g. root vs non-root). Zod: `.superRefine((v,ctx)=>...)`. Pydantic: `@model_validator(mode="after")`. All three must reject the same violating case.
- Make closed-enum open/closed-world posture explicit in a `$comment`; note that widening a signed enum is a `/v2`.

## The CI gate chain (in order of how they've bitten — beyond `pnpm run check`)

1. **tsd** ("Type tests — second-opinion against published surface", `pnpm run test:types`): runs in the `lint + typecheck + test + build` CI job but is easy to miss locally. Any new/changed predicate or entity field → update the `test-d/*.test-d.ts` fixtures (add the new required field; spreads inherit it, standalone objects don't). (origin: iec#59)
2. **api-extractor golden snapshot**: new public fields drift `api/intentsolutions-core.api.md` → the "API diff report" step fails. FIX: `pnpm run api:extract` (builds + regenerates) and commit the snapshot in the same PR. The SemVer bump is the tag step, separate. (origin: iec#59)
3. **changelog-observance**: a `schemas/` change without a CHANGELOG entry fails. Add an `[Unreleased]` entry; if a prior `[Unreleased]` entry now misdescribes the shape, add a `### Changed` block that explicitly governs where it conflicts. (origin: iec#59)
4. **harness-hash --verify**: changing a hash-pinned file fails until `pnpm exec audit-harness init` re-pins; commit the updated `.harness-hash`. Note: `.harness-hash` pins `.github/workflows/*` in some repos but NOT `ALLOWLIST.md`. (origin: iel#172, iec#58)
5. **boundary checker**: a new top-level dotfile must be registered in `ALLOWLIST.md` (fenced block + annotation), then re-pin. New files under `schemas/`, `src/`, `python/`, `tests/` are fine. (origin: iec#58)

## Merge mechanics (intent-eval-* repos)

- Branch protection has `required_conversation_resolution: True` and `required_status_checks: strict` (must be up to date with main), but `required_approving_review_count: None`. So a fully-green PR can still show `BLOCKED` purely because review threads (e.g. Gemini inline comments) are unresolved. After addressing a thread's finding in code, RESOLVE the thread (GraphQL `resolveReviewThread`) — then it merges.
- `gh pr merge --squash --delete-branch` prints little on success; verify with `gh pr view <n> --json state`.

## Governance

- Two contradictory ratified clauses on a one-way-door artifact → HALT and escalate, never silently pick (DR-085 D1; `scripts/ratified-clause-conflict-check.sh` fires the reminder but cannot detect the contradiction — that's a human/reasoning duty).
- `@core` tag/publish is gated by DR directives; never tag without explicit go (it publishes npm + PyPI with sigstore provenance).
