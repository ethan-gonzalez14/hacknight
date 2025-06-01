<svelte:head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sigma.js/2.4.0/sigma.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphology/0.25.4/graphology.umd.min.js"></script>
</svelte:head>

<script lang="ts">
	import { onMount } from 'svelte';
    import { browser } from '$app/environment';
	import { random } from "$lib";

    import type { Person, Relationship } from "$lib/types";
	import Modal from "./Modal.svelte";

    let { cachedPeople }: { cachedPeople: Person[] } = $props();

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
    let graph: any;
    let modal_showing = $state(false);

    function showModal() {
        modal_showing = true;
    }

    if (browser) {
        onMount(() => {
                const width = canvas.clientWidth;
                const height = canvas.clientHeight;
                const half_width = width / 2 / 2;
                const half_height = height / 2 / 2;
                console.log("DIMENSIONS", width, height, half_width, half_height)

                graph = new (window as (Window & typeof globalThis & { graphology: any })).graphology.Graph();

                let people: Set<string> = new Set();
                for (let relationship of relationships) {
                    people.add(relationship.person1);
                    people.add(relationship.person2);
                }
                graph.addNode(center, { label: center, x: half_width, y: half_height, size: 20, color: "orange" });
                let angle = 0;
                let increment = Math.PI * 2 / Math.max(1, people.size - 1);
                for (let person of people) {
                    if (person === center) continue; // Skip the center node

                    const random_length = random(0.9, 1);
                    console.log(random_length)

                    const x = half_width + half_width * 0.2 * random_length * Math.cos(angle);
                    const y = half_height + half_height * 0.2 * random_length * Math.sin(angle);
                    graph.addNode(person, { label: person, x, y, size: 20, color: "lightblue" });
                    angle += increment;
                }
                for (let relationship of relationships) {
                    graph.addEdge(relationship.person1, relationship.person2, { size: 1, color: "gray" });
                }
                
                const renderer = new (window as any).Sigma(
                    graph,
                    canvas
                );
                renderer.on("clickNode", (event: any) => {
                    const node = event.node;
                    console.log("Clicked node:", node, graph.getNodeAttributes(node));
                    modal_showing = true;
                });
            
        });
    }
    
</script>

<Modal visible={modal_showing} changeVisible={(vis) => modal_showing = vis}> </Modal>
<div class="graph" bind:this={canvas}></div>

<style>
    .graph {
        width: 100vw;
        height: 100vw;
        background-color: #F1F1F1;
    }
</style>