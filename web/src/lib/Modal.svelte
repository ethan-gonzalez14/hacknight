<script lang="ts">
	import { fade, scale } from 'svelte/transition';

	export let children: any;
	export let visible: boolean;
	export let changeVisible: (val: boolean) => void;

	function handleButtonClick() {
		visible = true;
		changeVisible(true);
	}

	function closePopup() {
		visible = false;
		changeVisible(false);
	}

	function handleSocialClick() {
		console.log('Social button clicked');
	}
</script>

{#if visible}
	<div class="overlay" on:click={closePopup} transition:fade>
		<div class="popup-content" on:click|stopPropagation transition:scale={{ duration: 500 }}>
			{#if children}
				{@render children()}
			{/if}
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
		background: white;
		padding: 20px;
		height: 600px;
		width: 1000px;
		max-height: 90vw;
		max-width: 90vw;
		border-radius: 25px;
		border: 2px solid #000;
		box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
		overflow-y: auto;
	}
</style>
