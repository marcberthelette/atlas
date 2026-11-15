"""Build the Azure explorer view (views/explorer/, spec in views/explorer/docs/spec.md) into dist/explorer/index.html.

It has no content of its own: it reads the resolved Azure data (dist/azure/services.resolved.json, built first), where each service carries
`scope` (the levels it applies at). The data is embedded in the page as JSON and drawn in the browser, so the page works from file://.
"""
import html
import json
import sys

import atlas
import transit

VIEW_ID = "explorer"
# The Azure service that stands for each level of the tree, shown as the "contains" step and as the Atlas link of the level.
STRUCTURE = {"tenant": "entra-tenant", "management-group": "management-groups", "subscription": "subscriptions", "resource-group": "resource-groups"}


def data():
    path = atlas.DIST / "azure" / "services.resolved.json"
    if not path.exists():
        sys.exit("build the azure topic first: dist/azure/services.resolved.json is missing")
    az = json.loads(path.read_text(encoding="utf-8"))
    levels = [l["id"] for l in az["scope_levels"]]
    bad = []
    for s in az["services"]:
        sc = s["scope"]
        if not sc["levels"] or any(l not in levels for l in sc["levels"]):
            bad.append(f"{s['id']}: scope needs levels from scope_levels")
    for sid in STRUCTURE.values():
        if sid not in {s["id"] for s in az["services"]}:
            bad.append(f"structure service {sid} is not an Azure service")
    if bad:
        sys.exit("\n".join("bad: " + b for b in bad))
    checked = max(s["freshness"]["changed_at"] or "" for s in az["services"])
    return {
        "checked": checked,
        "levels": az["scope_levels"],
        "structure": STRUCTURE,
        "categories": az["categories"],
        "services": [{"id": s["id"], "name": s["name"], "category": s["category"], "tier": s["tier"], "purpose": s["purpose"],
                      "scope": {k: s["scope"][k] for k in ("levels", "status", "note")}} for s in az["services"]],
    }


def main():
    reg = atlas.load()
    v = next(x for x in reg.get("views", []) if x["id"] == VIEW_ID)
    d = data()
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (atlas.SITE / "shared" / "explorer.html").read_text(encoding="utf-8")
    template = template.replace("__TITLE__", html.escape(v["label"])).replace("__NAME__", html.escape(reg["name"])).replace("__DATA__", blob)
    twin = transit.explorer(template)
    page = (atlas.themed(template)
            .replace(atlas.BANNER_MARK, atlas.banner(VIEW_ID, "../", atlas.twin(f"{VIEW_ID}/index.html"))).replace(atlas.CSS_MARK, atlas.CSS).replace(atlas.FOOTER_MARK, atlas.FOOTER))
    out = atlas.DIST / VIEW_ID
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    transit.write(f"{VIEW_ID}/index.html", twin)
    print(f"built dist/{VIEW_ID}/index.html")


if __name__ == "__main__":
    main()
