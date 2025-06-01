<style> 
    :root {
        --family: #855daf;
        --friend: #efa639;
        --school: #3d97c7;
        --work: #3067bc;
        --online: #467d3c;
        --romantic: #d64842;
    }
    button {
        height: 100px;
        width: 100px;
        /* set with js */
        /* background-color: #bbb; */ 
        border-radius: 50%;
        display: inline-block;
        transition: transform 0.3s;
    }
    button:hover {
    /* background-color: #1c86ee; */
    transform: scale(1.3);
    }
</style>

<script>
    export let text = "username";
    export let onClick = () => {};
  </script>
  
  <button on:click={onClick}>
    {text}
</button>