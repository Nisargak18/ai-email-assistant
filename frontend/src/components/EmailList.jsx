import { useEffect, useMemo, useState } from 'react';
import ReplyBox from './ReplyBox';

export default function EmailList({ api, emails, loading }) {
  const [rows, setRows] = useState([]);
  const [selected, setSelected] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    const enrich = async () => {
      if (!emails || emails.length === 0) { setRows([]); return; }
      const limited = emails.slice(0, 50).map(e => ({ ...e, sentiment: '...', priority: '...' }));
      setRows(limited); // show immediately
      setAnalyzing(true);

      // progressively update each row as analysis returns
      await Promise.all(limited.map(async (e, idx) => {
        try {
          const { data } = await api.post('/analyze', { body: e.body });
          setRows(prev => {
            const next = [...prev];
            next[idx] = { ...e, sentiment: data.sentiment, priority: data.priority };
            return next;
          });
        } catch {
          setRows(prev => {
            const next = [...prev];
            next[idx] = { ...e, sentiment: 'neutral', priority: 'not_urgent' };
            return next;
          });
        }
      }));
      setAnalyzing(false);
    };
    enrich();
  }, [api, emails]);

  const columns = useMemo(() => ['Sender', 'Subject', 'Date', 'Sentiment', 'Priority', 'Action'], []);

  return (
    <div className="space-y-4">
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-gray-700">
            <tr>
              {columns.map((c) => (
                <th key={c} className="text-left px-4 py-2 whitespace-nowrap">{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading && rows.length === 0 ? (
              <tr><td className="px-4 py-4" colSpan={columns.length}>Loading…</td></tr>
            ) : rows.map((r, idx) => (
              <tr key={idx} className="border-t">
                <td className="px-4 py-2">{r.sender}</td>
                <td className="px-4 py-2">{r.subject}</td>
                <td className="px-4 py-2">{r.date}</td>
                <td className="px-4 py-2 capitalize">{r.sentiment || '...'}</td>
                <td className="px-4 py-2 capitalize">{(r.priority || '...').toString().replace('_', ' ')}</td>
                <td className="px-4 py-2">
                  <button
                    className="px-3 py-1 rounded bg-blue-600 text-white hover:bg-blue-700"
                    onClick={() => setSelected(r)}
                  >View & Reply</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && (
        <ReplyBox api={api} email={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}


