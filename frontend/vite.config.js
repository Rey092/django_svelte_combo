import {resolve} from 'path';
import {defineConfig} from 'vite'
import {svelte} from '@sveltejs/vite-plugin-svelte'
import removeEntriesPlugin from '../static/js/removeEntriesPlugin.js';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        svelte({
            prebundleSvelteLibraries: true,
            onwarn(warning, defaultHandler) {
                if ([
                    'a11y-no-noninteractive-element-interactions',
                    'a11y-click-events-have-key-events'
                ].includes(warning.code)
                ) return;

                // handle all other warnings normally
                defaultHandler(warning);
            }
        }),
    ],
    root: resolve('.'),
    base: '/static/',
    server: {
        host: 'localhost',
        port: 3000,
        open: false,
        watch: {
            usePolling: true,
            disableGlobbing: false,
        },
    },
    resolve: {
        extensions: ['.js', '.jsx', '.json', '.svelte'],
    },
    build: {
        outDir: resolve('../dist'),
        assetsDir: '',
        manifest: true,
        emptyOutDir: true,
        target: 'es2015',
        rollupOptions: {
            input: {
                main: resolve('../static/js/main.js'),
            },
            output: {
                chunkFileNames: undefined,
            },
        },
        plugins: [
            removeEntriesPlugin(),
        ],
    },
})
