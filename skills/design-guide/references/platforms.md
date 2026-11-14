# Platform conventions — Apple HIG, Material, the web

Read this when the request touches navigation, system gestures, bars, sheets, alerts, control
styles, capitalisation, icons, or anything people have learned from other apps on the same
platform. Conventions that people have built muscle memory for are `law` (Jakob's law — breaking
them makes people fail, not just hesitate). Style preferences inside the convention are
`guideline` or `taste`.

Use the platform named in the project config. If the product ships on several, check each
screen against *its* platform — an iOS screen that copies an Android pattern (or the reverse) is
itself a finding.

## Apple platforms (iOS / iPadOS; Human Interface Guidelines)

**Law — muscle memory**
- Left-edge swipe goes back in a navigation stack. Don't hijack it with a custom horizontal
  gesture starting at the edge, and don't hide the back button without keeping the swipe.
- Bottom home indicator / swipe up = go home; top-right swipe = Control Center; top = notifications.
  Nothing important starts within those edge zones.
- Tab bar at the bottom for top-level sections, 2–5 items (more goes into "More" or a different
  structure); tabs switch sections, they never trigger actions.
- Destructive actions use the destructive (red) style, and a confirmation or Undo when the loss
  matters. In alerts the destructive button is not the default (bold) one.
- Alerts are for important, actionable interruptions only; two buttons side by side, Cancel on the
  left (or the conventional placement the system gives you).
- Sheets dismiss by swiping down unless data would be lost (then confirm or prevent).
- Pull to refresh at the top of a scrolling list; standard system share sheet; system pickers for
  dates/photos/files; Settings deep link for permissions.
- Respect Safe Areas (notch, Dynamic Island, home indicator).
- Permission prompts (notifications, contacts, location) are asked at the moment of value and with
  a clear purpose string; never trick or reward opting in (App Store rule 5.1.1 / 4.5.4).

**Guideline**
- Minimum hit target 44×44 pt (law via accessibility #4).
- Title-style capitalisation for buttons, menu items, alert buttons and tab/bar titles
  ("Mark as Read"); sentence case for body text, descriptions and alert messages.
- SF Symbols for system concepts, at the weight matching adjacent text; one icon style
  (outline vs fill) per role — iOS tab bars use filled for selected.
- Large titles collapse to inline titles on scroll; one primary action per screen.
- Use the system font sizes / text styles (Body 17 pt, Footnote 13, Caption 12) or custom fonts
  scaled `relativeTo:` a text style. Body text below 11 pt is a law finding only when it can't scale.
- Liquid Glass / materials (iOS 26+): controls float on glass over content; keep text on glass at
  contrast with Reduce Transparency on and off.
- Haptics confirm meaningful moments (success, selection change), not every tap.

## Android (Material Design 3)

**Law — muscle memory**
- System back (gesture or button) always goes back one step or closes the current layer; never
  swallow it. Predictive back preview on Android 14+.
- Bottom navigation bar 3–5 destinations; navigation drawer for more; top app bar with up arrow.
- Edge-to-edge with system bar insets respected.

**Guideline**
- Touch targets 48×48 dp.
- Sentence case for buttons and most UI text (Material's convention), unlike iOS.
- One floating action button per screen at most, for the primary action.
- Snackbars for brief feedback with at most one action (often Undo); dialogs for decisions.
- Material type scale (Display/Headline/Title/Body/Label), `sp` units.

## The web

**Law — muscle memory**
- Links look like links and go somewhere; buttons do something. Browser back works (don't break
  history with client routing); URLs are shareable for content states.
- Logo top-left links home; search is findable; standard form controls behave natively
  (Tab order, Enter submits, Esc closes dialogs).
- Never disable zoom (`user-scalable=no`) — also an accessibility law.

**Guideline**
- Body text 16 px or more; line length 45–75 characters.
- Primary navigation consistent across pages; visible focus styles.
- Respect `prefers-color-scheme` and `prefers-reduced-motion`.

## Hook bank for platform rules
- **Back gesture:** iPhone users perform the left-edge back swipe thousands of times a month
  without thinking. Override it and every one of those becomes a "huh?" — that's what "muscle
  memory" costs.
- **Title case vs sentence case:** this is the clearest example of a rule that is *platform
  taste made law by convention* — neither is objectively better, but mixing them inside one app
  reads as unfinished, and using the other platform's style reads as a port.
- **Tabs are not buttons:** a tab that performs an action (e.g. "Compose" in the tab bar) breaks the
  promise that tapping a tab only changes where you are. People then fear tapping tabs.
