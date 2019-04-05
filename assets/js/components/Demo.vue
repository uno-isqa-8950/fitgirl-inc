<template>
    <div id="app">
        <div id="content">
            <form @submit.prevent="submitData">
                <label>Title</label>
                <input type="text" v-model="formData.title"/>
                <label>Contentss</label>
                <textarea v-model="formData.content"></textarea>
                <br/>
                <button type="submit">Submit</button>
                <p>Weekly points Report!</p>
                <canvas ref="chart"></canvas>
            </form>
        </div>
    </div>
</template>

<script>
    import Chart from 'chart.js';
    import api from '../../../api/index'
    export default {
        name: 'app',
        data() {
            return {
                msg: 'Welcome!',
                formData: {
                    title: '',
                    content: ''
                }
            }
        },
        methods: {
            submitData () {
                api.fetchData('get', null, this.formData).then(res =>{
                    this.msg = 'Saved'
                }).catch((e) => {
                    this.msg = e.response
                })
            }
        },
        mounted() {
            var chart = this.$refs.chart;
            var ctx = chart.getContext("2d");
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    // labels: [],
                    datasets: [{
                        label: 'Total points',
                        data: [12, 19, 3, 5, 2, 3, 4, 7, 2, 8, 12, 9],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
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
        margin-top: 60px;
    }
    #content {
        margin: auto;
        width: 1024px;
        background-color: #FFFFFF;
        padding: 20px;
    }
</style>