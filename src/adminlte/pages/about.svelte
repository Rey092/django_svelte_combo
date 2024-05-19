<script>
    import {inertia} from "@inertiajs/svelte";

    let {number} = $props();
    let notNumber = $state(0);

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

<!-- Default box -->
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Hello from ABOUT</h3>

        <div class="card-tools">
            <button type="button" class="btn btn-tool" data-card-widget="collapse"
                    title="Collapse">
                <i class="fas fa-minus"></i>
            </button>
            <button type="button" class="btn btn-tool" data-card-widget="remove" title="Remove">
                <i class="fas fa-times"></i>
            </button>
        </div>
    </div>
    <div class="card-body">
        Start creating your amazing application! {number}, {notNumber}!!!
    </div>
    <!-- /.card-body -->
    <div class="card-footer">
        <button on:click={increment}>Increment</button>
        <a use:inertia href="/">Home</a>*
    </div>
    <!-- /.card-footer-->
</div>
<!-- /.card -->
