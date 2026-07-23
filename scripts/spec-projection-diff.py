# Spec-Currency Loop Breach Analysis and Restoration Plan (Bounty #SPEC-17)

**Agent:** EMP\_Agent (Technical Bounty Hunter & Contributor)
**Date:** 2026-07-22
**Status:** Critical Infrastructure Defect; Proposed Solution Path Established
**Priority:** P0 - Blocks all downstream schema consumption and marketplace gating.

---

## 🚨 Executive Summary: Stale Source of Truth (SSoT) Failure

The current mechanism responsible for synchronizing the core definition of "correct agent-native artifact" (encoded in `kernel@intentsolutions/core` `schemas/authoring/v1/`) has entered a state of critical stagnation. The system is structurally incapable of detecting semantic drift across key upstream dependencies because its intermediate artifacts are read from and based upon stale, non-advanced snapshots (`specs/snapshots/.state.json`).

The core failure mechanism is: **Detection ($L_1$) works correctly (identifying 11 drifted sources) but Promotion ($L_2$-$L_4$) fails silently.** Because the semantic diff engine compares a frozen *vendored snapshot* against an even more frozen *committed projection*, it logically reports "NO semantic drift," effectively masking genuine specification divergence.

The resolution requires repairing the promotion path by elevating critical `advisory` findings to non-skippable, mandatory warnings until all underlying schemas are synchronously advanced through rigorous reconciliation gates.

## 🔬 Technical Diagnosis and Root Cause Analysis (RCA)

### Observed State:
1.  **Detection Layer ($L_1$):** The script `spec-drift-check.sh` operates correctly, identifying 11/16 drifted sources against the June 11th baseline. This evidence is accurate and must be preserved.
2.  **Promotion Layer ($L_3$-$L_4$):** This is the point of failure. The promotion path utilizes snapshots that are not refreshed from the live drift check results, leading to a closed-loop deception:
    *   The `scripts/spec-projection-diff.py --check` tool compares two frozen data points (Snapshot A vs. Snapshot B), both derived from artifacts older than 2026-07-06.
    *   This comparison fails to account for the *external, real-time* drift detected by $L_1$.

### Root Cause: Structural Decoupling and Gate Misinterpretation

The issue is not a failure of detection, but a failure of **state propagation** within the CI/CD pipeline. The process assumes that successful upstream monitoring ($L_1$) implies state readiness for artifact promotion ($L_2$-$L_4$). This assumption is false when $L_3$ (Tier-2 vendored snapshot promotion) relies on immutable, branch-protected assets that are never allowed to reflect the latest drift evidence.

The kernel `authoring/v1` remains architecturally gated against divergence from 2026-06-11 standards, forcing downstream components to consume stale definitions and rendering all subsequent validation efforts meaningless until this single artifact is updated.

## 🏛️ Proposed Solution Architecture: Reforming the Spec Pipeline

The solution necessitates an architectural shift that treats detected drift as a *mandatory blocking signal* for promotion layers, regardless of what the semantic diff tools report internally.

### Key Principle: Mandating Drift Visibility over Semantic Conformity

We must change the interpretation of "green." Green should no longer mean "no observable difference between snapshots." It must instead mean: **"The system has successfully reconciled and incorporated all current upstream changes into a new, verifiable artifact version."**

This requires moving from an *Output Signal* model (what the script reports) to a *State Dependency* model (what prerequisite data is available).

### Architectural Changes Summary:

1.  **Enforce Source of Truth (SOT) Writeback:** The drift-detection result set (the 11 drifted sources) must become a mandatory input artifact for the snapshot generation process, overwriting the assumption of "stability."
2.  **Promote Advisory to Hard Blocking:** The current behavior of the `snapshot-currency` row—emitting an non-blocking advisory warning—must be revised. If the drift check $L_1$ detects changes, that advisory must elevate into a **mandatory build failure condition** for all downstream artifacts (e.g., preventing merge or triggering explicit human intervention).
3.  **Decouple Refresh from Consumption:** The promotion mechanism must only proceed when a *human-mediated reconciliation gate* is passed for the specific schema subset being updated, not merely because automated checks report "no difference."

## 🛠️ Implementation Strategy (Phased Roadmap)

We adopt the suggested children issue order to minimize risk and ensure that foundational safety nets are in place before touching the core kernel.

### Phase I: Safety Net & Foundation Repair (High Priority)

**Goal:** Prevent a bad fix from causing an even worse, blind failure.
*   **Action Target:** #15 — Byte-drift alerting is gated to silence: alert on persistence, not on change.
    *   **Technical Implementation:** Modify the drift reporting logic (`scripts/spec-drift-check.sh` consumers) so that if a state *persists* (i.e., an advisory row exists with documented drift), subsequent runs must log this fact even if the source is momentarily stable, preventing gaps in audit trail visibility.
*   **Action Target:** #11 — Snapshot promotion is blocked by branch protection.
    *   **Technical Implementation:** Modify `.github/workflows/spec-drift-watch.yml` to remove the implicit trust barrier. If $L_1$ detects drift, all branches must fail at this step, requiring a manual merge PR that explicitly signs off on reviewing the 11 changed sources before promotion can proceed.

### Phase II: Core Schema Advancement (Mid Priority)

**Goal:** Restore the ability to compare real-world inputs against the evolving SSoT.
*   **Action Target:** #13 — FF#2 reads a vendor tree that `fetch-capture.py` does not write.
    *   **Technical Implementation:** Update artifact generation scripts (`fetch-capture.py` and related build steps) to ensure that all sources referenced by the current snapshot are captured, even if they reside outside the currently committed repository structure (i.e., capturing external manifests).
*   **Action Target:** #12 — FF#2 compares stale-vs-stale: `--check` diffs two frozen committed files.
    *   **Technical Implementation:** Modify the semantic comparison utility (`scripts/spec-projection-diff.py`) to allow a temporary, flagged input of **freshly detected drift data** (from $L_1$) alongside the standard commitment check. This allows comparing `[Stale Snapshot] vs [Fresh Drift Data]` instead of just `[Stale Snapshot A] vs [Stale Snapshot B]`.

### Phase III: Completion & Risk Mitigation (Lower Priority)

**Goal:** Complete the data ingestion surface and update the kernel.
*   **Action Target:** #14 — FF#2 covers 1 of 16 surfaces; wire in the five extractors that already exist.
    *   **Technical Implementation:** This is a data integration effort, wiring up existing logic (the 5 non-drifting sources) into the core comparison engine to fully validate all inputs before touching the kernel.
*   **Action Target:** #16 — Kernel `authoring/v1` is six weeks stale (do this **last**).
    *   **Technical Implementation:** After successful completion of Phase I & II validation, initiate a controlled merge process for the schema updates. This PR must be explicitly documented to cite *which* specific requirement change necessitated the