<template>
  <el-row>
    <el-col :span="6" :offset="4" class="Banner">
      <LoginBanner />
    </el-col>
    <el-col :span="8" :offset="2" class="Login">
      <amplify-authenticator> </amplify-authenticator>
      <amplify-sign-out></amplify-sign-out>
    </el-col>
  </el-row>
</template>

<script>
  // @ is an alias to /src
  import { AmplifyEventBus } from "aws-amplify-vue";
  import { Auth } from "aws-amplify";
  import LoginBanner from "../components/LoginBanner";

  export default {
    data() {
      return {
        authStatus: "",
      };
    },
    mounted() {
      AmplifyEventBus.$on("authState", (info) => {
        window.sessionStorage.setItem("authState", info);
        console.log("auth", window.sessionStorage.getItem("authState"));
        this.authStatus = window.sessionStorage.getItem("authState");
        if (info === "signedIn") {
          console.log(Auth.currentSession());
          this.$router.push("home");
        }
      });
    },
    name: "login",
    components: { LoginBanner },
  };
</script>
<style>
  .banner {
    margin-top: 20px;
  }
</style>
