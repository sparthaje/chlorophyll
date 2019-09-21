<template>
    <div id="app">
        <div class="container-fluid">
            <div class="row title-row">
                CEILING
            </div>
            <div class="row button-row" v-on:click="updateFirebase('CEILING', 'LIGHT', true)">
                <Button msg="Turn Light On" color="rgb(0, 100, 0)"/>
            </div>
        </div>
    </div>
</template>

<script>
    import * as firebase from "firebase/app";
    import firebaseConfig from '../secret.json'

    require('firebase/auth');
    require('firebase/database');

    import Button from './components/Button.vue'

    export default {
        name: 'app',
        components: {
            Button
        },
        data: function () {
            return {
                database: '',
                state: {}
            }
        },
        methods: {
            updateFirebase: function (location, fixture, value) {
                const ref = this.$data.database.child('/' + location).child('/' + fixture);
                ref.set(value).then();
            },
            listenFirebase: function(snapshot) {
              this.$data.state = snapshot.val()
            },
        },
        mounted: function () {
            // Initialize Firebase
            firebase.initializeApp(firebaseConfig);
            firebase.auth().signInWithEmailAndPassword(process.env.VUE_APP_EMAIL, process.env.VUE_APP_PASSWORD).catch();

            var database = firebase.database().ref('/state');
            database.on('value', this.listenFirebase);

            this.$data.database = database
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
