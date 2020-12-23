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
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    name: "app",
    components: { MainNav },
    data() {
      return {
        uuid: "",
        userId: "",
        scheduleId: "",
        existuserIds: "",
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
            name: "Helper",
            imageUrl: "https://proj-for-attraction-photos.s3.amazonaws.com/avator-info.png",
          },
        ], // the list of all the participant of the conversation. `name` is the user name, `id` is used to establish the author of a message, `imageUrl` is supposed to be the user avatar.
        titleImageUrl: "https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png",
        messageList: [{ type: "text", author: `user2`, data: { text: `Welcome to the online chat page!` } }], // the list of the messages to show, can be paginated and adjusted dynamically
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
            // console.log(eventData);
            let newMessage = eventData.value.data.subscribeToNewMessage;
            // console.log(newMessage);
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
      async createUserConversation() {
        // console.log("create converstaion!", this.uuid);
        await API.graphql({
          query: mutations.createUserConversations,
          variables: { conversationId: this.scheduleId, userId: this.uuid },
        }).then(() => {});
      },
      userPromise(user) {
        this.uuid = user.username;
        this.user = user;
        this.userId = "user-" + user.username;
        this.createUserConversation();
        return this.userId;
      },
      dataInit(user) {
        this.initDataTable(this.scheduleId, user)
          .then(this.ParseData)
          .then(this.PromiseParticipants);
      },

      ParseData(data) {
        // console.log("table", data);
        var existuserIds = [];
        existuserIds = [...existuserIds, data.ownerId];
        for (var i = 0; i < data.editorIds.length; i++) {
          existuserIds = [...existuserIds, data.editorIds[i]];
        }
        this.existuserIds = existuserIds;
        console.log(existuserIds);
      },

      PromiseInit() {
        this.scheduleId = this.$route.params.scheduleId;
        console.log("schedule", this.scheduleId);
        var user = Auth.currentAuthenticatedUser();
        user.then(this.userPromise).then(this.dataInit);
      },
      async PromiseParticipants() {
        await API.graphql({
          query: queries.allUser,
        })
          .then((resp) => {
            console.log("", resp);
          })
          .catch((err) => {
            console.log(err);
            var allUser = err.data.allUser;
            // console.log(this.participants);
            // console.log("allUser", allUser);
            for (var i = 0; i < allUser.length; i++) {
              var getParticipant = this.ParseParticipant(allUser[i]);
              if (getParticipant.id) {
                this.participants = [...this.participants, getParticipant];
              }
            }
          });
        // console.log("user", data.data);
      },
      ParseParticipant(newParticipant) {
        var participant = {};
        if (this.existuserIds.includes("user-" + newParticipant.id)) {
          participant = { id: newParticipant.id, name: newParticipant.username };
        }
        return participant;
      },
      async initDataTable(scheduleId, userId) {
        console.log("init Preselect table", this.scheduleId, this.userId);
        const session = await Auth.currentSession();
        this.tableData = [];
        this.attracationIdList = [];
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: scheduleId,
        };
        var pathTemplate = "/schedule/{scheduleId}";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: userId,
          },
        };
        var body = {};

        return new Promise(function(resolve, reject) {
          apigClient
            .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then((response) => {
              if (response.status === 200) {
                // console.log("Get resp", response.data);
                resolve(response.data);
              }
            })
            .catch((err) => {
              console.log(err);
              reject(err);
            });
        });
      },
    },
    mounted() {
      // this.PromiseParticipants();
    },

    created() {
      this.PromiseInit();
      this.subscribe();
      // this.createUserConversation();
    },
  };
</script>
