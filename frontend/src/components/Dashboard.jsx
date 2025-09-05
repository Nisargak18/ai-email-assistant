import { useEffect, useMemo, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, ChartTooltip, Legend);

export default function Dashboard({ api, emails, loading }) {
  const [sentimentCounts, setSentimentCounts] = useState({ positive: 0, negative: 0, neutral: 0 });
  const [resolved, setResolved] = useState(0);

  useEffect(() => {
    const analyzeAll = async () => {
      if (!emails || emails.length === 0) {
        setSentimentCounts({ positive: 0, negative: 0, neutral: 0 });
        return;
      }
      const counts = { positive: 0, negative: 0, neutral: 0 };
      const limited = emails.slice(0, 20); // limit for demo/perf
      await Promise.all(
        limited.map(async (e) => {
          try {
            const { data } = await api.post('/analyze', { body: e.body });
            counts[data.sentiment] = (counts[data.sentiment] || 0) + 1;
          } catch {}
        })
      );
      setSentimentCounts(counts);
    };
    analyzeAll();
  }, [api, emails]);

  const total24h = useMemo(() => emails.length, [emails]);
  const pending = useMemo(() => Math.max(total24h - resolved, 0), [total24h, resolved]);
  const pieData = useMemo(() => ({
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        data: [
          sentimentCounts.positive,
          sentimentCounts.neutral,
          sentimentCounts.negative,
        ],
        backgroundColor: ['#22c55e', '#94a3b8', '#ef4444'],
        borderWidth: 0,
      },
    ],
  }), [sentimentCounts]);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Total (last 24h)</div>
          <div className="text-2xl font-semibold">{loading ? '…' : total24h}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Resolved</div>
          <div className="text-2xl font-semibold">{resolved}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Pending</div>
          <div className="text-2xl font-semibold">{pending}</div>
        </div>
      </div>

      <div className="p-4 bg-white rounded shadow">
        <div className="mb-2 font-medium">Sentiment distribution</div>
        <div className="w-full max-w-sm">
          <Pie data={pieData} />
        </div>
      </div>
    </div>
  );
}


