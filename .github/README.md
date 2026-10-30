# Claude agent team

A team of 25 Claude Code subagents for building software securely, accessibly and efficiently, led by a chief of staff. Each file is one agent. They hand work to each other in a shared format, and every high-impact decision comes back to a human.

## The team

**Leading the work**

| Agent | Model | Role |
|---|---|---|
| `chief-of-staff` | opus | Your chief of staff. Challenges and shapes requests, runs the team, brings decisions to you, gives briefings and keeps priorities across projects. Start it with `claude --agent chief-of-staff`. |
| `human-in-the-loop` | opus | Approval gatekeeper. Writes decision briefs and keeps the approvals log. Never approves anything itself. |
| `agent-steward` | sonnet | Builds and improves agents to the team's conventions, keeps this README current and runs retrospectives. |

**Understanding the problem**

| Agent | Model | Role |
|---|---|---|
| `expert` | opus | Becomes an expert in whatever field the project is about, with a lasting domain profile and cited sources. |
| `product-manager` | sonnet | Problem, outcomes, minimal scope, user stories and roadmap. |
| `user-researcher` | sonnet | Plans inclusive research and turns findings and feedback into evidence. |
| `behavioural-scientist` | opus | Diagnoses behaviour (COM-B and more) and owns the science of A/B tests. |
| `commercial-analyst` | sonnet | Business cases, running costs, pricing and payback. |

**Designing**

| Agent | Model | Role |
|---|---|---|
| `security-architect` | opus | Asks what you're building, then designs a simple, secure architecture. |
| `threat-modeller` | opus | STRIDE threat models in plain English. |
| `ux-designer` | sonnet | Accessible, distinctive design with A/B prototype options. |
| `writer` | sonnet | Plain English, UK GOV.UK style, no AI writing tells. |
| `analytics-engineer` | sonnet | Privacy-safe tracking plans and precise metrics. |

**Building and checking**

| Agent | Model | Role |
|---|---|---|
| `engineer` | session model | Writes as little code as possible. Works on its own branch; never pushes. |
| `delivery-engineer` | session model | Secure CI/CD pipelines, deployment scripts and infrastructure as code. Never deploys. |
| `code-reviewer` | session model | Security-focused code review. |
| `test-writer` | sonnet | Tests with security cases, and clear plain-English test logs. |
| `platform-security` | opus | Supply chain, CI/CD, infrastructure and containers. |
| `reliability-engineer` | sonnet | Service levels, performance, load tests, security logging, recovery and cost. |
| `ai-red-teamer` | opus | Tests AI features and this team against prompt injection and misuse, in approved test scopes only. |

**Governing, shipping and launching**

| Agent | Model | Role |
|---|---|---|
| `grc` | opus | Policies, risk register, risk appetite and compliance (ISO 27001, UK GDPR, NIST, AI governance). |
| `release-manager` | sonnet | Go/no-go checklist, release notes and rollback plan. |
| `go-to-market-lead` | sonnet | Audience, positioning, launch plan and honest, legal marketing. |
| `incident-responder` | opus | Incident response, including the UK GDPR 72-hour ICO deadline. |
| `token-minimiser` | sonnet | Finds ways to use fewer tokens without cutting safeguards. |

## Restore on a new device

1. Install Claude Code and the GitHub CLI, and sign in with `gh auth login`.
2. Clone this repository into your Claude agents folder:

   ```bash
   gh repo clone inkleyoliver/claude-agent-team ~/.claude/agents
   ```

   If `~/.claude/agents` already exists, move its contents somewhere safe first.
3. Start a new Claude Code session. The agents are available straight away.

## Saving changes

The `agent-steward` agent commits and pushes changes for you. To do it by hand, from `~/.claude/agents`:

```bash
git add -A && git commit -m "Describe the change" && git push
```
