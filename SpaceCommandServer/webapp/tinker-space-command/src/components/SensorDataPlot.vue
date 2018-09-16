<template>
  <div class="hello">
    <h2>Sensor: {{sensor.name}}, Channel: {{channelId}}</h2>
{{dateStart}} {{dateEnd}}
    <p v-if="sensor.description">{{ sensor.description }}</p>
    <table>
      <tr>
        <th>External ID</th>
        <td>{{ sensor.externalId }}</td>
      </tr>
      <tr>
        <th>Online</th>
	<td>{{ sensor.online }}</td>
      </tr>
      <tr>
        <th>Last Value Received</th>
	<td>{{ sensor.timeLastValueReceived }}</td>
      </tr>
      <tr>
        <th>Last Heartbeat Received</th>
	<td>{{ sensor.timeLastHeartbeatReceived }}</td>
      </tr>
    </table>

    <h3>Channels</h3>
    
    <table>
      <tr>
        <th>Channel</th>
	<th>Sensed</th>
        <th>Last Value</th>
      </tr>
      <tr :key="channel.channelId" v-for="channel in sensor.activeChannels">
        <td>{{channel.channelName}}</td>
        <td><router-link :to="'/space/' + channel.sensedItemId">{{ channel.sensedItemName }}</router-link></td>
        <td>{{channel.currentValue}}</td>
      </tr>
    </table>

    <div>
      <date-picker v-model="dateStart" lang="en" format="YYYY-MM-DD" ></date-picker>
      <date-picker v-model="dateEnd" lang="en" format="YYYY-MM-DD"></date-picker>
    </div>
    <div>
      <button v-on:click="plot(0)"  type="button" :disabled="disabled">Plot</button>
    </div>
    <div id='chart'></div>
  </div>
</template>

<script>
import TinkerSpaceCommandApi from '@/services/api/TinkerSpaceCommandApi'
import DatePicker from 'vue2-datepicker'
import plotly from 'plotly.js'
import moment from 'moment'

export default {
  name: 'SensorDataPlot',
  components: { DatePicker },
  data () {
    return {
      sensorId: this.$route.params.id,
      channelId: this.$route.params.channel,
      sensor: null,
      dateStart: '',
      dateEnd: '',
      disabled: false
    }
  },

  created () {
    TinkerSpaceCommandApi.getSensor(this.sensorId).subscribe(sensor => {
      this.sensor = sensor
      console.log(sensor)
    })
  },

  methods: {
    plot (arg) {
      var startDate = moment(this.dateStart).format('YYYY-MM-DD');
      var endDate = moment(this.dateEnd).format('YYYY-MM-DD');
      TinkerSpaceCommandApi.getSensorChannelDataQuery(this.sensorId, this.channelId, startDate, endDate).subscribe(data => {
        console.log(data);
        this.drawPlot(data);
      });
    },

    drawPlot(dataResult) {
      var values = dataResult.data.value;
      var dateTimes = dataResult.data.dateTime;
      
      var trace1 = {
        x: dateTimes,
        y: values,
        mode: 'markers',
        name: 'data',
        type: 'scatter',
      };

      var data = [trace1];

      var layout = {
        hovermode: 'closest',
        shapes: [
          {
            fillcolor: 'rgb(44, 160, 44)',
            line: {
              color: 'rgba(68, 68, 68, 100)',
              width: 0
            },
            opacity: 0.3,
            type: 'rectangle',
            x0: 0,
            x1: 1,
            xref: 'paper',
            y0: 70,
            y1: 81,
            yref: 'y'
          }
        ],
        showlegend: true,
        xaxis: {
          autorange: true,
          range: [dateTimes[0], dateTimes[dateTimes.length - 1]],
          title: 'C',
          type: 'category'
        },
        yaxis: {
          autorange: false,
          range: [60, 95],
          title: 'data',
          type: 'linear'
        }
      };

      var element = document.getElementById('chart');
      plotly.plot(element, data, layout);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
th {
  text-align: left;
  padding-right: 1em;
}

</style>
