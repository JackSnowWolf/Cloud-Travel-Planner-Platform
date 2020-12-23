<template>
  <div class="EditPage">
    <MainNav />
    <Slider />
    <div class="main">
      <el-row class="select">
        <el-col :span="20">
          <h3>Your Trip Plan is Here!</h3>
          <h4>You can edit the tour order as you wish</h4>
          <ScheduleCard :userId="userId" :scheduleId="scheduleId" v-on:newChange="getChangedSchedule" />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="20" class="select-bucket">
          <div>
            <el-button type="continue" @click="handleSubmit" el-icon-check plain>Submit</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
  import MainNav from "../components/Navbars/MainNav";
  import Slider from "../components/Navbars/Slider.vue";
  import ScheduleCard from "../components/ScheduleListPage/ScheduleCard";
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    name: "SchduelSinglePage",
    components: {
      ScheduleCard,
      Slider,
      // SearchDialog,
      MainNav,
    },
    data() {
      return {
        loading: false,
        user: "",
        userId: "",
        scheduleId: "",
        scheduleChanged: [],
        schedule: {},
        dayScheduleContents: [],
      };
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

      createmethod() {
        this.setScheduleId();
      },

      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
      },
      getChangedSchedule(item) {
        // this.$loading.show();
        var promises = [];
        for (var i = 0; i < item.length; i++) {
          promises.push(this.patchChangedItem(item[i][0]));
        }
        Promise.all(promises).then(() => {
          this.$msg({
            type: "success",
            message: "You have changed your order",
          });
        });
        // this.$loading.close();
      },

      async patchChangedItem(item) {
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
        };
        var pathTemplate = "/schedule/{scheduleId}";
        var method = "PATCH";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
          },
        };
        var body = { NumDate: item.NumDate, Details: item.Details };
        // console.log("patchbody", body);
        apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              // if response
              console.log("patch Success!", response);
              //This is where you would put a success callback
              return true;
            }
          })
          .catch((err) => {
            console.log(err);
            return false;
          });
      },

      handleSubmit(e) {
        e.preventDefault();
        this.$msgbox
          .confirm("Submit your plan now?", "Warning", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          })
          .then(() => {
            this.getFinishSchedule()
              .then((resp) => {
                console.log(resp);
                this.$router.push("/review/" + this.scheduleId);
                this.$msg({
                  type: "success",
                  message: "Your are redirecting to your next step",
                });
              })
              .catch(() => {
                this.$msg({
                  type: "info",
                  message: "Failed",
                });
              });
          })
          .catch(() => {
            this.$msg({
              type: "info",
              message: "Canceled",
            });
          });
      },

      async getFinishSchedule() {
        const session = await Auth.currentSession();
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
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
          },
        };
        var body = {};
        return new Promise(function(resolve, reject) {
          apigClient
            .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then((response) => {
              // console.log(response);
              if (response.status === 200) {
                resolve(response);
              }
            })
            .catch((err) => {
              reject(err);
              console.log(err);
            });
        });
      },
    },
    mounted() {
      this.PromiseInit();
    },
    created() {
      this.createmethod();
    },
  };
</script>

<style scoped>
  .EditPage {
    color: #775039;
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background-image: url("https://proj-for-attraction-photos.s3.amazonaws.com/trip-bg-3.jpeg");
    background-size: cover;
    /* background-color: #abb8b5;
    background: linear-gradient(0deg, #abb8b5 0%, #cab895 100%); */
  }
  /* 主区域 */
  .main {
    position: absolute;
    top: 65px;
    left: 230px;
    bottom: 0px;
    right: 0px; /* 距离右边0像素 */
    padding: 10px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
    /* background-color: red; */
  }
  .select {
    margin-top: 20px;
  }
  .select-bucket-title {
    margin-bottom: 40px;
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
</style>
