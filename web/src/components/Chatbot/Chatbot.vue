<template>
  <el-scrollbar wrap-style="max-height: 300px;">
    <amplify-chatbot :chatbotConfig="chatbotConfig"></amplify-chatbot>
  </el-scrollbar>
</template>
<script>
  // import { AmplifyEventBus } from "aws-amplify-vue";
  // import { Auth } from "aws-amplify";
  import { Interactions } from "aws-amplify";
  export default {
    name: "ChatbotComponent",
    data() {
      return {
        chatbotConfig: {
          bot: "ScheduleBot_first_dev",
          clearComplete: true,
          botTitle: "Helper",
        },
      };
    },
    methods: {
      initChatbot() {
        Interactions.onComplete("ScheduleBot_first_dev", this.handleComplete);
      },
      handleComplete(err, confirmation) {
        // console.log("ppprint", JSON.stringify(confirmation));
        if (err) {
          alert(err);
          return;
        }
        // alert(JSON.stringify(confirmation));
        console.log("chatComplete", confirmation);
        this.$emit("chatComplete", confirmation);
        // AmplifyEventBus.$emit("chatComplete");
      },
    },
    mounted() {
      this.initChatbot();
    },
  };
</script>
<style scoped>
  .chatbot {
    max-height: 200px;
  }
</style>
