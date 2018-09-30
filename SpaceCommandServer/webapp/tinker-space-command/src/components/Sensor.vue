<template>
  <div class="hello">
    <h2>Sensor: {{sensor.name}}</h2>

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
        <th>Commands</th>
        <th>Channel</th>
        <th>Sensed</th>
        <th>Last Value</th>
      </tr>
      <tr :key="channel.channelId" v-for="channel in sensor.activeChannels">
        <td><router-link :to="'/sensordataplot/' + sensor.externalId + '/' + channel.channelId">Plot</router-link></td>
        <td>{{channel.channelName}}</td>
        <td><router-link :to="'/space/' + channel.sensedItemId">{{ channel.sensedItemName }}</router-link></td>
        <td>{{channel.currentValue}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import TinkerSpaceCommandApi from '@/services/api/TinkerSpaceCommandApi'

export default {
  name: 'Sensor',
  data () {
    return {
      sensorId: this.$route.params.id,
      sensor: null
    }
  },

  created () {
    TinkerSpaceCommandApi.getSensor(this.sensorId).subscribe(sensor => {
      this.sensor = sensor
      console.log(sensor)
    })
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
