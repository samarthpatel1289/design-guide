# Findings format — `design-findings/v1`

The auditor's output, also read by schedulers (e.g. a proactive-watch sweep). Write a draft with
the fields below, then let `scripts/findings.py finalize DRAFT OUT [PREVIOUS]` add ids, statuses,
`resolved`, ranking, the summary, and a Markdown twin (`OUT.md`). Don't compute those by hand.

```json
{
  "schema": "design-findings/v1",
  "generated_at": "2026-01-31T09:00:00+00:00",
  "app": "Acme Notes",
  "config": "path/to/config.md",
  "inputs": [{"id": "s1", "path": "…/inbox.png", "kind": "screenshot|xcresult|url|code", "label": "inbox"}],
  "summary": {"blocker": 0, "major": 2, "minor": 3, "nit": 1, "new": 4, "resolved": 1, "accepted": 1},
  "resolved": ["9f2c1ab07e33"],
  "findings": [{
    "id": "3e1f0c9a7b2d",
    "status": "new | still | accepted",
    "severity": "blocker | major | minor | nit",
    "firmness": "law | guideline | taste",
    "category": "ux | brand | consistency | accessibility",
    "title": "Close button hit area is 28 pt",
    "where": {"screen": "inbox", "element": "search close button", "file": "optional/path.swift", "line": 42},
    "rule": {"id": "hig-target-44", "name": "Minimum hit target 44×44 pt", "source": "Apple HIG; WCAG 2.5.8"},
    "evidence": "Hierarchy frame 28×28 pt; neighbours 4 pt away.",
    "fix": "Keep the 17 pt glyph; pad the hit area to 44×44 with contentShape."
  }]
}
```

## Field rules
- **id** = first 12 hex of sha1(`category|rule.id|where.screen|where.element`, lower-cased). So
  keep `screen` labels (from `collect_screens.py`) and `element` names stable between runs —
  describe the element by role and position, not by content that changes.
- **status:** `new` (not in previous run), `still` (was there), `accepted` (covered by a recorded
  user decision — shown, never pushed, excluded from severity counts). Set `accepted` in the
  draft; finalize computes the other two.
- **severity** — how much it hurts people:
  - `blocker`: some people cannot complete a core task (unlabelled primary button, text that
    vanishes in dark mode, swipe-only core action).
  - `major`: a law is broken or a core flow is noticeably worse for many people.
  - `minor`: a guideline is broken, or a law breach on a rare path.
  - `nit`: polish.
- **firmness** is the rule's strength (see SKILL.md). `taste` findings can only be minor or nit.
- **evidence** is what you measured or saw — never personal data (no names, addresses, subjects,
  message text). Describe: "third row's sender line", not what it says.
- **fix** is concrete and uses the project's tokens/components.

## Ranking
`finalize` sorts accepted last, then severity, then firmness. Within that, list cross-screen
consistency problems once with all screens named in `where.screen` (e.g. "inbox, reader").
