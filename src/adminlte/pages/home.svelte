<script>
    import {inertia} from "@inertiajs/svelte";
    let { number } = $props();
    let notNumber = $state(0)

    function increment() {
        number += 1;
        notNumber += 1;
    }
</script>

<style>
    h1 {
        font-size: 100px;
        color: #ff0000;
    }
</style>

<div>
    <h1>Hello World</h1>
    <h2>{number}</h2>
    <h2>{notNumber}</h2>
    <button on:click={increment}>Increment</button>
    <a use:inertia href="/">About</a>*
</div>
