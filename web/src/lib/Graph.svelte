<svelte:head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/2.4.0/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphology/0.25.4/graphology.umd.min.js"></script>
</svelte:head>

<script lang="ts">
    import circular from "graphology-layout/circular";
	import { onMount } from 'svelte';
        import { browser } from '$app/environment';


    let canvas: HTMLDivElement;
    let graph;

    onMount(() => {
        if (browser) {
            graph = new (window as (Window & typeof globalThis & { graphology: any })).graphology.Graph();
            graph.addNode("1", { label: "Node 1", size: 10, color: "blue" });
            graph.addNode("2", { label: "Node 2", size: 20, color: "red" });
            graph.addEdge("1", "2", { size: 5, color: "purple" });

            const sigmaInstance = new Sigma(
                graph,
                document.getElementById("container")
            );

            circular.assign(graph);
        }

    });
    
</script>

<div class="graph" bind:this={canvas}></div>