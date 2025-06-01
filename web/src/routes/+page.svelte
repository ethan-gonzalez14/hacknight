<script lang="ts">
    import { add_relationship }  from '$lib/query-server';
    import Graph from "$lib/Graph.svelte";
    import Modal from "$lib/Modal.svelte";
	import Input from '$lib/Input.svelte';
	import { text } from '@sveltejs/kit';
	import SocialButton from '$lib/SocialButton.svelte';

    let code_modal = $state(false);
    function get_code_modal() {
        console.log("HEY... WTF")
        code_modal = true;
    }

    let code = "";
    let relationship = "";
    let error = $state("");
    let message = $state("");
    let how_met = $state("");
    async function find() {
        let processed = relationship.toLowerCase();
        switch (processed) {
            case "best_friends":
            case "friends":
            case "family":
            case "work":
            case "married":
            case "romantic":
                break;
            default:
                error = "Please select a valid relationship type.";
                return;
        }
        if (code == "") {
            error = "Please enter a code.";
            return;
        }
        if (how_met.length > 10) {
            console.log(how_met.length);
            error = "Please enter a valid 'How did you meet?' description. It should be 10 characters or less.";
            return;
        }
        if (!/[0-9]+/.test(code)) {
            error = "Please enter a valid code. It should only contain numbers.";
            return;
        }

        const add = await add_relationship(data.username, code, processed, how_met);
        if (add.error) {
            switch (add.error) {
                case "CODE_DOES_NOT_EXIST":
                    error = "The code you entered does not exist.";
                    break;
                case "ALREADY_CONNECTED":
                    error = "You're already friends with this person! See if you can find them in the graph 😉.";
                    break;
                case "USER_ALREADY_HAS_BEST_FRIEND":
                    error = "Sorry, honey, you're taken! You've already got a best friend. Don't let your second-best know, though 😉";
                    break;
                case "OTHER_ALREADY_HAS_BEST_FRIEND":
                    error = "Oof, that's gotta sting! Looks like you're not as special as you thought you were. Maybe try being more interesting next time?";
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
<!-- <button class="add" onclick={get_code_modal}>
    &plus;
</button> -->
<SocialButton onClick={get_code_modal} width="60x" height="60x" fontSize="40px" className="add">
	&plus;
</SocialButton>
<SocialButton width="100px" height="10%" type="search">
    <a href="/search" class="material-symbols-outlined">search</a>
</SocialButton>

<form action="?/logout" method="POST">
    <!-- <button class="logout" type="submit">Log Out</button> -->
    <SocialButton label="Log Out" width="100px" height="10%" type="submit"></SocialButton>
</form>
</div>
<Modal visible={code_modal} changeVisible={(val: boolean) => code_modal = val} >
    <h2>Friend Codes</h2>

    <br/>

    <Input type="text" name="friendCode" bind:value={code} placeholder="Enter a friend's code here" multiline={false} />

    <br/>

    <input placeholder="And your relationship here" list="relationship" name="relationship" class="datalist-input" bind:value={relationship} />
    <datalist id="relationship">
    <br/>
    <Input type="text" name="friendCode" bind:value={code} placeholder="Enter a friend's code here" multiline={false} />
    <br/>
    <input placeholder="And your relationship here" list="relationship" name="relationship" bind:value={relationship} />
    <datalist id="relationship" >
        <option value="Friends">Friends 😎</option>
        <option value="Best_Friends">BFFS 😊</option>
        <option value="Family">Family 🥰</option>
        <option value="Romantic">Romantic 💋</option>
        <option value="Married">Married 🤱</option>
        <option value="Work">Profressional 💼</option>
    </datalist>
    <br/> <br/>

    <input type="text" placeholder="How did you two meet? (10 chars)" bind:value={how_met} class="context">

    <br/><br/>

    <SocialButton class="find" label="Find Your Friend" onClick={find} width="100%" />
    
    <SocialButton class="find" label="Find Your Friend" onClick={find} width="100%" height="60px"/>
    <!-- <button class="find" onclick={find}>Find Your Friend</button> -->
    {#if error}
    <p class="red">{error}</p>
    {/if}
    {#if message}
    <p class="yellow">{message}</p>
    {/if}
</Modal>

<Graph cachedPeople={[]} center={data.username} />

<style lang="scss">
    .datalist-input,
    .context {
        width: 100%;
    }
    .red {
        color: red;
    }

    .modal {
        width: 100%;
        height: 100%;
        input, button {
            width: 100%;
        }
    }

    .add {
        aspect-ratio: 1 / 1;
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

    .input-button-row {
	display: flex;
	gap: 12px;
	align-items: center;
    }

    h2 {
    font-family: "Titillium Web", sans-serif;
    font-weight: 700;
    font-style: normal;
    font-size: 30px;
    }
    
</style>

{:else}

<style>
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@200;300;400;600;700;900&family=WDXL+Lubrifont+TC&display=swap');

.wdxl-lubrifont-tc-regular {
  font-family: "WDXL Lubrifont TC", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.titillium-web-regular {
  font-family: "Titillium Web", sans-serif;
  font-weight: 400;
  font-style: normal;
}

body {
  background-image: url('/background-resized.png');
  color: white;
  font-family: "Titillium Web", sans-serif;
}

input {
    color: black;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.8s ease-out both;
}
</style>
<div class="container">
    <h1 class="titillium-web-regular fade-in-up">Gain personal <span style="text-decoration: underline;">and</span> professional contacts, all in one place.</h1>

    <p class="titillium-web-regular fade-in-up" style="animation-delay: 1s; margin-bottom: 24px;">MyWeb makes it easy to remember who's who. And don't worry about your boss finding out your secret nightlife
        drug dealing or having a dance fiesta — control who sees your public and private bios.
    </p>

    <h1 class="wdxl-lubrifont-tc-regular" style="margin-bottom: 24px;">Enough Talk. Get Talking.</h1>
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
		align-items: left;
	}
	.error {
		color: red;
		margin: 0;
	}

	.login-container {
		width: 25%;

		border-radius: 10px;
		border: 2px solid lightgrey;

		padding: 5px 10px;
        background-color: #171717;
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