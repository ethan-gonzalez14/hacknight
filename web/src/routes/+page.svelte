<script lang="ts">
    import { add_relationship, get_relationships }  from '$lib/query-server';
    import Graph from "$lib/Graph.svelte";
    import Modal from "$lib/Modal.svelte";
	import Input from '$lib/Input.svelte';
	import { text } from '@sveltejs/kit';

    let code_modal = $state(false);
    function get_code_modal() {
        console.log("HEY... WTF")
        code_modal = true;
    }

    let code = "";
    let error = $state("");
    let message = $state("");
    async function find() {
        const add = await add_relationship(data.username, code);
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
       data: { loggedIn: boolean; username: string; },
       form: { error: string } | { success:true }
    } = $props();

</script>

{#if data.loggedIn}
<div class="menu">
<button class="add" onclick={get_code_modal}>
    &plus;
</button>
<button class="search">
    <a href="/search" class="material-symbols-outlined">search</a>
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

<Graph cachedPeople={[]} center={data.username} />

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
    .search > * {
        vertical-align: middle;
        text-align: center;
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

<div class="container">
    <h1>Gain personal <span style="text-decoration: underline;">and</span> professional contacts, all in one place.</h1>

    <p>The Web makes it easy to remember who's who. And don't worry about your boss finding out your secret nightlife
        drug dealing or having a dance fiesta — control who sees your public and private bios.
    </p>

    <h1>Enough Talk. Get Talking.</h1>
    <br/>

    <div class="login-container">
        <div class="form-container">
            <form method="POST">
                <b>Sign Up Today To Stay Connected</b>
                <Input type="text" name="username" placeholder="Username" required />
                <p>@</p>
                <Input type="text" name="socials" placeholder="Social Media Handles" />
                <button type="submit" formaction="?/login">Log In</button>
                <br/>
                <button type="submit" formaction="?/register">Sign Up</button>
            </form>

            <p class="error">
                {#if form && 'error' in form}
                    {form.error}
                {/if}
            </p>
        </div>
    </div>
</div>

{/if}

<style lang="scss">
    h1 {
        font-size: 3rem;
    }
    h1, p {
        width: 100%;
        text-align: center;
    }
	button {
		background-color: #9e9bf8;
		color: white;
		border: none;

		padding: 7px 8px;
		border-radius: 0;
	}

	.container {
		width: 100%;
		height: 100%;
		display: flex;
        flex-direction: column;
		align-items: center;
	}
	.error {
		color: red;
		margin: 0;
	}

	.login-container {
		width: 40%;

		border-radius: 10px;
		border: 2px solid lightgrey;

		padding: 5px 10px;
	}
	.login-container form {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	@media (max-width: 1000px) {
		.login-container {
			width: 70%;
		}
	}
	@media (max-width: 700px) {
		.login-container {
			width: 90%;
		}
	}
</style>