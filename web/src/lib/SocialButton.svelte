<script>
	export let onClick;
</script>

<button on:click={onClick} class="social-button">My Graph</button>

<style>
	.social-button {
        height: 80px;
        width: 120px;
		padding: 10px 20px;
		background-color: #1c86ee;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}

	.social-button:hover {
		background-color: #155a9c;
	}
</style>
