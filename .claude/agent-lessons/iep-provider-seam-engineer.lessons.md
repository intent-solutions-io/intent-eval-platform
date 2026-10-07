# iep-provider-seam-engineer — accumulated implementation lessons

Operator-appended record of provider-layer patterns and non-obvious gates that have
bitten this work. The agent reads this first, every task, and re-checks each entry.
**The agent does not edit this file — the operator appends.**

---

## Seed lessons (from the 2026-07-10 provider-seam publish — j-rig #203/#204)

1. **`workspace:^`, not a plain caret.** The CLI's `^0.2.0` range on `@intentsolutions/refiner`
   resolved the *published* refiner, so the shipped CLI lagged the workspace and lacked
   `refine score --provider`. Fix: `workspace:^` (links locally; `pnpm publish` rewrites to a
   caret). Verify a publish-shape change with a real clean `npm install`, never by inspection.

2. **Preset parity is a real invariant.** #204 existed only because the eval preset table had
   drifted from the refiner provider registry (openai preset missing on the eval side). Change
   both sides in one PR; add a parity test.

3. **OpenAI-compat correctness trio:** `response_format: json_object` for JSON calls; early
   empty-model guard (fail fast); op-parse tolerance (drop one malformed op, keep the rest).

4. **Anthropic-never-required is a hard line.** Auto-pick is `groq → deepseek → openai →
   anthropic → nvidia`-last. NEVER wire an Anthropic key into an automated/scheduled eval —
   unfunded providers fail closed with a clear error, they do not reroute to a paid model.
   (Cross-ref memory: automated evals must not burn Anthropic keys.)

5. **`@j-rig` scope 403s on publish.** Published scope is `@intentsolutions`; the CLI bundles the
   private `@j-rig/{core,db,migrate}` engine so external installs need no `@j-rig/*` resolution.
