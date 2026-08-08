export default function SearchInput({ query, setQuery, handleSearch, isLoading }) {
  return (
    <div className="bg-white/70 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 p-6 mb-8 transition-all duration-300 hover:shadow-2xl">
      <form onSubmit={handleSearch} className="relative flex items-center">
        <input
          type="text"
          className="w-full pl-6 pr-32 py-4 text-lg bg-white/50 border border-gray-200 rounded-full focus:outline-none focus:ring-4 focus:ring-indigo-500/30 focus:border-indigo-500 transition-all text-gray-800 placeholder-gray-400"
          placeholder="Ask a question about your documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="absolute right-2 top-2 bottom-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium px-8 rounded-full shadow hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isLoading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Searching...
            </span>
          ) : (
            'Search'
          )}
        </button>
      </form>
    </div>
  );
}
