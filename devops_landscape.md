# DevOps Landscape: Domains, Disciplines, Methods, and Platform Engineering

A mental model for placing DevOps buzzwords. There is no official taxonomy, and the edges are fuzzy. This is a way to organize the terms, not a standard.

## The layers at a glance

| Layer | What it is | Examples |
|---|---|---|
| **Domains** | What you are building and operating | DevOps, MLOps, DataOps, LLMOps |
| **Disciplines** ("buckets") | The concerns inside a domain | Build/CI, delivery, infrastructure, security, observability, reliability, cost |
| **Methods** | Ways of doing things | GitOps, IaC, AIOps, policy as code, ChatOps |
| **Tools / building blocks** | Concrete pieces | Terraform, Argo CD, Crossplane, CI pipelines, Prometheus |
| **Operating models** | How the work is organized | Platform engineering, SRE, enabling teams |

Some items straddle layers. IaC, for example, is both a method (the idea) and a building block (the tool).

---

## 1. Disciplines inside DevOps

Starting point: platform engineering, application delivery, and monitoring/observability. A fuller list:

- **Build and integration (CI):** source control workflows, build pipelines, artifact registries, automated testing.
- **Application delivery (CD):** deployment strategies, release management, GitOps-style reconciliation.
- **Infrastructure and configuration management:** IaC, config management, cluster and cloud provisioning.
- **Observability / monitoring:** metrics, logs, traces, alerting.
- **Reliability (SRE):** SLOs, error budgets, incident response, on-call, postmortems, capacity planning, chaos testing.
- **Security (DevSecOps):** secrets management, supply-chain scanning, policy as code, compliance.
- **Cost management (FinOps):** cloud spend visibility and optimization.
- **Culture and process:** shared ownership, blameless practice, feedback loops. This was the original point of DevOps.

Platform engineering is **not** a peer of these. It is a layer on top (see section 2).

---

## 2. Platform engineering

**Definition:** a delivery model where a platform team packages several disciplines (IaC, CI/CD, observability, security guardrails) into a **self-service internal product**, the internal developer platform (IDP), so app teams don't assemble the pieces themselves.

Key points:

- **Built on the disciplines.** Without the underlying buckets there is nothing to bundle. It does not need all of them, though. A platform can start with two or three and grow.
- **Adds product thinking.** Know who the users are, make the interface easy, measure adoption, treat developers as customers. Well-run buckets without this are still just good DevOps.
- **Not the same as automation.** Spinning up a whole stack from code is a prerequisite, not the discipline itself. It becomes platform engineering when packaged as self-service (portal, API, CRD, templates, golden paths) for other engineers.
- **Not always internal-only.** If your SaaS provisions resources per customer (tenant, database, namespace), that provisioning layer is a **control plane**. It uses the same tools (Crossplane, operators) but serves customers, so it is part of the product.
- **Build vs. buy of tools is not a rivalry.** Terraform, Argo CD, and Crossplane are parts you pick from inside the layers, not competing alternatives.

---

## 3. Domains ("Ops" for X)

The "Ops" suffix mostly means "apply the DevOps playbook to X." The principles stay the same: automate, version everything, ship small changes often, monitor in production, close the feedback loop. Each domain adapts them to what is unusual about X.

| Domain | Artifacts | What is unusual |
|---|---|---|
| **DevOps** (classic apps) | Code, containers, binaries | Bugs and infrastructure failures |
| **MLOps** | Code, data, trained models | Models silently degrade as real-world data drifts, even when no code changed |
| **DataOps** | Data pipelines | Data quality, schema changes, lineage, freshness |
| **LLMOps** | Prompts, retrieval setup, evals, guardrails | Non-deterministic output, model upgrades, cost per token |
| **DevSecOps** | Security across the lifecycle | More a discipline than a domain; the line blurs |

### DataOps in detail

- Applies DevOps principles to **data pipelines**, which are versioned, tested, and deployed through CI/CD.
- Includes **quality gates on the data**, not management of the data's content. Automated checks pass, warn, or block:
  - no nulls in a key column
  - row count within a tolerance of the previous run
  - data arrived within the expected window
  - schema matches the contract
- A failed check halts the pipeline, quarantines the batch, or alerts someone, so bad data does not reach the next layer.
- **Medallion layers:**
  - **Bronze:** raw data landed as-is.
  - **Silver:** cleaned, deduplicated, validated, conformed.
  - **Gold:** aggregated, business-ready tables for dashboards, reporting, or ML features.
- Typical tools: dbt, Airflow, Dagster, Great Expectations.
- **Neighbouring topic:** database DevOps / schema migration management (Flyway, Liquibase, Alembic) covers the transactional side, where a database backs an app. DataOps is the analytical side. They overlap on schema drift.

### MLOps in detail

- Data and model versioning, training pipelines, experiment tracking, model registries, deployment, drift monitoring.
- Platform teams increasingly add GPU scheduling and model serving to their internal platform.

### LLMOps in detail

MLOps adapted to apps built on large language models. Most teams do not train the model. They call a foundation model and engineer everything around it.

- **What you version and ship:** prompts and system instructions, retrieval setup (RAG: chunking, embeddings, vector store, indexing pipelines), tool and agent configs, guardrails and filters.
- **Evals are the tests.** Outputs are non-deterministic, so you run a fixed test set and score results (often LLM-as-judge or human review). The eval suite is the quality gate before a prompt or model change ships.
- **Model upgrades are a risk.** A provider updating or retiring a model can change behavior with no change on your side. Re-run evals when that happens.
- **Cost and latency are first-class metrics:** token usage, caching, model routing.
- **Observability is trace-based:** log prompts, retrieved context, tool calls, and responses so you can debug a bad answer.
- **New failure modes:** hallucination, prompt injection, data leakage, unsafe output.
- **Applies to** chatbots and agent harnesses (e.g. Claude Code style). Harnesses add tool definitions, permission rules, context management, and the agent loop. Evals are harder because a run is a multi-step trajectory, so you check task completion, safe tool use, and token burn.
- **Skills and MCP** are artifacts and building blocks (versioned instructions, tool integration layer), not LLMOps itself. LLMOps is the CI/CD, testing, and monitoring discipline you put around them.
- The model provider handles training and serving. The team building the app handles everything around it.

---

## 4. AIOps (a method, not a domain)

AIOps is the reverse of LLMOps:

- **LLMOps / MLOps:** operating AI systems.
- **AIOps:** using AI to operate any system.

Typical capabilities:

- **Noise reduction:** correlating many alerts into one incident.
- **Anomaly detection:** finding abnormal metrics or logs without hand-tuned thresholds.
- **Root-cause analysis:** pointing at the likely culprit (e.g. latency spiked after a deploy).
- **Automated remediation:** restart, scale out, roll back.
- **Capacity forecasting.**

It mostly sharpens observability and incident response. Tools such as Datadog, Dynatrace, PagerDuty, and Moogsoft have features along these lines.

**Newer wave:** LLM-based "AI SRE" agents that read logs, traces, and runbooks, investigate an alert, and propose or perform a fix. That is AIOps built with an LLM harness, so it also needs LLMOps discipline: evals, guardrails, and tight permissions, since an agent with production access can do real damage.

**Caveat:** the term is heavily marketed. Many products labelled AIOps are statistical alerting with a new name. Ask what specific toil it removes.

---

## 5. Methods and building blocks

- **GitOps** is a method, not a bucket. Git is the source of truth and a controller reconciles toward it. It lives inside the delivery discipline.
- **IaC** is the foundation of infrastructure management and a building block of platform engineering.
- **Pipelines, Terraform, Argo CD, Crossplane** are tools you pick from inside the layers.
- A data or ML platform built from code (cluster, config, sources, transforms, outputs) is IaC plus pipeline-as-code. It becomes a **data platform / ML platform**, which is platform engineering applied to that domain, when it is packaged as self-service.

---

## 6. Operating models and relatives of platform engineering

**Different practices at the same level:**

- **SRE:** software engineering applied to reliability (SLOs, error budgets, toil reduction). Focused on keeping services healthy more than building self-service tools. Overlaps heavily with platform work.
- **Enabling teams** (Team Topologies): coaches who help other teams adopt practices, then step away. A platform team provides a product. An enabling team provides expertise.
- **Developer experience (DevEx) teams:** focus on friction in the dev workflow (build times, local environments, tooling). Often owned by the platform team, but can be separate.
- **Cloud / DevOps Center of Excellence:** a central group that sets standards and guidance. Governance-heavy. Platform engineering is partly a reaction to CoEs that only advise and do not build.

**Flavors of platform engineering:**

- Internal developer platform (IDP), the classic one
- Data platform
- ML platform
- Security platform (guardrails and scanning as self-service)

A typical org might run several: an SRE team keeping production reliable, a platform team building the self-service layer, and sometimes an enabling team helping squads adopt both.

---

## Summary

- Disciplines sit at the bottom. Platform engineering is a layer on top that bundles them into a self-service product.
- Domains (MLOps, DataOps, LLMOps) apply the same principles to different artifacts.
- Methods (GitOps, IaC, AIOps) and tools (Terraform, Argo CD, Crossplane) are the ways and parts used inside the layers.
- A platform is only as good as what it bundles, and it needs product thinking to be more than good DevOps.
