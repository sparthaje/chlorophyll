<template>
    <div class="col-12 col-lg-6 ml-auto mr-auto button" v-bind:style="{ 'background-color': color }">
        {{msg}}
    </div>
</template>

<script>
    export default {
        name: "Button.vue",
        props: {
            msg: String,
            color: String
        }
    }
</script>

<style scoped>
    .button {
        border-radius: 10px;
        background-color: black;
        color: white;
        font-size: 25px;
        text-align: center;
    }

    .col-12 {
        padding: 40px;
    }
</style>