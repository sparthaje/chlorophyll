import Vue from 'vue'
import App from './App.vue'

import * as firebase from "firebase/app";
require('firebase/auth');
require('firebase/database');

import firebaseConfig from '../secret.json'

Vue.config.productionTip = false;

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.auth().signInWithEmailAndPassword(process.env.VUE_APP_EMAIL, process.env.VUE_APP_PASSWORD).catch();

const database = firebase.database();
const ref = database.ref('/state').child('/CEILING').child('/LIGHT');
ref.set(true).then();

new Vue({
  render: h => h(App),
}).$mount('#app');
