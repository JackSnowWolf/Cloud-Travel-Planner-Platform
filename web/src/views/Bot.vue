<template>
  <div id="app">
    <amplify-chatbot :chatbotConfig="chatbotConfig"></amplify-chatbot>
  </div>
</template>

<script>
import { Interactions } from "aws-amplify";
export default {
  data: () => ({
    chatbotConfig: {
      bot: "ScheduleBot_first_dev",
      clearComplete: false,
    },
  }),
  mounted() {
    Interactions.onComplete("ScheduleBot_first_dev", this.handleComplete);
  },
  methods: {
    handleComplete(err, confirmation) {
      if (err) {
        alert(err);
        return;
      }
      alert(JSON.stringify(confirmation));
    },
  },
};
</script>
