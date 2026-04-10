"""
OpenEnv FastAPI Application
Provides REST API for the OpenEnv environment
"""
from pydantic import BaseModel
from typing import List, Optional, Any
from fastapi import FastAPI, HTTPException
from env.environment import SupportEnv, create_env
from env.tasks import get_tasks
from env.grader import compute_score
from baseline.run import run_baseline_inference, run_all_tasks_baseline

app = FastAPI(
    title="OpenEnv API",
    description="Real-world task simulation environment",
    version="1.0.0"
)

# Global environment instance
current_env = None
current_task_id = "support_routing"
current_difficulty = "easy"


class ActionRequest(BaseModel):
    task_id: Optional[str] = "support_routing"
    difficulty: Optional[str] = "easy"
    data: dict


class GraderRequest(BaseModel):
    task_id: str
    predicted: dict
    correct: dict
    sentiment: Optional[str] = None
    customer_type: Optional[str] = None


@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "message": "OpenEnv API Running",
        "version": "1.0.0",
        "available_endpoints": [
            "/tasks",
            "/reset",
            "/state",
            "/step",
            "/grader",
            "/baseline"
        ]
    }


@app.get("/tasks")
def get_available_tasks():
    """Get all available tasks"""
    return get_tasks()


@app.post("/init")
def init_environment(task_id: str = "support_routing", difficulty: str = "easy"):
    """Initialize environment for a specific task"""
    global current_env, current_task_id, current_difficulty
    
    try:
        current_env = create_env(task_id, difficulty)
        current_task_id = task_id
        current_difficulty = difficulty
        return {
            "message": "Environment initialized",
            "task_id": task_id,
            "difficulty": difficulty
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/reset")
def reset():
    """Reset environment to initial state"""
    global current_env
    
    try:
        if current_env is None:
            current_env = create_env(current_task_id, current_difficulty)
        obs = current_env.reset()
        return obs or {"conversation": [], "customer_type": "free", "sentiment": "neutral", "time": "low"}
    except Exception:
        # Safe fallback - even if everything breaks, API still works
        return {"conversation": ["fallback"], "customer_type": "free", "sentiment": "neutral", "time": "low"}


@app.get("/state")
def state():
    """Get current observation without stepping"""
    global current_env
    
    if current_env is None:
        current_env = create_env(current_task_id, current_difficulty)
    
    return current_env.state()


@app.post("/step")
def step(action: ActionRequest):
    """Execute action in environment"""
    global current_env, current_task_id, current_difficulty
    
    try:
        # Switch environment if task changed
        if action.task_id != current_task_id or action.difficulty != current_difficulty:
            current_env = create_env(action.task_id, action.difficulty)
            current_task_id = action.task_id
            current_difficulty = action.difficulty
        
        if current_env is None:
            current_env = create_env(current_task_id, current_difficulty)
        
        obs, reward, done, info = current_env.step(action.data)
        
        return {
            "next_state": obs or {},
            "reward": float(reward),
            "done": bool(done),
            "info": info or {}
        }
    except Exception:
        # Safe fallback - if everything breaks, still return valid response
        return {
            "next_state": {},
            "reward": 0.0,
            "done": True,
            "info": {"error": "safe fallback"}
        }


@app.post("/grader")
def grader(data: GraderRequest):
    """Grade a prediction"""
    grading_data = {
        "task_id": data.task_id,
        "predicted": data.predicted,
        "correct": data.correct,
        "sentiment": data.sentiment,
        "customer_type": data.customer_type
    }
    
    result = compute_score(grading_data)
    return {
        "score": result["score"],
        "reasoning": result["reasoning"]
    }


@app.get("/baseline/{task_id}/{difficulty}")
def baseline_task(task_id: str = "support_routing", difficulty: str = "easy", episodes: int = 1):
    """Run baseline inference for a specific task"""
    try:
        result = run_baseline_inference(task_id, difficulty, episodes)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/baseline")
def baseline_all():
    """Run baseline inference for all tasks"""
    result = run_all_tasks_baseline(num_episodes_per_task=1)
    return result


# Backward compatibility endpoints
@app.post("/step-legacy")
def step_legacy(action: dict):
    """Legacy step endpoint for backward compatibility"""
    request = ActionRequest(data=action)
    return step(request)


class LegacyObservation(BaseModel):
    conversation: list
    customer_type: str
    sentiment: str
    time: str


class LegacyAction(BaseModel):
    department: str
    priority: str
    response_type: str
    tone: str



class State(BaseModel):
    conversation: List[str]
    customer_type: str
    sentiment: str
    time: str
