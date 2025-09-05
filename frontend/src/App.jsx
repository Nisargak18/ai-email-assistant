import { useEffect, useState, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';

import Dashboard from './components/Dashboard';
import EmailList from './components/Emaillist';

//  Centralized API instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Backend must be running here
  headers: {
    'Content-Type': 'application/json',
  },
});

export default function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchEmails = async () => {
      try {
        setLoading(true);
        setError('');
        const res = await api.get('/emails/'); //  include trailing slash for FastAPI
        setEmails(res.data || []);
      } catch (e) {
        setError('Failed to load emails: ' + (e.response?.data?.detail || e.message));
        console.error('Email fetch error:', e);
      } finally {
        setLoading(false);
      }
    };
    fetchEmails();
  }, []);

  const appHeader = useMemo(() => (
    <header className="w-full border-b bg-white">
      <div className="max-w-6xl mx-auto px-4 py-6 flex items-center justify-between">
        <nav className="flex gap-4">
          <Link className="text-blue-600 hover:underline" to="/dashboard">Dashboard</Link>
          <Link className="text-blue-600 hover:underline" to="/emails">Emails</Link>
        </nav>
        <span className="text-xl font-semibold">AI Email Assistant</span>
      </div>
    </header>
  ), []);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {appHeader}
        <main className="max-w-6xl mx-auto px-4 py-6">
          {error && (
            <div className="mb-4 p-3 rounded bg-red-50 text-red-700 border border-red-200">
              {error}
            </div>
          )}
          <Routes>
            <Route path="/" element={<Dashboard api={api} emails={emails} loading={loading} />} />
            <Route path="/emails" element={<EmailList api={api} emails={emails} loading={loading} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
