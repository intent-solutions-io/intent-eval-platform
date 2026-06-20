# Changelog — Intent Eval Platform

All notable releases across the six Intent Eval Platform repos, aggregated in one place.

This file follows the spirit of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
The platform has **no single version number** — each repo versions independently under
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) — so the aggregated section
below is organized by **release date**, newest first, rather than by one SemVer line.

- **Per-repo detail lives in each repo's own `CHANGELOG.md`** (linked below). This file is
  the cross-repo "what shipped where" index — not a replacement for them. For the full,
  categorized notes on any single release, open that repo's changelog.
- The region between the `AUTO:BEGIN` / `AUTO:END` HTML comments is **auto-generated** from
  each repo's GitHub Releases by [`scripts/aggregate-changelog.mjs`](./scripts/aggregate-changelog.mjs)
  via the [`aggregate-changelog`](./.github/workflows/aggregate-changelog.yml) workflow (daily,
  on `workflow_dispatch`, and on a `release-published` repository dispatch). **Do not hand-edit
  that region — your edits will be overwritten.** Put hand-written platform-level notes under
  [Unreleased], above the generated block.
- The repo set is read from [`ecosystem.json`](./ecosystem.json); `claude-code-plugins` is
  intentionally **not** aggregated here — it manages its own changelog.

Per-repo changelogs:
[core](https://github.com/jeremylongshore/intent-eval-core/blob/main/CHANGELOG.md) ·
[lab](https://github.com/jeremylongshore/intent-eval-lab/blob/main/CHANGELOG.md) ·
[audit-harness](https://github.com/jeremylongshore/intent-audit-harness/blob/main/CHANGELOG.md) ·
[j-rig](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/main/CHANGELOG.md) ·
[rollout-gate](https://github.com/jeremylongshore/intent-rollout-gate/blob/main/CHANGELOG.md) ·
[dashboard](https://github.com/jeremylongshore/intent-eval-dashboard/blob/main/CHANGELOG.md)

## [Unreleased]

Platform-level notes that span repos go here (hand-edited; survives regeneration).

- Cross-repo aggregated changelog introduced; every platform repo now ships a detailed
  Keep a Changelog of its own, and this umbrella index regenerates from their GitHub Releases.

<!-- AUTO:BEGIN -->

### 2026-06-20

- **intent-audit-harness [v1.2.3](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.2.3)**

### 2026-06-19

- **intent-eval-core [v0.8.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.8.0)** — docs: rebuild detailed Keep-a-Changelog CHANGELOG.md

### 2026-06-16

- **intent-audit-harness [v1.2.1](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.2.1)**
- **intent-audit-harness [v1.2.2](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.2.2)**
- **intent-eval-core [v0.7.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.7.0)** — feat(authoring): cross-schema invariant catalog + 6767-h coverage map + 3 CI gates [0h4u + 2t2p]

### 2026-06-15

- **intent-audit-harness [v1.2.0](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.2.0)**
- **intent-rollout-gate [v0.3.0](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.3.0)** — fix(release): dispatch-only production signing with reversible dry-run (drop sigstage); pre-flight always gates
- **j-rig-skill-binary-eval [v2.1.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v2.1.0)**

### 2026-06-13

- **intent-audit-harness [v1.1.8](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.1.8)**
- **intent-eval-core [v0.6.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.6.0)** — fix(validators): scoring open-world parity + NORMATIVE gate_reasons enforcement
- **intent-rollout-gate [v0.2.0](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.2.0)** — chore: record public gist id

### 2026-06-12

- **intent-rollout-gate [v0.1.0](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.1.0)** — v0.1.0 — M5 TypeScript MVP (experimental)
- **j-rig-skill-binary-eval [v2.0.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v2.0.0)**

### 2026-06-11

- **intent-eval-core [v0.4.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.4.0)** — feat: 4-fold isMarketplace authoring-tier decomposition (SAK foundation)
- **intent-eval-core [v0.4.1](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.4.1)** — release: v0.4.1 — relax skill-frontmatter allowed-tools to string|array (CCP shadow reconciliation)
- **intent-eval-core [v0.5.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.5.0)** — feat(iec): authoring/v2 skill-frontmatter — strict IS-marketplace contract (v0.5.0) [DR-049 / CCP-shadow parity]

### 2026-06-08

- **intent-audit-harness [v1.1.6](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.1.6)**
- **intent-audit-harness [v1.1.7](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.1.7)**
- **intent-eval-core [v0.3.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.3.0)** — iec-E12 — EvidenceBundlePayload + EvidenceStatement + cross-field invariants (I1 subject↔gate_id, I2 digest↔input_hash) + extensions escape hatch. Purely add…
- **intent-eval-core [v0.3.1](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.3.1)** — fix(ci): create-or-upload the GitHub Release for the evidence asset
- **intent-eval-lab [v0.3.0](https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.3.0)**
- **j-rig-skill-binary-eval [v1.2.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v1.2.0)**

### 2026-05-26

- **intent-eval-core [v0.1.1](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.1.1)**
- **intent-eval-lab [v0.2.0](https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.2.0)**
- **intent-rollout-gate [v0.0.1](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.0.1)**
- **j-rig-skill-binary-eval [v1.1.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v1.1.0)**

### 2026-05-17

- **intent-eval-core [v0.1.0](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.1.0)** — v0.1.0 — First public release

### 2026-05-13

- **j-rig-skill-binary-eval [v0.15.3](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.15.3)**
- **j-rig-skill-binary-eval [v0.16.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.16.0)**
- **j-rig-skill-binary-eval [v0.17.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.17.0)**
- **j-rig-skill-binary-eval [v0.18.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.18.0)**
- **j-rig-skill-binary-eval [v0.19.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.19.0)**
- **j-rig-skill-binary-eval [v0.20.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.20.0)**
- **j-rig-skill-binary-eval [v0.20.1](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.20.1)**
- **j-rig-skill-binary-eval [v0.21.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.21.0)**
- **j-rig-skill-binary-eval [v0.22.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.22.0)**
- **j-rig-skill-binary-eval [v0.23.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.23.0)**
- **j-rig-skill-binary-eval [v0.23.1](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.23.1)**
- **j-rig-skill-binary-eval [v0.23.2](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.23.2)**

### 2026-05-12

- **j-rig-skill-binary-eval [v0.15.1](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.15.1)**
- **j-rig-skill-binary-eval [v0.15.2](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.15.2)**

### 2026-05-10

- **intent-audit-harness [v0.2.0](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v0.2.0)**
- **intent-eval-lab [v0.1.0](https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.1.0)**

### 2026-05-08

- **j-rig-skill-binary-eval [v0.15.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.15.0)**

### 2026-05-01

- **j-rig-skill-binary-eval [v0.14.1](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.14.1)**

### 2026-04-22

- **intent-audit-harness [v0.1.0](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v0.1.0)** — v0.1.0 — initial release

### 2026-04-01

- **j-rig-skill-binary-eval [v0.14.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.14.0)**

### 2026-03-30

- **j-rig-skill-binary-eval [v0.10.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.10.0)**
- **j-rig-skill-binary-eval [v0.11.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.11.0)**
- **j-rig-skill-binary-eval [v0.12.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.12.0)**
- **j-rig-skill-binary-eval [v0.13.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.13.0)**
- **j-rig-skill-binary-eval [v0.7.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.7.0)**
- **j-rig-skill-binary-eval [v0.8.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.8.0)**
- **j-rig-skill-binary-eval [v0.9.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.9.0)**

### 2026-03-29

- **j-rig-skill-binary-eval [v0.3.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.3.0)**
- **j-rig-skill-binary-eval [v0.4.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.4.0)**
- **j-rig-skill-binary-eval [v0.5.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.5.0)**
- **j-rig-skill-binary-eval [v0.6.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.6.0)**

### 2026-03-25

- **j-rig-skill-binary-eval [v0.2.10](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.10)**
- **j-rig-skill-binary-eval [v0.2.11](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.11)**
- **j-rig-skill-binary-eval [v0.2.7](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.7)** — v0.2.7 - Templates & References Library
- **j-rig-skill-binary-eval [v0.2.8](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.8)**
- **j-rig-skill-binary-eval [v0.2.9](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.9)**

### 2026-03-24

- **j-rig-skill-binary-eval [v0.1.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.1.0)**
- **j-rig-skill-binary-eval [v0.2.0](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.0)**
- **j-rig-skill-binary-eval [v0.2.1](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.1)**
- **j-rig-skill-binary-eval [v0.2.2](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.2)**
- **j-rig-skill-binary-eval [v0.2.3](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.3)**
- **j-rig-skill-binary-eval [v0.2.4](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.4)**
- **j-rig-skill-binary-eval [v0.2.5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.5)**
- **j-rig-skill-binary-eval [v0.2.6](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/v0.2.6)**

---

**Pre-release (no tagged releases yet):** intent-eval-dashboard — tracked here; entries appear on first GitHub Release.

<!-- AUTO:END -->
