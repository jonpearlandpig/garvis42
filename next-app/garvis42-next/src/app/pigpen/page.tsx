import { useEffect, useState } from 'react';

interface Operator {
  id: string;
  name: string;
  domain: string;
  is_active: boolean;
  description: string;
}

export default function PigPenPage() {
  const [operators, setOperators] = useState<Operator[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/pigpen')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch operators');
        return res.json();
      })
      .then((data) => setOperators(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold text-accent mb-6">Pig Pen Operators</h1>
      {loading && <div className="text-gray-400">Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {operators.map((op) => (
          <div key={op.id} className="rounded-xl border border-border bg-card/80 p-6 shadow">
            <h2 className="text-xl font-semibold text-orange-400">{op.name}</h2>
            <p className="text-sm text-gray-300 mb-2">{op.domain}</p>
            <p className="text-xs text-gray-400 mb-4">{op.description}</p>
            <span className={`inline-block px-2 py-1 rounded text-xs font-bold ${op.is_active ? 'bg-green-700 text-white' : 'bg-gray-700 text-gray-300'}`}>
              {op.is_active ? 'Active' : 'Inactive'}
            </span>
            <button className="ml-4 px-3 py-1 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors text-xs">
              Invoke
            </button>
          </div>
        ))}
      </div>
    </main>
  );
}
