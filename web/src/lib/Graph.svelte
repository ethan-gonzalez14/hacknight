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
    import Input from './Input.svelte';
	import { get_person, get_relationships, get_user_code, update_private_bio, update_public_bio } from './query-server';
	import { getByPlaceholderText } from '@testing-library/svelte';

    let { cachedPeople, center }: { cachedPeople: Person[]; center: Person } = $props();

    let updatedCenter = $state(center);

    const level_colors: Record<string, string> = {
        "best_friends": "#006400",
        "family": "#db1f54",
        "friends": "green",
        "work": "orange",
        "married": "purple",
        "romantic": "pink"
    };

    let canvas: HTMLDivElement;
    let graph: any;
    let modal_showing = $state(false);

    function showModal() {
        modal_showing = true;
    }

    let person: Record<string, any> | null = $state({});
    // The relationship between the center person and the clicked person
    let highlighted_relationship: Relationship | null = $state(null);

    if (browser) {
        onMount(async () => {
            graph = new (window as (Window & typeof globalThis & { graphology: any })).graphology.Graph();
            
            $effect(async () => {
                // Hack to clear the graph (No time in Hackathon to figure out how to properly clear it)
                // TODO: Find a better way to clear the graph
                canvas.innerHTML = '';
                
                // TODO: Figure out why this isn't working
                const renderer = new (window as any).Sigma(
                graph,
                canvas,
                {
                    labelColor: {
                    color: "attribute",         // Tells Sigma to use the node attribute
                    attribute: "labelColor",    // Attribute name you're using
                    },
                    defaultNodeLabelColor: "#ffffff"  // Optional fallback
                }
                ); 
                
                renderer.on("clickNode", async (event: any) => {
                    const node = event.node;
                    console.log("Clicked node:", node, graph.getNodeAttributes(node));
                    const attributes = graph.getNodeAttributes(node);
                    modal_showing = true;

                    if (relationship_map[attributes.label]) {
                        highlighted_relationship = relationship_map[attributes.label];
                    } else {
                        highlighted_relationship = null;
                    }

                    person = await get_person(attributes.label);
                    console.log("PERSON: " , person)
                    console.log("HIGHLIGHTED RELATIONSHIP: " , highlighted_relationship)
                });
                renderer.getGraph().clear();
                
                const relationships: Relationship[] = (await get_relationships(updatedCenter)).relationships;
                // Relationships the center person has with the others
                let relationship_map: Record<string, Relationship> = {};

                const width = canvas.clientWidth;
                const height = canvas.clientHeight;
                const half_width = width / 4;
                const half_height = height / 4;

                let people: Set<string> = new Set();
                // graph.addNode(updatedCenter, { label: updatedCenter, x: half_width, y: half_height, size: 30, color: "#f8f6d8", labelColor: "#00ff00" });
                graph.addNode(updatedCenter, {
                label: updatedCenter,
                x: half_width,
                y: half_height,
                size: 30,
                color: "#f8f6d8",
                labelColor: "#ffffff"  // white label color
                });
                for (let relationship of relationships) {
                    people.add(relationship.person1);
                    people.add(relationship.person2);

                    if (relationship.person1 == center || relationship.person2 == center) {
                        relationship_map[relationship.person1 == center ? relationship.person2 : relationship.person1] = relationship;
                    }
                }
                let angle = 0;
                let increment = Math.PI * 2 / Math.max(1, people.size - 1);
                for (let person of people) {
                    if (person === updatedCenter) continue; // Skip the center node

                    const random_length = random(0.9, 1);
                    console.log(random_length)

                    const x = half_width + half_width * 0.1 * random_length * Math.cos(angle);
                    const y = half_height + half_height * 0.1 * random_length * Math.sin(angle);
                    graph.addNode(person, { label: person, x, y, size: 30, color: "#a7a48d" });
                    angle += increment;
                }
                for (let relationship of relationships) {
                    graph.addEdge(relationship.person1, relationship.person2, { size: 5, label: "hey!", color: level_colors[relationship.level] });
                }
         
        });
    });
    }
    
    function handleSocialClick(name: string) {
        if (updatedCenter != name) updatedCenter = name;
        modal_showing = false;
    }

    function submitBioChanges() {
        update_private_bio(center, person.publicBio);
        update_public_bio(center, person.privateBio);
    }

    function handleSubmit() {
		console.log(person);
	}
    
    let code: string | null = $state(null);
    // Dynamically load the code for the center person when we need it
    async function getCode() {
        if (code == null) code = (await get_user_code(center)).friendCode;
        return true;
    }
</script>

<Modal visible={modal_showing} changeVisible={(vis) => modal_showing = vis}>
    <!-- <img src="/your-image.jpg" alt="Popup Image" class="popup-image" /> -->
{#if person}
    <div class="popup-text">
        <h2>{person.name}</h2>

        {#if person.socials?.length > 0}
        <span style="color: gray;">@{person.socials}</span>
        {/if}

        <p><span class="bio">Public Bio:</span> {person.publicBio}</p>
        <p style="margin-bottom: 24px;"><span class="bio">Private Bio:</span> {person.privateBio}</p>
        <SocialButton label="{person.name}'s Web" width="100%" height="20%" onClick={() => handleSocialClick(person.name)} />

        {#if person.name?.toLowerCase() == center.toLowerCase()}

        {#await getCode()}
        <p>Loading your friend code from our Web Magic...</p>
        {:then success}
        <p style="margin-bottom: 24px;"><span>Your Code:</span> {code}</p>
        {/await}

        <h2>Change Bio</h2>

        <br/>

        <!-- <Input type="text" name="publicBio" placeholder="Add Public Bio" />
        <Input type="text" name="privateBio" placeholder="Add Private Bio" /> -->
        <form on:submit|preventDefault={handleSubmit}>
            <Input name="publicBio" bind:value={person.publicBio} placeholder="Add Public Bio" multiline={true} />
            <Input name="privateBio" bind:value={person.privateBio} placeholder="Add Private Bio" multiline={true} />
            <SocialButton label="Submit Changes" width="100%" height="10%" type="submit" onClick={submitBioChanges} />
            <!-- <button type="submit">Save Person</button> -->
        </form>
        {:else if highlighted_relationship}
            <h3>Remember when you two met? You do now: &ldquo;{highlighted_relationship.context}&rdquo;</h3>

            <br/>
            <p><b>Public Bio:</b> {person.public_bio}</p>
            {#if highlighted_relationship.level != 'work'}
            <p><b>Private Bio:</b> {person.private_bio}</p>
            {/if}
        {/if}
    </div>
{/if}
</Modal>

<div class="graph-container">
    <div class="graph" bind:this={canvas}></div>
</div>

<style>
    .graph-container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #222222;
    }
    .graph {
        width: 100%;
        height: 100%;
        /* border: 2px solid #000; */
        touch-action: manipulation;
    }
    .bio {
        font-weight: bold;
    }
    button {
        background-color: #1c86ee;
        color: white;
        cursor: pointer;
        width: 100%;
        height: 10vh;
    }

    span {
    font-family: "Titillium Web", sans-serif;
    font-weight: 500;
    font-style: normal;
    font-size: 20px;
    }

</style>