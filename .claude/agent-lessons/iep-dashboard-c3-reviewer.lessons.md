# iep-dashboard-c3-reviewer — accumulated catch-list

Operator-appended record of DR-035 § 8 integrity-binding violations (and near-misses)
caught on `intent-eval-dashboard/`. The agent reads this first, every review, and
re-checks each entry against the diff. **The agent does not edit this file.**

---

## Seed guidance (no catches yet — 2026-07-19)

No live catches recorded yet. Until this fills in, weight the review toward the two
classes most likely to slip past a green scanner:

1. **Structure over scanner.** The C3 defence is that no type carries an aggregate field
   and no function combines two dimensions. A diff adding a `rolledScore` / `overallScore` /
   `passPct` field — or any exported `roll*`/`aggregate*`/`composite*` symbol — is a violation
   even while `lint:c3` is still green. Check the *types*, not just the grep.

2. **No-data leak.** Trace every zero-row path. A bucket's `kind` must be `no-data` IFF row
   count === 0, with no carry-forward. The 25h-silent-worker test is the canonical proof; any
   change that lets a prior pass appear in an in-window bucket breaks the CFO/Gregg binding.

**Cardinal rule:** a diff that edits a `c3-scan` / `lint-uptime` / `arm-symmetry` gate to make
a test pass is the highest-severity finding there is — never let a weakened gate through.
