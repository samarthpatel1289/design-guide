# Accessibility — WCAG 2.2 and the platform minimums

Read this when a request or a screen touches text colour, sizes, gestures, motion, labels,
forms, toasts, or sign-in. Every entry has the same shape:

- **Firmness** — `law` (stop before building), `guideline` (push back once), `taste` (opinion only).
- **Threshold** — the number or condition that decides pass/fail.
- **Check** — how to verify instead of eyeballing.
- **Hook** — the short story for a first meeting with the idea.
- **Deeper** — the next layer, for the third time the user meets it.

WCAG level A and AA criteria are `law`; AAA criteria are `guideline`. A project config may raise
the target (e.g. "AAA for body text"), never lower a law silently — lowering one is a recorded
decision (see SKILL.md, "When the user overrules").

Never invent statistics for the consequence. Say what the person will experience ("the thumb
covers the whole button, so a quick tap often lands on the row behind it") and cite a number only
from the hooks below or a source you can name.

---

## Contents
1. Text contrast · 2. Non-text contrast · 3. Colour alone · 4. Tap target size ·
5. Dynamic Type / text resize · 6. Screen-reader names · 7. Gesture alternatives ·
8. Motion · 9. Status messages and timing · 10. Focus · 11. Forms and errors ·
12. Sign-in · 13. Platform switches people turn on

---

## 1. Text contrast — WCAG 1.4.3 (AA), 1.4.6 (AAA)
- **Firmness:** law (AA) · guideline (AAA)
- **Threshold:** 4.5:1 for normal text; 3:1 for large text (at least 18 pt / 24 px regular, or
  14 pt / ~18.7 px bold). AAA: 7:1 and 4.5:1. Placeholder text, disabled-looking-but-enabled text,
  timestamps and captions all count. Truly disabled controls and logos are exempt.
- **Check:** `scripts/measure.py contrast FG BG` for tokens; `measure.py pairs CONFIG` for every
  declared pair in light and dark; `measure.py sample SHOT.png x y w h` for a region of a
  screenshot (pixels). Check dark mode separately — a pair that passes in light often fails in dark.
- **Hook:** About 1 in 12 men has some colour-vision deficiency, and everyone is low-vision on a
  sunny pavement at 30% screen brightness. WebAIM's yearly scan of the top million home pages finds
  low-contrast text on roughly four out of five of them — it is the most common accessibility
  failure on the web. Light grey "for elegance" is how it happens.
- **Deeper:** Contrast is about *lightness*, not hue: a saturated red on a saturated green can
  look loud and still fail. WCAG 2's formula is known to overrate dark-on-light vs light-on-dark
  differently and ignores font weight; APCA (proposed for WCAG 3) models perceived lightness and
  asks thin or small type for more contrast. Use WCAG 2 for pass/fail today; use the APCA idea to
  explain why a 4.6:1 hairline font still feels faint.

## 2. Non-text contrast — WCAG 1.4.11 (AA)
- **Firmness:** law
- **Threshold:** 3:1 against adjacent colours for anything a person must see to use the UI:
  control boundaries (an outlined text field's border, an unselected checkbox ring), icons that
  carry meaning, focus indicators, chart lines.
- **Check:** `measure.py contrast` on the border/icon colour vs its background.
- **Hook:** The empty checkbox ring is often the *only* sign something can be selected. Draw it at
  1.5:1 and the feature is invisible to a lot of people — they never learn it exists.
- **Deeper:** Decorative separators are exempt; the test is "would a person miss a function if
  they missed this shape?" A selected state that differs only by a faint fill needs a second cue
  (checkmark, weight, shape).

## 3. Colour alone — WCAG 1.4.1 (A)
- **Firmness:** law
- **Threshold:** colour may not be the *only* way to convey state, meaning, or a call to action.
  Pair it with text, an icon, weight, shape, or position.
- **Check:** view the screenshot mentally in greyscale; would "unread", "error", "selected",
  "required" still read?
- **Hook:** Red/green is the most common deficiency (deuteranomaly). A form that marks errors only
  by turning the border red tells about 8% of men "nothing happened".
- **Deeper:** Redundant coding is not a tax — it helps everyone scan faster (preattentive features:
  shape and weight are read before colour by many people at a glance).

## 4. Tap/click target size — WCAG 2.5.8 (AA), 2.5.5 (AAA), platform minimums
- **Firmness:** law for the platform minimum on touch platforms and for WCAG 2.5.8; guideline above it.
- **Threshold:** Apple HIG 44×44 pt; Material 48×48 dp; WCAG 2.5.8 floor 24×24 CSS px, or enough
  spacing that a 24 px circle centred on each target does not touch another target. Inline links
  in text are exempt. The *hit area* is what counts, not the visible shape.
- **Check:** XCUITest "App UI hierarchy" attachments carry exact frames:
  `measure.py targets HIERARCHY.txt 44`. Otherwise measure the screenshot (pixels ÷ scale factor:
  @3x phones divide by 3) or read the code (`.frame`, padding, `contentShape`, `hitSlop`,
  CSS box size).
- **Hook:** In 1954 Paul Fitts, working on Air Force cockpit controls, showed that the time to hit
  a target grows with distance and shrinks with size. A fingertip is roughly 8–10 mm wide; Apple's
  44 pt is about 7 mm. Below that, people tap twice, or hit the neighbour — and on a destructive
  neighbour that's real damage.
- **Deeper:** Separate *visual* size from *hit* size — keep a small, quiet icon and give it a
  44 pt invisible hit area (SwiftUI `.contentShape(Rectangle())` with padding; CSS padding;
  Android `TouchDelegate`). Then think about *where*: Steven Hoober's field observations (2013)
  found about half of people use a phone one-handed, so frequent actions belong in the thumb's
  easy arc (bottom/middle), rare or dangerous ones at the top.

## 5. Dynamic Type / text resize — WCAG 1.4.4 (AA), 1.4.10 Reflow (AA), 1.4.12 (AA)
- **Firmness:** law
- **Threshold:** iOS: text uses Dynamic Type (or `relativeTo:` for custom fonts) and the layout
  survives every size up to AX5 (body grows from 17 pt to 53 pt) — no clipping, no overlap,
  truncation only where the full text is reachable. Android: `sp` units, survives 200% font scale.
  Web: 200% zoom without loss; reflow at 320 CSS px wide without horizontal scrolling; no fixed
  heights that clip when line-height/letter-spacing are increased.
- **Check:** AX-size screenshots (XCUITest with `UIPreferredContentSizeCategoryName`), code for
  fixed `.font(.system(size:))` without scaling, `lineLimit(1)` on important text, fixed heights.
- **Hook:** A big share of iPhone owners change the default text size, and the people who push it
  furthest are often the ones who most need your app to work — older parents, people with low
  vision. A layout that only works at the default size works for the designer.
- **Deeper:** At large sizes, horizontal layouts should *stack* (SwiftUI `ViewThatFits` or
  `dynamicTypeSize.isAccessibilitySize`), icons-plus-labels can become icon-only *only* if the
  label stays available to VoiceOver and Large Content Viewer, and scaling should be proportional
  for custom fonts (`Font.custom(_:size:relativeTo:)`).

## 6. Screen-reader names, roles, values — WCAG 1.1.1 (A), 4.1.2 (A), 2.5.3 Label in Name (A)
- **Firmness:** law
- **Threshold:** every control has an accessible name that says what it does ("Compose", not
  "square.and.pencil"); role is right (button, not static text); state is exposed (selected,
  expanded, unread); the visible label is contained in the accessible name (so Voice Control
  "tap Mark as Read" works); decorative images are hidden.
- **Check:** hierarchy attachments show `label:` and `value:`; empty labels, SF Symbol names,
  file names, or "button" alone are failures.
- **Hook:** In WebAIM's screen-reader survey about seven in ten mobile screen-reader users are on
  iPhone with VoiceOver. An unlabeled icon button is read as its image name — or just "button" —
  and the feature does not exist for them.
- **Deeper:** Group a row into one element with a summary label and custom actions instead of
  making people swipe through six fragments; order matters (sender before time); use hints
  sparingly — the name should carry the meaning.

## 7. Gesture alternatives — WCAG 2.5.1 Pointer Gestures (A), 2.5.7 Dragging Movements (AA)
- **Firmness:** law
- **Threshold:** anything done with a swipe, path, multi-finger gesture, or drag also works with
  a single tap/click (a button, a menu item) and is exposed to assistive tech (iOS
  `accessibilityActions`, Android custom actions). Swipe-only is a failure.
- **Hook:** Apple Mail's swipe-to-archive is also a button in the open message and an action in
  VoiceOver's rotor. Swipes are accelerators for experts, not the only door.
- **Deeper:** Gestures are invisible (Nielsen's "recognition rather than recall") — so even for
  sighted users, the first discovery path should be visible. Avoid conflicts with system gestures
  (iOS left-edge back swipe, home indicator, Android back).

## 8. Motion — WCAG 2.3.3 (AAA), 2.2.2 (A), platform Reduce Motion
- **Firmness:** law for honouring the OS Reduce Motion setting on native platforms and
  `prefers-reduced-motion` on the web; law for 2.2.2 (auto-moving content over 5 s can be paused);
  guideline for the rest.
- **Threshold:** under Reduce Motion, replace slides, zooms, parallax and bounces with fades or
  nothing; no flashing more than 3 times a second (2.3.1, A — law).
- **Hook:** When iOS 7 shipped its zooming, parallax home screen in 2013, people with vestibular
  disorders reported nausea; Apple added the Reduce Motion switch within weeks (iOS 7.0.3).
- **Deeper:** Motion should explain *where things went* (spatial continuity); motion that only
  decorates is the first thing to cut, with or without the setting.

## 9. Status messages and timing — WCAG 4.1.3 (AA), 2.2.1 Timing Adjustable (A)
- **Firmness:** law
- **Threshold:** toasts, "Saved", "Marked as read", error banners and result counts are announced
  to screen readers without moving focus (iOS `AccessibilityNotification.Announcement` /
  `UIAccessibility.post(.announcement)`, ARIA `role="status"`). Anything that disappears on a timer
  and offers an action (Undo) must give enough time — or stay until dismissed when VoiceOver is
  running — or let the user extend it.
- **Hook:** An Undo toast that vanishes in 4 seconds is fine for a fast sighted thumb and a trap
  for someone whose screen reader is still reading the previous row.
- **Deeper:** Undo beats confirmation dialogs (see `ux-laws.md`, user control) — but only if the
  Undo is reachable by everyone.

## 10. Focus — WCAG 2.4.7 (AA), 2.4.11 Focus Not Obscured (AA), 2.1.1 Keyboard (A), 2.4.3 (A)
- **Firmness:** law (web and keyboard/switch users on native)
- **Threshold:** every interactive element reachable by keyboard / Full Keyboard Access / Switch
  Control in a sensible order; focus visible (3:1 indicator); the focused element is not hidden
  under a sticky header, keyboard, or bottom sheet.
- **Hook:** Removing the browser's focus ring because "it looks ugly" is the single most common
  way designers lock keyboard users out.

## 11. Forms and errors — WCAG 3.3.1 (A), 3.3.2 (A), 3.3.3 (AA), 3.3.7 Redundant Entry (A), 1.3.5 (AA)
- **Firmness:** law
- **Threshold:** visible labels (not placeholder-only); errors identified in text next to the
  field and announced; suggestions offered when known; don't ask for the same information twice
  in one flow; set input purpose (`textContentType`, `autocomplete`) so autofill works.
- **Hook:** A placeholder that doubles as the label disappears the moment you start typing — so
  you are asked to remember the question while answering it.

## 12. Sign-in — WCAG 3.3.8 Accessible Authentication (AA)
- **Firmness:** law
- **Threshold:** no cognitive test to log in (no "type characters 3 and 7 of your password",
  no puzzle without an alternative). Allow paste, password managers, passkeys, and
  "Sign in with Apple/Google". Never block paste in password or code fields.
- **Hook:** Blocking paste "for security" pushes people towards short, memorable — guessable —
  passwords. The UK's National Cyber Security Centre has publicly said to let people paste.

## 13. Switches people turn on — test that the UI respects them
Bold Text, Increase Contrast / high-contrast, Reduce Transparency (glass and blur must stay
legible), Smart Invert / dark mode, Button Shapes, Differentiate Without Colour, larger cursor and
zoom (web). Missing support is a `guideline` finding unless it breaks a law above (e.g. text that
loses contrast under Reduce Transparency → law #1).
