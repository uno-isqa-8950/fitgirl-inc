window.$ = window.jQuery = require('jquery');
require('bootstrap-sass');
import Vue from 'vue';

import Demo from "./components/Demo.vue";
import ActivityGraph from "./components/ActivityGraph/ActivityGraph.vue"

Vue.component('activity-graph', ActivityGraph)
const app = new Vue({
    el: '.Pre-assessment',
    components: {
        ActivityGraph
    }
});