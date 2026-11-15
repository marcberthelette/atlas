# Azure explorer: spec

Status: approved by the owner on 2026-11-14 (both open decisions taken as proposed). Mockups: https://claude.ai/artifact/DgPdGpGVSGzfSKEyRSCDVZ (direction C, Layers, chosen by the owner; A and B are not built).
Nothing is built yet. Format: `docs/topic-spec.md`, adapted for a view that reads another topic's data.

## Purpose and audience

Answers "where is this Azure service?" before "how does it connect?". The reader moves down from the tenant, through the subscription and the
resource group, and sees at each level what lives there and which services are always around. When the service is found, a link opens its
Atlas entry (`../azure/index.html#<service-id>`) for the relationships, Terraform and sources. The explorer locates, Atlas explains.

## Scope

- In: the Azure services of the `azure` topic (tier 0 and 1, 42 services). Levels: tenant, subscription, resource group, service. Search that
  answers with the path ("Key Vault: tenant > subscription > resource group"). A link to the Atlas entry on every service.
- Out: facts about a service (they stay in the Azure topic), a real estate (the reference view only; "Your estate" is a later idea), tier 2 and 3
  services until the Azure topic covers them, anything taken from an employer or client.
- Rule that decides: a service appears at every level where it applies. A service with no container is ambient (tier 0 today).

## Layout

One page, `/explorer/`, built from `dist/azure/services.resolved.json` (the stable contract) and a small catalogue of levels. Layers: the level above
(collapsed), the level you are in (open) and a preview of the level below. Each level shows its containers and the ambient services that apply there;
ambient services from higher levels stay visible as dim pills. Click a container to go one level down; the breadcrumb goes back up. Deep links by hash.
Must work from `file://` and with the keyboard, in light and dark.

## Sources

The Azure topic's data, which carries the Learn pages and versions. A level (`scope`) is a judgement checked against Learn, not copied from it.
The page shows the Azure data version and the date of the check, like every other page.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `tenant` | planned | tier 0 services around the tenant |
| `subscription` | planned | RBAC, Policy, Cost Management, Defender for Cloud and others at this level |
| `resource-group` | planned | the 27 services the Azure data says a resource group contains, by category |
| `service` | planned | links to the Atlas entry; relationships stay in Atlas |

## Known gaps

- The mockups guess which level each ambient service belongs to. Nothing is verified against Learn yet.
- Azure DevOps and Log Analytics do not attach to the tree the way a subscription does; how to show it is open.
- The example subscriptions and resource groups in the mockups are placeholders.

## Decisions

- Layers layout (C): the context never leaves the screen. Reason: the owner's choice after seeing three layouts.
- Link to Atlas, no duplicated facts. Reason: root `CLAUDE.md` ("centralise, don't copy").
- Where the level lives: a `scope` list on each Azure service (tenant, management group, subscription, resource group), checked by
  `make azure-validate`. Rejected for now: a separate catalogue in `views/explorer/data/`.
- Location: `views/explorer/`, like `views/lenses/`, with its own build and a link in the banner.

## Updating

When the Azure topic adds a service or changes its edges, rebuild the Azure data first, then this page. Re-read the levels against Learn.
