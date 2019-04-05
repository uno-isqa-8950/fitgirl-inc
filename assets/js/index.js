window.$ = window.jQuery = require('jquery');
require('bootstrap-sass');
import Vue from 'vue'
import axios from 'axios'

import Demo from "./components/Demo.vue";

const app = new Vue({
    el: '#app',
    beforeCreate () {
      Vue.prototype.$http = axios
      axios.defaults.xsrfHeaderName = 'X-CSRFToken'
      axios.defaults.xsrfCookieName = 'csrftoken'
    },
    components: {
        Demo
    }
});