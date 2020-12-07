<template>
  <div class="Login">
    <amplify-authenticator>   
    </amplify-authenticator>
    
    <amplify-sign-out></amplify-sign-out>
  </div>
</template>

<script>
// @ is an alias to /src
import { AmplifyEventBus } from 'aws-amplify-vue';
import { Auth } from 'aws-amplify';

export default {
  mounted() {
    AmplifyEventBus.$on("authState", info => {
      window.sessionStorage.setItem("authState",info)
      console.log("auth", window.sessionStorage.getItem("authState"));
      if (info === "signedIn") {
        console.log(Auth.currentSession())
        this.$router.push("about");
      }
    });
  },
  name: "login",
  components: {}
};
</script>
