<template>
  <div class="PreselectPage">
    <MainNav class="header" />
    <Slider />
    <div class="main">
      <el-row class="select">
        <el-col :span="12">
          <h3 class="subtitle">Best Spotlights</h3>
          <LocationList v-on:itemAdded="getAddedItem" v-on:itemLike="getItemLike" v-on:itemDislike="getItemDislike" />
        </el-col>
        <el-col :span="12" class="select-bucket">
          <h3 class="select-bucket-title">Your selection bucket</h3>
          <div v-if="ownerView">
            <LocationTable :attractionAdd="add_attraction" :scheduleId="scheduleId" :userId="userId" v-if="userId" class="table" />
          </div>
          <div v-else>
            You have no permission
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  import LocationTable from "../components/CreatePage/LocationTable";
  import LocationList from "../components/CreatePage/LocationList";
  import Slider from "../components/Navbars/Slider";
  import MainNav from "../components/Navbars/MainNav";
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    name: "preselect",
    components: {
      LocationTable,
      LocationList,
      Slider,
      MainNav,
    },
    data() {
      return {
        add_attraction: Object,
        add_likeAttraction: String,
        add_dislikeAttraction: String,
        userId: "",
        user: "",
        scheduleId: null,
        ownerView: false,
      };
    },
    methods: {
      async setUserInfo() {
        const user = await Auth.currentAuthenticatedUser();
        this.user = user;
        this.userId = "user-" + user.username;
        console.log(this.userId);
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

      getAddedItem(t) {
        this.add_attraction = t;
        console.log(this.add_attraction);
        if (this.ownerView) {
          this.putIntoScheduleContent(t);
        } else {
          this.postLike(t.attractionId, false);
        }
      },

      getItemLike(t) {
        // console.log("Like!!!!");
        this.add_likeAttraction = t;
        var flag = true;
        this.postLike(t, flag);
      },

      getItemDislike(t) {
        // console.log("Dislike!!!!");
        this.add_dislikeAttraction = t;
        var flag = false;
        this.postLike(t, flag);
      },

      async postLike(Id, flag) {
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: Id,
        };
        var pathTemplate = "/schedule/{scheduleId}/attraction/{attractionId}";
        var method = "POST";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
            like: flag,
          },
        };
        var body = {
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log("post resp", response);
              this.$msg({
                type: "success",
                message: response.data.msg,
              });
            } else if (response.status === 400) {
              this.$msg({
                type: "failed",
                message: "You can not add like twice",
              });
            }
          })
          .catch((err) => {
            console.log(err);
            this.$msg({
              type: "failed",
              message: err + "Tell onwer to add to your schedule",
            });
          });
      },

      async putIntoScheduleContent(addItem) {
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: addItem.attractionId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = "/schedule/{scheduleId}/attraction/{attractionId}";
        var method = "PUT";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
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
            if (response.status === 200) {
              // if response
              console.log("post resp", response);
              isSuccess = true;
              //This is where you would put a success callback
            }
          })
          .catch((err) => {
            console.log(err);
          });
        if (isSuccess) {
          return isSuccess;
        } else {
          return false;
        }
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
        var ownerView = false;
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            // console.log("init", response);
            if (response.status === 200) {
              // if response
              console.log("Get resp", response.data.ownerId);
              if (userId === response.data.ownerId) {
                ownerView = true;
                this.ownerView = true;
              }
              // var object = response.data.scheduleContent;
            }
          })
          .catch((err) => {
            console.log(err);
          });
        if (ownerView) {
          return true;
        } else {
          return false;
        }
      },
    },
    mounted() {
      console.log("Tye".this.ownerView);
      // this.checkUserType(this.scheduleId,this.userId)
      // this.initDataTable(this.scheduleId,this.userId)
    },
    created() {
      this.createmethod();
    },
  };
</script>
<style scoped>
  .PreselectPage {
    color: #775039;
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background: #c2a19a;
    background: linear-gradient(90deg, #c2a19a 0%, #d1c78c 100%);
  }
  .main {
    position: absolute;
    top: 50px;
    left: 200px;
    bottom: 0px;
    right: 0px; /* 距离右边0像素 */
    padding: 10px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
  }
  .select {
    margin-top: 20px;
  }
  .subtitle {
    margin-bottom: 20px;
  }
  .select-bucket-title {
    margin-bottom: 20px;
    margin-right: 40px;
  }
</style>
