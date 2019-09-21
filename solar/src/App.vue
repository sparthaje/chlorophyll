<template>
    <div id="app">
        <div class="container-fluid">
            <div class="row title-row">
              CEILING
            </div>
            <div class="row button-row">
                <Button msg="Turn Light On" color="rgb(0, 100, 0)"/>
            </div>
        </div>
    </div>
</template>

<script>
    import Button from './components/Button.vue'

    export default {
        name: 'app',
        components: {
            Button
        },
        data: function () {
            return {}
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 20px;
    }

    .button-row {
        padding: 30px;
    }

    @media (prefers-color-scheme: dark) {
        body {
            background-color: #353535;
            color: white;
        }
        #app {
          color: white;
        }
    }
</style>
