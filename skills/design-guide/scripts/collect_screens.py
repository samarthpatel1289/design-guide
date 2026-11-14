#!/usr/bin/env python3
"""Turn audit inputs into one flat list of screens with stable labels.

  collect_screens.py OUT_DIR INPUT [INPUT ...]

INPUT may be an image file, a directory (searched recursively for images), or an Xcode
.xcresult bundle (named image attachments are exported; recordings, plist UI snapshots and
synthesized events are skipped; each screenshot is paired with the nearest-in-time
"App UI hierarchy" text from the same test, which `measure.py targets` reads).

Prints the `inputs` array of the design-findings/v1 format as JSON on stdout. Labels come from
file or attachment names, so the same screen keeps the same label run after run — finding ids
depend on that.
"""
import json
import os
import re
import shutil
import subprocess
import sys

IMAGE = (".png", ".jpg", ".jpeg", ".heic", ".webp")


def label_of(name):
    stem = os.path.splitext(os.path.basename(name))[0]
    return re.sub(r"_\d+_[0-9A-F-]{36}$", "", stem)  # XCTAttachment adds _0_<UUID>


def from_xcresult(bundle, out):
    dest = os.path.join(out, label_of(bundle) + "-attachments")
    os.makedirs(dest, exist_ok=True)
    subprocess.run(["xcrun", "xcresulttool", "export", "attachments", "--path", bundle,
                    "--output-path", dest], check=True, capture_output=True)
    screens = []
    for test in json.load(open(os.path.join(dest, "manifest.json"))):
        atts = test.get("attachments", [])
        trees = [a for a in atts if a["suggestedHumanReadableName"].startswith("App UI hierarchy")]
        for a in atts:
            if not a["suggestedHumanReadableName"].lower().endswith(IMAGE):
                continue
            near = min(trees, key=lambda t: abs(t["timestamp"] - a["timestamp"]), default=None)
            screens.append({"path": os.path.join(dest, a["exportedFileName"]),
                            "label": label_of(a["suggestedHumanReadableName"]),
                            "kind": "xcresult",
                            "test": test.get("testIdentifier"),
                            "hierarchy": os.path.join(dest, near["exportedFileName"]) if near else None})
    return screens


def collect(out, inputs):
    screens = []
    for item in inputs:
        item = item.rstrip("/")
        if item.endswith(".xcresult"):
            screens += from_xcresult(item, out)
        elif os.path.isdir(item):
            for root, _, files in os.walk(item):
                screens += [{"path": os.path.join(root, f), "label": label_of(f), "kind": "screenshot"}
                            for f in sorted(files) if f.lower().endswith(IMAGE)]
        elif item.lower().endswith(IMAGE):
            screens.append({"path": item, "label": label_of(item), "kind": "screenshot"})
        else:
            print(f"skipped (not an image, folder or .xcresult): {item}", file=sys.stderr)
    seen = {}
    for i, s in enumerate(screens, 1):  # duplicate labels get -2, -3 so ids stay distinct
        n = seen[s["label"]] = seen.get(s["label"], 0) + 1
        if n > 1:
            s["label"] += f"-{n}"
        s["id"] = f"s{i}"
    return screens


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if not shutil.which("xcrun") and any(a.endswith(".xcresult") for a in sys.argv[2:]):
        sys.exit(".xcresult input needs Xcode's xcrun on this machine")
    os.makedirs(sys.argv[1], exist_ok=True)
    print(json.dumps(collect(sys.argv[1], sys.argv[2:]), indent=1))
