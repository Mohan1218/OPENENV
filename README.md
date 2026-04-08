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
