import os
import sys
from typing import List, Optional
from openai import OpenAI

# Handle imports
try:
    from .models import HealthScore, Risk, Recommendation
    from .config import get_ai_prompts, OPENAI_API_KEY, OPENAI_MODEL
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import HealthScore, Risk, Recommendation
    from config import get_ai_prompts, OPENAI_API_KEY, OPENAI_MODEL


class AIService:
    def __init__(self):
        self.prompts = get_ai_prompts()
        # Initialize OpenAI client if API key is available
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.client = None
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text using AI."""
        if not self.client:
            # Fallback to simple keyword-based sentiment if no API key
            return self._fallback_sentiment(text)
        
        try:
            prompt = self.prompts["sentiment_analysis"].format(text=text)
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis tool. Respond with only one word: 'positive', 'neutral', or 'negative'."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            sentiment = response.choices[0].message.content.strip().lower()
            if sentiment in ["positive", "neutral", "negative"]:
                return sentiment
            return "neutral"
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return self._fallback_sentiment(text)
    
    def _fallback_sentiment(self, text: str) -> str:
        """Fallback sentiment analysis using keywords."""
        text_lower = text.lower()
        positive_keywords = ["great", "excellent", "good", "thanks", "appreciate", "awesome", "perfect"]
        negative_keywords = ["urgent", "critical", "blocking", "delayed", "broken", "failed", "error", "bug", "issue", "problem"]
        
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"
    
    def generate_recommendations(
        self,
        health_score: HealthScore,
        risks: List[Risk],
        project_name: str
    ) -> List[Recommendation]:
        """Generate AI-powered recommendations to improve project health."""
        if not self.client:
            return self._fallback_recommendations(health_score, risks)
        
        try:
            # Format dimension breakdown
            breakdown = "\n".join([
                f"- {dim.name}: {dim.score}/100 (weight: {dim.weight*100}%)"
                for dim in health_score.dimensions
            ])
            
            # Format risks
            risks_text = "\n".join([
                f"- {risk.title} ({risk.severity}): {risk.description}"
                for risk in risks
            ]) if risks else "No specific risks detected."
            
            prompt = self.prompts["recommendations"].format(
                score=health_score.overall_score,
                status=health_score.status.value,
                breakdown=breakdown,
                risks=risks_text
            )
            
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a project management advisor. Provide specific, actionable recommendations to improve project health."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            recommendations_text = response.choices[0].message.content.strip()
            return self._parse_recommendations(recommendations_text, health_score)
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return self._fallback_recommendations(health_score, risks)
    
    def _parse_recommendations(self, text: str, health_score: HealthScore) -> List[Recommendation]:
        """Parse AI-generated recommendations from text."""
        recommendations = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            
            # Parse format: "1. [Title] - [Description] (Priority: high/medium/low, Category: [category])"
            try:
                # Remove numbering
                content = line.split('.', 1)[1].strip() if '.' in line else line
                
                # Extract priority and category if present
                priority = "medium"
                category = "general"
                title = content
                description = ""
                
                if " - " in content:
                    parts = content.split(" - ", 1)
                    title = parts[0].strip()
                    description = parts[1].strip()
                    
                    # Extract priority
                    if "priority:" in description.lower():
                        priority_part = description.lower().split("priority:")[1].split(",")[0].strip()
                        if "high" in priority_part:
                            priority = "high"
                        elif "low" in priority_part:
                            priority = "low"
                    
                    # Extract category
                    if "category:" in description.lower():
                        category_part = description.lower().split("category:")[1].split(")")[0].strip()
                        category = category_part
                    
                    # Clean description
                    description = description.split("(Priority:")[0].strip()
                    description = description.split("(priority:")[0].strip()
                
                recommendations.append(Recommendation(
                    id=f"rec_{i+1}",
                    title=title,
                    description=description or title,
                    priority=priority,
                    category=category,
                    impact="Expected to improve health score by 5-15 points"
                ))
            except Exception as e:
                print(f"Error parsing recommendation: {e}")
                continue
        
        # Ensure we have at least 3 recommendations
        if len(recommendations) < 3:
            recommendations.extend(self._fallback_recommendations(health_score, [])[:3-len(recommendations)])
        
        return recommendations[:5]  # Return max 5 recommendations
    
    def _fallback_recommendations(self, health_score: HealthScore, risks: List[Risk]) -> List[Recommendation]:
        """Generate fallback recommendations based on health score analysis."""
        recommendations = []
        
        # Find lowest scoring dimension
        lowest_dim = min(health_score.dimensions, key=lambda d: d.score)
        
        if lowest_dim.name == "Delivery Health":
            recommendations.append(Recommendation(
                id="rec_1",
                title="Address Aging Tasks",
                description="Review and update tasks that haven't been touched in over 7 days. Reassign or close stale tasks.",
                priority="high",
                category="delivery",
                impact="Expected to improve delivery health by 10-20 points"
            ))
            if lowest_dim.details.get("overdue_tasks", 0) > 0:
                recommendations.append(Recommendation(
                    id="rec_2",
                    title="Resolve Overdue Tasks",
                    description=f"Focus on completing {lowest_dim.details['overdue_tasks']} overdue task(s) immediately.",
                    priority="high",
                    category="delivery",
                    impact="Expected to improve delivery health by 15-25 points"
                ))
        
        if lowest_dim.name == "Workload Balance":
            recommendations.append(Recommendation(
                id="rec_3",
                title="Redistribute Workload",
                description="Balance task assignments across team members to prevent overload and underutilization.",
                priority="medium",
                category="workload",
                impact="Expected to improve workload balance by 10-15 points"
            ))
        
        if lowest_dim.name == "Communication & Sentiment":
            recommendations.append(Recommendation(
                id="rec_4",
                title="Improve Client Communication",
                description="Schedule a check-in call with the client to address concerns and align expectations.",
                priority="high",
                category="sentiment",
                impact="Expected to improve sentiment score by 10-20 points"
            ))
        
        if lowest_dim.name == "Risk & Dependency Signals":
            if lowest_dim.details.get("blocked_tasks", 0) > 0:
                recommendations.append(Recommendation(
                    id="rec_5",
                    title="Unblock Blocked Tasks",
                    description=f"Identify and resolve blockers for {lowest_dim.details['blocked_tasks']} blocked task(s).",
                    priority="high",
                    category="risk",
                    impact="Expected to improve risk signals by 15-25 points"
                ))
        
        # Add general recommendations if we don't have enough
        if len(recommendations) < 3:
            recommendations.append(Recommendation(
                id="rec_6",
                title="Schedule Team Standup",
                description="Conduct a team standup to discuss blockers, priorities, and align on next steps.",
                priority="medium",
                category="general",
                impact="Expected to improve overall coordination"
            ))
        
        if len(recommendations) < 3:
            recommendations.append(Recommendation(
                id="rec_7",
                title="Review Project Timeline",
                description="Review project timeline and adjust deadlines if necessary to ensure realistic expectations.",
                priority="medium",
                category="delivery",
                impact="Expected to improve delivery planning"
            ))
        
        return recommendations[:5]

