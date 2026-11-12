# Claude agent team

A team of 27 Claude Code subagents for building software securely, accessibly and efficiently, led by a chief of staff. Each file is one agent. They hand work to each other in a shared format, and every high-impact decision comes back to a human.

## The team

**Leading the work**

| Agent | Model | Role |
|---|---|---|
| `chief-of-staff` | opus | Your chief of staff. Challenges and shapes requests, runs the team, brings decisions to you, gives briefings and keeps priorities across projects. See the setup sections below for how to start it. |
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
| `feature-planner` | sonnet | Takes one new feature or upgrade from request to an approved, backlog-ready plan, with the security-architect's input. |
| `feedback-manager` | sonnet | Triages feedback from users, finds where fixes apply and routes it. Features and upgrades go to `feature-planner`. |

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
| `code-reviewer` | session model | Security-focused code review, written to `code-reviews/`. |
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

## How a project works: interview, playbook, toolbox, proof

1. **Interview:** the chief of staff asks you one question at a time until it understands the goal, users, scope, constraints, risks and what done looks like, then plays back a summary for you to confirm.
2. **Playbook** (`playbook/playbook.md`): your answers become numbered rules (PB-1, PB-2...) that every agent follows. You approve them. New projects start from the master playbook in `.playbook/master-playbook.md`.
3. **Toolbox** (`playbook/toolbox.md`): everything you approve (designs, decisions, components, templates) is registered and tied to the rules it implements. Agents reuse it before building anything new.
4. **Proof** (`playbook/proof.md`): checkable criteria for done (PR-1, PR-2...), plus a showcase of the first approved piece of work. Every agent checks its work against the proof before saying it's done.
5. **Fixing:** when something goes wrong, the chief of staff traces it to a rule, proposes a change for you to approve, and re-runs only the work linked to that rule.

## Skills

Agents use skills for work that should be calculated or pattern-matched by code, not judged: tested Python scripts with short instructions. They live in `.skills/` and are installed with `install-skills.py`.

| Skill | Used by | What it does |
|---|---|---|
| `agent-lint` | `agent-steward` | Checks every agent against the team's conventions. |
| `secret-scan` | `code-reviewer`, `engineer`, `delivery-engineer`, `platform-security`, `release-manager` | Finds committed secrets without printing them. |
| `plain-english-check` | `writer`, `agent-steward` | Finds dashes, AI writing tells, American spellings and long sentences. |
| `experiment-stats` | `behavioural-scientist`, `analytics-engineer` | A/B test sample size, duration and analysis. |
| `risk-scoring` | `grc`, `threat-modeller` | Scores risks on the 5x5 matrix. |
| `token-usage` | `token-minimiser` | Totals token use from session transcripts. |
| `breach-clock` | `incident-responder` | The 72-hour ICO deadline. |
| `feedback-intake` | `feedback-manager`, `user-researcher` | Reads feedback CSV files, redacts personal data and flags urgent items. |
| `contrast-check` | `ux-designer`, `test-writer` | WCAG colour contrast ratios. |
| `approvals-check` | `human-in-the-loop`, `release-manager` | Finds expired and unanswered approvals. |
| `business-case` | `commercial-analyst` | Net present value, payback and sensitivity. |
| `service-levels` | `reliability-engineer` | Downtime budgets, error budget burn and percentiles. |
| `dependency-audit` | `platform-security` | First-pass supply chain check. |
| `feature-register` | `feature-planner` | Creates numbered feature files and checks no stage was skipped. |
| `adr-register` | `security-architect` | Creates numbered decision records and lists their status. |
| `backlog-check` | `product-manager` | Finds incomplete stories and calculates RICE scores. |
| `domain-profile-check` | `expert` | Finds uncited requirements and out-of-date sources. |
| `agent-attack-surface` | `ai-red-teamer` | Maps what each agent could do if manipulated, with a library of safe test cases. |
| `claims-check` | `go-to-market-lead`, `writer` | Finds marketing claims that need evidence. |
| `proof-status` | `chief-of-staff`, `release-manager` | Counts proof criteria met and not met. |

Two more are commands you type in a chief-of-staff session:

| Command | What it starts |
|---|---|
| `/new-feature <the feature>` | The feature route: questions, brief, security design, plan, your approval, backlog. |
| `/triage-feedback <CSV file>` | The feedback route: redact, group, flag urgent items, route fixes and feature requests. |

The scripts need Python 3.9 or later and nothing else.

## Using the team in the Claude app (cloud sessions)

If you work in the Claude app against your GitHub repositories, your sessions run in the cloud, not on your computer. Nothing in your own `.claude` folder is visible there. A setup script on the cloud environment fetches this repository and installs the skills each time a new session starts, so the team is available in every project.

**The setup script** (already saved on the Default environment):

```bash
#!/bin/bash
# Fetch the Claude agent team and install its skills for this session.
# Every step is allowed to fail, so a problem here never stops a session starting.
[ -d "$HOME/.claude/agents/.git" ] || git clone -q --depth 1 https://github.com/inkleyoliver/claude-agent-team "$HOME/.claude/agents" || true
[ -f "$HOME/.claude/agents/install-skills.py" ] && python3 "$HOME/.claude/agents/install-skills.py" | head -1 || true
```

To add it to another environment, open the environment menu in a session's title bar, choose Edit, and paste it in as the setup script.

**Things to know**

- Each new session fetches the latest `main`, so changes pushed here reach every new session. There is nothing to reinstall.
- This repository must stay public. The script fetches it without signing in, so if the repository is made private the fetch fails quietly and the agents do not load.
- A session that is already open keeps the version it started with.

**Check it worked.** In a new session, ask "List the agents you have available" and look for `chief-of-staff`. Then type `/` and look for `/new-feature` and `/triage-feedback`.

**Working with the team in the app**

| To do this | Type this |
|---|---|
| Plan a new feature or an upgrade | `/new-feature` and the feature in a sentence |
| Process new feedback | Upload the CSV file, then `/triage-feedback` |
| Use one agent | Ask for it by name, for example "use the code-reviewer agent on this change" |
| Run a whole project | "Act as chief of staff and follow `~/.claude/agents/chief-of-staff.md`" |

The app has no confirmed way to start a session as the chief of staff, as `claude --agent chief-of-staff` does in the terminal, so the last row is the way to do it there.

## Using the team on your own computer

This is for the terminal, or for sessions in the desktop app that work on folders on your computer. Cloud sessions do not use it.


1. Install Claude Code and the GitHub CLI, and sign in with `gh auth login`.
2. Clone this repository into your Claude agents folder:

   ```bash
   gh repo clone inkleyoliver/claude-agent-team ~/.claude/agents
   ```

   If `~/.claude/agents` already exists, move its contents somewhere safe first.
3. Install the skills (on Windows, use `py -3` if `python` is not found):

   ```bash
   python ~/.claude/agents/install-skills.py
   ```

   Run this again whenever you pull changes.
4. Start a new Claude Code session. The agents are available straight away. In the terminal, start the chief of staff with `claude --agent chief-of-staff`.

On Windows PowerShell, write `$HOME\.claude\agents` in place of `~/.claude/agents`, because PowerShell does not expand `~` for git.

## Saving changes

The `agent-steward` agent commits and pushes changes for you. In a cloud session, pushing needs this repository to be connected to the session. To do it by hand on your own computer, from `~/.claude/agents`:

```bash
git add -A && git commit -m "Describe the change" && git push
```
