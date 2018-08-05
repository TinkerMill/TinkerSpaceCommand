<template>
  <div class="hello">
    <h2>Space: {{space.name}}</h2>

    <p>{{ space.externalId }}</p>
    <p v-if="space.description">{{ space.description }}</p>
  </div>
</template>

<script>
import TinkerSpaceCommandApi from '@/services/api/TinkerSpaceCommandApi'

export default {
  name: 'Space',
  data () {
    return {
      spaceId: this.$route.params.id,
      space: null
      
    }
  },

  created () {
    TinkerSpaceCommandApi.getSpace(this.spaceId).subscribe(space => {
      this.space = space
      console.log(space)
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
