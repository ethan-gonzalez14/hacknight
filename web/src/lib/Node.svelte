<style> 
    button {
        height: 100px;
        width: 100px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: transform 0.3s;
    }
    button:hover {
    background-color: #1c86ee;
    transform: scale(1.3);
    }
</style>

<script>
    export let text = "Click me";
    export let onClick = () => {};
  </script>
  
  <button on:click={onClick}>
    {text}
</button>