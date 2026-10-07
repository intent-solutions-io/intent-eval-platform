# iep-spec-drift-auditor — accumulated catch-list

Operator-appended record of drift classes actually caught on the Intent Eval Platform.
The agent reads this first, every run, and re-checks each entry against current state.
**The agent does not edit this file — the operator appends after a confirmed catch.**

---

## 2026-07-19 — kernel CLAUDE.md understated its own published version

`intent-eval-core/CLAUDE.md` said "Published as `@intentsolutions/core@0.9.0`" while
`package.json` + tag `v0.10.0` were the truth (file mtime predated the 07-09 release).
**Check:** a repo's own CLAUDE.md "Published as / current version" line vs its package.json
`version` + newest git tag. Self-version drift is the highest-trust-surface class.

## 2026-07-19 — stale canonical-entity count in a sister-repo table

`intent-rollout-gate/CLAUDE.md` sister-repo table called the kernel "the 14 canonical
entities"; the current canonical count is **16** (13 Blueprint-B + SkillVersion + UsageEvent

+ HumanReview). **Check:** every "N canonical entities" across all 7 files against the current
count. Cross-repo tables drift independently — the same fact in six places goes stale in one.

## 2026-07-19 — a version fix in CLAUDE.md left the SIBLING README stale

The 0.9.0→0.10.0 kernel fix was applied to `intent-eval-core/CLAUDE.md` and the umbrella
`CLAUDE.md`, but the identical claim survived in `intent-eval-core/README.md:12` ("Status —
v0.9.0") and the umbrella `README.md:86` ("kernel is published (@…core@0.9.0)"). **Check:** a
repo carries its version/published claims in BOTH CLAUDE.md and README.md (+ CHANGELOG) — always
sweep all of them; a fix to one is not a fix to the repo. Same sweep also caught `intent-rollout-gate`
self-version behind (prose "v0.3.0" vs package.json/tag 0.3.2 — with version.txt=0.3.1 + no 0.3.2
CHANGELOG section, a release-bookkeeping mess to reconcile, not a clean doc typo) and a FALSE
"@intentsolutions/rollout-gate published at 2.1.0" (only 2.0.0 is on npm; 2.1.0 is an unpublished
workspace bump — cross-confirmed by memory reference_rollout_gate_package_name).

## Standing false-positive guards (do NOT flag these)

+ `"@intentsolutions/core": "^0.9.0"` dependency ranges — caret satisfies 0.10.0; a pinned
  older-but-valid range is not drift. Only narrative "Published as / current version" prose is.
+ `j-rig-binary-eval` (local FS dir) vs `j-rig-skill-binary-eval` (GH-canonical) — both legitimate.
+ `audit-harness` npm package + CLI + local dir names unchanged; only the *GitHub repo* renamed to
  `intent-audit-harness`. Flag only a claim wrong for its context.
