<template>
  <div>
    <basic-vue-chat :new-message="message" />
  </div>
</template>
<script>
  import BasicVueChat from "basic-vue-chat";
  export default {
    data() {
      return {
        message: {
          id: 0,
          author: "Person",
          //   imageUrl: "http://path/to/image",
          image: "",
          contents: "hi there",
          date: "16:30",
        },
      };
    },
    components: {
      BasicVueChat,
    },
  };
</script>
