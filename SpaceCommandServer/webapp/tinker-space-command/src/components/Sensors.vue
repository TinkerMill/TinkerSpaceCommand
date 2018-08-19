<template>
  <div class="hello">
    <h2>Sensors</h2>

    <table>
      <tr :key="sensor.sensorId" v-for="sensor in sensors">
        <td><router-link :to="'/sensor/' + sensor.externalId">Details</router-link></td>
        <td>{{sensor.name}}</td>
      </tr>
    </table>
  </div>
</template>

<script>

import TinkerSpaceCommandApi from '@/services/api/TinkerSpaceCommandApi'

export default {
  name: 'Sensors',
  data () {
    return {
      loading: true,
      sensors: []
    }
  },

  created () {
    TinkerSpaceCommandApi.getSensors().subscribe(sensors => {
      this.sensors = sensors
      console.log(sensors)
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
</style>
