# Project config — format, drafting, and the decision review

The skill holds no project specifics. Each project has one Markdown config. Location (first hit
wins): `$DESIGN_GUIDE_CONFIG` · `design-guide.config.md` or `.claude/design-guide.config.md` in the
repo · `~/.claude/design-guide/projects/<name>.config.md` whose `repos:` line names the repo
(match against `git remote get-url origin`). Keep private projects' configs outside the repo if
the repo is public. A complete example: `examples/acme-notes.config.md` in the plugin root.

## Format

````markdown
# <App name> — design-guide config
repos: <repo-name>[, <repo-name>]
platform: ios-swiftui | android-compose | web-react | … (several allowed)
accessibility: WCAG 2.2 AA; Dynamic Type to AX5; VoiceOver; Reduce Motion
audit_inputs:
- ~/.claude/design-guide/screens/<app>/      # drop folder: fixture screenshots or .xcresult
- https://…                                  # a prototype or staging URL
source_of_truth: <path to tokens in code, e.g. App/DesignSystem/DesignSystem.swift>

## Tokens
```json
{
  "colors": {
    "background": {"light": "#FBF9F4", "dark": "#181715"},
    "textPrimary": {"light": "#141312", "dark": "#EEEBE5"},
    "accent": "#145CD1"
  },
  "pairs": [
    {"fg": "textPrimary", "bg": "background", "min": 4.5, "use": "body text"},
    {"fg": "accent", "bg": "background", "min": 3, "use": "icons, selected ring"}
  ],
  "type": {"display": "DM Serif Display 26/relativeTo title2", "body": "Inter 15/relativeTo body"},
  "spacing": [4, 8, 12, 16, 24, 32],
  "radii": [8, 16, 24],
  "motion": {"fade": "easeOut 0.2s", "move": "cubic(0.2,0.8,0.2,1) 0.35s"}
}
```
`measure.py pairs` reads this block: list every text/background and icon/background pair the
product actually uses, in light and dark.

## Voice and tone
<3–6 lines: who the product sounds like, words it uses and avoids, how errors and success read.>

## Logo and imagery
<logo clear space, colours, misuse; illustration/photo style; avatar rules.>

## Components
<the canonical components and where they live, so the auditor can say "use X instead".>

## House rules
### HR-1 <short title>
- **Rule:** <one sentence, testable>
- **Firmness:** law (house) | guideline
- **Provenance:** decided by <who>, <date>, <where it was recorded>. Why: <their reason>.
- **Status:** decided | questioned | confirmed (date)
- **Challenge:** <only when questioned — see below>
````

## Drafting a config when none exists
Offer once ("I can draft a design config from your code so I can check things against *your*
brand — want that?"). Then read, don't guess:
- iOS: `DesignSystem*.swift`, `Theme*.swift`, `Assets.xcassets/*.colorset`, `Font.custom` calls,
  `Info.plist` fonts. Android: `colors.xml`, `themes.xml`, `Theme.kt`/`Color.kt`/`Type.kt`.
  Web: `tailwind.config.*`, CSS custom properties, `theme.ts`, design-token JSON, Figma exports.
- Voice: the app's own strings (`Localizable.strings`, `strings.xml`, i18n JSON) — infer it from
  what's there, quote nothing personal.
- House rules: project docs (CLAUDE.md, AGENTS.md, design docs, ADRs), notes, the user.
Mark every inferred value `(inferred)` and every rule with its provenance. Show the user the
draft; they confirm before it becomes the source of truth.

## The decision review — recorded decisions are not ground truth
Project decisions (house rules, design docs, memory notes, "the owner decided X" records, and
guardian-mode overrides in the progress file) were made by people with the information they had.
Some are wrong, some went stale, some contradict each other. Treat each one like a new request:

1. Check it against the laws and guidelines in the references, against the other decisions, and
   against evidence that has appeared since (analytics, user feedback, platform changes).
2. If it holds, leave it `decided` (or `confirmed`).
3. If it conflicts with a **law**, a **strong guideline**, or another decision, set it to
   `questioned` and write the **Challenge**:
   - **Conflicts with:** the law/guideline/decision, by name and source.
   - **Consequence:** what users will experience, concretely (and a hook if useful).
   - **Proposal:** the smallest change that keeps the decision's intent.
   - **Question:** one question the decision-owner can answer yes/no or pick from.
4. Never silently override a recorded decision, and never silently obey one that breaks a
   law. Keep building to the decision until the owner re-decides — except for a law conflict,
   where you say so each time you'd have to build the violation (once per scope, not per line).
5. When the owner re-decides, update **Status** to `confirmed (date)` or rewrite the rule, and
   keep the old reason in the provenance — the history is part of the lesson.

Run the review when you first adopt or draft a config, when the user asks, and in audits
(questioned rules appear as findings with category = the rule's area and `firmness` of the law
they conflict with).
