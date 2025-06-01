<script>
	export let label = "Click Me";
	export let type = "button";
	export let onClick = null;

	export let width = "120px";
	export let height = "80px";
	export let fontSize = "17px";
</script>

<button
	type={type}
	on:click={onClick}
	class="social-button"
	style="width: {width}; height: {height}; font-size: {fontSize};"
>
	<slot>{label}</slot>
</button>

<style>
	.social-button {
		padding: 10px 20px;
		background-color: #9e9bf8;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: transform 0.3s;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.social-button:hover {
		background-color: #706bf2;
		transform: scale(0.95);
	}
</style>
