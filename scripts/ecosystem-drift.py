#!/usr/bin/env python3
"""
ecosystem-drift — REPORT-ONLY drift checker for the Intent Eval Platform.

Reads ecosystem.json and, for each repo whose automation is "report-only",
resolves the live upstream version (npm latest, or newest git tag) and compares
it to the manifest's pinned_version. Prints a markdown drift report.

SAFE-SLICE GUARANTEES (do not weaken without an explicit, reviewed change):
  * NEVER opens a PR, pushes a commit, or mutates any repo. Read-only.
  * NEVER touches repos in the manifest's "excluded" block (claude-code-plugins) —
    they are listed for visibility and skipped by design.
  * ALWAYS exits 0. Drift is advisory; this script has no exit authority.

Stdlib only. Network: registry.npmjs.org (no auth) + api.github.com (optional
GITHUB_TOKEN from env for higher rate limits). Soft-fails per repo.
"""
import json
import os
import sys
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "..", "ecosystem.json")


# Some registries/APIs (notably api.github.com) reject the default Python
# urllib User-Agent. Send a descriptive UA on every request, centrally.
_UA = "ecosystem-drift (+https://github.com/intent-solutions-io/intent-eval-platform)"


def _get_json(url, headers=None, timeout=15):
    hdrs = {"User-Agent": _UA}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def npm_latest(pkg):
    if not pkg:
        return None
    try:
        return _get_json(f"https://registry.npmjs.org/{pkg}/latest").get("version")
    except (urllib.error.URLError, ValueError, TimeoutError):
        return None


def newest_tag(gh):
    if not gh:
        return None
    headers = {"Accept": "application/vnd.github+json"}  # UA centralized in _get_json
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        tags = _get_json(f"https://api.github.com/repos/{gh}/tags", headers=headers)
        return tags[0]["name"] if tags else None
    except (urllib.error.URLError, ValueError, TimeoutError, KeyError, IndexError):
        return None


def _norm(v):
    return v.lstrip("v") if isinstance(v, str) else v


def resolve(repo):
    src = repo.get("version_source")
    if src == "npm":
        return npm_latest(repo.get("package"))
    if src == "git-tag":
        return newest_tag(repo.get("gh"))
    return None


def status_for(pinned, latest):
    if pinned is None and latest is None:
        return "untagged (no pin / no release)"
    if latest is None:
        return "unknown (lookup failed)"
    if pinned is None:
        return "untagged (no pin)"
    if _norm(pinned) == _norm(latest):
        return "current"
    return "BEHIND"


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        doc = json.load(f)

    rows, behind = [], 0
    for repo in doc.get("repos", []):
        if repo.get("automation") != "report-only":
            continue
        latest = resolve(repo)
        st = status_for(repo.get("pinned_version"), latest)
        if st == "BEHIND":
            behind += 1
        rows.append((repo.get("name", "unknown"), repo.get("version_source", "—"),
                     str(repo.get("pinned_version")), str(latest), st))

    lines = []
    lines.append(f"# Ecosystem drift report (report-only) — manifest v{doc.get('manifest_version')}")
    lines.append("")
    lines.append(f"Mode: **{doc.get('automation', {}).get('mode')}** · auto-PR: "
                 f"**{doc.get('automation', {}).get('auto_pr')}** · repos behind: **{behind}**")
    lines.append("")
    lines.append("| Repo | Source | Pinned | Latest upstream | Status |")
    lines.append("|------|--------|--------|-----------------|--------|")
    for name, src, pinned, latest, st in rows:
        lines.append(f"| {name} | {src} | {pinned} | {latest} | {st} |")
    excluded = doc.get("excluded", [])
    if excluded:
        lines.append("")
        lines.append("## Excluded from automation (skipped by design)")
        for ex in excluded:
            lines.append(f"- **{ex.get('name', 'unknown')}** — {ex.get('reason', 'excluded')}")
    lines.append("")
    lines.append("_Advisory only. This report opens no PRs and mutates nothing. "
                 "To act on drift, re-verify upstream and bump `pinned_version` in "
                 "`ecosystem.json` via a reviewed PR._")
    report = "\n".join(lines)

    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        try:
            with open(summary, "a", encoding="utf-8") as f:
                f.write(report + "\n")
        except OSError:
            pass

    # Advisory: never any exit-code authority.
    sys.exit(0)


if __name__ == "__main__":
    main()
