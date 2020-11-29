<template>
  <div class="home">
    <amplify-authenticator>
      
    </amplify-authenticator>
    
    <amplify-sign-out></amplify-sign-out>
  </div>
</template>

<script>
// @ is an alias to /src
import { AmplifyEventBus } from 'aws-amplify-vue';

export default {
  mounted() {
    AmplifyEventBus.$on("authState", info => {
      console.log("auth", info);
      if (info === "signedIn") {
        this.$router.push("about");
      }
    });
  },
  name: "home",
  components: {}
};
</script>
