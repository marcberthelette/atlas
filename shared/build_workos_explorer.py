"""Build the WorkOS explorer view (views/workos-explorer/, spec in views/workos-explorer/docs/spec.md) into dist/workos-explorer/index.html.

It has its own small catalogue, views/workos-explorer/data/levels.json (levels, objects and credentials, each with the docs pages it was read from).
The data is embedded in the page as JSON and drawn in the browser, so the page works from file://.
`build_workos_explorer.py check` only validates the catalogue (make validate).
"""
import html
import json
import sys

import atlas
import transit

VIEW_ID = "workos-explorer"
DATA = atlas.SITE / "views" / VIEW_ID / "data" / "levels.json"
STATUS = {"verified", "unconfirmed"}


def problems(d):
    """Errors in the catalogue: unknown levels, entries or page keys, and items without a source."""
    bad = []
    levels = {l["id"] for l in d["levels"]}
    entries = {e["id"] for e in json.loads((atlas.SITE / "topics" / "workos" / "data" / "workos.json").read_text(encoding="utf-8"))["entries"]}
    for l in d["levels"]:
        if l["parent"] is not None and l["parent"] not in levels:
            bad.append(f"level {l['id']}: unknown parent {l['parent']}")
    seen = set()
    for kind in ("levels", "objects", "keys"):
        for x in d[kind]:
            where = f"{kind} {x['id']}"
            if x["id"] in seen:
                bad.append(f"{where}: duplicate id")
            seen.add(x["id"])
            if x["entry"] not in entries:
                bad.append(f"{where}: entry {x['entry']} is not a WorkOS entry")
            if not x["src"] or any(k not in d["pages"] for k in x["src"]):
                bad.append(f"{where}: needs src keys from pages")
            if kind != "levels" and x["status"] not in STATUS:
                bad.append(f"{where}: status must be one of {sorted(STATUS)}")
            if kind != "levels" and x["status"] == "unconfirmed" and not x.get("note"):
                bad.append(f"{where}: an unconfirmed item says why in note")
    for o in d["objects"]:
        if o["at"] not in levels or any(l not in levels for l in o["also"]):
            bad.append(f"objects {o['id']}: at and also need level ids")
    for k in d["keys"]:
        if k["level"] not in levels:
            bad.append(f"keys {k['id']}: level is not a level id")
    return bad


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    bad = problems(d)
    if bad:
        sys.exit("\n".join("bad: " + b for b in bad))
    if sys.argv[1:] == ["check"]:
        print(f"workos-explorer levels {len(d['levels'])} objects {len(d['objects'])} credentials {len(d['keys'])} bad 0")
        return
    reg = atlas.load()
    v = next(x for x in reg.get("views", []) if x["id"] == VIEW_ID)
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (atlas.SITE / "shared" / "workos_explorer.html").read_text(encoding="utf-8")
    template = template.replace("__TITLE__", html.escape(v["label"])).replace("__NAME__", html.escape(reg["name"])).replace("__DATA__", blob)
    twin = transit.skin(template, transit.EXPLORER_CSS, VIEW_ID)
    page = (atlas.themed(template)
            .replace(atlas.BANNER_MARK, atlas.banner(VIEW_ID, "../", atlas.twin(f"{VIEW_ID}/index.html"))).replace(atlas.CSS_MARK, atlas.CSS).replace(atlas.FOOTER_MARK, atlas.FOOTER))
    out = atlas.DIST / VIEW_ID
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    transit.write(f"{VIEW_ID}/index.html", twin)
    print(f"built dist/{VIEW_ID}/index.html")


if __name__ == "__main__":
    main()
