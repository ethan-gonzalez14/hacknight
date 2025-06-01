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
	import { get_relationships } from './query-server';

    let { cachedPeople, center }: { cachedPeople: Person[]; center: Person } = $props();

    // const levelColors: Record<number, string> = {
    //     1: "red",
    //     2: "orange",
    //     3: "yellow",
    //     4: "blue",
    //     5: "violet"
    // };

    let canvas: HTMLDivElement;
    let graph: any;
    let modal_showing = $state(false);

    function showModal() {
        modal_showing = true;
    }

    if (browser) {
        onMount(async () => {
                const relationships: Relationship[] = (await get_relationships(center)).relationships;
                console.log(relationships)

                const width = canvas.clientWidth;
                const height = canvas.clientHeight;
                const half_width = width / 4;
                const half_height = height / 4;
                console.log("DIMENSIONS", width, height, half_width, half_height)

                graph = new (window as (Window & typeof globalThis & { graphology: any })).graphology.Graph();

                let people: Set<string> = new Set();
                for (let relationship of relationships) {
                    console.log("RELATIONSHIP", relationship)
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
                    graph.addEdge(relationship.person1, relationship.person2, { size: 5, color: `purple` });
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
        background-color: black;
        height: 100vh;
    }
</style>