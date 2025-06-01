<script lang="ts">
	export let name: string = '';
	export let placeholder: string;
	export let value: string = '';
	export let type: string = 'text';
	export let required: boolean = false;
	export let multiline: boolean = false;

	export let highlight_color: string = '#ccc';
	export let resting_color: string = highlight_color;

	let focused = false;
</script>
<div
	class="input-container"
	style="--input-highlight-color:{highlight_color};--input-resting-color:{resting_color};"
>
	{#if multiline}
		<textarea
			{...{ name, required }}
			placeholder={focused ? '' : placeholder}
			on:focus={() => (focused = true)}
			on:focusout={() => (focused = false)}
			class="input-field"
			bind:value
		/>
	{:else}
		<input
			{...{ type, name, required }}
			placeholder={focused ? '' : placeholder}
			on:focus={() => (focused = true)}
			on:focusout={() => (focused = false)}
			class="input-field"
			bind:value
		/>
	{/if}
	<label class="placeholder" for={name}>{placeholder}</label>
</div>

<style lang="scss">
	.input-container {
		position: relative;
	}

	.input-field {
		width: 100%;
		padding: 0.6em 0.9em;
		border: 1px solid var(--input-resting-color);
		border-radius: 4px;
		transition: border-color 0.3s ease;
		font-size: 1rem;
		resize: none;
		min-height: 2.5em;
	}
	.input-field:focus,
	.input-field:focus-visible,
	.input-field:focus-within {
		outline: 1px solid var(--input-highlight-color);
		+ label {
			color: var(--input-highlight-color);
		}
	}

	.placeholder {
		background-color: white;
		position: absolute;
		top: 0.5rem;
		left: 0.5rem;
		font-size: 0.9rem;
		color: #888;
		transition:
			transform 0.3s ease,
			font-size 0.3s ease;
		transform-origin: top left;
		pointer-events: none;
		display: block;
		visibility: hidden;

		padding: 0px 3px;
	}
	.input-field:focus + .placeholder,
	.input-field:not(:placeholder-shown) + .placeholder {
		transform: translateY(-100%) scale(0.9);
		font-size: 1rem;
		visibility: visible;
	}

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
</style>