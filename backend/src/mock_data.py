import random
from datetime import datetime, timedelta
from typing import List
import sys
import os

# Handle imports
try:
    from .models import (
        Project, Task, TeamMember, Communication, TaskStatus
    )
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import (
        Project, Task, TeamMember, Communication, TaskStatus
    )


def generate_mock_team_members() -> List[TeamMember]:
    """Generate mock team members."""
    return [
        TeamMember(id="tm1", name="Alice Johnson", email="alice@example.com"),
        TeamMember(id="tm2", name="Bob Smith", email="bob@example.com"),
        TeamMember(id="tm3", name="Carol Williams", email="carol@example.com"),
        TeamMember(id="tm4", name="David Brown", email="david@example.com"),
    ]


def generate_mock_tasks(team_member_ids: List[str], days_ago: int = 30) -> List[Task]:
    """Generate mock tasks with varying states and ages."""
    tasks = []
    now = datetime.now()
    
    # Create a mix of tasks in different states
    task_templates = [
        # Healthy project tasks
        {"title": "Implement user authentication", "status": TaskStatus.DONE, "days_old": 5, "assignee": 0},
        {"title": "Design database schema", "status": TaskStatus.DONE, "days_old": 8, "assignee": 1},
        {"title": "Setup CI/CD pipeline", "status": TaskStatus.IN_PROGRESS, "days_old": 2, "assignee": 0},
        {"title": "Write API documentation", "status": TaskStatus.IN_PROGRESS, "days_old": 1, "assignee": 2},
        {"title": "Add unit tests", "status": TaskStatus.TODO, "days_old": 0, "assignee": 1},
        {"title": "Performance optimization", "status": TaskStatus.TODO, "days_old": 0, "assignee": 3},
        
        # Some at-risk tasks
        {"title": "Fix critical bug #214", "status": TaskStatus.BLOCKED, "days_old": 12, "assignee": 0, "is_blocked": True, "is_reopened": True},
        {"title": "Refactor legacy code", "status": TaskStatus.IN_PROGRESS, "days_old": 15, "assignee": 1},  # Aging task
        {"title": "Update dependencies", "status": TaskStatus.TODO, "days_old": 20, "assignee": None},  # Very old todo
        
        # More tasks for workload distribution
        {"title": "Create user dashboard", "status": TaskStatus.IN_PROGRESS, "days_old": 3, "assignee": 0},
        {"title": "Implement search feature", "status": TaskStatus.DONE, "days_old": 4, "assignee": 2},
        {"title": "Write integration tests", "status": TaskStatus.TODO, "days_old": 2, "assignee": 3},
        {"title": "Setup monitoring", "status": TaskStatus.DONE, "days_old": 6, "assignee": 1},
    ]
    
    for i, template in enumerate(task_templates):
        created_at = now - timedelta(days=template["days_old"])
        updated_at = created_at + timedelta(days=random.randint(0, template["days_old"]))
        due_date = now + timedelta(days=random.randint(-5, 10)) if random.random() > 0.3 else None
        
        assignee_id = team_member_ids[template["assignee"]] if template.get("assignee") is not None else None
        
        task = Task(
            id=f"task_{i+1}",
            title=template["title"],
            status=template["status"],
            assignee_id=assignee_id,
            created_at=created_at,
            updated_at=updated_at,
            due_date=due_date,
            is_blocked=template.get("is_blocked", False),
            is_reopened=template.get("is_reopened", False),
            comments=generate_mock_comments(template.get("status") == TaskStatus.BLOCKED),
            tags=random.sample(["bug", "feature", "urgent", "backend", "frontend"], k=random.randint(0, 2))
        )
        tasks.append(task)
    
    return tasks


def generate_mock_comments(include_negative: bool = False) -> List[str]:
    """Generate mock comments with varying sentiment."""
    positive_comments = [
        "Great progress on this!",
        "Looks good, ready to merge.",
        "Excellent work, thanks!",
    ]
    neutral_comments = [
        "Please review when you have a chance.",
        "Updated the implementation.",
        "Added requested changes.",
    ]
    negative_comments = [
        "This is blocking our release.",
        "We need this fixed ASAP, client is waiting.",
        "This has been delayed too long.",
        "Not meeting the requirements.",
    ]
    
    comments = []
    if include_negative:
        comments.extend(random.sample(negative_comments, k=random.randint(1, 2)))
    else:
        comments.extend(random.sample(positive_comments + neutral_comments, k=random.randint(0, 2)))
    
    return comments


def generate_mock_communications(project_id: str, days_ago: int = 30) -> List[Communication]:
    """Generate mock communications with varying sentiment."""
    # Communication is already imported at the top of the file
    now = datetime.now()
    communications = []
    
    comm_templates = [
        {"source": "email", "author": "client@example.com", "content": "The project is looking great! Keep up the good work.", "sentiment": "positive", "days_ago": 2},
        {"source": "slack", "author": "Alice Johnson", "content": "Can we discuss the API changes in the standup?", "sentiment": "neutral", "days_ago": 1},
        {"source": "comment", "author": "Bob Smith", "content": "This bug is critical and needs immediate attention.", "sentiment": "negative", "days_ago": 3},
        {"source": "bug", "author": "client@example.com", "content": "The login feature is not working as expected. This is urgent.", "sentiment": "negative", "days_ago": 5},
        {"source": "email", "author": "client@example.com", "content": "Thanks for the quick turnaround on the last issue.", "sentiment": "positive", "days_ago": 7},
        {"source": "slack", "author": "Carol Williams", "content": "I've completed the frontend updates.", "sentiment": "neutral", "days_ago": 1},
    ]
    
    for i, template in enumerate(comm_templates):
        comm = Communication(
            id=f"comm_{i+1}",
            source=template["source"],
            author=template["author"],
            content=template["content"],
            timestamp=now - timedelta(days=template["days_ago"]),
            sentiment=template["sentiment"]
        )
        communications.append(comm)
    
    return communications


def generate_mock_project(project_id: str = "proj_1", project_name: str = "E-Commerce Platform") -> Project:
    """Generate a complete mock project with tasks, team, and communications."""
    team_members = generate_mock_team_members()
    team_member_ids = [tm.id for tm in team_members]
    
    tasks = generate_mock_tasks(team_member_ids)
    
    # Update team members with their assigned tasks
    for task in tasks:
        if task.assignee_id:
            for tm in team_members:
                if tm.id == task.assignee_id:
                    tm.tasks.append(task.id)
    
    communications = generate_mock_communications(project_id)
    
    return Project(
        id=project_id,
        name=project_name,
        description="A modern e-commerce platform with AI-powered recommendations",
        tasks=tasks,
        team_members=team_members,
        communications=communications,
        created_at=datetime.now() - timedelta(days=60)
    )


def generate_multiple_projects() -> List[Project]:
    """Generate multiple projects with varying health scores."""
    projects = [
        generate_mock_project("proj_1", "E-Commerce Platform"),
        generate_mock_project("proj_2", "Mobile Banking App"),
        generate_mock_project("proj_3", "Healthcare Dashboard"),
    ]
    return projects

