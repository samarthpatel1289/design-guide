# UX laws and heuristics — Nielsen's 10 and the Laws of UX

Read this when a request changes flow, layout, choices, feedback, errors, or navigation, or when
an audit needs the "why" behind a UX finding. Same entry shape as `accessibility.md`
(firmness · test · hook · deeper). These are mostly `guideline`: well-evidenced, but context can
justify an exception — so push back once, clearly, then respect the decision.

Two of them become `law` in specific cases, called out below: destroying user data without a way
back (heuristics 3 and 5), and breaking an established platform convention (Jakob's law — see
`platforms.md` for the concrete conventions).

## Contents
Nielsen: H1 status · H2 real world · H3 control & freedom · H4 consistency · H5 error prevention ·
H6 recognition · H7 efficiency · H8 minimalism · H9 error recovery · H10 help
Laws: Fitts · Hick · Jakob · Miller · Doherty · Tesler · von Restorff · aesthetic-usability ·
peak-end · Gestalt (proximity, similarity, common region) · serial position · goal-gradient ·
Postel

---

## Nielsen's 10 usability heuristics (1994, refined from Nielsen & Molich 1990)

**H1 Visibility of system status** — guideline. People should always know what is happening:
loading, syncing, saved, sent, failed. Test: after every action, is there feedback within ~0.1 s
(acknowledge) and progress if it takes over ~1 s? Hook: the elevator button that lights up — it
doesn't make the lift faster, it stops you pressing it nine times. Deeper: honest status beats
optimistic status; a "Sent" that later turns out false costs more trust than a slower "Sending…".

**H2 Match between system and the real world** — guideline. Use the user's words, not the
database's ("Couldn't connect to Gmail", not "OAuth token refresh 401"). Test: would the user say
this sentence out loud? Hook: the Mac Trash can — people already knew what a bin does.

**H3 User control and freedom** — guideline; **law when an action destroys user data with no
way back** (no Undo, no Trash, no confirmation). Provide a clearly marked exit and Undo. Hook:
Gmail's "Undo Send" began as a Labs experiment in 2009 and became a permanent feature in 2015 —
a few seconds of reversibility removed a whole category of regret. Deeper: prefer Undo over "Are
you sure?" — confirmations get clicked through on autopilot; Undo lets people act fast *and* be safe.

**H4 Consistency and standards** — guideline (platform conventions → see Jakob, often law).
Same thing, same name, same look, same place, everywhere in the product. Test: list every place
the concept appears; do they match in wording, casing, icon, colour, position? This heuristic is
the backbone of the audit's `consistency` category. Hook: if "Archive" is a box icon on one screen
and a tick on another, people stop trusting either.

**H5 Error prevention** — guideline; **law for irreversible destructive actions placed where they
are easy to trigger by accident** (next to a frequent action, same style, no undo). Test: what
is the easiest mistake on this screen and what does it cost? Hook: in Hawaii's 2018 false
missile alert, investigators pointed to an alert menu of similarly worded options where a drill
and a live warning took the same few clicks — and no quick way to retract. Interface design was
part of the failure, not only the operator.

**H6 Recognition rather than recall** — guideline. Show options rather than make people remember
them: visible actions, recent searches, autocomplete, labels on icons. Hidden gestures and
icon-only toolbars lean on recall. Hook: nobody remembers which of five identical grey icons is
"snooze" — they hover, guess, or give up.

**H7 Flexibility and efficiency of use** — guideline. Accelerators for experts (swipes, shortcuts,
long-press menus) that novices don't need to know about. They are additions, never the only path
(see accessibility #7).

**H8 Aesthetic and minimalist design** — guideline. Every extra element competes with the ones
that matter. Test: delete it in your head — does anyone lose something they need? Hook: Google's
homepage in 1998 was a box and two buttons while portals like Yahoo crammed hundreds of links;
the sparse one became the default.

**H9 Help users recognise, diagnose and recover from errors** — guideline (WCAG 3.3.1/3.3.3 make
the form cases law). Plain-language problem + cause + a way out, placed where the problem is.
Test: does the message say what to do next, with a button that does it?

**H10 Help and documentation** — guideline. Best when not needed; when needed, in context and
task-focused. Note: a product may deliberately reject tutorials (a house rule) — then the design
itself must carry the learning (affordances, empty states, progressive disclosure).

---

## Laws of UX

**Fitts's law** — law at the platform minimum (see accessibility #4), guideline above it.
Time to acquire a target depends on distance and size. Big, close targets for frequent actions;
small, far ones for rare or dangerous ones. Hook: the Mac menu bar sits against the top edge of
the screen, so you can fling the pointer up and never overshoot — an "infinitely tall" target.
Deeper: edges and corners are the cheapest real estate on desktop; on phones, the bottom of the
screen is closest to the thumb, which is why iOS put tab bars and Safari's address bar down there.

**Hick's law (Hick–Hyman, 1952)** — guideline. Decision time rises with the number and
complexity of choices (roughly logarithmically). Fewer, clearer options; group and progressively
disclose the rest; highlight a recommended default. Hook: a restaurant with a 12-page menu makes
you slower *and* less happy with what you ordered. Deeper: Hick's law is about *decisions*, not
counting items — 30 options in a well-sorted alphabetical list are fast; 6 ambiguous ones are slow.

**Jakob's law (Nielsen, 2000)** — **law when it breaks platform muscle memory**, otherwise
guideline. People spend most of their time in *other* apps, so they expect yours to work the same
way. Hook: Snapchat's 2018 redesign rearranged where friends and stories lived; over a million
people signed a petition to undo it, and one celebrity tweet saying she no longer opened the app
was followed by a ~$1.3 billion drop in the company's market value that day. Deeper: you *can*
break a convention — when the new pattern is so much better that it's worth teaching, and you
pay that teaching cost on purpose. Most redesigns aren't.

**Miller's law (1956)** — guideline, and frequently misused. Working memory holds a handful of
chunks (Miller said 7±2; later research, e.g. Cowan 2001, suggests about 4). It is about what
people must *hold in their head*, not a cap on menu items or tabs. Use it for: chunking codes and
numbers (555-123-4567), not making people remember values between screens. Hook: you can read
back a 10-digit phone number only because it's chunked 3-3-4.

**Doherty threshold (Doherty & Thadani, IBM, 1982)** — guideline. When a system responds in under
~400 ms, people stay in flow; productivity rose sharply in their studies. Respond instantly
(optimistic UI where the action is safe and reversible), show progress for longer waits, keep
frequent animations short. Hook: the same IBM work argued that the *computer's* speed paid for
itself in human speed — time spent waiting is time people spend forgetting what they were doing.

**Tesler's law — conservation of complexity (Larry Tesler, Xerox PARC/Apple)** — guideline.
Every task has complexity that can't be removed, only moved — onto the user or into the system.
Absorb it in the system (smart defaults, autocomplete, inference). Hook: Tesler was the
"no modes" crusader behind modeless editing and cut/copy/paste; his licence plate read NO MODES.
Deeper: "simplifying" by removing a needed option just moves the complexity onto the user's
workaround.

**Von Restorff effect — isolation (1933)** — guideline. The one thing that looks different is
the one people notice and remember. Use it for the single primary action or the one thing that
needs attention; overuse kills it. Hook: highlight every line in a textbook and you've highlighted
nothing. Deeper: accent colour is a budget — spending it on decoration leaves nothing for the
call to action or the warning.

**Aesthetic–usability effect (Kurosu & Kashimura, Hitachi, 1995)** — guideline. People perceive
attractive designs as easier to use and forgive small problems in them. In the original study,
people rated ATM layouts as more usable when they found them more beautiful. Use it as a reason to
polish — and as a warning: pretty prototypes hide usability problems in testing.

**Peak–end rule (Kahneman et al., 1993; Redelmeier & Kahneman, 1996)** — guideline. People judge
an experience mostly by its most intense moment and its end. Make the peaks (finishing a task,
clearing the inbox, sending) and the ending moments feel good; fix the worst moment first. Hook:
Mailchimp shows a cartoon hand giving you a high-five at the most nerve-racking moment —
right after you hit send to thousands of people.

**Gestalt — proximity, similarity, common region, continuity** — guideline. People group what is
close together, looks alike, or shares a container. Test: are related things closer to each
other than to unrelated things (a label nearer its field than the previous field)? Do things that
behave alike look alike, and things that behave differently look different? Hook: put equal
spacing between a heading and the text above and below it, and readers can't tell which section
it belongs to. Deeper: spacing *is* information — internal spacing should be smaller than
external spacing (see `fundamentals.md`).

**Serial position effect** — guideline. People remember the first and last items best. Put key
navigation at the ends (first and last tabs), least important in the middle.

**Goal-gradient effect** — guideline. People speed up as they approach a goal; show progress and
start them partway when honest ("2 of 3 done"). Hook: car-wash loyalty cards needing 10 stamps
with 2 already filled were completed far more often than cards needing 8 from blank — the same
work, a head start (Nunes & Drèze, 2006).

**Postel's law — be liberal in what you accept** — guideline. Accept messy input (spaces in card
numbers, any phone format, pasted addresses with names) and normalise it; be strict and clear in
what you output.
