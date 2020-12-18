<template>
  <div>
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
            <el-button type="success" icon="el-icon-download" plain>Create My PDF</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
  <!-- <el-container class="review">
    <el-aside width="250px">
      <Slider />
    </el-aside>
    <el-container>
      <el-header>
        header
      </el-header>
      <el-container>
        <el-main>
          <TimeLineList :dayScheduleContents="dayScheduleContents" />
        </el-main>
        <el-footer>
          <el-row>
            <el-col :span="12">
              <div>
                <el-button type="warning">Submit</el-button>
              </div>
            </el-col>
            <el-col :span="12"><div>xx</div></el-col>
          </el-row>
        </el-footer>
      </el-container>
    </el-container>
  </el-container> -->
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
        console.log("Generate PDF", this.scheduleId, this.userId);
        // const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
        };
        var pathTemplate = "/schedule/{scheduleId}/finish";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            // Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
          },
        };
        var body = {
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log("Get resp init", response.data);
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
  .review {
    background: rgb(34, 193, 195);
    background: linear-gradient(0deg, rgba(34, 193, 195, 1) 0%, rgba(253, 187, 45, 1) 100%);
  }
  .main {
    position: absolute;
    top: 50px;
    left: 230px;
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
