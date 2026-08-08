import { useState } from 'react';
import Notification from '../components/Notification';
import SearchInput from '../components/SearchInput';
import SearchResults from '../components/SearchResults';

export default function SearchDashboard() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Search failed. Please try again.');
      }

      const latency = response.headers.get('x-process-time') || 'Unknown';
      const cacheHit = response.headers.get('x-cache-hit') === 'true';
      const data = await response.json();

      setResults({ ...data, latency, cacheHit });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-16 animate-fade-in-up">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 tracking-tight sm:text-6xl">
          Guidely Knowledge Search
        </h1>
        <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
          Find answers instantly across all your company documents.
        </p>
      </div>

      <SearchInput 
        query={query} 
        setQuery={setQuery} 
        handleSearch={handleSearch} 
        isLoading={isLoading} 
      />

      {error && (
        <Notification type="error" message={error} onClose={() => setError(null)} />
      )}

      <SearchResults results={results} />
    </div>
  );
}
