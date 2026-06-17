#!/usr/bin/env node
// Aggregate the platform-wide changelog from each sub-repo's GitHub Releases.
//
// Zero-dependency Node (ESM, Node 20+). The repo list is read from ecosystem.json
// (the single source of truth — it already lists the six platform repos and keeps
// claude-code-plugins in the `excluded` block, which this script never touches).
//
// For each repo we pull GitHub Releases via the `gh` CLI (which reads GH_TOKEN /
// GITHUB_TOKEN from the environment; public release data is readable cross-org with
// the default Actions token). We render a date-stamped, newest-first section and
// splice it between the AUTO:BEGIN / AUTO:END markers in CHANGELOG.md, leaving the
// hand-written intro + [Unreleased] region untouched.
//
// Deterministic by construction (output depends only on upstream release data, never
// on the wall clock), so a second run with no new releases produces no diff.
//
// Prints "changed" or "no-change" and always exits 0 on success.

import { readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const MANIFEST = resolve(REPO_ROOT, 'ecosystem.json');
const CHANGELOG = resolve(REPO_ROOT, 'CHANGELOG.md');
const BEGIN = '<!-- AUTO:BEGIN -->';
const END = '<!-- AUTO:END -->';

/** One-line, deterministic summary for a release ('' when nothing descriptive). */
function summarize(rel) {
  const tag = (rel.tag_name || '').trim();
  const name = (rel.name || '').trim();
  if (name && name.toLowerCase() !== tag.toLowerCase()) return finalize(name, tag);
  const body = (rel.body || '').replace(/\r/g, '');
  for (const rawLine of body.split('\n')) {
    let line = rawLine.trim();
    if (!line) continue;
    line = line.replace(/^#{1,6}\s*/, '').trim(); // strip heading markers
    if (!line) continue;
    if (/^what'?s\s+changed$/i.test(line)) continue;
    if (/^full\s+changelog/i.test(line)) continue;
    line = line.replace(/^[-*+]\s+/, '').replace(/\*\*/g, '').trim(); // strip bullet + bold
    if (!line) continue;
    return finalize(line, tag);
  }
  return '';
}

function finalize(raw, tag) {
  // Strip GitHub's auto-generated "by @user in <pr-url>" attribution tail.
  let s = raw.replace(/\s+by @[\w-]+ in https?:\/\/\S+$/i, '').trim();
  s = s.replace(/\s+/g, ' ').trim();
  // Drop bare auto-titles like "audit-harness v1.2.1" / "intent-eval-lab v0.3.0" —
  // they only restate the bolded repo+tag link, adding no information.
  const ver = tag.replace(/^v/, '');
  if (ver && s.includes(ver) && s.split(/\s+/).filter(Boolean).length <= 3) return '';
  return s.length > 160 ? s.slice(0, 157).trimEnd() + '…' : s;
}

/** Fetch all (non-draft, published) releases for a repo via the gh CLI. */
function fetchReleases(ghSlug) {
  let raw;
  try {
    raw = execFileSync('gh', ['api', `repos/${ghSlug}/releases`, '--paginate'], {
      encoding: 'utf8',
      maxBuffer: 64 * 1024 * 1024,
    });
  } catch (err) {
    const msg = err && err.stderr ? String(err.stderr) : String(err);
    throw new Error(`gh api failed for ${ghSlug}: ${msg.trim()}`);
  }
  // --paginate concatenates JSON arrays; join them into one.
  const arrays = raw
    .split(/\n(?=\[)/)
    .map((chunk) => chunk.trim())
    .filter(Boolean)
    .map((chunk) => JSON.parse(chunk));
  const releases = [].concat(...arrays);
  return releases.filter((r) => !r.draft && r.published_at);
}

function main() {
  const manifest = JSON.parse(readFileSync(MANIFEST, 'utf8'));
  const repos = (manifest.repos || []).map((r) => ({ name: r.name, gh: r.gh }));

  const rows = [];
  const preRelease = [];
  for (const repo of repos) {
    const releases = fetchReleases(repo.gh);
    if (releases.length === 0) {
      preRelease.push(repo.name);
      continue;
    }
    for (const rel of releases) {
      rows.push({
        repo: repo.name,
        tag: (rel.tag_name || '').trim(),
        date: rel.published_at.slice(0, 10),
        url: rel.html_url,
        summary: summarize(rel),
      });
    }
  }

  // Newest first by date; deterministic tie-break by repo then tag.
  rows.sort((a, b) => {
    if (a.date !== b.date) return a.date < b.date ? 1 : -1;
    if (a.repo !== b.repo) return a.repo < b.repo ? -1 : 1;
    return a.tag < b.tag ? -1 : 1;
  });

  const byDate = new Map();
  for (const row of rows) {
    if (!byDate.has(row.date)) byDate.set(row.date, []);
    byDate.get(row.date).push(row);
  }

  const sections = [];
  for (const [date, items] of byDate) {
    const bullets = items.map((it) => {
      const head = `- **${it.repo} [${it.tag}](${it.url})**`;
      return it.summary ? `${head} — ${it.summary}` : head;
    });
    sections.push(`### ${date}\n\n${bullets.join('\n')}`);
  }

  let rendered = sections.join('\n\n');
  if (preRelease.length > 0) {
    const list = preRelease.sort().join(', ');
    const note = `**Pre-release (no tagged releases yet):** ${list} — tracked here; entries appear on first GitHub Release.`;
    rendered = rendered ? `${rendered}\n\n---\n\n${note}` : note;
  }
  if (!rendered) rendered = '_No releases found across the platform repos yet._';

  const original = readFileSync(CHANGELOG, 'utf8');
  // Anchor the markers to their own lines so an inline mention of the marker
  // text elsewhere in the file (e.g. in the intro) can never be matched.
  const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const marker = new RegExp(`^${esc(BEGIN)}$[\\s\\S]*?^${esc(END)}$`, 'm');
  if (!marker.test(original)) {
    throw new Error(`CHANGELOG.md is missing the ${BEGIN} / ${END} marker pair (each on its own line).`);
  }
  const updated = original.replace(marker, `${BEGIN}\n\n${rendered}\n\n${END}`);

  if (updated === original) {
    console.log('no-change');
    return;
  }
  writeFileSync(CHANGELOG, updated);
  console.log('changed');
}

main();
