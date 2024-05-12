import {createInertiaApp} from '@inertiajs/svelte'
import Layout from '../layout.svelte'
import axios from "axios";
// import HomeSvelte from '../../src/adminlte/pages/Home.svelte'

createInertiaApp({
    resolve: async (name) => {
        const [app_name, file_name] = name.split(':')
        const comps = import.meta.glob('../../src/**/pages/*.svelte');
        const match = comps[`../../src/${app_name}/pages/${file_name}.svelte`];
        const page = (await match());
        return Object.assign({layout: Layout}, page);
    },
    setup({el, App, props}) {
        new App({target: el, props})
    },
    progress: {
        // The delay after which the progress bar will appear, in milliseconds...
        delay: 250,

        // The color of the progress bar...
        color: 'linear-gradient(90deg, #ff5860 0%, #ff55a5 100%)',

        // Whether to include the defuault NProgress styles...
        includeCSS: true,

        // Whether the NProgress spinner will be shown...
        showSpinner: false,
    },
});

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"
