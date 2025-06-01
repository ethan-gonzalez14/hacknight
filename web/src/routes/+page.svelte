<script lang="ts">
    import { add_relationship, get_relationships }  from '$lib/query-server';
    import Graph from "$lib/Graph.svelte";
    import Modal from "$lib/Modal.svelte";
	import { onMount } from 'svelte';

    const username = "alice";

    let code_modal = $state(false);
    function get_code_modal() {
        console.log("HEY... WTF")
        code_modal = true;
    }

    let code = "";
    let error = $state("");
    let message = $state("");
    async function find() {
        const add = await add_relationship(username, code);
        if (add.error) {
            switch (add.error) {
                case "CODE_DOES_NOT_EXIST":
                    error = "The code you entered does not exist.";
                    break;
            }
        }
        else message = "Friend added successfully! Reload to see changes";
    }

    let { data, form }: {
       data: { loggedIn: boolean; },
       form: { error: string } | { success:true }
    } = $props();

</script>

{#if data.loggedIn}
<div class="menu">
<button class="add" onclick={get_code_modal}>
    &plus;
</button>
<form action="?/logout" method="POST">
    <button class="logout" type="submit">Log Out</button>
</form>
</div>
<Modal visible={code_modal} changeVisible={(val: boolean) => code_modal = val} >
    <h2>Enter your code</h2>
    <input type="text" placeholder="Enter your code here" bind:value={code} />
    <button class="find" onclick={find}>Find Your Friend</button>
    {#if error}
    <p class="red">{error}</p>
    {/if}
    {#if message}
    <p class="yellow">{message}</p>
    {/if}
</Modal>

<Graph cachedPeople={[]} center={username} />

<style>
    .add {
        aspect-ratio: 1 / 1;;
    }
    .logout {
        padding: 10px 10px;
    }
    .find {
        background-color: orange;
        padding: 7px 8px;
        color: white;
        cursor: pointer;
    }
    .menu button {
        background-color: #1c86ee;
        color: white;
        cursor: pointer;
        width: 100%;
    }
    .menu {
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: absolute;
        z-index: 1;
        top: 10px;
        left: 10px;
        width: 100px;
    }
</style>

{:else}

<form method="POST">
    <input type="text" name="username" placeholder="Username" required />
    @<input type="text" name="socials" placeholder="Social Media Handles" />
    <button type="submit" formaction="?/login">Log In</button>
    <button type="submit" formaction="?/register">Sign Up</button>
</form>
{#if form && 'error' in form}
    <p class="error">{form.error}</p>
{/if}

{/if}

<style>
    .error {
        color: red;
    }
</style>