# Claude agent team

A team of 19 Claude Code subagents for building software securely, accessibly and efficiently. Each file is one agent. They hand work to each other in a shared format, and every high-impact decision comes back to a human.

## The team

**Leading the work**

| Agent | Model | Role |
|---|---|---|
| `orchestrator` | opus | Plans the route through the team, runs agents, passes handoffs and brings decisions to you. Start it with `claude --agent orchestrator`. |
| `human-in-the-loop` | opus | Approval gatekeeper. Writes decision briefs and keeps the approvals log. Never approves anything itself. |

**Understanding the problem**

| Agent | Model | Role |
|---|---|---|
| `expert` | opus | Becomes an expert in whatever field the project is about, with a lasting domain profile and cited sources. |
| `product-manager` | sonnet | Problem, outcomes, minimal scope, user stories and roadmap. |
| `behavioural-scientist` | opus | Diagnoses behaviour (COM-B and more) and owns the science of A/B tests. |

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
| `code-reviewer` | session model | Security-focused code review. |
| `test-writer` | sonnet | Tests with security cases, and clear plain-English test logs. |
| `platform-security` | opus | Supply chain, CI/CD, infrastructure and containers. |
| `ai-red-teamer` | opus | Tests AI features and this team against prompt injection and misuse, in approved test scopes only. |

**Governing and shipping**

| Agent | Model | Role |
|---|---|---|
| `grc` | opus | Policies, risk register, risk appetite and compliance (ISO 27001, UK GDPR, NIST, AI governance). |
| `release-manager` | sonnet | Go/no-go checklist, release notes and rollback plan. |
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

After changing an agent, from `~/.claude/agents`:

```bash
git add -A && git commit -m "Describe the change" && git push
```
