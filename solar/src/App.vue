<template>
    <div id="app">
        <div class="header">Dashboard</div>
        <div class="container-fluid">
            <div v-for="location in Object.keys(state)" class="location">
                <div class="row title">
                    {{location}}
                </div>
                <div v-for="fixture in Object.keys(state[location])" class="row button-row" v-on:click="updateFirebase(location, fixture, !state[location][fixture])">
                    <Button v-if="state[location][fixture]" v-bind:msg="fixture" color="rgb(69, 158, 87)"/>
                    <Button v-else v-bind:msg="fixture" color="rgb(188, 69, 97)"/>
                </div>
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
            listenFirebase: function (snapshot) {
                this.$data.state = snapshot.val()
            },
        },
        mounted: function () {
            // Initialize Firebase
            firebase.initializeApp(firebaseConfig);
            firebase.auth().signInWithEmailAndPassword(process.env.VUE_APP_EMAIL, process.env.VUE_APP_PASSWORD).catch();

            const database = firebase.database().ref('/state');
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
        color: #2c3e50;
        margin-top: 20px;

        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;

        font-size: 60px;
    }

    .header {
        margin-left: 40px;
        margin-bottom: 10px;
    }

    .location {
        background-color: rgb(235, 235, 235);
        border-radius: 10px;
        padding: 30px;
    }

    .title {
        font-size: 30px;
        padding-left: 20px;
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

        .location {
            background-color: #454545;
        }
    }
</style>
