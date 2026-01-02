'use client';

import { Risk } from '@/lib/api';

interface RiskSummaryProps {
  risks: Risk[];
}

export default function RiskSummary({ risks }: RiskSummaryProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
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
      case 'momentum':
        return '📊';
      default:
        return '🔍';
    }
  };

  if (risks.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Risk Summary</h2>
        <div className="flex-1 flex items-center justify-center text-gray-500 dark:text-gray-400">
          <div className="text-center">
            <div className="text-5xl mb-3">✅</div>
            <div className="font-medium">No risks detected</div>
            <div className="text-sm mt-1">Project is in good health!</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Risk Summary</h2>
        <span className="px-2 py-1 bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 rounded-full text-xs font-semibold">
          {risks.length} {risks.length === 1 ? 'risk' : 'risks'}
        </span>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto">
        {risks.map((risk) => (
          <div
            key={risk.id}
            className={`border-l-4 rounded-lg p-4 ${getSeverityColor(risk.severity)}`}
          >
            <div className="flex items-start gap-3">
              <span className="text-xl flex-shrink-0">{getCategoryIcon(risk.category)}</span>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-sm">{risk.title}</h3>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold uppercase ${getSeverityColor(risk.severity)}`}>
                    {risk.severity}
                  </span>
                </div>
                <p className="text-sm opacity-90 mb-2">{risk.description}</p>
                <div className="text-xs opacity-75">
                  {risk.category} • {new Date(risk.detected_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
