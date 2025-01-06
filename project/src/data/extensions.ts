import { Extension } from '../types';

export const extensions: Extension[] = [
  {
    name: "Sample Extension 1",
    extension_id: "abcdefghijklmnopqrstuvwxyz",
    description: "This is a sample extension that demonstrates the functionality.",
    version: "1.0.0",
    crx_url: "/extensions/sample1.crx"
  },
  {
    name: "Sample Extension 2",
    extension_id: "zyxwvutsrqponmlkjihgfedcba",
    description: "Another sample extension with different features and capabilities.",
    version: "2.1.0",
    crx_url: "/extensions/sample2.crx"
  }
];