# OpenEnv Real-World Tasks Environment

This project implements a multi-task OpenEnv environment for realistic workflow automation.
It includes three practical tasks with deterministic graders and per-step reward feedback.

## Environment Overview

This environment simulates real operational tasks (not games):

1. Email triage/classification
2. Code review issue detection
3. Customer support routing

The design targets agent benchmarking with reproducible scoring and clear progression from easy to hard scenarios.

## Tasks and Difficulty

### 1) Email Classification (Easy)
Objective: classify each email as `important`, `spam`, or `promotional`.

### 2) Code Review (Medium)
Objective: identify code issues and severity (`security`, `performance`, `style`, etc.).

### 3) Support Routing (Hard)
Objective: choose department, priority, response type, and tone for customer tickets.

## OpenEnv Interface Compliance

Environment implementation provides:

- `reset() -> observation`
- `state() -> observation`
- `step(action) -> (observation, reward, done, info)`

Typed models are defined with Pydantic in `env/models.py` for action/observation/reward schemas.
Metadata is provided in `openenv.yaml`.

## Observation and Action Spaces

### Email Classification
Observation keys:
- `email_subject`, `email_body`, `sender_domain`, `has_links`, `has_attachments`, `word_count`

Action keys:
- `classification`: one of `important | spam | promotional`
- `confidence`: float in `[0.0, 1.0]`

### Code Review
Observation keys:
- `code_snippet`, `language`, `context`, `function_name`, `lines_of_code`

Action keys:
- `issue_types`: list of issue labels
- `severity`: `critical | major | minor | none`
- `suggested_fix` (optional), `priority`

### Support Routing
Observation keys:
- `ticket_subject`, `ticket_description`, `customer_type`, `sentiment`, `issue_category`
- `previous_interactions`, `account_age_days`, `is_vip`

Action keys:
- `department`: `billing | tech_support | general_support | escalation`
- `priority`: `low | medium | high | urgent`
- `response_type`: `auto_reply | human_review | escalate`
- `tone`: `empathetic | formal | urgent | casual`
- `estimated_resolution_time_hours`: integer in `[1, 72]`

## Graders and Reward Function

Each task has a deterministic grader in `env/grader.py` returning score in `[0.0, 1.0]`.

Reward behavior:
- Per-step feedback (not only terminal)
- Partial credit for partial correctness
- Penalties for undesirable outputs (e.g., overconfident wrong classifications, incorrect routing/tone)

This provides meaningful progress signals along the trajectory.

## Baseline Inference

Baseline script: `baseline/run.py`

- Runs all tasks and difficulty levels
- Produces reproducible summary scores
- Uses OpenAI API client when `OPENAI_API_KEY` is set
- Falls back to deterministic rule-based policy if key is absent

Run baseline:

```bash
python3 -m baseline.run
```

Example (2 episodes per task-difficulty) normalized baseline scores from local run:

| Task | Easy | Medium | Hard |
|---|---:|---:|---:|
| Email Classification (`avg reward/step`) | 0.633 | 0.675 | 0.900 |
| Code Review (`avg reward/step`) | 0.500 | 0.667 | 0.333 |
| Support Routing (`avg reward/step`) | 0.675 | 0.633 | 0.369 |

Overall normalized baseline score (`overall_average_reward_per_step`): **0.598**

## Setup

```bash
cd /home/mohan/openenv-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables (Required for inference.py)

Configure these variables for the inference script:

- `API_BASE_URL`: LLM API endpoint (default: `https://api.openai.com/v1`)
- `MODEL_NAME`: Model identifier (default: `gpt-4o-mini`)
- `HF_TOKEN`: Hugging Face API key (or use `OPENAI_API_KEY` directly)

Example:
```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your_api_key_here"
# or
export OPENAI_API_KEY="your_api_key_here"
```

### Running Inference

Run the benchmark inference script:

```bash
python3 inference.py
```

The script outputs structured logs in the following format:
- `[START] task_id=..., difficulty=..., num_episodes=...`
- `[STEP] episode=..., step=..., reward=..., action=...`
- `[END] task_id=..., difficulty=..., average_reward=..., average_reward_per_step=...`

Example output:
```
[START] task_id=email_classification, difficulty=easy, num_episodes=1
[STEP] episode=1, step=1, reward=0.900, action={'classification': 'important', 'confidence': 0.6}
[STEP] episode=1, step=2, reward=1.000, action={'classification': 'spam', 'confidence': 0.8}
[END] task_id=email_classification, difficulty=easy, average_reward=1.900, average_reward_per_step=0.950
```

### Run API Server Locally

For testing the FastAPI endpoints:

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

Test endpoints:
```bash
curl http://127.0.0.1:7860/   # Health check
curl http://127.0.0.1:7860/tasks   # List tasks
```

## Docker (Working)

Build:

```bash
docker build -t openenv .
```

Run:

```bash
docker run -p 7860:7860 openenv
```

Health check:

```bash
curl http://127.0.0.1:7860/
```

## Hugging Face Spaces Deployment

Use Docker Space runtime:

1. Create a new Docker Space
2. Push this repository
3. Ensure `openenv.yaml` includes deployment metadata
4. Add required secrets in Space settings:
   - `API_BASE_URL` (LLM API endpoint)
   - `MODEL_NAME` (model identifier)
   - `HF_TOKEN` (Hugging Face API key) or `OPENAI_API_KEY`

The app serves on port `7860` as required.

### Running Inference in Space

The `inference.py` script is the entry point for benchmark evaluation. It:
- Reads environment variables for LLM configuration
- Evaluates all tasks (email, code review, support routing) across all difficulties
- Outputs structured logs in `[START]`, `[STEP]`, `[END]` format
- Produces JSON results with performance metrics

Example HF Space command:
```bash
python3 inference.py
```

The baseline policy automatically falls back to rule-based heuristics if the LLM is unavailable.

## Reward Design

Each task implements a **sophisticated multi-component reward function** with base scores, penalties for errors, and bonuses for excellent performance.

### Email Classification Reward Structure

**Base Scoring** (60% weight):
- Correct classification: +0.6
- Incorrect classification: -0.25

**Confidence Calibration** (40% weight):
- Correct prediction with high confidence (≥0.85): +0.4
- Correct prediction with moderate confidence (0.65-0.85): +0.3
- Correct prediction with low confidence (0.5-0.65): +0.15
- Incorrect prediction with high confidence: -0.2 (overconfidence penalty)
- Incorrect prediction with moderate confidence: -0.1

**Bonuses**:
- Well-calibrated confidence (within ±0.1 of target): +0.15 bonus

### Code Review Reward Structure

**Issue Detection** (50% weight):
- Perfect detection (all issues found, no false positives): +0.5 (+0.1 bonus for 2+ issues)
- Partial credit: 0.5 × (overlap / total_unique_issues)
- Missed critical security issue: -0.15 penalty
- False positives: -0.05 per false positive (capped at -0.1)
- Missed all issues: -0.2 penalty

**Severity Assessment** (50% weight):
- Correct severity: +0.5 (+0.1 bonus if critical severity is correct)
- Severity off by 1 level: +0.25
- Severity off by 2+ levels: -0.2 penalty

### Support Routing Reward Structure

**Department Routing** (38% base):
- Correct department: +0.38
- Wrong department: -0.25 penalty
- Missed escalation case (critical): -0.15 severe penalty
- VIP correctly escalated: +0.08 bonus

**Priority Assessment** (22% base):
- Correct priority: +0.22
- Priority off by 1 level: +0.11
- Wrong priority: -0.15 penalty
- Critical urgency prioritized correctly: +0.08 bonus

**Response Type** (22% base):
- Correct response type: +0.22
- Wrong response type: -0.12 penalty

**Tone Appropriateness** (18% base):
- Correct tone: +0.18
- Empathetic for frustrated customer: +0.1 bonus
- No empathy for angry customer: -0.15 penalty
- Wrong tone for VIP premium: -0.12 penalty

### Penalty and Bonus System

**Automatic Penalties** (applied on top of grading):
- Missing required action keys: -0.2 per missing key (capped at -0.5)
- Unexpected action keys: -0.05 per unexpected key (capped at -0.2)

**Explanation Breakdown** (in step info):
Each step's `info["explanation_breakdown"]` includes:
- `score_components`: Dict of each component's contribution
- `penalties_applied`: List of penalty names and values
- `bonuses_applied`: List of bonus names and values
- `detailed_reasoning`: Full text explanation of the score

## Validation

If OpenEnv CLI is installed:

```bash
openenv validate
```

If not installed, validate via:

- baseline execution (`python3 -m baseline.run`)
- API startup (`uvicorn app:app`)
- Docker build/run success

## Project Files

- `inference.py`: **Main benchmark inference script** (required for submission)
- `app.py`: FastAPI service with environment endpoints
- `env/environment.py`: Environment core with `step/reset/state` interface
- `env/models.py`: Pydantic typed schemas for actions/observations/rewards
- `env/grader.py`: Deterministic graders (0.0–1.0 range per task)
- `env/tasks.py`: Task metadata and constants
- `openenv.yaml`: Environment metadata specification
- `baseline/run.py`: Legacy baseline evaluation script
- `requirements.txt`: Python dependencies (fastapi, uvicorn, pydantic, openai)
- `Dockerfile`: Container runtime for local development and HF Spaces
