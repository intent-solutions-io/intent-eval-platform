#!/usr/bin/env bash
# Wire CI secrets from the SOPS-encrypted secrets.ci.sops.yaml into the GitHub
# Actions secrets of each platform source repo. Idempotent — re-run any time the
# token rotates. Decrypts a single value in-process; never writes plaintext to
# disk and never prints the secret.
#
#   bash scripts/wire-ci-secrets.sh            # wire UMBRELLA_DISPATCH_TOKEN to all source repos
#
# Requires: sops + the IEP age key (~/.config/sops/age/keys.txt), gh (authenticated
# with admin on the source repos).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOPS_FILE="${HERE}/secrets.ci.sops.yaml"
SECRET_NAME="UMBRELLA_DISPATCH_TOKEN"
PLACEHOLDER="github_pat_REPLACE_ME"

# Source repos whose release.yml notify-umbrella-changelog job consumes the secret.
REPOS=(
  jeremylongshore/intent-eval-core
  jeremylongshore/intent-eval-lab
  jeremylongshore/intent-audit-harness
  jeremylongshore/j-rig-skill-binary-eval
  jeremylongshore/intent-rollout-gate
)

if [[ ! -f "$SOPS_FILE" ]]; then
  echo "ERROR: $SOPS_FILE not found." >&2
  echo "  Create it:  cp secrets.example.yaml secrets.ci.sops.yaml && sops secrets.ci.sops.yaml" >&2
  exit 1
fi

# Extract just the one value, decrypted in memory.
TOKEN="$(sops --decrypt --extract "[\"${SECRET_NAME}\"]" "$SOPS_FILE")"

if [[ -z "${TOKEN:-}" || "$TOKEN" == "$PLACEHOLDER" ]]; then
  echo "ERROR: ${SECRET_NAME} is empty or still the placeholder in $SOPS_FILE." >&2
  exit 1
fi

echo "Wiring ${SECRET_NAME} into ${#REPOS[@]} repos…"
for repo in "${REPOS[@]}"; do
  printf '%s' "$TOKEN" | gh secret set "$SECRET_NAME" --repo "$repo"
  echo "  ✓ ${repo}"
done
unset TOKEN

echo
echo "Done. Verify (shows name + updated_at only, never the value):"
echo "  gh secret list --repo ${REPOS[0]} | grep ${SECRET_NAME}"
