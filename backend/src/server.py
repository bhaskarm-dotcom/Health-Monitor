from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import sys
import os

# Handle imports - support both relative (package) and absolute (script) imports
try:
    from .models import HealthReport, Project
    from .data_adapter import DataAdapter
    from .health_calculator import HealthCalculator
    from .ai_service import AIService
except ImportError:
    # If relative imports fail, use absolute imports
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import HealthReport, Project
    from data_adapter import DataAdapter
    from health_calculator import HealthCalculator
    from ai_service import AIService

app = FastAPI(title="AI Project Health Monitor API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],  # Frontend ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_adapter = DataAdapter(use_mock=True)
health_calculator = HealthCalculator()
ai_service = AIService()

# Store previous scores for trend calculation (in production, use a database)
previous_scores = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Project Health Monitor API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Project Health Monitor API"}


@app.get("/api/projects", response_model=List[dict])
async def get_projects():
    """Get list of all projects."""
    projects = data_adapter.get_all_projects()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "created_at": p.created_at.isoformat(),
        }
        for p in projects
    ]


@app.get("/api/projects/{project_id}", response_model=dict)
async def get_project(project_id: str):
    """Get project details."""
    project = data_adapter.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at.isoformat(),
        "task_count": len(project.tasks),
        "team_member_count": len(project.team_members),
    }


@app.get("/api/projects/{project_id}/health", response_model=HealthReport)
async def get_project_health(project_id: str):
    """Get comprehensive health report for a project."""
    project = data_adapter.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get previous score for trend calculation
    previous_score = previous_scores.get(project_id)
    
    # Calculate health score
    health_score = health_calculator.calculate_health_score(project, previous_score)
    
    # Store current score for next calculation
    previous_scores[project_id] = health_score.overall_score
    
    # Detect risks
    risks = health_calculator.detect_risks(project, health_score)
    
    # Generate AI recommendations
    recommendations = ai_service.generate_recommendations(
        health_score, risks, project.name
    )
    
    # Create health report
    report = HealthReport(
        project_id=project.id,
        project_name=project.name,
        health_score=health_score,
        risks=risks,
        recommendations=recommendations,
        generated_at=datetime.now()
    )
    
    return report


@app.get("/api/projects/{project_id}/health/score", response_model=dict)
async def get_health_score(project_id: str):
    """Get just the health score (lightweight endpoint)."""
    project = data_adapter.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    previous_score = previous_scores.get(project_id)
    health_score = health_calculator.calculate_health_score(project, previous_score)
    previous_scores[project_id] = health_score.overall_score
    
    return {
        "score": health_score.overall_score,
        "status": health_score.status.value,
        "trend": health_score.trend,
        "calculated_at": health_score.calculated_at.isoformat(),
    }


@app.post("/api/analyze-sentiment")
async def analyze_sentiment(text: str):
    """Analyze sentiment of provided text."""
    sentiment = ai_service.analyze_sentiment(text)
    return {"text": text, "sentiment": sentiment}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

