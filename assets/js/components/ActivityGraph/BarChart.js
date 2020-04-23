import {Bar} from 'vue-chartjs'
import axios from 'axios';

export default ({
    extends: Bar,
        props: {
            url: String,
        },
  mounted () {
    console.log("url: "+this.url);
    axios.get(this.url)
      .then(response => {
        this.rows = response.data.downloads.map(downloads => downloads.downloads)
        this.labels = response.data.downloads.map(downloads => downloads.day)
        this.setGraph() 
      })
  },
  data () {
      return{
          rows:[],
          labels:[],

      }
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
