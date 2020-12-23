<template>
  <el-container class="HomePage">
    <MainNav />
    <div class="main">
      <h1 class="title">
        Almost 100,000 people have used our planner for their next trips
      </h1>
      <h2 class="subtitle">
        Start yout trip right now!
      </h2>
      <el-row class="select">
        <el-col :span="24">
          <h4 class="select-text">Please Select Your Main Destination</h4>
          <UserPerference class="select-destination" />
        </el-col>
      </el-row>
      <el-row class="select">
        <el-col :span="24" class="select-option">
          <el-popover placement="top-start" title="Instruction" width="200" trigger="hover" content="First select a main destination and then click me!">
            <el-button @click="createNew" type="create" icon="el-icon-plus" slot="reference">Create My Next Trip Plan</el-button>
          </el-popover>
        </el-col>
      </el-row>
      <el-row class="select">
        <el-col :span="24" class="select-option">
          <el-popover placement="bottom" title="Instruction" width="200" trigger="hover" content="Click me to see what you have created with our web">
            <el-button @click="continueOne" type="continue" icon="el-icon-edit" slot="reference">Continue Your Trip Plan</el-button>
          </el-popover>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row>
        <el-col :span="24" class="select-chatbot">
          <h4 class="select-text">Try To Talk With Our Bot to Have Some Ideas</h4>
          <Chatbot v-on:chatComplete="getslot" />
        </el-col>
      </el-row>
    </div>
  </el-container>
</template>
<script>
  import MainNav from "../components/Navbars/MainNav";
  import UserPerference from "../components/CustomlizePage/UserPerference";
  import Chatbot from "../components/Chatbot/Chatbot";
  import { Auth } from "aws-amplify";
  import { API } from "aws-amplify";
  import * as mutations from "@/graphql/mutations";
  var apigClientFactory = require("aws-api-gateway-client").default;

  export default {
    name: "home",
    components: {
      MainNav,
      UserPerference,
      Chatbot,
    },
    data() {
      return {
        user: "",
        userId: "",
        targetArea: "",
        newSchedule: "",
        session: "",
      };
    },
    mounted() {
      this.initChatbot;
    },
    methods: {
      userPromise(user) {
        this.user = user;
        this.userId = "user-" + user.username;
        return this.userId;
      },

      PromiseInit() {
        var user = Auth.currentAuthenticatedUser();
        user.then(this.userPromise);
      },

      pickArea(val) {
        this.targetArea = val;
      },

      getslot(slots) {
        this.targetArea = slots.slots.Location;
        var title = String(new Date()) + "bot";
        console.log("emit!", this.targetArea, title);
        if (this.targetArea) {
          this.postNewSchedule(title).then((resp) => {
            if (resp) {
              // console.log("post", resp.scheduleId);
              sessionStorage.setItem("tripMode", slots.slots.Mode);
              sessionStorage.setItem("AttractionType", slots.slots.AttractionType);
              setTimeout(this.$router.push("/createnew/" + resp.scheduleId), 5000);
            }
          });
        }
      },

      createNew(e) {
        e.preventDefault();
        // console.log("test");
        this.$msgbox
          .prompt("Please input your planner name", "Tip", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
          })
          .then(({ value }) => {
            this.$msg({
              type: "success",
              message: "You are redirecting to your next :" + value + "plan",
            });
            this.postNewSchedule(value).then((resp) => {
              if (resp) {
                // console.log("async", resp.scheduleId);
                this.createConversation(resp.scheduleId);
                this.$router.push("/createnew/" + resp.scheduleId);
              }
            });
          })
          .catch(() => {
            this.$msg({
              type: "info",
              message: "Canceled to start a new plan",
            });
          });
      },

      continueOne(e) {
        e.preventDefault();
        this.$router.push("/schedulelist/" + this.userId);
      },
      async postNewSchedule(name) {
        const session = await Auth.currentSession();
        var config = {
          invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1",
        };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {};
        var pathTemplate = "/schedule/";
        var method = "POST";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            scheduleTitle: name,
            targetArea: this.targetArea,
            userId: this.userId,
          },
        };
        var body = {};
        return new Promise(function(resolve, reject) {
          apigClient
            .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then((response) => {
              if (response.status === 200) {
                // console.log("post resp", response);
                resolve(response.data);
              }
            })
            .catch((err) => {
              console.log(err);
              reject(err);
            });
        });
      },
      async createConversation(schduleId) {
        console.log("create");
        await API.graphql({
          query: mutations.createConversation,
          variables: { id: schduleId, name: schduleId, createdAt: new Date() },
        }).then(() => {});
      },
    },
    created() {
      this.PromiseInit();
    },
  };
</script>
<style scoped>
  .HomePage {
    color: #775039;
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background-image: url("https://proj-for-attraction-photos.s3.amazonaws.com/trip-bg-1.jpeg");
    background-size: cover;
    background-color: #abb8b5;
    /* background: linear-gradient(0deg, #abb8b5 0%, #cab895 100%); */
  }
  .title {
    font-size: 30px;
    text-align: center;
  }
  .subtitle {
    text-shadow: 4px 4px 4px rgba(20, 110, 55, 0.699);
    font-size: 15px;
    text-align: center;
  }
  .createbn {
    margin-top: 40px;
    /* margin-bottom: 40px; */
  }
  .main {
    position: absolute;
    top: 50px;
    bottom: 0px;
    right: 0px; /* 距离右边0像素 */
    left: 0px;
    padding: 20px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
    /* background-color: red; */
  }
  .select {
    padding: 5px;
  }
  .select-destination {
    margin-top: 5px;
  }
  .select-option {
    margin-top: 10px;
  }
  .select-text {
    margin-top: 0px;
  }
  .el-button--continue {
    background: #1a968f;
    border-color: #1a968f;
    color: #fff;
  }
  .el-button--continue:hover {
    background: #205355;
    border-color: #205355;
    color: #b58860;
  }

  .el-button--create {
    background: #425d8a;
    border-color: #425d8a;
    color: #fff;
  }
  .el-button--create:hover {
    background: #38576d;
    border-color: #38576d;
    color: #b58860;
  }
</style>
