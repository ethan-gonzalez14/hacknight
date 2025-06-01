<script>
    import Graph from "$lib/Graph.svelte";
    import Node from '$lib/Node.svelte';
	import SocialButton from '$lib/SocialButton.svelte';
    import { fade, scale } from 'svelte/transition';


	let visible = false;

	function handleButtonClick() {
		visible = true;
	}

	function closePopup() {
		visible = false;
	}

	function handleSocialClick() {
    alert("Social Button clicked!");
  	}
</script>

<Graph />

{#if visible}
{console.log('Visible is true')}
	<div class="overlay" on:click={closePopup} transition:fade>
		<div class="popup-content" on:click|stopPropagation transition:scale={{ duration: 500 }}>
			<img src="/your-image.jpg" alt="Popup Image" class="popup-image" />
			<div class="popup-text">
				<h2>Popup Title</h2>
				<p>Popup content goes here.</p>
			</div>
			<SocialButton on:click={handleSocialClick} />
		</div>
	</div>
{/if}

<style>
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 5;
	}

	.popup-content {
	display: flex;
	background: white;
	padding: 20px;
	height: 400px;
	width: 600px;
	max-width: 90vw;
	border-radius: 25px;
	border: 2px solid #000;
	box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
	overflow: hidden;
	}

	.popup-image {
		width: 200px;
		height: 100%;
		object-fit: cover;
		border-radius: 20px 0 0 20px;
	}

	.popup-text {
		flex: 1;
		padding-left: 20px;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

    :global(body) {
        margin: 0;
        background-image: url('/space.webp');
        background-size: cover;
        font-family: sans-serif;
    }

	view-button {
        height: 100px;
        width: 100px;
        background-color: #bbb;
        border-radius: 90%;
        display: inline-block;
        transition: transform 0.3s;
    }
    view-button:hover {
        background-color: #1c86ee;
        transform: scale(1.3);
    }
</style>
