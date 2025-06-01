<script>
	import Node from '$lib/Node.svelte';

	let visible = false;

	function handleButtonClick() {
		visible = !visible;
	}

	function closePopup() {
		visible = false;
	}
</script>

<Node onClick={handleButtonClick} />

{#if visible}
	<!-- The popup is the full-screen overlay -->
	<div class="popup" on:click={closePopup}>
		<!-- Inner content box -->
		<div class="popup-content" on:click|stopPropagation>
			<span>Popup content!</span>
		</div>
	</div>
{/if}

<style>
	.popup {
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
		
		/* animation */
		animation: fadeInOverlay 0.3s ease forwards;
	}

	.popup-content {
		background: white;
		padding: 20px;
		width: 600px;
		max-width: 90vw;
		border-radius: 25px;
		border: 2px solid #000;
		box-shadow: 0 0 15px rgba(0,0,0,0.4);

		/* scale animation */
		transform: scale(0.8);
		opacity: 0;
		animation: scaleIn 0.3s ease forwards;
	}

	@keyframes fadeInOverlay {
		from { background-color: rgba(0,0,0,0); }
		to { background-color: rgba(0,0,0,0.5); }
	}

	@keyframes scaleIn {
		from {
			transform: scale(0.8);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
