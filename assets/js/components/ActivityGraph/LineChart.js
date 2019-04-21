
import axios from 'axios';
import {Line, mixins} from 'vue-chartjs';

export default ({
    extends: Line,
        props: {
            url: String,
        },
  mounted () {
    console.log("url: "+this.url);
    axios.get(this.url)
      .then(response => {
        // this.rows = response.data.downloads.map(downloads => downloads.downloads)
        // this.labels = response.data.downloads.map(downloads => downloads.day)
        this.rows = response.data.useractivity.map(useractivity => useractivity.activity)
        this.labels = response.data.useractivity.map(useractivity => useractivity.week)
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
