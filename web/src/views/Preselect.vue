<template>
  <div class="PreselectPage">
    <MainNav />
    <Slider />
    <div class="main">
      <el-row class="select">
        <el-col :span="10">
          <h3 class="subtitle">Best Spotlights</h3>
          <LocationList v-on:itemAdded="getAddedItem" v-on:itemLike="getItemLike" v-on:itemDislike="getItemDislike" />
        </el-col>
        <el-col :span="14" class="select-bucket">
          <h3 class="select-bucket-title">Your selection bucket</h3>
          <div>
            <LocationTable :attractionAdd="add_attraction" :scheduleId="scheduleId" :userId="userId" :ownerView="ownerView" class="table" />
          </div>
          <!-- <div v-else>
            You have no permission
          </div> -->
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
        add_attraction: "",
        add_likeAttraction: "",
        add_dislikeAttraction: "",
        userId: "",
        user: "",
        scheduleId: null,
        ownerView: false,
      };
    },
    methods: {
      userPromise(user) {
        this.user = user;
        this.userId = "user-" + user.username;
        return this.userId;
      },

      dataInit(user) {
        console.log("test", user);
        this.initDataTable(this.scheduleId, user).then(this.ParseData);
      },

      ParseData(data) {
        if (this.userId === data) {
          this.ownerView = true;
        }
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

      getAddedItem(t) {
        var add_id = t.attractionId;
        // this.add_attraction = t;
        // console.log(this.add_attraction);
        this.putIntoScheduleContent(t)
          .then(this.ParseAddData(add_id))
          .then((resp) => {
            // console.log("resp", resp);
            this.add_attraction = add_id;
            this.$msg({
              type: "success",
              message: resp.data.msg,
            });
          })
          .catch((error) => {
            console.log(error);
            this.$msg({
              type: "info",
              message: "Can not add twice " + error,
            });
          });
      },

      ParseAddData(attractionId) {
        return new Promise(function(resolve) {
          resolve(attractionId);
        });
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
        var body = {};
        return new Promise(function(resolve, reject) {
          apigClient
            .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then((response) => {
              if (response.status === 200) {
                console.log("post resp", response);
                resolve(response);
              }
            })
            .catch((err) => {
              console.log(err);
              reject(err);
            });
        });
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
                console.log("Get resp", response.data.ownerId);
                resolve(response.data.ownerId);
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
      this.PromiseInit();
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
    background-image: url("https://proj-for-attraction-photos.s3.amazonaws.com/trip-bg-1.jpeg");
    background-size: cover;
    background-color: #abb8b5;
    /* background: linear-gradient(0deg, #abb8b5 0%, #cab895 100%); */
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
