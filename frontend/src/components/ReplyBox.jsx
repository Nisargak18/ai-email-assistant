import { useEffect, useState } from "react";
import axios from "axios";

export default function ReplyBox({ email, onClose }) {
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  //  Better: reuse same axios instance (or import from api.js if created)
  const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: { "Content-Type": "application/json" },
  });

  useEffect(() => {
    const fetchDraft = async () => {
      if (!email) return;
      try {
        setLoading(true);
        setError("");
        const response = await api.post("/emails/generate-reply", {
          subject: email.subject,
          body: email.body,
        });
        setDraft(response.data.reply || "");
      } catch (e) {
        setError("Failed to generate reply: " + (e.response?.data?.detail || e.message));
        console.error("Reply generation error:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchDraft();
  }, [email]);

  const handleSend = () => {
    alert(" Sent!\n\n" + draft);
    onClose();
  };

  return (
    <div className="p-4 bg-white rounded shadow space-y-3">
      <div className="flex items-start justify-between">
        <div>
          <div className="font-medium">Reply to: {email?.sender}</div>
          <div className="text-sm text-gray-500">Subject: {email?.subject}</div>
        </div>
        <button
          className="text-gray-500 hover:text-gray-700"
          onClick={onClose}
        >
          ✖ Close
        </button>
      </div>

      {error && (
        <div className="p-2 rounded bg-red-50 text-red-700 border border-red-200">
          {error}
        </div>
      )}

      <textarea
        className="w-full h-40 p-3 border rounded focus:outline-none focus:ring"
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        placeholder={loading ? " Generating reply..." : "Write your reply..."}
        disabled={loading}
      />

      <div className="flex justify-end gap-2">
        <button
          className="px-4 py-2 rounded bg-gray-100 hover:bg-gray-200"
          onClick={onClose}
        >
          Cancel
        </button>
        <button
          className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
          onClick={handleSend}
          disabled={loading || !draft.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}

