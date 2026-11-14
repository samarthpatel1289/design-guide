# design-guide

A Claude skill that is your app's **design guide and design engineer** at once.

- **Guardian** — when you ask for a UI or UX change, it checks the request against firm design
  laws first (WCAG 2.2, Apple HIG, Material, Nielsen's heuristics, the Laws of UX, typography /
  colour / spacing / motion fundamentals). If the request breaks one, it stops, says plainly
  which rule and what will happen to real people, and offers a version that keeps your intent.
  You can still overrule it; it records your decision and stops nagging.
- **Auditor** — give it screenshots, a folder, an Xcode `.xcresult`, a URL or code, and it returns
  ranked findings (UX, brand drift, inconsistency, accessibility) as JSON + Markdown. Schedulers
  can call it; findings carry stable ids so a run can report only what's new.
- **Teacher** — every rule comes with a short, true story (Fitts and the cockpit, the Snapchat
  redesign, the iOS 7 motion sickness) and a before/after. It remembers what you've learned, so
  the third time you meet a law it shows you the deeper idea instead of repeating itself.

It also questions **your own past decisions**: house rules, design docs and old overrides are
checked against the same laws, and anything that now looks wrong comes back to you as a question
— never silently overridden, never silently obeyed.

## Install

Claude Code, as a plugin:

```bash
claude plugin marketplace add samarthpatel1289/design-guide
```
```bash
claude plugin install design-guide@design-guide
```

Or clone and copy just the skill:

```bash
git clone https://github.com/samarthpatel1289/design-guide && cp -R design-guide/skills/design-guide ~/.claude/skills/
```

Claude.ai / Claude Desktop: zip `skills/design-guide` and upload it under Settings → Capabilities → Skills.

Requirements: Python 3.9+ (stdlib only). Xcode's `xcrun` only for `.xcresult` input.

## Set up your project (two minutes)

Ask Claude: *"Draft a design-guide config for this repo."* It reads your tokens/theme files and
strings, and drafts `design-guide.config.md` for you to confirm. Or copy
[`examples/acme-notes.config.md`](examples/acme-notes.config.md) and edit it. A config holds:

- colour tokens (light/dark) and the text/background pairs you actually use — `measure.py pairs`
  checks every one against WCAG;
- type scale, spacing scale, radii, motion timings;
- voice and tone, logo and imagery rules, canonical components;
- platform and accessibility targets;
- `audit_inputs` — where screens for scheduled audits come from;
- house rules, each with provenance (who decided, when, why) and status
  (`decided` / `questioned` / `confirmed`).

Put the config in the repo, or — for a private project — in
`~/.claude/design-guide/projects/<name>.config.md` with a `repos:` line naming your repo.

Your learning progress and decisions live in `~/.claude/design-guide/progress.md`.

## Try it

- "Make the delete button smaller and put it next to Save." → expect a Guardian stop.
- "Audit the screenshots in ./shots against our config." → ranked findings.
- "Why does everyone say 44 points?" → a lesson.

## Use from a scheduler

Invoke the skill in audit mode with a config, an output path and (optionally) the previous
findings file. With no inputs it uses the config's `audit_inputs`; if nothing changed it writes
nothing. Output format: [`references/findings-format.md`](skills/design-guide/references/findings-format.md).

```bash
python3 skills/design-guide/scripts/findings.py finalize draft.json findings.json previous.json
```

## Scripts (all stdlib)

| Script | Does |
|---|---|
| `measure.py contrast FG BG` | WCAG contrast ratio and AA/AAA verdicts |
| `measure.py pairs CONFIG` | checks every declared colour pair, light and dark |
| `measure.py sample SHOT.png X Y W H` | contrast inside a screenshot region |
| `measure.py targets HIERARCHY.txt [44]` | undersized controls from an XCUITest UI hierarchy |
| `collect_screens.py OUT INPUT…` | images / folders / `.xcresult` → labelled screen list |
| `findings.py finalize\|render\|validate` | ids, new/still/resolved, ranking, Markdown |

## Companions

Works alongside `ui-ux-pro-max` (searchable design data) and `frontend-design` (new visual
direction) if you have them. This skill guards, audits and teaches; it doesn't invent a brand.

## License

MIT
