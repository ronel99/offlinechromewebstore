import { useState, useMemo } from 'react';
import { Extension } from '../types';

export function useSearch(extensions: Extension[]) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredExtensions = useMemo(() => {
    const query = searchQuery.toLowerCase();
    return extensions.filter((extension) =>
      extension.name.toLowerCase().includes(query) ||
      extension.description.toLowerCase().includes(query) ||
      extension.extension_id.toLowerCase().includes(query)
    );
  }, [extensions, searchQuery]);

  return {
    searchQuery,
    setSearchQuery,
    filteredExtensions,
  };
}