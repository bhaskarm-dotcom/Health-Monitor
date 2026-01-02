from datetime import datetime, timedelta
from typing import List, Dict
import sys
import os

# Handle imports
try:
    from .models import (
        Project, Task, TaskStatus, HealthScore, HealthStatus,
        DimensionScore, Risk
    )
    from .config import get_scoring_config
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import (
        Project, Task, TaskStatus, HealthScore, HealthStatus,
        DimensionScore, Risk
    )
    from config import get_scoring_config


class HealthCalculator:
    def __init__(self):
        self.config = get_scoring_config()
        self.weights = self.config["dimension_weights"]
        self.thresholds = self.config["health_thresholds"]
        self.aging_threshold = self.config["aging_task_threshold_days"]
        self.overload_threshold = self.config["overload_threshold_tasks"]
        self.underutilization_threshold = self.config["underutilization_threshold_tasks"]
    
    def calculate_health_score(self, project: Project, previous_score: float = None) -> HealthScore:
        """Calculate overall health score for a project."""
        dimensions = [
            self._calculate_delivery_health(project),
            self._calculate_workload_balance(project),
            self._calculate_communication_sentiment(project),
            self._calculate_risk_signals(project),
            self._calculate_momentum_trend(project, previous_score),
        ]
        
        # Calculate weighted overall score
        overall_score = sum(dim.score * dim.weight for dim in dimensions)
        
        # Determine status
        if overall_score >= self.thresholds["healthy"]:
            status = HealthStatus.HEALTHY
        elif overall_score >= self.thresholds["watch"]:
            status = HealthStatus.WATCH
        else:
            status = HealthStatus.AT_RISK
        
        # Determine trend
        trend = None
        if previous_score is not None:
            if overall_score > previous_score + 5:
                trend = "improving"
            elif overall_score < previous_score - 5:
                trend = "declining"
            else:
                trend = "stable"
        
        return HealthScore(
            overall_score=round(overall_score, 1),
            status=status,
            dimensions=dimensions,
            calculated_at=datetime.now(),
            previous_score=previous_score,
            trend=trend
        )
    
    def _calculate_delivery_health(self, project: Project) -> DimensionScore:
        """Calculate delivery health score (30% weight)."""
        tasks = project.tasks
        if not tasks:
            return DimensionScore(
                name="Delivery Health",
                score=0,
                weight=self.weights["delivery_health"],
                details={"error": "No tasks found"}
            )
        
        # Task status ratios
        total = len(tasks)
        done = sum(1 for t in tasks if t.status == TaskStatus.DONE)
        in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        todo = sum(1 for t in tasks if t.status == TaskStatus.TODO)
        
        done_ratio = done / total if total > 0 else 0
        in_progress_ratio = in_progress / total if total > 0 else 0
        
        # Aging tasks (no movement for X days)
        now = datetime.now()
        aging_tasks = sum(
            1 for t in tasks
            if (now - t.updated_at).days > self.aging_threshold
            and t.status != TaskStatus.DONE
        )
        aging_ratio = aging_tasks / total if total > 0 else 0
        
        # Deadline tracking
        overdue = sum(
            1 for t in tasks
            if t.due_date and t.due_date < now and t.status != TaskStatus.DONE
        )
        upcoming_deadlines = sum(
            1 for t in tasks
            if t.due_date and t.due_date > now and (t.due_date - now).days <= 7
        )
        
        overdue_ratio = overdue / total if total > 0 else 0
        
        # Calculate score (0-100)
        # Positive factors: high done ratio, good in-progress ratio
        # Negative factors: aging tasks, overdue tasks
        score = 100
        score -= (aging_ratio * 30)  # Penalize aging tasks
        score -= (overdue_ratio * 40)  # Penalize overdue tasks
        score += (done_ratio * 20)  # Reward completed tasks
        score += (in_progress_ratio * 10)  # Reward active work
        
        score = max(0, min(100, score))
        
        return DimensionScore(
            name="Delivery Health",
            score=round(score, 1),
            weight=self.weights["delivery_health"],
            details={
                "total_tasks": total,
                "done": done,
                "in_progress": in_progress,
                "todo": todo,
                "aging_tasks": aging_tasks,
                "overdue_tasks": overdue,
                "upcoming_deadlines": upcoming_deadlines,
            }
        )
    
    def _calculate_workload_balance(self, project: Project) -> DimensionScore:
        """Calculate workload balance score (20% weight)."""
        team_members = project.team_members
        tasks = project.tasks
        
        if not team_members:
            return DimensionScore(
                name="Workload Balance",
                score=0,
                weight=self.weights["workload_balance"],
                details={"error": "No team members found"}
            )
        
        # Count tasks per team member
        task_counts = {}
        for tm in team_members:
            assigned_tasks = [t for t in tasks if t.assignee_id == tm.id]
            task_counts[tm.id] = {
                "name": tm.name,
                "total": len(assigned_tasks),
                "done": sum(1 for t in assigned_tasks if t.status == TaskStatus.DONE),
                "in_progress": sum(1 for t in assigned_tasks if t.status == TaskStatus.IN_PROGRESS),
            }
        
        # Calculate workload distribution metrics
        if task_counts:
            task_totals = [counts["total"] for counts in task_counts.values()]
            avg_tasks = sum(task_totals) / len(task_totals) if task_totals else 0
            max_tasks = max(task_totals) if task_totals else 0
            min_tasks = min(task_totals) if task_totals else 0
            
            # Overload detection
            overloaded = sum(1 for total in task_totals if total > self.overload_threshold)
            underutilized = sum(1 for total in task_totals if total < self.underutilization_threshold)
            
            # Calculate score
            score = 100
            
            # Penalize overload
            if max_tasks > self.overload_threshold:
                overload_ratio = (max_tasks - self.overload_threshold) / self.overload_threshold
                score -= min(30, overload_ratio * 20)
            
            # Penalize underutilization
            if min_tasks < self.underutilization_threshold and avg_tasks > 0:
                score -= 15
            
            # Penalize high variance (uneven distribution)
            if avg_tasks > 0:
                variance = sum((total - avg_tasks) ** 2 for total in task_totals) / len(task_totals)
                std_dev = variance ** 0.5
                if std_dev > avg_tasks * 0.5:  # High variance
                    score -= 20
            
            score = max(0, min(100, score))
        else:
            score = 50  # Neutral if no assignments
        
        return DimensionScore(
            name="Workload Balance",
            score=round(score, 1),
            weight=self.weights["workload_balance"],
            details={
                "task_distribution": task_counts,
                "overloaded_members": overloaded if task_counts else 0,
                "underutilized_members": underutilized if task_counts else 0,
            }
        )
    
    def _calculate_communication_sentiment(self, project: Project) -> DimensionScore:
        """Calculate communication & sentiment score (25% weight)."""
        communications = project.communications
        
        if not communications:
            return DimensionScore(
                name="Communication & Sentiment",
                score=50,  # Neutral if no communications
                weight=self.weights["communication_sentiment"],
                details={"message": "No communications found"}
            )
        
        # Count sentiment
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for comm in communications:
            if comm.sentiment:
                sentiment_counts[comm.sentiment] = sentiment_counts.get(comm.sentiment, 0) + 1
        
        total = len(communications)
        positive_ratio = sentiment_counts["positive"] / total if total > 0 else 0
        neutral_ratio = sentiment_counts["neutral"] / total if total > 0 else 0
        negative_ratio = sentiment_counts["negative"] / total if total > 0 else 0
        
        # Calculate score
        score = 50  # Start neutral
        score += (positive_ratio * 50)  # Boost for positive
        score -= (negative_ratio * 50)  # Penalize negative
        
        score = max(0, min(100, score))
        
        # Recent sentiment trend (last 7 days)
        now = datetime.now()
        recent_comms = [c for c in communications if (now - c.timestamp).days <= 7]
        recent_negative = sum(1 for c in recent_comms if c.sentiment == "negative")
        if recent_comms and recent_negative / len(recent_comms) > 0.3:
            score -= 10  # Penalize recent negative trend
        
        score = max(0, min(100, score))
        
        return DimensionScore(
            name="Communication & Sentiment",
            score=round(score, 1),
            weight=self.weights["communication_sentiment"],
            details={
                "total_communications": total,
                "positive": sentiment_counts["positive"],
                "neutral": sentiment_counts["neutral"],
                "negative": sentiment_counts["negative"],
                "recent_negative_trend": recent_negative > len(recent_comms) * 0.3 if recent_comms else False,
            }
        )
    
    def _calculate_risk_signals(self, project: Project) -> DimensionScore:
        """Calculate risk & dependency signals score (15% weight)."""
        tasks = project.tasks
        
        if not tasks:
            return DimensionScore(
                name="Risk & Dependency Signals",
                score=100,  # No tasks = no risks
                weight=self.weights["risk_signals"],
                details={}
            )
        
        # Count risk indicators
        blocked = sum(1 for t in tasks if t.is_blocked)
        reopened = sum(1 for t in tasks if t.is_reopened)
        
        # High-risk keywords/tags
        risk_keywords = ["urgent", "critical", "blocker", "bug"]
        high_risk_tags = sum(
            1 for t in tasks
            if any(keyword in [tag.lower() for tag in t.tags] for keyword in risk_keywords)
        )
        
        total = len(tasks)
        blocked_ratio = blocked / total if total > 0 else 0
        reopened_ratio = reopened / total if total > 0 else 0
        risk_tag_ratio = high_risk_tags / total if total > 0 else 0
        
        # Calculate score
        score = 100
        score -= (blocked_ratio * 40)  # Heavy penalty for blocked tasks
        score -= (reopened_ratio * 30)  # Penalty for reopened issues
        score -= (risk_tag_ratio * 20)  # Penalty for high-risk tags
        
        score = max(0, min(100, score))
        
        return DimensionScore(
            name="Risk & Dependency Signals",
            score=round(score, 1),
            weight=self.weights["risk_signals"],
            details={
                "blocked_tasks": blocked,
                "reopened_tasks": reopened,
                "high_risk_tagged_tasks": high_risk_tags,
            }
        )
    
    def _calculate_momentum_trend(self, project: Project, previous_score: float = None) -> DimensionScore:
        """Calculate momentum trend score (10% weight)."""
        tasks = project.tasks
        
        if not tasks:
            return DimensionScore(
                name="Momentum Trend",
                score=50,  # Neutral
                weight=self.weights["momentum_trend"],
                details={"message": "No tasks found"}
            )
        
        # Week-over-week completion rate
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        # Tasks completed in last week
        recent_completed = [
            t for t in tasks
            if t.status == TaskStatus.DONE
            and t.updated_at >= week_ago
        ]
        
        # Tasks completed in previous week
        two_weeks_ago = now - timedelta(days=14)
        previous_week_completed = [
            t for t in tasks
            if t.status == TaskStatus.DONE
            and two_weeks_ago <= t.updated_at < week_ago
        ]
        
        recent_count = len(recent_completed)
        previous_count = len(previous_week_completed)
        
        # Calculate momentum
        if previous_count > 0:
            momentum_ratio = recent_count / previous_count
        else:
            momentum_ratio = 1.0 if recent_count > 0 else 0.5
        
        # Calculate score
        score = 50  # Start neutral
        
        if momentum_ratio > 1.2:  # Improving
            score = 80
        elif momentum_ratio > 0.8:  # Stable
            score = 60
        else:  # Declining
            score = 30
        
        # Factor in previous health score if available
        if previous_score is not None:
            delivery_score = self._calculate_delivery_health(project).score * self.weights["delivery_health"]
            workload_score = self._calculate_workload_balance(project).score * self.weights["workload_balance"]
            current_health = delivery_score + workload_score  # Simplified for momentum calculation
            
            if current_health > previous_score + 5:
                score = min(100, score + 20)
            elif current_health < previous_score - 5:
                score = max(0, score - 20)
        
        score = max(0, min(100, score))
        
        return DimensionScore(
            name="Momentum Trend",
            score=round(score, 1),
            weight=self.weights["momentum_trend"],
            details={
                "recent_completions": recent_count,
                "previous_completions": previous_count,
                "momentum_ratio": round(momentum_ratio, 2),
            }
        )
    
    def detect_risks(self, project: Project, health_score: HealthScore) -> List[Risk]:
        """Detect and list specific risks based on health analysis."""
        risks = []
        now = datetime.now()
        
        # Delivery risks
        delivery_dim = next((d for d in health_score.dimensions if d.name == "Delivery Health"), None)
        if delivery_dim:
            details = delivery_dim.details
            if details.get("aging_tasks", 0) > 3:
                risks.append(Risk(
                    id="risk_1",
                    title="Multiple Aging Tasks",
                    description=f"{details['aging_tasks']} tasks have not been updated in over {self.aging_threshold} days",
                    severity="high" if details['aging_tasks'] > 5 else "medium",
                    category="delivery",
                    detected_at=now
                ))
            if details.get("overdue_tasks", 0) > 0:
                risks.append(Risk(
                    id="risk_2",
                    title="Overdue Tasks",
                    description=f"{details['overdue_tasks']} tasks are past their due dates",
                    severity="high",
                    category="delivery",
                    detected_at=now
                ))
        
        # Workload risks
        workload_dim = next((d for d in health_score.dimensions if d.name == "Workload Balance"), None)
        if workload_dim:
            details = workload_dim.details
            if details.get("overloaded_members", 0) > 0:
                risks.append(Risk(
                    id="risk_3",
                    title="Team Member Overload",
                    description=f"{details['overloaded_members']} team member(s) have excessive task assignments",
                    severity="medium",
                    category="workload",
                    detected_at=now
                ))
        
        # Sentiment risks
        sentiment_dim = next((d for d in health_score.dimensions if d.name == "Communication & Sentiment"), None)
        if sentiment_dim:
            details = sentiment_dim.details
            if details.get("negative", 0) > details.get("positive", 0):
                risks.append(Risk(
                    id="risk_4",
                    title="Negative Sentiment Trend",
                    description="Negative communications outnumber positive ones",
                    severity="high",
                    category="sentiment",
                    detected_at=now
                ))
            if details.get("recent_negative_trend", False):
                risks.append(Risk(
                    id="risk_5",
                    title="Recent Negative Sentiment",
                    description="High proportion of negative communications in the last 7 days",
                    severity="medium",
                    category="sentiment",
                    detected_at=now
                ))
        
        # Risk signal risks
        risk_dim = next((d for d in health_score.dimensions if d.name == "Risk & Dependency Signals"), None)
        if risk_dim:
            details = risk_dim.details
            if details.get("blocked_tasks", 0) > 0:
                risks.append(Risk(
                    id="risk_6",
                    title="Blocked Tasks",
                    description=f"{details['blocked_tasks']} task(s) are currently blocked",
                    severity="high",
                    category="risk",
                    detected_at=now
                ))
            if details.get("reopened_tasks", 0) > 0:
                risks.append(Risk(
                    id="risk_7",
                    title="Reopened Issues",
                    description=f"{details['reopened_tasks']} task(s) have been reopened, indicating quality issues",
                    severity="medium",
                    category="risk",
                    detected_at=now
                ))
        
        return risks

