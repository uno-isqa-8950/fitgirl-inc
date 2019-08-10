<template src="./ActivityGraph.html">
<bar-chart
    :width="500"
    :height="300"
    :labels="['Jan', 'Feb', 'Mar', 'Apr', 'May']"
    :datasets="[1,2,3,4,5]"
  ></bar-chart>
</template>
<script>
import LineChart from './LineChart';
import BarChart from './BarChart';
export default {
    components:{
        'line-chart':LineChart,
        'bar-chart':BarChart,

    },
    data () {
      return {
        downloads: [],
        labels: []
      }
    }
}
</script>
