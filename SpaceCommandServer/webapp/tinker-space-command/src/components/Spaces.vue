<template>
  <div class="hello">
    <h2>Spaces</h2>

    <table>
      <tr :key="space.externalId" v-for="space in spaces">
        <td><router-link :to="'/space/' + space.externalId">Details</router-link></td>
        <td>{{space.name}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import TinkerSpaceCommandApi from '@/services/api/TinkerSpaceCommandApi'
export default {
  name: 'Spaces',
  data () {
    return {
      loading: true,
      spaces: []
    }
  },

  created () {
    TinkerSpaceCommandApi.getSpaces().subscribe(spaces => {
      this.spaces = spaces
      console.log(spaces)
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
