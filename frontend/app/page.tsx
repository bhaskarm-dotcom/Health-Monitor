'use client';

import { useState, useEffect } from 'react';
import { apiClient, Project, HealthReport } from '@/lib/api';
import HealthScore from '@/components/HealthScore';
import DimensionBreakdown from '@/components/DimensionBreakdown';
import RiskSummary from '@/components/RiskSummary';
import Recommendations from '@/components/Recommendations';
import TrendChart from '@/components/TrendChart';
import Sidebar from '@/components/Sidebar';
import MobileMenuButton from '@/components/MobileMenuButton';

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');
  const [healthReport, setHealthReport] = useState<HealthReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');

  // Initialize sidebar state based on screen size
  useEffect(() => {
    const checkScreenSize = () => {
      if (window.innerWidth >= 1024) {
        setSidebarOpen(true);
      } else {
        setSidebarOpen(false);
      }
    };
    
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  useEffect(() => {
    if (currentPage === 'dashboard') {
      loadProjects();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage]);

  useEffect(() => {
    if (selectedProjectId && currentPage === 'dashboard') {
      loadHealthReport(selectedProjectId);
    }
  }, [selectedProjectId, currentPage]);

  const loadProjects = async () => {
    try {
      setLoadingProjects(true);
      setError(null);
      const data = await apiClient.getProjects();
      setProjects(data);
      if (data.length > 0 && !selectedProjectId) {
        setSelectedProjectId(data[0].id);
      }
    } catch (err: any) {
      const errorMessage = err?.response?.data?.detail || err?.message || 'Failed to load projects';
      const fullError = err?.response?.status 
        ? `HTTP ${err.response.status}: ${errorMessage}`
        : `Network Error: ${errorMessage}`;
      setError(`Failed to load projects: ${fullError}`);
      console.error('Error loading projects:', err);
    } finally {
      setLoadingProjects(false);
    }
  };

  const loadHealthReport = async (projectId: string) => {
    setLoading(true);
    setError(null);
    try {
      const report = await apiClient.getProjectHealth(projectId);
      setHealthReport(report);
    } catch (err: any) {
      const errorMessage = err?.response?.data?.detail || err?.message || 'Failed to load health report';
      setError(`Failed to load health report: ${errorMessage}`);
      console.error('Error loading health report:', err);
    } finally {
      setLoading(false);
    }
  };

  // Mock trend data (in production, this would come from the API)
  const trendData = healthReport
    ? [
        { date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), score: healthReport.health_score.previous_score || healthReport.health_score.overall_score - 5 },
        { date: healthReport.health_score.calculated_at, score: healthReport.health_score.overall_score },
      ]
    : [];

  const getPageTitle = () => {
    switch (currentPage) {
      case 'dashboard':
        return 'Dashboard';
      case 'projects':
        return 'Projects';
      case 'reports':
        return 'Reports';
      case 'analytics':
        return 'Analytics';
      case 'settings':
        return 'Settings';
      case 'help':
        return 'Help & Support';
      case 'about':
        return 'About';
      default:
        return 'Dashboard';
    }
  };

  const renderPageContent = () => {
    switch (currentPage) {
      case 'dashboard':
        return (
          <>
            {error && (
              <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4 rounded-r-lg">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <span className="text-red-400 text-xl">⚠️</span>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {loading && (
              <div className="flex items-center justify-center py-20">
                <div className="text-center">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                  <p className="text-gray-600">Loading health report...</p>
                </div>
              </div>
            )}

            {healthReport && !loading && (
              <div className="space-y-6">
                {/* Top Row: Health Score and Quick Stats */}
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                  <div className="lg:col-span-1">
                    <HealthScore healthScore={healthReport.health_score} />
                  </div>
                  <div className="lg:col-span-3">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-full">
                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border-l-4 border-blue-500 border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Risks</p>
                          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{healthReport.risks.length}</p>
                        </div>
                        <div className="text-4xl">⚠️</div>
                      </div>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border-l-4 border-green-500 border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Recommendations</p>
                          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{healthReport.recommendations.length}</p>
                        </div>
                        <div className="text-4xl">💡</div>
                      </div>
                    </div>
                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border-l-4 border-purple-500 border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Project</p>
                          <p className="text-lg font-bold text-gray-900 dark:text-white mt-2 truncate">{healthReport.project_name}</p>
                        </div>
                        <div className="text-4xl">📊</div>
                      </div>
                    </div>
                    </div>
                  </div>
                </div>

                {/* Second Row: Dimensions and Trend */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <DimensionBreakdown dimensions={healthReport.health_score.dimensions} />
                  </div>
                  <div className="lg:col-span-1">
                    <TrendChart data={trendData} />
                  </div>
                </div>

                {/* Third Row: Risks and Recommendations */}
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                  <RiskSummary risks={healthReport.risks} />
                  <Recommendations recommendations={healthReport.recommendations} />
                </div>
              </div>
            )}

            {!healthReport && !loading && !loadingProjects && (
              <div className="text-center py-20">
                <div className="text-6xl mb-4">📊</div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No Project Selected</h3>
                <p className="text-gray-600 dark:text-gray-400">Select a project from the dropdown above to view its health report</p>
              </div>
            )}
          </>
        );

      case 'projects':
        return (
          <div className="bg-white rounded-xl shadow-md p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">All Projects</h2>
            <div className="space-y-4">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => {
                    setSelectedProjectId(project.id);
                    setCurrentPage('dashboard');
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>
                      <p className="text-sm text-gray-600 mt-1">{project.description}</p>
                      <p className="text-xs text-gray-500 mt-2">
                        Created: {new Date(project.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-2xl">📁</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'reports':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Reports</h2>
            <div className="space-y-4">
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Weekly Health Report</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Comprehensive weekly analysis of all project health metrics</p>
                <button className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors">
                  Generate Report
                </button>
              </div>
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Risk Assessment Report</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Detailed analysis of project risks and mitigation strategies</p>
                <button className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors">
                  Generate Report
                </button>
              </div>
            </div>
          </div>
        );

      case 'analytics':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Analytics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">📈 Health Score Trends</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Track health score trends over time across all projects</p>
              </div>
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">📊 Risk Distribution</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Analyze risk patterns and distribution across projects</p>
              </div>
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">⚡ Team Performance</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Monitor team workload and performance metrics</p>
              </div>
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6 bg-white dark:bg-gray-800">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">💬 Sentiment Analysis</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Track communication sentiment trends</p>
              </div>
            </div>
          </div>
        );

      case 'settings':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Settings</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Health Score Configuration</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">Delivery Health Weight</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Current: 30%</p>
                    </div>
                    <button className="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">
                      Edit
                    </button>
                  </div>
                  <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">Notification Preferences</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Email alerts for health score changes</p>
                    </div>
                    <button className="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300">
                      Configure
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'help':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Help & Support</h2>
            <div className="space-y-4">
              <div className="border-l-4 border-blue-500 dark:border-blue-400 pl-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Getting Started</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Learn how to use the AI Project Health Monitor to track and improve your project health.
                </p>
              </div>
              <div className="border-l-4 border-green-500 dark:border-green-400 pl-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Understanding Health Scores</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Health scores are calculated based on 5 key dimensions: Delivery, Workload, Sentiment, Risk, and Momentum.
                </p>
              </div>
              <div className="border-l-4 border-yellow-500 dark:border-yellow-400 pl-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Contact Support</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Need help? Contact our support team at support@zeelai.com
                </p>
              </div>
            </div>
          </div>
        );

      case 'about':
        return (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 border border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">About</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">AI-Powered 360° Project Health Monitor</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  A preventive AI system that identifies project risks, explains why they are happening, 
                  and provides actionable recommendations before they impact the client.
                </p>
              </div>
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Version</h3>
                <p className="text-gray-600 dark:text-gray-400">1.0.0</p>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 flex">
      {/* Sidebar */}
      <Sidebar 
        currentPage={currentPage}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNavigate={setCurrentPage}
      />

      {/* Main Content Area */}
      <div className="flex-1 lg:ml-64 flex flex-col min-h-screen">
        {/* Header */}
        <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-10">
          <div className="px-4 lg:px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <MobileMenuButton 
                  onClick={() => setSidebarOpen(!sidebarOpen)} 
                  isOpen={sidebarOpen}
                />
                <div>
                  <h1 className="text-xl lg:text-2xl font-bold text-gray-900 dark:text-white">
                    {getPageTitle()}
                  </h1>
                  <p className="text-xs lg:text-sm text-gray-500 dark:text-gray-400 mt-0.5 hidden sm:block">
                    {currentPage === 'dashboard' ? 'Project health monitoring and insights' : 'Manage your project health'}
                  </p>
                </div>
              </div>
              {currentPage === 'dashboard' && (
                <div className="flex items-center gap-4">
                  {loadingProjects ? (
                    <div className="text-sm text-gray-500">Loading...</div>
                  ) : (
                    <select
                      value={selectedProjectId}
                      onChange={(e) => setSelectedProjectId(e.target.value)}
                      className="px-3 lg:px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm font-medium"
                      disabled={projects.length === 0}
                    >
                      {projects.length === 0 ? (
                        <option value="">No projects</option>
                      ) : (
                        projects.map((project) => (
                          <option key={project.id} value={project.id}>
                            {project.name}
                          </option>
                        ))
                      )}
                    </select>
                  )}
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 p-4 lg:p-6 overflow-y-auto">
          {renderPageContent()}
        </main>
      </div>
    </div>
  );
}
