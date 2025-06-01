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
    import SocialButton from './SocialButton.svelte';
	import { get_person, get_relationships, get_user_code } from './query-server';

    let { cachedPeople, center }: { cachedPeople: Person[]; center: Person } = $props();

    let updatedCenter = $state(center);

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

    let person: Record<string, any> = $state({

    });

    if (browser) {
        onMount(async () => {
            graph = new (window as (Window & typeof globalThis & { graphology: any })).graphology.Graph();
            
            $effect(async () => {
                // Hack to clear the graph (No time in Hackathon to figure out how to properly clear it)
                // TODO: Find a better way to clear the graph
                canvas.innerHTML = '';
                
                // TODO: Figure out why this isn't working
                // renderer.getGraph().clear();
                const renderer = new (window as any).Sigma(
                    graph,
                    canvas
                );     
                renderer.on("clickNode", async (event: any) => {
                    const node = event.node;
                    console.log("Clicked node:", node, graph.getNodeAttributes(node));
                    const attributes = graph.getNodeAttributes(node);
                    modal_showing = true;

                    person = await get_person(attributes.label);
                    console.log(person)
                });
                renderer.getGraph().clear();
                
                console.log(canvas.childNodes)
                console.log("UPDATED CENTER", updatedCenter);

                const relationships: Relationship[] = (await get_relationships(updatedCenter)).relationships;
                console.log(relationships)

                const width = canvas.clientWidth;
                const height = canvas.clientHeight;
                const half_width = width / 4;
                const half_height = height / 4;
                console.log("DIMENSIONS", width, height, half_width, half_height)
                console.log(relationships)

                let people: Set<string> = new Set();
                graph.addNode(updatedCenter, { label: updatedCenter, x: half_width, y: half_height, size: 30, color: "orange" });
                for (let relationship of relationships) {
                    console.log("RELATIONSHIP", relationship)
                    people.add(relationship.person1);
                    people.add(relationship.person2);
                }
                let angle = 0;
                let increment = Math.PI * 2 / Math.max(1, people.size - 1);
                for (let person of people) {
                    if (person === updatedCenter) continue; // Skip the center node

                    const random_length = random(0.9, 1);
                    console.log(random_length)

                    const x = half_width + half_width * 0.1 * random_length * Math.cos(angle);
                    const y = half_height + half_height * 0.1 * random_length * Math.sin(angle);
                    graph.addNode(person, { label: person, x, y, size: 30, color: "lightblue" });
                    angle += increment;
                }
                for (let relationship of relationships) {
                    graph.addEdge(relationship.person1, relationship.person2, { size: 5, color: `purple` });
                }
         
        });
    });
    }
    

    function handleSocialClick(name: string) {
        console.log('Social button clicked');
        if (updatedCenter != name) {
            console.log('Social button clicked for:', name);
            updatedCenter = name;
        } else {
            console.log('Social button clicked for center:', center);
        }
        modal_showing = false;
    }
    let code: string | null = $state(null);
    // Dynamically load the code for the center person when we need it
    async function getCode() {
        if (code == null) code = (await get_user_code(center)).friendCode;
    }
</script>

<Modal visible={modal_showing} changeVisible={(vis) => modal_showing = vis}>
    <img src="/your-image.jpg" alt="Popup Image" class="popup-image" />
    <div class="popup-text">
        <h2>{person.name}</h2>
        <span style="color: gray;">@{person.socials}</span>
        <p><span class="bio">Public Bio: </span>{person.publicBio}</p>
        <p><span class="bio">Private Bio: </span>{person.privateBio}</p>
        <SocialButton onClick={() => handleSocialClick(person.name)} />

        {#if person.name == center && getCode()}
        <p><span>Code: </span>{code}</p>
        {/if}
    </div>
</Modal>
<div class="graph" bind:this={canvas}></div>

<style>
    .graph {
        width: 90vw;
        background-color: white;
        height: 100vh;
        border: 2px solid #000;
    }
    .bio {
        font-weight: bold;
    }
</style>