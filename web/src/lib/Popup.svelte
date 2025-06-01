<script>
    import { fade, scale } from 'svelte/transition';
    export let show = false;
    export let title = "Popup Title";
    export let content = "Popup content goes here.";
    export let onClose = () => {};
  </script>
  
  {#if show}
    <div class="overlay" on:click={onClose}>
      <div
        class="popup"
        on:click|stopPropagation
        transition:fade={{ duration: 300 }}
        transition:scale={{ duration: 300, start: 0.8 }}
      >
        <button class="close-button" on:click={onClose}>✕</button>
        <h2>{title}</h2>
        <p>{content}</p>
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
      z-index: 1000;
    }
  
    .popup {
      background: white;
      padding: 2rem;
      border-radius: 20px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
      width: 80%;
      max-width: 500px;
      text-align: center;
      position: relative;
    }
  
    .close-button {
      position: absolute;
      top: 0.5rem;
      right: 0.7rem;
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
    }
  </style>