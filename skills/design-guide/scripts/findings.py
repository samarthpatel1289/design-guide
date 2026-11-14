#!/usr/bin/env python3
"""Finalize, render and validate design-findings/v1 files (format: references/findings-format.md).

  findings.py finalize DRAFT.json OUT.json [PREVIOUS.json]
      Adds stable ids, marks each finding new/still (accepted stays accepted), lists ids that
      disappeared since PREVIOUS as resolved, ranks, counts, validates, and writes OUT.json plus
      a Markdown twin OUT.md.
  findings.py render FILE.json      Markdown to stdout
  findings.py validate FILE.json    exit 1 with reasons when the file breaks the format
  findings.py selftest
"""
import datetime
import hashlib
import json
import sys

SEVERITY = ["blocker", "major", "minor", "nit"]
FIRMNESS = ["law", "guideline", "taste"]
CATEGORY = ["ux", "brand", "consistency", "accessibility"]
STATUS = ["new", "still", "accepted"]
REQUIRED = ["title", "severity", "firmness", "category", "where", "rule", "evidence", "fix"]


def finding_id(f):
    key = "|".join([f["category"], f["rule"].get("id", ""), f["where"].get("screen", ""),
                    f["where"].get("element", "")]).lower()
    return hashlib.sha1(key.encode()).hexdigest()[:12]


def problems(doc):
    out = []
    if doc.get("schema") != "design-findings/v1":
        out.append("schema must be design-findings/v1")
    for i, f in enumerate(doc.get("findings", [])):
        out += [f"findings[{i}]: missing {k}" for k in REQUIRED if not f.get(k)]
        for k, allowed in (("severity", SEVERITY), ("firmness", FIRMNESS),
                           ("category", CATEGORY), ("status", STATUS)):
            if f.get(k) and f[k] not in allowed:
                out.append(f"findings[{i}].{k}={f[k]!r} not in {allowed}")
        if f.get("firmness") == "taste" and f.get("severity") in ("blocker", "major"):
            out.append(f"findings[{i}]: taste can be minor or nit, never {f['severity']}")
    return out


def finalize(draft, previous=None):
    doc = dict(draft, schema="design-findings/v1")
    doc.setdefault("generated_at", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
    before = {f["id"] for f in (previous or {}).get("findings", []) if f.get("status") != "accepted"}
    for f in doc["findings"]:
        f["id"] = finding_id(f)
        if f.get("status") != "accepted":
            f["status"] = "still" if f["id"] in before else "new"
    # Two drafts of one problem collapse to the first; the id is the identity.
    doc["findings"] = list({f["id"]: f for f in reversed(doc["findings"])}.values())[::-1]
    doc["findings"].sort(key=lambda f: (f["status"] == "accepted", SEVERITY.index(f["severity"]),
                                        FIRMNESS.index(f["firmness"])))
    now = {f["id"] for f in doc["findings"]}
    doc["resolved"] = sorted(before - now) if previous else []
    live = [f for f in doc["findings"] if f["status"] != "accepted"]
    doc["summary"] = {s: sum(f["severity"] == s for f in live) for s in SEVERITY}
    doc["summary"].update(new=sum(f["status"] == "new" for f in live), resolved=len(doc["resolved"]),
                          accepted=len(doc["findings"]) - len(live))
    return doc


def render(doc):
    s = doc["summary"]
    lines = [f"# Design audit — {doc.get('app', 'app')}", "",
             f"{doc['generated_at']} · {len(doc.get('inputs', []))} screens · "
             f"{s['blocker']} blocker · {s['major']} major · {s['minor']} minor · {s['nit']} nit · "
             f"{s['new']} new · {s['resolved']} resolved · {s['accepted']} accepted", ""]
    for n, f in enumerate(doc["findings"], 1):
        w, r = f["where"], f["rule"]
        place = " · ".join(str(v) for v in (w.get("screen"), w.get("element"), w.get("file")) if v)
        lines += [f"## {n}. {f['title']}",
                  f"**{f['severity']}** · {f['firmness']} · {f['category']} · {f['status']} · `{f['id']}`  ",
                  f"**Where:** {place}  ",
                  f"**Rule:** {r.get('name', '')} ({r.get('source', '')})  ",
                  f"**Evidence:** {f['evidence']}  ",
                  f"**Fix:** {f['fix']}", ""]
    if doc.get("resolved"):
        lines += ["## Resolved since last run", ", ".join(f"`{i}`" for i in doc["resolved"]), ""]
    return "\n".join(lines)


def selftest():
    f = {"title": "t", "severity": "major", "firmness": "law", "category": "accessibility",
         "where": {"screen": "inbox", "element": "x"}, "rule": {"id": "wcag-2.5.8"},
         "evidence": "e", "fix": "f"}
    first = finalize({"findings": [dict(f), dict(f, severity="nit", firmness="taste", where={"screen": "inbox", "element": "y"})]})
    assert not problems(first), problems(first)
    assert [x["status"] for x in first["findings"]] == ["new", "new"]
    second = finalize({"findings": [dict(f)]}, first)
    assert second["findings"][0]["status"] == "still" and len(second["resolved"]) == 1
    assert problems({"schema": "design-findings/v1", "findings": [dict(f, firmness="taste")]})
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["finalize"] and len(a) >= 3:
        doc = finalize(json.load(open(a[1])), json.load(open(a[3])) if len(a) > 3 else None)
        bad = problems(doc)
        if bad:
            sys.exit("\n".join(bad))
        json.dump(doc, open(a[2], "w"), indent=1)
        open(a[2].rsplit(".", 1)[0] + ".md", "w").write(render(doc))
        print(json.dumps(doc["summary"]))
    elif a[:1] == ["render"] and len(a) == 2:
        print(render(json.load(open(a[1]))))
    elif a[:1] == ["validate"] and len(a) == 2:
        bad = problems(json.load(open(a[1])))
        print("\n".join(bad) or "ok")
        sys.exit(1 if bad else 0)
    elif a[:1] == ["selftest"]:
        selftest()
    else:
        sys.exit(__doc__)
