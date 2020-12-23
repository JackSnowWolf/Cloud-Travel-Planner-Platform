<template>
  <div class="PreselectPage">
    <MainNav />
    <!-- <Slider /> -->
    <div class="main">
      <beautiful-chat
        :participants="participants"
        :titleImageUrl="titleImageUrl"
        :onMessageWasSent="onMessageWasSent"
        :messageList="messageList"
        :newMessagesCount="newMessagesCount"
        :isOpen="isChatOpen"
        :close="closeChat"
        :open="openChat"
        :showEmoji="false"
        :showFile="false"
        :showEdition="true"
        :showDeletion="true"
        :showTypingIndicator="showTypingIndicator"
        :showLauncher="true"
        :showCloseButton="true"
        :colors="colors"
        :alwaysScrollToBottom="alwaysScrollToBottom"
        :messageStyling="messageStyling"
        @onType="handleOnType"
        @edit="editMessage"
      />
    </div>
  </div>
</template>
<script>
  import { API } from "aws-amplify";
  import { Auth } from "aws-amplify";
  // import Slider from "../components/Navbars/Slider";
  import MainNav from "../components/Navbars/MainNav";
  import * as queries from "@/graphql/queries";
  import * as subscriptions from "@/graphql/subscriptions";
  import * as mutations from "@/graphql/mutations";
  export default {
    name: "app",
    components: { MainNav },
    data() {
      return {
        uuid: "",
        scheduleId: "",
        icons: {
          open: {
            // img: OpenIcon,
            name: "default",
          },
          close: {
            // img: CloseIcon,
            name: "default",
          },
          file: {
            // img: FileIcon,
            name: "default",
          },
          closeSvg: {
            // img: CloseIconSvg,
            name: "default",
          },
        },
        participants: [
          // {
          //   id: "user1",
          //   name: "Matteo",
          //   imageUrl: "https://avatars3.githubusercontent.com/u/1915989?s=230&v=4",
          // },
          {
            id: "user2",
            name: "Your Friends",
            imageUrl: "https://avatars3.githubusercontent.com/u/37018832?s=200&v=4",
          },
        ], // the list of all the participant of the conversation. `name` is the user name, `id` is used to establish the author of a message, `imageUrl` is supposed to be the user avatar.
        titleImageUrl: "https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png",
        messageList: [{ type: "text", author: `user2`, data: { text: `Let's chat!` } }], // the list of the messages to show, can be paginated and adjusted dynamically
        newMessagesCount: 0,
        isChatOpen: false, // to determine whether the chat window should be open or closed
        showTypingIndicator: "", // when set to a value matching the participant.id it shows the typing indicator for the specific user
        colors: {
          header: {
            bg: "#4e8cff",
            text: "#ffffff",
          },
          launcher: {
            bg: "#4e8cff",
          },
          messageList: {
            bg: "#ffffff",
          },
          sentMessage: {
            bg: "#4e8cff",
            text: "#ffffff",
          },
          receivedMessage: {
            bg: "#eaeaea",
            text: "#222222",
          },
          userInput: {
            bg: "#f4f7f9",
            text: "#565867",
          },
        }, // specifies the color scheme for the component
        alwaysScrollToBottom: false, // when set to true always scrolls the chat to the bottom when new events are in (new message, user starts typing...)
        messageStyling: true, // enables *bold* /emph/ _underline_ and such (more info at github.com/mattezza/msgdown)
      };
    },
    methods: {
      sendMessage(text) {
        if (text.length > 0) {
          // this.subscribe();
          this.newMessagesCount = this.isChatOpen ? this.newMessagesCount : this.newMessagesCount + 1;
          this.onMessageWasSent({ author: "support", type: "text", data: { text } });
        }
      },
      onMessageWasSent(message) {
        // called when the user sends a message
        // this.subscribe();
        this.createMessage(message.data.text);
        // console.log("onmess", message);
        // this.messageList = [...this.messageList, message];
      },
      openChat() {
        // called when the user clicks on the fab button to open the chat
        this.isChatOpen = true;
        this.newMessagesCount = 0;
      },
      closeChat() {
        // called when the user clicks on the botton to close the chat
        this.isChatOpen = false;
      },
      handleScrollToTop() {
        // called when the user scrolls message list to top
        // leverage pagination for loading another page of messages
      },
      handleOnType() {
        console.log("Emit typing event");
      },
      editMessage(message) {
        const m = this.messageList.find((m) => m.id === message.id);
        m.isEdited = true;
        m.data.text = message.data.text;
      },
      praseSubmsgToMsg(newMessage) {
        var message = {};
        if (newMessage.sender === this.uuid) {
          message = { type: "text", author: "me", data: { text: newMessage.content } };
        } else {
          message = { type: "text", author: newMessage.sender, data: { text: newMessage.content } };
        }
        return message;
      },
      subscribe() {
        API.graphql({ query: subscriptions.subscribeToNewMessage, variables: { conversationId: this.scheduleId } }).subscribe({
          next: (eventData) => {
            console.log(eventData);
            let newMessage = eventData.value.data.subscribeToNewMessage;
            console.log(newMessage);
            let message = this.praseSubmsgToMsg(newMessage);
            this.messageList = [...this.messageList, message];
          },
        });
      },
      async createMessage(message) {
        console.log("create");
        await API.graphql({
          query: mutations.createMessage,
          variables: { conversationId: this.scheduleId, id: "11122", createdAt: new Date(), content: message },
        }).then(() => {});
      },
      PromiseInit() {
        this.scheduleId = this.$route.params.scheduleId;
        console.log("schedule", this.scheduleId);
        Auth.currentAuthenticatedUser().then((user) => {
          this.uuid = user.username;
          console.log(this.uuid);
        });
      },
      async PromiseParticipants() {
        await API.graphql({
          query: queries.allUser,
        })
          .then((resp) => {
            console.log("user", resp);
          })
          .catch((err) => {
            console.log(err);
          });
        // console.log("user", data.data);
      },
    },
    mounted() {
      this.PromiseParticipants();
    },

    created() {
      this.PromiseInit();
      this.subscribe();
    },
  };
</script>
