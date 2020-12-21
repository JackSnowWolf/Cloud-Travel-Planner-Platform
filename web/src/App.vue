<template>
  <div id="app">
    <div v-if="$route.name === 'Login' || $route.name === 'About'" id="nav">
      <router-link to="/">Login</router-link> |
      <!-- <router-link to="/about">About</router-link>｜ -->
      <router-link to="/home">Home</router-link>
    </div>
    <!-- <div v-else>
    </div> -->
    <router-view />
  </div>
</template>
<script>
  // import MainNav from "./components/Navbars/MainNav"
  export default {
    // components:{MainNav}
  };
</script>

<style scoped>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #b58860;
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background: #abb8b5;
    background: linear-gradient(180deg, #38576d 0%, #92a9c0 100%);
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #b58860;
  }

  #nav a.router-link-exact-active {
    color: #e7933c;
  }
</style>
