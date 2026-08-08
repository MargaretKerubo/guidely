export default function SearchResults({ results }) {
  if (!results) return null;

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
        <div className="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-800">Generated Answer</h3>
          <div className="flex items-center space-x-3 text-xs font-medium text-gray-500">
            <span className="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full border border-indigo-100 flex items-center">
              <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              {results.latency !== 'Unknown' ? `${parseFloat(results.latency).toFixed(3)}s` : 'Unknown'}
            </span>
            {results.cacheHit && (
              <span className="bg-green-50 text-green-700 px-3 py-1 rounded-full border border-green-100 flex items-center">
                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                Cache Hit
              </span>
            )}
          </div>
        </div>
        <div className="p-6">
          <div className="prose prose-indigo max-w-none text-gray-700">
            <p className="text-lg leading-relaxed">{results.answer}</p>
          </div>
        </div>
      </div>

      {results.sources && results.sources.length > 0 && (
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h4 className="text-md font-semibold text-gray-700 flex items-center">
              <svg className="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              Sources
            </h4>
          </div>
          <ul className="divide-y divide-gray-100">
            {results.sources.map((source, index) => (
              <li key={index} className="p-6 hover:bg-gray-50 transition duration-150">
                <div className="flex items-center mb-2">
                  <span className="inline-flex items-center justify-center h-6 w-6 rounded-full bg-indigo-100 text-indigo-800 text-xs font-bold mr-3">
                    {index + 1}
                  </span>
                  <h5 className="text-sm font-medium text-gray-900">{source.filename}</h5>
                </div>
                <p className="text-sm text-gray-600 italic border-l-4 border-indigo-200 pl-4 py-1">
                  "{source.snippet}"
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
