<template>
  <div>
    <MainNav class="header" />
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
          <el-popover placement="top-start" title="Descirption" width="200" trigger="hover" content="Descirption Descirption Descirption">
            <el-button @click="createNew" type="primary" icon="el-icon-plus" slot="reference">hover Create My Next Trip Plan</el-button>
          </el-popover>
        </el-col>
      </el-row>
      <el-row class="select">
        <el-col :span="24" class="select-option">
          <el-popover placement="bottom" title="Descirption" width="200" trigger="hover" content="Descirption Descirption Descirption">
            <el-button @click="continueOne" type="primary" icon="el-icon-edit" slot="reference">Continue Your Trip Plan</el-button>
          </el-popover>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row>
        <el-col :span="24" class="select-chatbot">
          <h4 class="select-text">Try To Talk With Our Bot to Have Some Ideas</h4>
          <Chatbot />
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
  import MainNav from "../components/Navbars/MainNav";
  import UserPerference from "../components/CustomlizePage/UserPerference";
  import Chatbot from "../components/Chatbot/Chatbot";
  import { Auth } from "aws-amplify";
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
      getslot(slots) {
        this.targetArea = slots.slots.Location;
        var title = String(new Date()) + "bot";
        console.log("emit!", this.targetArea, title);
        if (this.targetArea) {
          this.postNewSchedule(title).then((resp) => {
            if (resp) {
              console.log("async", resp.scheduleId);
              setTimeout(this.$router.push("/createnew/" + resp.scheduleId), 5000);
              // this.$router.push("/createnew/" + resp.scheduleId);
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
                console.log("async", resp.scheduleId);
                setTimeout(this.$router.push("/createnew/" + resp.scheduleId), 5000);
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
  /* .banner {
    text-align: center;
    background-image: url("https://i.loli.net/2020/11/30/RTndCaxA3PL9JUi.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 700px;
  } */
  .title {
    font-size: 30px;
    text-align: center;
  }
  .subtitle {
    text-shadow: 4px 4px 4px rgba(45, 204, 106, 0.699);
    font-size: 15px;
    text-align: center;
  }
  .createbn {
    margin-top: 40px;
    /* margin-bottom: 40px; */
  }
  .chatbot {
    max-height: 200px;
    margin-top: 40px;
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
    margin-top: 10px;
  }
</style>
