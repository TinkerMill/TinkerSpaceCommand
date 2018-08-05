<template>
  <div id="app">
    <h1>Tinker Space Command</h1>

    <div class="menu">
      <ul>
        <li><router-link to="/spaces">Spaces</router-link></li>
        <li><router-link to="/sensors">Sensors</router-link></li>
      </ul>
    </div>

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 1em;
}

div.menu > ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

div.menu > ul > li {
  float: left;
}

div.menu > ul > li > a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

div.menu > ul > li > a:hover {
  background-color: #111;
}

</style>
