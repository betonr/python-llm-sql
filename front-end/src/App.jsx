import React, { useState } from 'react';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setAnswer(data.answer);
    } catch (error) {
      setAnswer('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-white">
      <h1 className="text-2xl font-bold mb-4">LLM Chatbot for Sales BI</h1>
      <textarea
        className="w-full max-w-xl border border-gray-300 rounded-lg p-2 mb-4"
        rows="4"
        placeholder="Ask your question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        onClick={handleAsk}
        disabled={loading || !question.trim()}
      >
        {loading ? 'Asking...' : 'Ask'}
      </button>
      {answer && (
        <div className="mt-6 w-full max-w-xl bg-gray-50 p-4 border border-gray-300 rounded">
          <p className="text-sm text-gray-700 whitespace-pre-wrap">{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
