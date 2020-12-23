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
            <el-button @click="getPDF" type="create" icon="el-icon-download" plain>Create My PDF</el-button>
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
  import fileDownload from "js-file-download";
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
        scheduleId: "",
        userId: "",
        user: "",
        dayScheduleContents: [],
      };
    },
    methods: {
      userPromise(user) {
        this.user = user;
        this.userId = "user-" + user.username;
        return this.userId;
      },

      dataInit(user) {
        // console.log("test", user);
        this.initDataTable(this.scheduleId, user).then(this.ParseData);
      },

      ParseData(data) {
        this.dayScheduleContents = data;
      },

      PromiseInit() {
        var user = Auth.currentAuthenticatedUser();
        // user.then(this.userPromise).then(this.dataInit);
        user.then(this.userPromise).then(this.dataInit);
      },

      createmethod() {
        this.setScheduleId();
      },

      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
      },

      async initDataTable(scheduleId, userId) {
        // console.log("init Preselect table", this.scheduleId, this.userId);
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
                // console.log("Get resp init", response.data.scheduleContent.dayScheduleContents);
                // this.dayScheduleContents = response.data.scheduleContent.dayScheduleContents;
                resolve(response.data.scheduleContent.dayScheduleContents);
              }
            })
            .catch((err) => {
              console.log(err);
              reject(err);
            });
        });
      },

      async getPDF(e) {
        e.preventDefault();
        console.log("Generate PDF");
        const session = await Auth.currentSession();
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
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {},
        };
        var body = {};
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              fileDownload(response.data, String(this.scheduleId) + ".pdf");
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },

    mounted() {
      // this.initDataTable(this.scheduleId, this.userId);
      this.PromiseInit();
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
    background-image: url("https://proj-for-attraction-photos.s3.amazonaws.com/trip-bg-2.jpeg");
    background-size: cover;
    /* background-color: #abb8b5;
    background: linear-gradient(0deg, #abb8b5 0%, #cab895 100%); */
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
