from typing import List, Optional
import sys
import os

# Handle imports
try:
    from .models import Project
    from .mock_data import generate_mock_project, generate_multiple_projects
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from models import Project
    from mock_data import generate_mock_project, generate_multiple_projects


class DataAdapter:
    """
    Data adapter layer that abstracts data fetching.
    Currently uses mock data, but designed to support real API integrations in the future.
    """
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self._mock_projects_cache = None
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Fetch a single project by ID."""
        if self.use_mock:
            # For mock, generate or retrieve from cache
            if self._mock_projects_cache is None:
                self._mock_projects_cache = {p.id: p for p in generate_multiple_projects()}
            
            if project_id in self._mock_projects_cache:
                return self._mock_projects_cache[project_id]
            
            # Generate a new project if not in cache
            return generate_mock_project(project_id, f"Project {project_id}")
        
        # Future: Real API integration
        # return self._fetch_from_api(project_id)
        raise NotImplementedError("Real API integration not yet implemented")
    
    def get_all_projects(self) -> List[Project]:
        """Fetch all projects."""
        if self.use_mock:
            if self._mock_projects_cache is None:
                self._mock_projects_cache = {p.id: p for p in generate_multiple_projects()}
            return list(self._mock_projects_cache.values())
        
        # Future: Real API integration
        # return self._fetch_all_from_api()
        raise NotImplementedError("Real API integration not yet implemented")
    
    def get_project_history(self, project_id: str, days: int = 30) -> List[Project]:
        """
        Get historical project snapshots for trend analysis.
        For mock data, returns current project (real implementation would store snapshots).
        """
        project = self.get_project(project_id)
        if project:
            return [project]  # Mock: return current state
        return []
    
    # Future methods for real API integration:
    # def _fetch_from_api(self, project_id: str) -> Project:
    #     """Fetch project from real API (Notion, Jira, etc.)"""
    #     pass
    #
    # def _fetch_all_from_api(self) -> List[Project]:
    #     """Fetch all projects from real API"""
    #     pass

