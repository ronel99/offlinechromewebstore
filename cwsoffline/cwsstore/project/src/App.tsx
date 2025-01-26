import React from 'react';
import { extensions } from './data/extensions';
import { ExtensionCard } from './components/ExtensionCard';
import { SearchBar } from './components/SearchBar';
import { useSearch } from './hooks/useSearch';
import { Store } from 'lucide-react';

function App() {
  const { searchQuery, setSearchQuery, filteredExtensions } = useSearch(extensions);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8 text-center">
          <div className="flex items-center justify-center mb-4">
            <Store className="w-10 h-10 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Chrome Extensions Store
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Download and install Chrome extensions offline
          </p>
        </header>

        <SearchBar value={searchQuery} onChange={setSearchQuery} />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredExtensions.map((extension) => (
            <ExtensionCard
              key={extension.extension_id}
              extension={extension}
            />
          ))}
        </div>

        {filteredExtensions.length === 0 && (
          <p className="text-center text-gray-600 dark:text-gray-400 mt-8">
            No extensions found matching your search.
          </p>
        )}
      </div>
    </div>
  );
}

export default App;