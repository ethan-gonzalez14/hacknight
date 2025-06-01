<script lang="ts">
    import Input from "$lib/Input.svelte";
    import { find_user_match } from "$lib/query-server";
	import type { User } from "$lib/types";
	import { onMount } from "svelte";

    let search = $state('');

    let match: User | null = $state(null);
    let { data }: {
        data: { username: string }
    } = $props();

    console.log(data)
    onMount(() => {
        $effect(() => {
            let current_search = search;
            // Make sure we don't fetch the data until the user has waiting at least 150 milliseconds
            setTimeout(async () => {
                // Let them keep typing
                if (search != current_search) return;
                if (search.length < 2) return;

                console.log(data.username)
                const person = await find_user_match(data.username, search);
                if (person.error || (person.message === "NO_MATCH")) return;

                console.log(person)

                match = {
                    username: person.name,
                    socials: person.socials,
                    degrees_of_separation: person.degrees,
                }
                }, 150);
            });
        });
    
</script>

<Input type="text" bind:value={search} placeholder="Search for someone..." />

{#if match != null}
<div class="match">
    <p>{match.username}</p>
    <p>{match.degrees_of_separation == -1 ? "No Connection" : match.degrees_of_separation + 1}</p>
</div>
{/if}

<style>
    .match {
        border: 3px solid #000;
        width: 50%;
        min-height: 45px;
    }
</style>