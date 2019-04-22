import axios from 'axios';
import {Line, mixins} from 'vue-chartjs'

export default ({
    extends: Line,
    data () {
        return{
            rows:[],
            labels:[]
        }
    },
    // mounted () {
    //     axios.get('http://www.mocky.io/v2/5cae8d853400001716ab6d3a').then(response => {
    //         this.rows = response.data.list.map(list => {
    //           return list.day
  
    //         this.labels = response.data.list.map(list => {
    //           return list.downloads
    //         })
    //         .catch(err => {
    //             this.errorMessage = err.response.data.error
    //             this.showError = true
    //           })
    //         // .then(
    //         //     response =>{
    //         //         console.log(response.data.day[0])
    //         //         this.rows = response.data.day
    //         //         this.labels = response.data.downloads
    //         //         this.setGraph()
    //         //     }
    //         // ) 
    //     this.setGraph()       
    // },
    
  mounted () {
    axios.get('http://www.mocky.io/v2/5cae8d853400001716ab6d3a')
      .then(resp => {
        console.log('resp', resp.data.data)
        this.rows = response.data.list.map(list => {return list.day})
        this.labels = response.data.list.map(list => {return list.downloads})
        this.setUpGraph()
      })
  },
    methods:{
        setGraph(){
            this.renderChart({
                labels:this.labels,
                // labels: ['jan','feb','mar','april','may'],
                datasets:[
                    {
                        label:"my activities",
                        backdropColor: "black",
                        data:this.rows
                        // data:[23,34,45,67,23]
                    }
                ]
                },
                {
                        responsive:true,
                        maintainAspectRatio:false
            })
        }
    }
})
