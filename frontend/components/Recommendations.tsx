'use client';

import { Recommendation } from '@/lib/api';

interface RecommendationsProps {
  recommendations: Recommendation[];
}

export default function Recommendations({ recommendations }: RecommendationsProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-50 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800';
      case 'medium':
        return 'bg-yellow-50 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800';
      case 'low':
        return 'bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 border-blue-200 dark:border-blue-800';
      default:
        return 'bg-gray-50 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      case 'low':
        return '🔵';
      default:
        return '⚪';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'delivery':
        return '📦';
      case 'workload':
        return '👥';
      case 'sentiment':
        return '💬';
      case 'risk':
        return '⚠️';
      case 'general':
        return '📋';
      default:
        return '💡';
    }
  };

  if (recommendations.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">AI Recommendations</h2>
        <div className="flex-1 flex items-center justify-center text-gray-500 dark:text-gray-400">
          <div className="text-center">
            <div className="text-5xl mb-3">✨</div>
            <div className="font-medium">No recommendations</div>
            <div className="text-sm mt-1">Project is performing well!</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">AI Recommendations</h2>
        <span className="px-2 py-1 bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 rounded-full text-xs font-semibold">
          {recommendations.length} {recommendations.length === 1 ? 'action' : 'actions'}
        </span>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto">
        {recommendations.map((rec, index) => (
          <div
            key={rec.id}
            className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start gap-3">
              <div className="text-2xl flex-shrink-0">{getCategoryIcon(rec.category)}</div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <span className="text-sm font-semibold text-gray-800 dark:text-white">
                    {index + 1}. {rec.title}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold uppercase ${getPriorityColor(rec.priority)}`}>
                    {getPriorityIcon(rec.priority)} {rec.priority}
                  </span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">{rec.description}</p>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-500 dark:text-gray-400">{rec.category}</span>
                  <span className="text-green-600 dark:text-green-400 font-medium">{rec.impact}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
