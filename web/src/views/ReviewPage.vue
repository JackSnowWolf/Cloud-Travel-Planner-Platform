<template>
  <div class="ReviewPage">
    <MainNav class="header" />
    <Slider />
    <div class="main">
      <el-row class="list">
        <el-col :span="24">
          <TimeLineList :dayScheduleContents="dayScheduleContents" />
        </el-col>
      </el-row>
      <el-row class="button">
        <el-col :span="24">
          <div>
            <el-button @click="getPDF" type="success" icon="el-icon-download" plain>Create My PDF</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
  import TimeLineList from "../components/ReviewPage/TimeLineList";
  import MainNav from "../components/Navbars/MainNav";
  import Slider from "../components/Navbars/Slider";
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    name: "ReviewPage",
    components: {
      TimeLineList,
      Slider,
      MainNav,
    },
    data() {
      return {
        scheduleId: String,
        userId: "",
        user: "",
        dayScheduleContents: "",
      };
    },
    methods: {
      async setUserInfo() {
        const user = await Auth.currentAuthenticatedUser();
        this.user = user;
        this.userId = "user-" + user.username;
        // console.log(this.userId);
        return true;
      },
      async createmethod() {
        this.setUserInfo().then((resp) => {
          if (resp) {
            this.setScheduleId();
            this.initDataTable(this.scheduleId, this.userId);
          }
        });
      },
      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
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
        var body = {
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log("Get resp init", response.data.scheduleContent.dayScheduleContents);
              this.dayScheduleContents = response.data.scheduleContent.dayScheduleContents;
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
      async getPDF(e) {
        e.preventDefault();
        console.log("Generate PDF");
        // const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
        };
        var pathTemplate = "/schedule/{scheduleId}/download";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            // Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            // userId: this.userId,
          },
        };
        var body = {
          // name: "melody",
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log("getPDF", response.data);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },

    mounted() {
      this.initDataTable(this.scheduleId, this.userId);
    },
    created() {
      this.createmethod();
    },
  };
</script>

<style scoped>
  .ReviewPage {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background: #abb8b5;
    background: linear-gradient(0deg, #abb8b5 0%, #cab895 100%);
  }
  .main {
    position: absolute;
    top: 50px;
    left: 200px;
    bottom: 0px;
    right: 0px; /* 距离右边0像素 */
    padding: 10px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */

    /* background-color: red; */
  }
  .list {
    margin-top: 10px;
    margin-right: 40px;
  }
  .button {
    margin-top: 20px;
  }
</style>
