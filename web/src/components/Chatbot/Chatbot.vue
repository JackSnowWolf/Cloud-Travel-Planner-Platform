<template>
  <el-scrollbar wrap-style="max-height: 300px;">
    <amplify-chatbot :chatbotConfig="chatbotConfig"></amplify-chatbot>
  </el-scrollbar>
</template>
<script>
  import { AmplifyEventBus } from "aws-amplify-vue";
  // import { Auth } from "aws-amplify";
  import { Interactions } from "aws-amplify";
  export default {
    name: "ChatbotComponent",
    data() {
      return {
        chatbotConfig: {
          bot: "ScheduleBot_first_dev",
          clearComplete: false,
          botTitle: "Helper",
        },
      };
    },
    methods: {
      initChatbot() {
        Interactions.onComplete("ScheduleBot_first_dev", this.handleComplete);
      },
      handleComplete(err, confirmation) {
        console.log("ppprint", JSON.stringify(confirmation));
        if (err) {
          alert(err);
          return;
        }
        alert(JSON.stringify(confirmation));
        console.log("chatComplete", confirmation);
        AmplifyEventBus.$emit("chatComplete", this.options.botTitle);
      },
    },
    mounted() {
      this.initChatbot();
    },
  };
</script>
<style scoped>
  .chatbot {
    min-height: 100px;
    max-height: 200px;
  }
</style>
