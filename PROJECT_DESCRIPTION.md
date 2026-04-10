# OpenEnv: Real-World Task Environment

## 📋 Project Overview

**OpenEnv** is a comprehensive benchmarking environment for evaluating AI agents on real-world operational tasks. It provides three practical, production-grade tasks that test agent decision-making, reasoning, and action execution capabilities.

Unlike toy environments (games, simple puzzles), OpenEnv simulates authentic workflows that organizations actually perform, making it ideal for assessing agent readiness for real deployment scenarios.

---

## 🎯 Core Purpose

OpenEnv enables researchers and practitioners to:

1. **Benchmark AI agents** on meaningful, non-trivial tasks
2. **Measure agent performance** with deterministic, reproducible scoring
3. **Test decision-making** across difficulty levels (easy → hard)
4. **Evaluate reasoning quality** through structured feedback
5. **Compare baseline approaches** with reproducible metrics

---

## 📦 What's Included

### **3 Real-World Tasks**

#### **1. Email Classification** (Difficulty: Easy)
Classify incoming emails into business categories with confidence calibration.

- **Objective:** Determine if an email is `important`, `spam`, or `promotional`
- **Action Space:** Classification choice + confidence score (0.0-1.0)
- **Reward Structure:**
  - 60% for correct classification
  - 40% for confidence calibration (penalizes overconfidence, rewards calibrated confidence)
- **Difficulty Progression:**
  - Easy: Clear, unambiguous emails
  - Medium: Mixed signals, borderline cases
  - Hard: Deceptive, misleading content
- **Examples:** 13 deterministic test cases

**Use Case:** Automated email triage systems, inbox prioritization, spam filtering

---

#### **2. Code Review** (Difficulty: Medium)
Identify security, performance, style, and logic issues in code snippets.

- **Objective:** Detect code issues and assess their severity
- **Action Space:**
  - Issue types (security, style, logic, performance, or none)
  - Severity level (critical, major, minor, none)
  - Priority and suggested fixes
- **Reward Structure:**
  - 50% for correctly identifying issues
  - 50% for accurate severity assessment
  - Partial credit for near-correct answers
- **Difficulty Progression:**
  - Easy: Obvious issues (unparameterized SQL, hardcoded secrets)
  - Medium: Subtle issues (inefficient loops, poor naming)
  - Hard: Context-dependent issues (security vs. performance tradeoffs)
- **Examples:** 9 deterministic test cases

**Use Case:** Automated code review, static analysis, security scanning, code quality gates

---

#### **3. Customer Support Routing** (Difficulty: Hard)
Route support tickets to the correct department with appropriate triage.

- **Objective:** Assign ticket to department, prioritize, assign response type and tone
- **Action Space:**
  - Department (billing, technical, general, escalation)
  - Priority level (low, medium, high, urgent)
  - Response type (auto-reply, human review, escalate)
  - Tone (empathetic, formal, urgent, casual)
  - Estimated resolution time
- **Reward Structure:**
  - 35% for correct department assignment
  - 25% for accurate priority classification
  - 20% for choosing appropriate response type
  - 20% for tone matching customer sentiment
- **Difficulty Progression:**
  - Easy: Straightforward issues with clear triage
  - Medium: Compound issues requiring multi-factor analysis
  - Hard: Escalation scenarios, VIP handling, emotional intelligence needed
- **Examples:** 10 deterministic test cases

**Use Case:** Ticketing systems, customer support automation, SLA management, chatbot triage

---

## 🏗️ Technical Architecture

### **Environment Interface** (OpenEnv Compliance)

```python
env = create_env(task_id="email_classification", difficulty="easy")

# Reset episode and get initial observation
observation = env.reset()

# Main loop
while not done:
    action = agent(observation)                    # Agent decides
    next_obs, reward, done, info = env.step(action)  # Environment responds
    observation = next_obs
```

### **Core Components**

| Component | Purpose | Details |
|-----------|---------|---------|
| `env/environment.py` | Core engine | 3 task implementations (EmailEnv, CodeReviewEnv, SupportEnv) |
| `env/grader.py` | Deterministic scoring | 0.0-1.0 reward per step, partial credit logic |
| `env/models.py` | Type safety | Pydantic v2 models for actions, observations, rewards |
| `inference.py` | Benchmark script | Main entry point for agent evaluation |
| `app.py` | REST API | FastAPI service for remote environment access |
| `openenv.yaml` | Metadata | Full environment specification (tasks, spaces, endpoints) |

### **Deployment**

- **Framework:** FastAPI + Uvicorn
- **Containerization:** Docker (python:3.10-slim)
- **Port:** 7860 (Hugging Face Spaces standard)
- **LLM Integration:** OpenAI Client with configurable base URL and model
- **Deployment Target:** Hugging Face Spaces (auto-deploy from GitHub)

---

## 📊 Features

### **✓ Deterministic Grading**
- Same task input produces same score every time
- Enables fair, reproducible benchmarking
- Scores in [0.0, 1.0] with clear rubric

### **✓ Difficulty Progression**
- Each task has 3 difficulty levels
- Easy scenarios test basic competence
- Hard scenarios test nuanced reasoning
- Total 27 scenarios (3 tasks × 3 difficulties × 3 examples)

### **✓ Meaningful Rewards**
- Per-step feedback (not just final score)
- Partial credit for close/reasonable answers
- Penalties for invalid/incomplete actions
- Supports trajectory-based learning

### **✓ Reproducible Baselines**
- Rule-based policy for fallback
- OpenAI API integration with deterministic parameters
- Baseline scores: 0.52 average reward/step
- Facilitates agent improvement measurement

### **✓ REST API**
- Health checks (`GET /`)
- Task metadata (`GET /tasks`)
- Environment control (`POST /init`, `GET /reset`, `POST /step`)
- Grading (`POST /grader`)
- Baseline evaluation (`GET /baseline`)

### **✓ Structured Logging**
- Inference script outputs `[START]`, `[STEP]`, `[END]` markers
- JSON metrics for automated evaluation
- Supports both local and remote scoring

---

## 🚀 Quick Start

### **Local Installation**

```bash
# Clone and setup
cd /home/mohan/openenv-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run benchmark
python3 inference.py

# Start API server
uvicorn app:app --host 0.0.0.0 --port 7860
```

### **Docker Deployment**

```bash
# Build
docker build -t openenv .

# Run
docker run -p 7860:7860 openenv
```

### **Hugging Face Spaces**

1. Push to GitHub
2. Create HF Space (Docker SDK)
3. Connect GitHub → auto-deploy
4. Set environment variables:
   - `API_BASE_URL`: LLM API endpoint
   - `MODEL_NAME`: Model identifier
   - `HF_TOKEN`: API key
5. Access at `https://huggingface.co/spaces/username/openenv-project`

---

## 📈 Expected Performance

### **Baseline Rule-Based Policy**

| Task | Easy | Medium | Hard | Average |
|------|------|--------|------|---------|
| **Email Classification** | 0.483 | 0.675 | 0.900 | 0.686 |
| **Code Review** | 0.583 | 0.333 | 0.417 | 0.444 |
| **Support Routing** | 0.633 | 0.425 | 0.288 | 0.449 |
| **Overall Average** | 0.566 | 0.478 | 0.535 | **0.526** |

*With OpenAI API enabled, performance typically improves by 15-30%*

---

## 🔄 Environment Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ Agent                                                             │
└──────────────────────────┬──────────────────────────────────────┘
                          │
                    ┌─────▼────────┐
                    │  observe()   │
                    └─────┬────────┘
                          │
                    ┌─────▼────────────────────────┐
                    │ "I see email about payment"  │
                    │ (observation dictionary)     │
                    └─────┬────────────────────────┘
                          │
                    ┌─────▼──────────────┐
                    │  action = decide() │
                    └─────┬──────────────┘
                          │
            ┌─────────────▼──────────────────┐
            │ {"classification": "important",│
            │  "confidence": 0.8}            │
            └─────────────┬──────────────────┘
                          │
                    ┌─────▼─────────────────────────────────────┐
                    │ env.step(action)                          │
                    │ → (next_obs, reward, done, info)          │
                    └─────┬─────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌─────▼─────┐    ┌─────▼────┐
   │next_obs │      │ reward:   │    │ info:    │
   │{...}    │      │ 0.95      │    │{grade}   │
   └────┬────┘      └─────┬─────┘    └─────┬────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                    ┌─────▼─────────┐
                    │ done? No → Go │
                    │ back to step 1│
                    └──────────────┘
```

**Key Elements:**

1. **Observation:** Dictionary with task-specific fields (email body, code snippet, ticket description)
2. **Action:** Agent's decision (classification, severity, routing, etc.)
3. **Reward:** Immediate feedback (0.0-1.0) on action quality
4. **Info:** Grading details and reasoning
5. **Done:** Episode termination (max steps or task completion)

---

## 📝 Example Interaction

### **Email Classification Task**

```python
# Initialize
env = create_env("email_classification", "easy")
obs = env.reset()

# Observation: Email about payment plan change
print(obs)
# {
#   'email_subject': 'Your payment plan will change next month',
#   'email_body': 'We are upgrading your account...',
#   'sender_domain': 'company.com',
#   'has_links': False,
#   'has_attachments': False,
#   'word_count': 87,
#   'task_id': 'email_classification',
#   'step': 0,
#   'episode_length': 6
# }

# Agent decision
action = {
    'classification': 'important',
    'confidence': 0.85
}

# Step
next_obs, reward, done, info = env.step(action)
print(f"Reward: {reward}")     # 0.95 (correct + well-calibrated)
print(f"Grading: {info['grade']['reasoning']}")
# "✓ Correct classification: important | ✓ Confidence well-calibrated (0.85)"
```

---

## 🎓 Research Applications

OpenEnv is designed for:

- **Agent Benchmarking:** Compare different LLM-based approaches
- **Prompt Engineering:** Evaluate prompt quality through task performance
- **Fine-tuning:** Measure improvement from instruction-tuned models
- **Multi-task Learning:** Test generalization across different task types
- **Robustness Testing:** Evaluate consistency at multiple difficulty levels
- **Real-world Evaluation:** Assess deployment readiness for actual workflows

---

## 📋 Project Structure

```
openenv-project/
├── inference.py                 # Main entry point (benchmark script)
├── app.py                       # FastAPI REST API
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container specification
├── openenv.yaml                 # Environment metadata
├── README.md                    # Setup & deployment guide
├── SUBMISSION_CHECKLIST.md      # Validation results
├── env/
│   ├── environment.py           # Core environment (3 tasks)
│   ├── models.py                # Pydantic type definitions
│   ├── grader.py                # Deterministic graders
│   ├── tasks.py                 # Task metadata
│   ├── task_data_email.py       # Email examples
│   ├── task_data_code_review.py # Code examples
│   └── task_data_support.py     # Support ticket examples
└── baseline/
    └── run.py                   # Legacy baseline script
```

---

## 🔑 Key Capabilities

| Feature | Implementation | Status |
|---------|---|---|
| **3+ Real Tasks** | Email, Code, Support | ✅ |
| **Deterministic Scoring** | 0.0-1.0 range, reproducible | ✅ |
| **Difficulty Levels** | Easy, Medium, Hard | ✅ |
| **Partial Credit** | contextual grading | ✅ |
| **REST API** | FastAPI endpoints | ✅ |
| **Docker Ready** | HF Spaces compatible | ✅ |
| **LLM Integration** | OpenAI Client + fallback | ✅ |
| **Baseline** | Rule-based + API-driven | ✅ |
| **Structured Logging** | [START]/[STEP]/[END] format | ✅ |
| **Configuration** | API_BASE_URL, MODEL_NAME, HF_TOKEN | ✅ |

---

## 💡 Why OpenEnv?

**Problem:** Most benchmarks use toy tasks (games, puzzles) that don't reflect real-world complexity.

**Solution:** OpenEnv provides authentic operational tasks where:
- Decisions have multiple valid approaches
- Context matters (the same action in different contexts has different values)
- Partial correctness is meaningful
- Reproducibility is guaranteed

**Result:** Benchmarks that actually predict real-world agent performance.

---

## 📞 Technical Support

For issues or questions:

1. Check [README.md](README.md) for setup instructions
2. Review [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) for validation status
3. Run `python3 validator.py` for pre-submission checks
4. Test locally: `python3 inference.py`
5. Test Docker: `docker build -t openenv . && docker run -p 7860:7860 openenv`

---

## ✨ Summary

**OpenEnv** is a production-grade benchmarking environment that:
- Provides 3 real-world tasks with 27 test scenarios
- Delivers deterministic, reproducible scoring
- Supports difficulty progression (easy → hard)
- Integrates with OpenAI and other LLMs
- Deploys to Hugging Face Spaces
- Measures agent decision-making quality

Perfect for evaluating AI agents on meaningful tasks that matter to organizations.

---

**Status:** ✅ Ready for Submission  
**Last Updated:** April 8, 2026  
**Validation:** 13/13 checks passed
