# Acme Notes — design-guide config
repos: acme-notes-ios, acme-notes-web
platform: ios-swiftui, web-react
accessibility: WCAG 2.2 AA; Dynamic Type to AX5; VoiceOver; Reduce Motion; web 200% zoom
audit_inputs:
- ~/.claude/design-guide/screens/acme-notes/
- https://staging.acme-notes.example/
source_of_truth: ios/AcmeNotes/Theme/Theme.swift, web/src/theme/tokens.json

## Tokens
```json
{
  "colors": {
    "background":  {"light": "#FFFFFF", "dark": "#121212"},
    "surface":     {"light": "#F5F5F7", "dark": "#1E1E20"},
    "textPrimary": {"light": "#1C1C1E", "dark": "#F2F2F7"},
    "textMuted":   {"light": "#6E6E73", "dark": "#A1A1A6"},
    "accent":      {"light": "#3B5BDB", "dark": "#8DA2FB"},
    "onAccent":    {"light": "#FFFFFF", "dark": "#0B1033"},
    "danger":      {"light": "#C92A2A", "dark": "#FF8787"}
  },
  "pairs": [
    {"fg": "textPrimary", "bg": "background", "min": 4.5, "use": "body"},
    {"fg": "textMuted",   "bg": "background", "min": 4.5, "use": "timestamps, captions"},
    {"fg": "textMuted",   "bg": "surface",    "min": 4.5, "use": "captions on cards"},
    {"fg": "accent",      "bg": "background", "min": 4.5, "use": "link text"},
    {"fg": "onAccent",    "bg": "accent",     "min": 4.5, "use": "primary button label"},
    {"fg": "danger",      "bg": "background", "min": 4.5, "use": "error text"}
  ],
  "type": {
    "title": "SF Pro Display Bold 28, relativeTo .title",
    "body": "SF Pro Text 17, relativeTo .body",
    "caption": "SF Pro Text 13, relativeTo .footnote",
    "web_body": "Inter 16px / 1.5"
  },
  "spacing": [4, 8, 12, 16, 24, 32, 48],
  "radii": [8, 12, 20],
  "motion": {"quick": "easeOut 0.15s", "move": "spring(response 0.35, damping 0.85)"}
}
```

## Voice and tone
Friendly, brief, practical — a tidy friend, not a cheerleader. Second person ("your notes").
Errors say what happened and the next step, no exclamation marks. Success is one short line.
Words we use: note, notebook, tag, share. Words we avoid: document, file, item, "oops".

## Logo and imagery
Wordmark only on launch and About; never stretched or recoloured outside `accent`/`textPrimary`;
clear space = height of the "A". Illustrations: flat, two-tone (accent + surface), no people.

## Components
Primary button `AcmeButton(.primary)`; list row `NoteRow`; empty states `EmptyState(icon:title:action:)`;
toasts `Toast` with optional Undo (stays 6 s, until dismissed under VoiceOver).

## House rules
### HR-1 One primary action per screen
- **Rule:** at most one `AcmeButton(.primary)` visible per screen.
- **Firmness:** guideline
- **Provenance:** decided by the design lead, 2025-11-02, design review notes. Why: focus (von Restorff).
- **Status:** decided

### HR-2 Swipe actions also live in the note's ⋯ menu
- **Rule:** every swipe action on a row is also in the row's context menu and in VoiceOver actions.
- **Firmness:** law (house; WCAG 2.5.1)
- **Provenance:** decided by the team, 2025-12-10, after an accessibility audit.
- **Status:** confirmed (2026-01-15)

### HR-3 Delete has no confirmation
- **Rule:** deleting a note happens immediately with an Undo toast; no "Are you sure?".
- **Firmness:** guideline
- **Provenance:** decided by the product owner, 2026-01-05. Why: confirmations get clicked through.
- **Status:** questioned
- **Challenge:**
  - **Conflicts with:** WCAG 2.2.1 Timing Adjustable / 4.1.3 Status Messages — the Undo toast
    disappears after 6 s and is not announced, so screen-reader users can't reach Undo.
  - **Consequence:** for VoiceOver users, delete is irreversible.
  - **Proposal:** keep no-confirm; announce the toast and keep it until dismissed while VoiceOver
    runs; keep deleted notes in "Recently Deleted" for 30 days.
  - **Question:** Keep instant delete, with an announced, persistent Undo and a Recently Deleted folder?
