'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface TrendChartProps {
  data: Array<{ date: string; score: number }>;
}

export default function TrendChart({ data }: TrendChartProps) {
  // If no historical data, show a placeholder
  if (data.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Health Trend</h2>
        <div className="flex-1 flex items-center justify-center text-gray-500 dark:text-gray-400">
          <div className="text-center">
            <div className="text-4xl mb-2">📊</div>
            <div className="text-sm">Historical data will appear here</div>
          </div>
        </div>
      </div>
    );
  }

  // Format data for chart
  const chartData = data.map((item) => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: item.score,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 h-full flex flex-col border border-gray-200 dark:border-gray-700">
      <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Health Trend</h2>
      <div className="flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-gray-700" />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              className="dark:stroke-gray-400"
              fontSize={12}
              tickLine={false}
            />
            <YAxis 
              domain={[0, 100]} 
              stroke="#6b7280"
              className="dark:stroke-gray-400"
              fontSize={12}
              tickLine={false}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                padding: '8px',
                color: '#111827'
              }}
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: '#3b82f6', r: 4 }}
              name="Health Score"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
