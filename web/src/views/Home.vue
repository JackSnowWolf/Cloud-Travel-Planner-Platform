<template>
  <el-container>
    <el-header> <MainNav /></el-header>
    <el-container>
      <!-- <el-aside width="200px">Aside</el-aside> -->
      <el-main>
        <section class="banner">
          <div class="banner-body">
            <h1 class="title">
              Almost 100,000 people have used our planner for their next trips
            </h1>
            <h2 class="subtitle">
              Start yout trip right now!
            </h2>
            <div class="createbn">
              <UserPerference v-on:pickArea="pickArea" />
            </div>
            <div class="createbn">
              <el-popover
                placement="top-start"
                title="Descirption"
                width="200"
                trigger="hover"
                content="Descirption Descirption Descirption"
              >
                <el-button
                  @click="createNew"
                  type="primary"
                  icon="el-icon-plus"
                  slot="reference"
                  >hover Create My Next Trip Plan</el-button
                >
              </el-popover>
            </div>
            <div class="createbn">
              <el-popover
                placement="bottom"
                title="Descirption"
                width="200"
                trigger="hover"
                content="Descirption Descirption Descirption"
              >
                <el-button
                  @click="continueOne"
                  type="primary"
                  icon="el-icon-edit"
                  slot="reference"
                  >Continue Your Trip Plan</el-button
                >
              </el-popover>
            </div>
            <div v-show="false" class="chatbot">
              <amplify-chatbot :chatbotConfig="chatbotConfig"></amplify-chatbot>
            </div>
            <div class="chatbot">
              <Chatbot />
            </div>
          </div>
        </section>
      </el-main>
    </el-container>
  </el-container>
</template>
<script>
import MainNav from "../components/Navbars/MainNav";
import UserPerference from "../components/CustomlizePage/UserPerference";
import { AmplifyEventBus } from "aws-amplify-vue";
import { Auth } from "aws-amplify";
import { Interactions } from "aws-amplify";
import Chatbot from "../components/Chatbot/Chatbot";
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
      chatbotConfig: {
        bot: "ScheduleBot_first_dev",
        clearComplete: true,
        botTitle: "Helper",
      },
    };
  },
  mounted() {
    this.initChatbot;
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

    async setUserInfo() {
      const user = await Auth.currentAuthenticatedUser();
      this.user = user;
      this.userId = "user-" + user.username;
      console.log(user);
    },
    pickArea(val) {
      this.targetArea = val;
      // console.log("area",val)
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
              console.log("async", resp.scheduleId);
              setTimeout(
                this.$router.push("/createnew/" + resp.scheduleId),
                5000
              );
              // this.$router.push("/createnew/" + resp.scheduleId);
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
      // console.log(session);
      this.session = session;
      var config = {
        invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1",
      };
      var apigClient = apigClientFactory.newClient(config);
      var pathParams = {
        // attractionId:'attr-0001',
      };
      var pathTemplate = "/schedule/";
      var method = "POST";
      var additionalParams = {
        //If there are query parameters or headers that need to be sent with the request you can add them here
        headers: {
          Authorization: session.idToken.jwtToken,
          // param0: '',
          // param1: ''
        },
        queryParams: {
          // pageSize:'4',
          // pageNo:'0',
          scheduleTitle: name,
          targetArea: this.targetArea,
          userId: this.userId,
        },
      };
      var body = {
        //This is where you define the body of the request
      };
      let isSuccess = false;
      await apigClient
        .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
        .then((response) => {
          if (response.status === 200) {
            // if response
            console.log("post resp", response);
            this.newSchedule = response.data;
            // this.scheduleTable = response.data
            // console.log( this.scheduleTable)
            isSuccess = true;
            // dayScheduleContents = response.data.scheduleContent.dayScheduleContents
            //This is where you would put a success callback
          }
        })
        .catch((err) => {
          console.log(err);
        });
      if (isSuccess) {
        return this.newSchedule;
      } else {
        return false;
      }
    },
  },
  created() {
    this.setUserInfo();
  },
};
</script>
<style scoped>
.banner {
  text-align: center;
  background-image: url("https://i.loli.net/2020/11/30/RTndCaxA3PL9JUi.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 680px;
}
.title {
  font-size: 40px;
}
.subtitle {
  text-shadow: 4px 4px 4px rgba(45, 204, 106, 0.699);
  font-size: 20px;
}
.createbn {
  margin-top: 40px;
  /* margin-bottom: 40px; */
}
.chatbot {
  max-height: 200px;
  margin-top: 40px;
}
</style>
