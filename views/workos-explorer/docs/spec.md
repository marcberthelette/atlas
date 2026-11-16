# WorkOS explorer: spec

Status: approved by the owner on 2026-11-15 (placement and scope taken as proposed). Built 2026-11-15 (`shared/workos_explorer.html`, `shared/build_workos_explorer.py`, catalogue `data/levels.json`). Data read from the WorkOS docs on 2026-11-15. Format: `docs/topic-spec.md`, adapted for a view with its own small catalogue (like `views/lenses/`), modelled on `views/explorer/docs/spec.md`.

## Purpose and audience

Answers "where does this WorkOS object live, and what does it belong to?" for a developer who knows the feature names but not the containment: which things are per team,
per project, per environment, per organization or per user, and how a user reaches an organization. Reading order is top down: team, project, environment, then what an
environment holds. When the object is found, a link opens its Atlas entry (`../workos/index.html#<id>`) for the facts, the API surface and the sources. The explorer locates, Atlas explains.

## Scope

- In: the objects of the `workos` topic that have a place in the hierarchy: team, project, environment, application, API key and client ID, user, organization, organization membership,
  domain, SSO connection, directory (with directory users and groups), organization and user API keys, role and permission, FGA resource and role assignment, audit log event, webhook endpoint,
  feature flag, Pipes provider and connection, Vault secret and key context, branding. Search that answers with the path ("SSO connection: environment > organization"). A link to the Atlas entry on every object.
- Out: facts about an object (they stay in the WorkOS topic), endpoints and fields, pricing and plan limits, a real account (reference view only), Radar, Widgets, WorkOS Connect and the other sections the WorkOS topic leaves out.
- Rule that decides: an object appears once, at the level that owns it, and as a dim pill at the levels below where it still applies. A relation that is not containment (a user reaches an organization through a membership) is drawn as a link, not as nesting.

## Layout

One page, `/workos-explorer/`, same Layers layout as the Azure explorer: the level above (collapsed), the level you are in (open) and a preview of the level below. Levels: team, project, environment, organization, user.
Each level lists what it owns and the ambient objects that apply. Click a container to go down; the breadcrumb goes back up. Deep links by hash. Works from `file://`, with the keyboard, in light and dark, in both looks like every view.

Two additions the Azure explorer has no use for:

- **Memberships.** A user is owned by the environment, not by an organization. On the organization level a "members" row shows the membership link and its role; on the user level an "organizations" row shows the same link from the other side.
- **Keys.** One "Where is the key?" panel separates the four credentials: the environment secret key and client ID, organization API keys, user API keys, and M2M applications.

Differences from the plan: the keys panel is a sixth step, "Keys", after the five levels; user and organization are both children of the environment, so the environment level zooms into either. Objects have an owner level (`at`) and levels they are also seen from (`also`): a level below the owner shows a dim pill ("Around from a level above"), a level in another branch shows a card ("Linked from here", for the membership and the user API key). The catalogue is checked by `make validate` (`shared/build_workos_explorer.py check`): known levels, WorkOS entries and page keys, a source on every item, a note on every unconfirmed one. Built in both looks.

## Containment read from the docs

```
Team                         dashboard members and roles, billing, team SSO/MFA
└─ Project                   groups the environments of one product; holds feature flag definitions, audit log schema, custom email domains
   └─ Environment            staging or production, isolated; holds API keys, users, organizations, connections, webhook endpoints, branding
      ├─ Application         one per client (web, mobile, desktop); own client ID, redirect URIs, sessions; shares the environment's users
      ├─ User                one per email address
      ├─ Organization        a customer (tenant) of the app
      │   ├─ Domain, SSO connection, Directory (users, groups), organization API keys, audit log events
      │   └─ Custom roles, FGA resources
      └─ Organization membership   links a user to an organization, with one or more roles; user API keys hang off it
```

## Sources

The WorkOS docs, one page per row of the coverage table. The page shows the docs read date, since the pages carry no date or version (same rule as the WorkOS topic).

| Level or object | Page |
|---|---|
| team, project, environment | `workos.com/docs/authkit/projects`, `authkit/environments`, `dashboard/members-and-roles` |
| application | `workos.com/docs/authkit/applications` |
| user, organization, membership | `workos.com/docs/authkit/users-organizations`, `reference/organization`, `reference/user-management/organization-membership` |
| domain, SSO connection | `workos.com/docs/sso/domains`, `sso` |
| directory | `workos.com/docs/directory-sync` |
| API keys | `workos.com/docs/authkit/api-keys` |
| roles, FGA | `workos.com/docs/rbac`, `rbac/custom-roles`, `fga/standalone-integration` |
| Pipes, Vault | `workos.com/docs/pipes`, `pipes/organization-scoped-providers`, `pipes/connection-sharing`, `vault` |

## Coverage

| Item | Status | Notes |
|---|---|---|
| `level:team` | done | dashboard members, team authentication, billing (billing unconfirmed); a dashboard user belongs to one team |
| `level:project` | done | groups environments; project-level settings |
| `level:environment` | done | what is scoped to it, staging against production |
| `level:organization` | done | domain, connection, directory, keys, roles, audit events |
| `level:user` | done | memberships, user API keys, Pipes connections |
| `view:keys` | done | the four credentials side by side |
| `platform` | done | team, project and environment link to it; the main-objects table stays there |

## Known gaps

- The WorkOS topic has no entry per object (it has per product), so a link goes to the product entry that covers the object, not to the object.
- Unconfirmed: the level of Vault secrets (the docs say keys are segmented "by organization, user, or any provided context", not that Vault is environment-scoped) and of Pipes provider settings other than the organization-scoped ones.
- Unconfirmed: limits on projects, environments and applications.
- 6 of 32 items are marked unconfirmed in the data (billing, M2M application twice, Pipes provider, Vault, Admin Portal link).
- Billing and plan differences between staging and production are left out; only the isolation is shown.

## Decisions

- A standalone view in `views/workos-explorer/`, linked from the banner like `/explorer/`. Reason: the owner chose it after the recommendation. The WorkOS topic keeps its entries unchanged.
- Scope includes Pipes, Vault and FGA. Reason: the owner chose it; they are all objects that sit inside an organization or an environment.
- Own catalogue (`views/workos-explorer/data/levels.json`), not new keys in the WorkOS data. Reason: the WorkOS topic has no per-object entries to hang a level on; reason unconfirmed that a later move into the topic data is wrong.
- Layers layout, as for Azure. Reason: the same question ("where is it?") and the owner's earlier choice.

## Updating

Re-read the pages in Sources a few times a year, with `workos.com/docs/llms.txt` for renamed or added objects. Change the catalogue and this spec in the same commit, run `make validate`, then `make build`.
