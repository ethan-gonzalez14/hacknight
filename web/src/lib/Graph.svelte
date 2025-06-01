<svelte:head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/2.4.0/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphology/0.25.4/graphology.umd.min.js"></script>
</svelte:head>

<script lang="ts">
    import circular from "graphology-layout/circular";
	import { onMount } from 'svelte';
    import { browser } from '$app/environment';

    type Relationship = {
        person1: string;
        person2: string;
    };
    type Person = string;

    const center: Person = "Kiyaan";
    const relationships: Relationship[] = [
        { person1: "Kiyaan", person2: "Aarav" },
        { person1: "Kiyaan", person2: "Vivaan" },
        { person1: "Kiyaan", person2: "Reyansh" },
        { person1: "Kiyaan", person2: "Anvi" },
        { person1: "Kiyaan", person2: "Aarvi" },
        { person1: "Aarvi", person2: "Anvi" },
        { person1: "Kiyaan", person2: "Aaradhya" },
        { person1: "Kiyaan", person2: "Saanvi" },
        { person1: "Saanvi", person2: "Aaradhya" },
        
    ];

    let canvas: HTMLDivElement;
    let graph;

    onMount(() => {
        if (browser) {
            const width = canvas.clientWidth;
            const height = canvas.clientHeight;

            graph = new (window as (Window & typeof globalThis & { graphology: any })).graphology.Graph();

            let people: Set<string> = new Set();
            for (let relationship of relationships) {
                people.add(relationship.person1);
                people.add(relationship.person2);
            }
            for (let person of people) {
                graph.addNode(person, { label: person, size: 10, color: "lightblue" });
            }
            for (let relationship of relationships) {
                graph.addEdge(relationship.person1, relationship.person2, { size: 1, color: "gray" });
            }

            circular.assign(graph);

            const sigmaInstance = new Sigma(
                graph,
                canvas
            );
        }
    });
    
</script>

<div class="graph" bind:this={canvas}></div>

<style>
    .graph {
        width: 800px;
        height: 600px;
    }
</style>