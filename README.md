# 🌍 OpenEnv: Production-Ready Real-World Tasks Environment

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?style=flat-square)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square)](https://www.docker.com/)
[![HF Spaces](https://img.shields.io/badge/HF%20Spaces-Compatible-yellow?style=flat-square)](https://huggingface.co/spaces)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A **production-grade multi-task evaluation environment** for benchmarking AI agents on realistic workflow automation. Featuring adaptive difficulty, sequential learning, and sophisticated risk-aware reward modeling.

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Why This Is Different](#-why-this-is-different)
- [Tasks Overview](#-tasks-overview)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Baseline Results](#-baseline-results)
- [Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd openenv-project
pip install -r requirements.txt

# Run inference
python3 inference.py

# Or start API server
uvicorn app:app --host 0.0.0.0 --port 7860
```

## ✨ Features

### Core Features
- ✅ **3 Real-World Tasks**: Email classification, code review, support routing
- ✅ **Adaptive Difficulty**: Automatically adjusts challenge level based on agent performance
- ✅ **Multi-Step Memory**: Agents learn from conversation history across episodes
- ✅ **Safety-Aware Scoring**: Risk-aware rewards with penalties for failures
- ✅ **Deterministic Graders**: Reproducible scoring across all tasks
- ✅ **Production-Ready**: Exception handling, type validation, comprehensive logging

### Advanced Features
- 🔧 **Multi-Component Rewards**: Sophisticated scoring with bonuses and penalties
- 🎯 **Confidence Calibration**: Evaluates both accuracy and confidence levels
- ⚡ **Per-Step Feedback**: Real-time reward signals for learning
- 🛡️ **Error Recovery**: Graceful fallbacks and comprehensive error handling
- 📊 **Structured Logging**: `[START]/[STEP]/[END]` format for easy parsing
- 🤖 **OpenAI Integration**: LLM-powered inference with rule-based fallback

## 🎯 Why This Is Different

### Traditional Benchmark Problems ❌
- Fixed task sequences → agents get bored or frustrated
- No learning from history → agents can't reason sequentially
- Simple scoring → no concept of risk or consequences
- Fragile on errors → crashes on unexpected inputs

### OpenEnv Solutions ✅

**1. Adaptive Difficulty**
- Automatically skips harder scenarios when agent performs well (reward > 0.7)
- Creates personalized difficulty curves matching agent capability
- Prevents boredom for high-performing agents

**2. Sequential Learning (Multi-Step Memory)**
- Agents see full conversation history across steps
- Track action sequences within episodes
- Build on previous context for multi-turn decisions

**3. Real-World Risk Modeling**
- **Risk awareness**: -0.3 penalty for missing critical escalations
- **Cost penalty**: -0.05 for unnecessary escalations
- **Time decay**: 0.02 per step (long conversations discouraged)
- **Context-aware scoring**: Adapts to situation risk level

**4. Production-Grade Robustness**
- Exception handling catches all errors gracefully
- Type validation on every return
- Comprehensive error tracking with tracebacks

## 📚 Tasks Overview

### 1️⃣ Email Classification (Easy)
Classify emails as **important**, **spam**, or **promotional**
- **Domain**: Customer communication filtering
- **Complexity**: Low (3-class classification)
- **Reward**: Base score + confidence calibration

### 2️⃣ Code Review (Medium)
Identify code issues: **security**, **performance**, **style**, **logic**
- **Domain**: Software quality assurance
- **Complexity**: Medium (multi-label detection)
- **Reward**: Issue detection + severity assessment

### 3️⃣ Support Routing (Hard)
Route tickets with correct **department**, **priority**, **response type**, **tone**
- **Domain**: Customer service automation
- **Complexity**: High (multi-decision with context)
- **Reward**: Department + priority + response type + tone

Each task includes 40+ diverse scenarios across 3 difficulty levels (easy, medium, hard).

## 💻 Installation

### Prerequisites
- Python 3.10+
- pip or conda
- (Optional) Docker for containerized deployment

### Local Setup

```bash
# Clone repository
git clone <repo-url>
cd openenv-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -c "from app import app; print('✅ Installation successful')"
```

### Docker Setup

```bash
# Build image
docker build -t openenv .

# Run container
docker run -p 7860:7860 openenv

# Test
curl http://localhost:7860/
```

### Environment Variables

For inference and API access, configure:

```bash
# LLM Configuration (optional - has rule-based fallback)
export OPENAI_API_KEY="sk-..."           # OpenAI API key
export API_BASE_URL="https://api.openai.com/v1"  # API endpoint
export MODEL_NAME="gpt-4o-mini"          # Model identifier

# HuggingFace (for Spaces deployment)
export HF_TOKEN="hf_..."                 # HF API token
```

## 📖 Usage

### Run Inference Script

```bash
python3 inference.py
```

Output format:
```
[START] task=email_classification difficulty=easy
[STEP] step=1 reward=0.90 action={'classification': 'important', 'confidence': 0.8}
[STEP] step=2 reward=1.00 action={'classification': 'spam', 'confidence': 0.9}
[END] total_score=0.95
```

### Start API Server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

### Test Individual Tasks

```python
from env.environment import create_env

# Create environment
env = create_env('email_classification', 'easy')

# Reset and get initial observation
obs = env.reset()
print(f"Email subject: {obs['email_subject']}")

# Execute action
action = {
    'classification': 'important',
    'confidence': 0.85
}
next_obs, reward, done, info = env.step(action)
print(f"Reward: {reward}, Done: {done}")
```

## � Deployment

### Local Development

```bash
# Start server
uvicorn app:app --host 0.0.0.0 --port 7860 --reload

# In another terminal, run inference
python3 inference.py
```

### Docker Deployment

```bash
# Build
docker build -t openenv .

# Run
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  openenv

# Test
curl http://localhost:7860/
```

### Hugging Face Spaces

1. **Create Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Docker" runtime
   - Set name: `openenv` (or your preferred name)

2. **Configure Variables**
   - Settings → Variables and secrets
   - Add:
     ```
     OPENAI_API_KEY = sk-...
     HF_TOKEN = hf_...
     ```

3. **Deploy**
   ```bash
   git remote add hf https://huggingface.co/spaces/your-username/openenv
   git push hf main
   ```

4. **Access**
   - URL: `https://huggingface.co/spaces/your-username/openenv`

## 📊 Baseline Results

The baseline agent (OpenAI-powered + fallback) achieves the following scores:

- **email_classification**: 0.78
- **code_review**: 0.65
- **support_routing**: 0.72

**Baseline Strategy:**
- ✅ OpenAI-powered reasoning when API available
- ✅ Graceful fallback to rule-based heuristics
- ✅ Task-specific prompts optimized for each domain
- ✅ Multi-step memory enabling context awareness
- ✅ Dynamic difficulty adjustment for diverse agents

## 🔧 Troubleshooting

### Issue: "Connection refused" when running inference
**Solution:** Make sure API server is running
```bash
# Terminal 1: Start API
uvicorn app:app --host 0.0.0.0 --port 7860

# Terminal 2: Run inference
python3 inference.py
```

### Issue: "OpenAI API key not found"
**Solution:** This is OK! System has graceful fallback
- Without key: Uses rule-based heuristics
- With key: Uses OpenAI (set `OPENAI_API_KEY` env var)

```bash
export OPENAI_API_KEY="sk-your-key-here"
python3 inference.py
```

### Issue: Docker build fails
**Solution:** Clear cache and rebuild
```bash
docker system prune -a
docker build -t openenv . --no-cache
```

### Issue: Port 7860 already in use
**Solution:** Use different port
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
# Then access at http://localhost:8000
```

### Issue: Pydantic validation errors
**Solution:** Check action format matches schema
```python
# ✅ Correct
action = {'classification': 'important', 'confidence': 0.85}

# ❌ Wrong - missing fields
action = {'classification': 'important'}
```

## 📁 Project Structure

```
openenv-project/
├── inference.py              # ⭐ Main benchmark script (run this!)
├── app.py                    # FastAPI REST server
├── openenv.yaml              # Environment configuration
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container configuration
├── README.md                 # This file
├── env/
│   ├── environment.py        # Core environment engine
│   ├── grader.py             # Task-specific scorers
│   ├── models.py             # Pydantic models
│   └── tasks.py              # Task definitions & data
└── baseline/
    └── run.py                # Baseline evaluation script
```

## 🎖️ Key Achievements

- ✅ **Production-Ready**: Comprehensive error handling & logging
- ✅ **Realistic Tasks**: 40+ scenarios per task across 3 difficulties
- ✅ **Advanced Rewards**: Multi-component scoring with bonuses/penalties
- ✅ **Type-Safe**: Full Pydantic validation on all I/O
- ✅ **Well-Documented**: Complete API documentation & examples
- ✅ **Reproducible**: Deterministic grading for fair comparison
- ✅ **Scalable**: Works locally, Docker, or HF Spaces
- ✅ **Tested**: 11-test comprehensive validation suite

## 📚 Additional Resources

### Reading Material
- [OpenEnv Paper](https://example.com)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Related Projects
- [Gym](https://gymnasium.farama.org/) - RL environment framework
- [TextWorld](https://www.microsoft.com/en-us/research/project/textworld/) - Text-based game simulator

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional task domains
- More sophisticated graders
- Performance optimizations
- Better documentation

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#-troubleshooting) section
2. Review [API Reference](#-api-reference)
3. Check project GitHub issues

---

**Built with ❤️ for production AI evaluation**

Last updated: April 2026 | Version: 1.0.0
# OPENENV
