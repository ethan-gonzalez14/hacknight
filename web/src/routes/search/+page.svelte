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

<br/><br/>

<div class="input-container">
<Input type="text" bind:value={search} placeholder="Search for someone..." />
</div>

<br />

{#if match != null}
<div class="match">
    <p class="username">{match.username}</p>
    <p class="count">{match.degrees_of_separation == -1 ? "No Connection" : match.degrees_of_separation}</p>
</div>
{/if}

<style>
    .input-container {
        width: 80%;
    }
    .match {
        border: 3px solid #000;
        width: 30%;
        min-height: 45px;
    }
    .match p {
        vertical-align: middle;
    }
    .username {
        font-size: 1.5rem;
        display: float;
        float: left;
        margin-left: 15px;
    }
    .count {
        font-size: 1rem;
        display: float;
        float: right;
        margin-right: 15px;
    }
</style>