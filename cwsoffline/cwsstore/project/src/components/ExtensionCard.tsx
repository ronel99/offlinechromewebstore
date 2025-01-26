import React from 'react';
import { Download } from 'lucide-react';
import { Extension } from '../types';

interface ExtensionCardProps {
  extension: Extension;
}

export function ExtensionCard({ extension }: ExtensionCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors">
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {extension.name}
      </h2>
      <div className="space-y-2 mb-4">
        <p className="text-sm text-gray-600 dark:text-gray-300">
          <span className="font-semibold">ID:</span> {extension.extension_id}
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          <span className="font-semibold">Version:</span> {extension.version}
        </p>
        <p className="text-gray-700 dark:text-gray-200">
          {extension.description}
        </p>
      </div>
      <a
        href={extension.crx_url}
        download
        className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
      >
        <Download className="w-4 h-4 mr-2" />
        Download
      </a>
    </div>
  );
}