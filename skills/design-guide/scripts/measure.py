#!/usr/bin/env python3
"""Measure what an audit should never eyeball: contrast ratios and tap-target sizes.

  measure.py contrast FG BG              WCAG 2.x ratio for two hex colours
  measure.py pairs CONFIG.md             every pair declared in a project config's tokens block
  measure.py sample SHOT.png X Y W H     ratio inside a screenshot region (pixels): background =
                                         most common colour on the box's border (leave a margin
                                         around the text), foreground = colour farthest from it
  measure.py targets HIERARCHY.txt [MIN] interactive elements smaller than MIN points (default 44)
                                         from an XCUITest "App UI hierarchy" attachment
  measure.py selftest

Stdlib only. Exit code 1 when anything fails its threshold, so a scheduler can branch on it.
"""
import json
import re
import struct
import sys
import zlib
from collections import Counter


def _hex(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def verdict(r):
    """WCAG 2.2: 1.4.3 text AA 4.5 (large 3), 1.4.6 AAA 7 (large 4.5), 1.4.11 non-text 3."""
    ok = lambda t: "pass" if r >= t else "FAIL"
    return {"ratio": round(r, 2), "text_AA": ok(4.5), "large_text_AA": ok(3),
            "non_text_AA": ok(3), "text_AAA": ok(7)}


def cmd_contrast(fg, bg):
    v = verdict(ratio(_hex(fg), _hex(bg)))
    print(json.dumps({"fg": fg, "bg": bg, **v}))
    return v["text_AA"] == "pass"


def tokens_block(path):
    """The first ```json block in a design-guide config (see references/config.md)."""
    m = re.search(r"```json\s*\n(.*?)\n```", open(path, encoding="utf-8").read(), re.S)
    if not m:
        sys.exit(f"{path}: no ```json tokens block")
    return json.loads(m.group(1))


def cmd_pairs(path):
    """Each pair: {"fg": token, "bg": token, "min": 4.5, "use": "..."}; colours may be
    "#hex" or {"light": "#hex", "dark": "#hex"}."""
    t = tokens_block(path)
    colors, ok = t.get("colors", {}), True
    for p in t.get("pairs", []):
        fg, bg = colors[p["fg"]], colors[p["bg"]]
        for mode in ("light", "dark"):
            f = fg[mode] if isinstance(fg, dict) else fg
            b = bg[mode] if isinstance(bg, dict) else bg
            if f is None or b is None:
                continue
            r = ratio(_hex(f), _hex(b))
            need = p.get("min", 4.5)
            passed = r >= need
            ok &= passed
            print(f"{'ok  ' if passed else 'FAIL'} {mode:5} {p['fg']} on {p['bg']}: "
                  f"{r:.2f} (needs {need}) {p.get('use', '')}")
            if not isinstance(fg, dict) and not isinstance(bg, dict):
                break
    return ok


def read_png(path):
    """8-bit non-interlaced RGB/RGBA/grey PNG → (w, h, rows of (r,g,b)). Enough for screenshots."""
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"{path}: not a PNG")
    pos, idat, palette = 8, b"", None
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, n, 3)]
        elif kind == b"IDAT":
            idat += body
        pos += 12 + n
    if depth != 8 or interlace:
        sys.exit(f"{path}: only 8-bit non-interlaced PNGs (got depth {depth})")
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw, stride, prev, rows, i = zlib.decompress(idat), w * bpp, bytearray(w * bpp), [], 0
    for _ in range(h):
        f, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b, c = prev[x], prev[x - bpp] if x >= bpp else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        if ctype == 3:
            rows.append([palette[v] for v in line])
        elif ctype in (0, 4):
            rows.append([(line[x],) * 3 for x in range(0, stride, bpp)])
        else:
            rows.append([tuple(line[x:x + 3]) for x in range(0, stride, bpp)])
    return w, h, rows


def cmd_sample(path, x, y, w, h):
    # ponytail: "farthest colour from the background" is the text colour for one-colour text on a
    # flat fill; gradients/photos behind text need a human look.
    # Background comes from the box's border, so draw the box with a little margin around the text.
    _, _, rows = read_png(path)
    box = [row[x:x + w] for row in rows[y:y + h]]
    px = [p for row in box for p in row]
    if not px:
        sys.exit("empty region")
    edge = box[0] + box[-1] + [r[0] for r in box] + [r[-1] for r in box]
    bg = Counter(edge).most_common(1)[0][0]
    fg = max(set(px), key=lambda p: ratio(p, bg))
    v = verdict(ratio(fg, bg))
    print(json.dumps({"bg": "#%02X%02X%02X" % bg, "fg": "#%02X%02X%02X" % fg, **v}))
    return v["text_AA"] == "pass"


INTERACTIVE = ("Button", "Link", "Switch", "Toggle", "TextField", "SecureTextField", "Slider",
               "SegmentedControl", "Stepper", "Tab", "MenuItem", "Cell", "SearchField", "Picker")
FRAME = re.compile(r"^\s*(\w+), 0x[0-9a-f]+, \{\{([\d.-]+), ([\d.-]+)\}, \{([\d.]+), ([\d.]+)\}\}(.*)$")


def cmd_targets(path, minimum=44.0):
    """Lists undersized interactive frames. 44 pt = Apple HIG; WCAG 2.5.8 AA floor is 24."""
    small = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = FRAME.match(line)
        if not m or m.group(1) not in INTERACTIVE:
            continue
        w, h = float(m.group(4)), float(m.group(5))
        if 0 < min(w, h) < minimum:
            ident = re.search(r"identifier: '([^']*)'", m.group(6))
            label = re.search(r"label: '([^']*)'", m.group(6))
            small.append({"type": m.group(1), "w": w, "h": h,
                          "identifier": ident.group(1) if ident else None,
                          "label": label.group(1) if label else None,
                          "below_wcag_24": min(w, h) < 24})
    print(json.dumps(small, indent=1))
    return not small


def selftest():
    assert round(ratio(_hex("#000"), _hex("#fff")), 2) == 21.0
    assert round(ratio(_hex("#767676"), _hex("#ffffff")), 2) == 4.54  # the classic AA-passing grey
    assert verdict(4.4)["text_AA"] == "FAIL" and verdict(4.4)["large_text_AA"] == "pass"
    line = "  Button, 0x1, {{1.0, 2.0}, {30.0, 30.0}}, identifier: 'x', label: 'Close'"
    m = FRAME.match(line)
    assert m and m.group(1) == "Button" and m.group(4) == "30.0"
    # 2×1 RGB PNG, black then white, filter 0
    raw = zlib.compress(b"\x00" + bytes([0, 0, 0, 255, 255, 255]))
    chunk = lambda k, b: struct.pack(">I", len(b)) + k + b + struct.pack(">I", zlib.crc32(k + b))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 1, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", raw) + chunk(b"IEND", b"")
    import os, tempfile
    fd, p = tempfile.mkstemp(suffix=".png")
    os.write(fd, png)
    os.close(fd)
    _, _, rows = read_png(p)
    os.unlink(p)
    assert rows == [[(0, 0, 0), (255, 255, 255)]]
    print("selftest ok")
    return True


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmds = {"contrast": lambda: cmd_contrast(a[1], a[2]),
            "pairs": lambda: cmd_pairs(a[1]),
            "sample": lambda: cmd_sample(a[1], *map(int, a[2:6])),
            "targets": lambda: cmd_targets(a[1], float(a[2]) if len(a) > 2 else 44.0),
            "selftest": selftest}
    if a[0] not in cmds:
        sys.exit(__doc__)
    sys.exit(0 if cmds[a[0]]() else 1)
