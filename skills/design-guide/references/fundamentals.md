# Fundamentals — typography, colour, spacing, layout, motion, words

Read this when a request is about how something *looks* or *reads*, or when an audit checks
brand and consistency. Most of this is `guideline` or `taste`. The project config's tokens and
house rules are the source of truth for *this* product; these fundamentals explain why the config
says what it says, and fill gaps where it is silent.

## Typography
- **Hierarchy with few steps.** One display face, one text face is plenty (two families max);
  4–6 sizes in a modular scale (e.g. ×1.2–1.333). Differentiate levels with size *and* weight or
  colour, not size alone by 1 pt. — guideline
- **Readable body.** iOS body 17 pt (custom fonts ~15–17 pt scaled to `.body`); web 16 px+;
  line height ~1.3–1.6× for body, tighter for headings; line length 45–75 characters (Bringhurst's
  ~66 ideal). — guideline (law if it breaks contrast or resize)
- **Weights:** avoid light/thin weights below ~20 pt — they fail perceived contrast even when the
  ratio passes. — guideline
- **Numbers:** tabular figures for things that update or align (times, counts, prices). — taste
- **Truncation:** truncate the least important text first; never truncate the thing people scan
  for (sender, amount, name). — guideline
- **Capitalisation:** follow the platform (see `platforms.md`) and the config; whichever it is,
  one style per role across the whole product. Mixed casing on controls is a `consistency` finding.
- Hook: the serif for headlines + sans for text pairing is old newspaper logic — the serif carries
  voice at large sizes; the sans stays legible small on screens.

## Colour
- **Semantic tokens, not raw values.** Code should use `textPrimary`, `danger`, `accent` — never
  a hex literal in a view. A raw value in a component is a `brand` finding even if it happens to
  match. — guideline (house rule in most configs)
- **Accent is a budget.** One accent for "act here / selected"; status colours (danger, warning,
  success) reserved for status. If the accent decorates, it stops meaning "tap me" (von Restorff).
- **60-30-10** as a starting balance: dominant neutral, secondary surface, accent. — taste
- **Dark mode is its own palette**, not an inversion: lift surfaces with lightness rather than
  shadows, desaturate bright accents, avoid pure white text on pure black for long reading.
  Re-check every contrast pair in dark. — guideline (contrast part is law)
- **Never colour alone** — law (accessibility #3).
- Hook: Tiffany Blue, Coca-Cola red, Cadbury purple — companies trademark single colours because
  colour is recognised before shape or word. That's why "almost our blue" is brand drift.

## Spacing and layout
- **One spacing scale** (usually 4 or 8 pt steps). Off-scale values (13, 18, 22) are a
  `consistency` finding when the config defines a scale. — guideline
- **Internal ≤ external.** Space inside a group is smaller than space between groups (Gestalt
  proximity). Equal spacing everywhere flattens the structure. — guideline
- **Alignment:** a few strong alignment lines; text left-aligned in LTR languages for anything
  longer than a line; consistent leading margins across screens (screen padding is a token).
- **Corner radii:** a small set (e.g. 8/16/24) used by role; nested radius = outer radius − padding
  so inner corners look concentric. — taste/guideline
- **Density:** pick one density per surface type (list rows, cards) and keep it; a dense list next
  to an airy one looks like two products.
- Hook: Swiss grid designers in the 1950s showed that invisible alignment lines are what make a
  page feel "calm" — readers can't name the grid, but they feel its absence.

## Iconography
- One icon family and style (outline vs filled, stroke weight, corner style) per role. — guideline
- Icons that act need a visible label or a universally known meaning (search, share, close) —
  plus an accessible name always (law: accessibility #6).
- Don't use emoji as UI icons; they render differently per platform and read oddly to VoiceOver.

## Motion
- **Purpose:** motion explains change — where something came from, where it went, what's
  connected. Decoration-only motion is the first to cut. — guideline
- **Duration:** small UI changes ~100–200 ms; screen-size moves ~250–400 ms; exits a little faster
  than entrances; frequent actions short (Doherty). One small set of timings and curves across the
  product (a config token). — guideline
- **Easing:** ease-out for things arriving, ease-in for leaving, springs for direct manipulation;
  avoid linear for movement.
- **Reduce Motion:** law (accessibility #8).
- Hook: Disney's animators wrote down "slow in and slow out" in the 1930s; it is still the reason
  ease curves feel natural — nothing real starts or stops instantly.

## Words (voice, tone, microcopy)
- **Voice is constant, tone flexes.** The config describes the voice (e.g. calm, plain, warm);
  tone shifts for errors (more direct, no jokes) and success (brief). — guideline
- **Buttons are verbs** that say what happens ("Delete Account", not "OK"); the same action uses
  the same word everywhere ("Remove" vs "Delete" vs "Disconnect" for one thing is a
  `consistency` finding).
- **Errors:** what happened, why (if known), what to do — no blame, no codes in the headline.
- **Plain language:** short words, active voice, user's vocabulary (H2); no internal jargon or
  feature codenames in UI.
- **Numbers and dates** in one format per context.
- Hook: Mailchimp published its voice-and-tone guide for anyone to read; its core idea is that
  the voice stays the same while the tone follows how the reader feels right now — nobody wants a
  joke on the screen that says their payment failed.
