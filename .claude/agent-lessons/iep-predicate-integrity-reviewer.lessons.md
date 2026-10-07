# Lessons — iep-predicate-integrity-reviewer

Curated catch-list. Each entry is a real failure class caught on the Intent Eval Platform kernel. Re-run every one against the diff under review. The operator appends new entries after a review surfaces something the checklist missed; the agent does not self-edit this file (auditable, no drift).

Format: `- [SEV] <class> — <what to check> (origin)`

## Three-way schema↔Zod↔Pydantic drift

- [P0] **Required-but-nullable rendered omittable in Pydantic.** A field in the JSON-Schema `required` array typed `oneOf[T, null]` is *required* (key present) AND *nullable* (value may be null). `datamodel-code-generator` renders it `T | None = None` — the `= None` makes the KEY omittable, so Pydantic accepts a doc that omits it while AJV/Zod reject it. FIX: a `models.py` wrapper re-declares the field without a default (`field: T | None`). CHECK: read the schema `required` array, then confirm each required-nullable field is overridden. (origin: Gemini HIGH on iec#59, `parent_version_id`/`parent_content_hash` — a direction the 3-agent glance missed.)
- [P0] **Optional-not-nullable rendered nullable in Pydantic.** A field NOT in `required`, `$ref`-ing a type with no `null` branch (Zod `.optional()` not `.nullable()`), is optional-but-not-nullable. codegen renders `T | None = None` (nullable). FIX: wrapper override `field: T = None  # type: ignore[assignment]` (annotation excludes None; absence allowed, explicit null rejected). (origin: code-reviewer on iec#57 — `tenant_id`, `cost_record_ref`, `replay_fidelity_level`, `signing_downgrade_reason`.)
- Rule of thumb: NEVER edit `_generated/*.py` to fix drift — add/extend a `models.py` wrapper class (the `GateResultV1` precedent). Editing generated files is erased on the next codegen.

## Cross-artifact semantic consistency

- [P0] **Hash-alphabet mismatch between a reference and its referent.** A field typed `Sha256Prefixed` (`sha256:<hex>`) referencing a value typed bare `sha256` (64-hex) never byte-matches; each schema validates in isolation so no gate sees it. CHECK: trace every hash reference to its referent and confirm one alphabet. (origin: Hickey "most costly" — `SkillVersion.source_snapshot_hash` prefixed vs `SkillSnapshot.combined_sha` bare; D3 aligned both to bare.)
- [P1] **Same field name, opposite meaning across two artifacts.** `source_snapshot_hash` meant pre-edit input on the entity but post-edit output on the predicate. FIX: add a distinct name (`result_snapshot_hash` for post-edit) and make the shared name mean one thing everywhere. (origin: Kleppmann on iec#56.)
- [INFO] **Intentional layer split is OK — but document it.** Entities use bare `sha256` (content-addressing); in-toto predicates use `sha256:`-prefixed (matches `gate-result/v1`). That divergence is by design; a consumer crossing entity↔predicate must normalize. Don't flag it as a bug, but confirm it's deliberate (check gate-result's convention) before passing it.

## Unenforced invariants on signed rows

- [P0] **Acceptance gate asserted in prose, enforced nowhere.** `verdict:"accept" ⇒ every named_dimension_deltas[].non_regressed === true` was in the schema description + TS interface + DR, but had no JSON-Schema `if/then`, no Zod `superRefine`, no Pydantic `model_validator` — so an `accept` with a regressed dimension passed all validators AND both fixture suites. This is the core anti-laundering property; a falsified pass would be immutable on Rekor. CHECK: construct the violating body and confirm all three layers reject it. (origin: code-reviewer, the critical P0 on iec#56.)
- [P0] **Discriminator valid on a state it must not be.** `version_kind ∈ {revert,restore}` was schema-valid on a `parent_version_id:null` root (a shipped fixture did it). FIX: enforce `version_kind ∈ {revert,restore} ⇒ parent ≠ null` at all three layers + a standalone negative fixture. (origin: Hickey + code-reviewer.)

## Claims-vs-code

- [P1] **Docblock claims Statement-layer enforcement that isn't implemented.** The validator header said `subject.digest.sha256 === result_snapshot_hash` is "enforced at the Statement layer like gate-result I1/I2" — but `evidence-statement.ts` only handled `GATE_RESULT_V1`; no `SkillRefinerPassV1Statement` existed. CHECK: every "is enforced" claim in a docblock must point at real code. (origin: Kleppmann F5 on iec#56; tracked as iec#60.)

## Scripts / tooling that silently no-op

- [P0] **Detection regex that never matches.** A halt-gate script pattern `/schemas/.*\.schema\.json` had a leading slash, but `git diff --name-only` paths are root-relative — so it never fired. An advisory gate that detects nothing is worse than none. CHECK: run the script against a known-positive AND known-negative input; confirm it fires/stays-silent correctly. Also flag `"${ARR[@]:-}"` under `set -u` (iterates once on an empty string) — use `${ARR[@]+"${ARR[@]}"}`. (origin: Gemini HIGH on iel#175.)

## CI gates beyond `pnpm run check`

- [P1] **`tsd` "second-opinion against published surface"** runs in CI but may not be in the local `pnpm run check` — a fixture on an old shape (missing a newly-required field) fails only here. CHECK: `pnpm run test:types` after any predicate/entity field change.
- [P1] **`api-extractor` golden-snapshot drift.** New public fields drift `api/intentsolutions-core.api.md`; the API-diff gate fails until `pnpm run api:extract` regenerates + the snapshot is committed in the same PR. (origin: iec#59.)
- [P2] **`changelog-observance`** fails when `schemas/` changes without a CHANGELOG entry; **`harness-hash --verify`** fails when a hash-pinned file changes without `audit-harness init` re-pin; **boundary check** requires new top-level dotfiles in `ALLOWLIST.md`. (origin: iec#58/#59, iel#172.)
