import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
  task_count?: number;
  team_member_count?: number;
}

export interface DimensionScore {
  name: string;
  score: number;
  weight: number;
  details: Record<string, any>;
}

export interface HealthScore {
  overall_score: number;
  status: 'healthy' | 'watch' | 'at_risk';
  dimensions: DimensionScore[];
  calculated_at: string;
  previous_score?: number;
  trend?: 'improving' | 'declining' | 'stable';
}

export interface Risk {
  id: string;
  title: string;
  description: string;
  severity: 'high' | 'medium' | 'low';
  category: string;
  detected_at: string;
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  category: string;
  impact: string;
}

export interface HealthReport {
  project_id: string;
  project_name: string;
  health_score: HealthScore;
  risks: Risk[];
  recommendations: Recommendation[];
  generated_at: string;
}

export const apiClient = {
  getProjects: async (): Promise<Project[]> => {
    const response = await api.get('/api/projects');
    return response.data;
  },

  getProject: async (projectId: string): Promise<Project> => {
    const response = await api.get(`/api/projects/${projectId}`);
    return response.data;
  },

  getProjectHealth: async (projectId: string): Promise<HealthReport> => {
    const response = await api.get(`/api/projects/${projectId}/health`);
    return response.data;
  },

  getHealthScore: async (projectId: string): Promise<{ score: number; status: string; trend?: string }> => {
    const response = await api.get(`/api/projects/${projectId}/health/score`);
    return response.data;
  },
};

