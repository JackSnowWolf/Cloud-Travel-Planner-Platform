<template>
  <el-container class="planedit">
    <el-aside width="250px">
      <Slider />
    </el-aside>
    <el-container>
      <el-header>
        header
      </el-header>
      <el-container v-loading="loading">
        <ScheduleCard :userId="userId" :scheduleId="scheduleId" v-on:newChange="getChangedSchedule" />
        <el-footer>
          <el-row>
            <el-col :span="12">
              <div>
                <el-button type="warning" @click="handleSubmit">Submit</el-button>
              </div>
            </el-col>
            <el-col :span="12"
              ><div><SearchDialog /></div
            ></el-col>
          </el-row>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>
<script>
  import SearchDialog from "../components/PlanEditPage/SearchDialog";
  import Slider from "../components/Navbars/Slider.vue";
  import ScheduleCard from "../components/ScheduleListPage/ScheduleCard";
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    name: "SchduelSinglePage",
    components: {
      ScheduleCard,
      Slider,
      SearchDialog,
    },
    data() {
      return {
        loading: false,
        user: "",
        userId: String,
        scheduleId: String,
        scheduleChanged: [],
        schedule: {},
        dayScheduleContents: [],
      };
    },
    methods: {
      async setUserInfo() {
        const user = await Auth.currentAuthenticatedUser();
        this.user = user;
        this.userId = "user-" + user.username;
        return true;
      },

      async createmethod() {
        this.setUserInfo().then((resp) => {
          if (resp) {
            this.setScheduleId();
            // this.initDataTable(this.scheduleId, this.userId);
          }
        });
      },
      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
      },
      getChangedSchedule(item) {
        // this.$loading.show();
        for (var i = 0; i < item.length; i++) {
          // console.log("patchItem", item[i][0]);
          this.patchChangedItem(item[i][0]);
        }
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
        console.log("patchbody", body);
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
                if (resp) {
                  this.$router.push("/review/" + this.scheduleId);
                  this.$msg({
                    type: "success",
                    message: "Your are redirecting to your next step",
                  });
                }
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
        let isSuccess = false;
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            console.log(response);
            if (response.status === 200) {
              // if response
              // console.log(response)
              isSuccess = true;
              //This is where you would put a success callback
            }
          })
          .catch((err) => {
            console.log(err);
          });
        if (isSuccess) {
          return true;
        } else {
          return false;
        }
      },
    },
    created() {
      this.createmethod();
    },
  };
</script>

<style scoped>
  .planedit {
    background: rgb(34, 193, 195);
    background: linear-gradient(0deg, rgba(34, 193, 195, 1) 0%, rgba(253, 187, 45, 1) 100%);
  }
</style>
