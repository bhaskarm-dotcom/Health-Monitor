'use client';

import { HealthScore as HealthScoreType } from '@/lib/api';

interface HealthScoreProps {
  healthScore: HealthScoreType;
}

export default function HealthScore({ healthScore }: HealthScoreProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800';
      case 'watch':
        return 'text-yellow-700 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-800';
      case 'at_risk':
        return 'text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800';
      default:
        return 'text-gray-700 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return '🟢';
      case 'watch':
        return '🟡';
      case 'at_risk':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'Healthy';
      case 'watch':
        return 'Watch';
      case 'at_risk':
        return 'At Risk';
      default:
        return 'Unknown';
    }
  };

  const getScoreColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 dark:text-green-400';
      case 'watch':
        return 'text-yellow-600 dark:text-yellow-400';
      case 'at_risk':
        return 'text-red-600 dark:text-red-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const getCircleColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-500 dark:text-green-400';
      case 'watch':
        return 'text-yellow-500 dark:text-yellow-400';
      case 'at_risk':
        return 'text-red-500 dark:text-red-400';
      default:
        return 'text-gray-500 dark:text-gray-400';
    }
  };

  const getTrendIcon = (trend?: string) => {
    switch (trend) {
      case 'improving':
        return '📈';
      case 'declining':
        return '📉';
      case 'stable':
        return '➡️';
      default:
        return '';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Health Score</h2>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusColor(healthScore.status)}`}>
          {getStatusIcon(healthScore.status)} {getStatusLabel(healthScore.status)}
        </span>
      </div>

      <div className="flex-1 flex items-center justify-center my-4">
        <div className="relative w-40 h-40">
          <svg className="transform -rotate-90 w-40 h-40">
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="currentColor"
              strokeWidth="10"
              fill="none"
              className="text-gray-200 dark:text-gray-700"
            />
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="currentColor"
              strokeWidth="10"
              fill="none"
              strokeDasharray={`${(healthScore.overall_score / 100) * 439.8} 439.8`}
              className={`${getCircleColor(healthScore.status)} transition-all duration-500`}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className={`text-4xl font-bold ${getScoreColor(healthScore.status)}`}>
                {healthScore.overall_score.toFixed(0)}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">/ 100</div>
            </div>
          </div>
        </div>
      </div>

      {healthScore.previous_score !== undefined && healthScore.trend && (
        <div className="text-center mb-3">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gray-50 dark:bg-gray-700 rounded-lg text-xs">
            <span>{getTrendIcon(healthScore.trend)}</span>
            <span className="text-gray-700 dark:text-gray-300">
              {healthScore.previous_score.toFixed(0)} → {healthScore.overall_score.toFixed(0)}
            </span>
          </div>
        </div>
      )}

      <div className="text-xs text-gray-500 dark:text-gray-400 text-center pt-2 border-t border-gray-100 dark:border-gray-700">
        Updated {new Date(healthScore.calculated_at).toLocaleTimeString()}
      </div>
    </div>
  );
}
