'use client';

import { DimensionScore } from '@/lib/api';

interface DimensionBreakdownProps {
  dimensions: DimensionScore[];
}

export default function DimensionBreakdown({ dimensions }: DimensionBreakdownProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-500 dark:bg-green-400';
    if (score >= 60) return 'bg-yellow-500 dark:bg-yellow-400';
    return 'bg-red-500 dark:bg-red-400';
  };

  const getIcon = (name: string) => {
    if (name.includes('Delivery')) return '📦';
    if (name.includes('Workload')) return '⚖️';
    if (name.includes('Sentiment') || name.includes('Communication')) return '💬';
    if (name.includes('Risk')) return '🚩';
    if (name.includes('Momentum')) return '⚡';
    return '📊';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Health Dimensions</h2>
      <div className="space-y-4">
        {dimensions.map((dim, index) => (
          <div key={index} className="border-b border-gray-100 dark:border-gray-700 last:border-b-0 pb-4 last:pb-0">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3 flex-1">
                <span className="text-2xl">{getIcon(dim.name)}</span>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-700 dark:text-gray-300 text-sm">{dim.name}</span>
                    <span className="text-lg font-bold text-gray-900 dark:text-white ml-2">{dim.score.toFixed(0)}</span>
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    Weight: {(dim.weight * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${getScoreColor(dim.score)}`}
                style={{ width: `${dim.score}%` }}
              />
            </div>
            {Object.keys(dim.details).length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2 text-xs text-gray-600 dark:text-gray-400">
                {Object.entries(dim.details)
                  .filter(([key]) => !key.includes('error') && !key.includes('message'))
                  .slice(0, 3)
                  .map(([key, value]) => (
                    <span key={key} className="px-2 py-0.5 bg-gray-50 dark:bg-gray-700 rounded">
                      {key.replace(/_/g, ' ')}: {String(value)}
                    </span>
                  ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
