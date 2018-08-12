<template>
  <div class="hello">
    <h2>Sensor: {{sensor.name}}</h2>

    <p>{{ sensor.externalId }}</p>
    <p v-if="sensor.description">{{ sensor.description }}</p>
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
</style>
