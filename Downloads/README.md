# CloudShift — Multi-Cloud FinOps Autopilot (Demo Monorepo)

This repo contains a **local-first demo** for the CloudShift MVP:
- **apps/api** — Fastify + TypeScript API (sample collectors, rules, Razorpay mock, Actions DSL runner)
- **apps/web** — React + Vite dashboard (Supabase Auth stub, Recharts)
- **packages/core** — normalization, rules engine, Lock‑in Escape Index™ (LEI), YAML actions

> Works **offline** using sample spend exports. Flip to live mode by plugging real SDK creds in `.env` later.

## Quickstart

```bash
# 0) Install pnpm first if needed
npm i -g pnpm

# 1) Install deps in all workspaces
pnpm i

# 2) Start API + Web (two terminals)
pnpm dev:api
pnpm dev:web
```

- API ➜ http://127.0.0.1:8787/health  
- Web ➜ http://127.0.0.1:5173

> Demo uses **sample CSVs** under `data/sample/`. No cloud credentials required.

---

## UAAL Evidence Core (v0.1)

### What this is

The **UAAL Evidence Core** is the foundational layer of UAAL that captures,
hashes, and verifies AI decisions as **cryptographic evidence**.

It answers one question only:

> *What decision did an AI system actually make, under which policy, with what inputs — and can that record be proven unmodified later?*

This layer:
- Records every AI decision with full context (inputs, policy, model, outcome)
- Computes deterministic cryptographic hashes for each decision
- Detects post-facto tampering through hash verification
- Preserves evidence even when enforcement or guardrails fail
- Supports deterministic replay and verification for audits and investigations

This is **not** a monitoring tool or a policy engine.  
It is an **evidence system**.

---

### Why this exists

Most AI security and authorization layers rely on *belief*:
> “The guardrail should have blocked this.”

UAAL Evidence Core relies on **proof**:
> “Here is the immutable record of what actually happened.”

Even if:
- a policy fails
- an agent misbehaves
- a developer makes a mistake

…the evidence survives.

---

### How this differs from Enterprise / Pilot Features

The Evidence Core is intentionally **minimal and uncompromising**.

| Evidence Core | Enterprise / Pilot Features |
|--------------|-----------------------------|
| Cryptographic decision records | Human-in-the-loop (HITL) workflows |
| Hash verification & tamper detection | SLAs, retries, escalation logic |
| Deterministic replay | Dashboards, metrics, alerting |
| Answers “what happened?” | Answer “what should we do now?” |
| Required for audits & legal review | Required for operations & scale |

Enterprise features **depend on** the Evidence Core —  
they do **not replace it**.

Without evidence, enterprise controls are opinions.

---

### Status

This branch (`prod-core`) represents:

**UAAL Evidence Core v0.1**
- Local UI for live verification (VERIFIED / INVALID)
- Policy enforcement failure capture (DENY vs ALLOW)
- Tamper detection with cryptographic proof
- Deterministic decision replay
- Demo-grade persistence for verification

This is the **non-negotiable foundation** of UAAL.

---

> **Authorization is belief.  
> Evidence is truth.**

