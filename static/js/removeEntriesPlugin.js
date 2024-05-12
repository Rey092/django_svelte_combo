// removeEntriesPlugin.js
export default function removeEntriesPlugin() {
  return {
    name: 'remove-entries-plugin',
    generateBundle(_, bundle) {
      // Iterate through each asset in the bundle
      for (const fileName in bundle) {
        const asset = bundle[fileName];

        // Remove specific entries from the manifest
        if (asset.isEntry) {
          delete asset.isEntry;
        }

        if (asset.assets) {
          delete asset.assets;
        }

        if (asset.dynamicImports) {
          delete asset.dynamicImports;
        }

        if (asset.isDynamicEntry) {
          delete asset.isDynamicEntry;
        }
      }
    },
  };
}
