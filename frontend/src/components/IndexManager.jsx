import { useState } from 'react';

export default function IndexManager({ showNotification }) {
  const [isReindexing, setIsReindexing] = useState(false);

  const handleReindex = async () => {
    setIsReindexing(true);
    try {
      const response = await fetch('http://localhost:8000/api/documents/reindex', {
        method: 'POST',
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Reindexing failed');
      }

      const data = await response.json();
      showNotification('success', `Reindexed successfully. Processed ${data.chunks_processed} chunks.`);
    } catch (err) {
      showNotification('error', err.message);
    } finally {
      setIsReindexing(false);
    }
  };

  return (
    <div className="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-100 transition-all hover:shadow-2xl">
      <div className="px-6 py-5 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
        <h3 className="text-lg leading-6 font-semibold text-gray-900 flex items-center">
          <svg className="w-5 h-5 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          Index Management
        </h3>
      </div>
      <div className="p-6 flex flex-col justify-between h-[calc(100%-61px)]">
        <div>
          <p className="text-sm text-gray-600 mb-6 leading-relaxed">
            Re-index the document database to include newly uploaded files. This will parse all files in the <code>data/sample-docs</code> directory, create chunks, and update the FAISS vector store embeddings.
          </p>
        </div>
        <button
          onClick={handleReindex}
          disabled={isReindexing}
          className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150"
        >
          {isReindexing ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Re-indexing...
            </span>
          ) : (
            'Trigger Re-index'
          )}
        </button>
      </div>
    </div>
  );
}
