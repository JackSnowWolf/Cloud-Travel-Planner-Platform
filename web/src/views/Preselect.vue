<template>
  <el-container class="preselect">
    <el-aside width="250px">
      <Slider />
    </el-aside>
    <el-container>
      <el-header>
        Pick Up Your Favorite Attractiones
      </el-header>
      <el-container>
        <el-aside width="500px"
          >Attraction List
          <div>
            <LocationList v-on:itemAdded="getAddedItem" v-on:itemLike="getItemLike" v-on:itemDislike="getItemDislike" />
          </div>
        </el-aside>
        <el-main>
          Main
          <div v-if="ownerView">
            <LocationTable :attractionAdd="add_attraction" :scheduleId="scheduleId" :userId="userId" class="table" />
          </div>
          <div v-else>
            You have no permission
          </div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>
<script>
  import LocationTable from "../components/CreatePage/LocationTable";
  import LocationList from "../components/CreatePage/LocationList";
  import Slider from "../components/Navbars/Slider";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    name: "preselect",
    components: {
      LocationTable,
      LocationList,
      Slider,
    },
    data() {
      return {
        add_attraction: Object,
        add_likeAttraction: String,
        add_dislikeAttraction: String,
        userId: "test-editor",
        scheduleId: null,
        ownerView: false,
      };
    },
    methods: {
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
        console.log("Like!!!!");
        this.add_likeAttraction = t;
        var flag = true;
        this.postLike(t, flag);
      },
      getItemDislike(t) {
        console.log("Dislike!!!!");
        this.add_dislikeAttraction = t;
        var flag = false;
        this.postLike(t, flag);
      },
      async postLike(Id, flag) {
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
            // param0: '',
            // param1: ''
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
            // param0: '',
            // param1: ''
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
        this.tableData = [];
        this.attracationIdList = [];
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: scheduleId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = "/schedule/{scheduleId}";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            // param0: '',
            // param1: ''
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
            console.log("init", response);
            if (response.status === 200) {
              // if response
              console.log("Get resp", response.data.ownerId);
              if (userId === response.data.ownerId) {
                ownerView = true;
                this.ownerView = true;
                // console.log(this.ownerView,"true")
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
      this.setScheduleId();
      this.initDataTable(this.scheduleId, this.userId);
    },
    // mounted(){

    // }
  };
</script>
<style scoped>
  .preselect {
    background: rgb(252, 198, 135);
    background: linear-gradient(90deg, rgba(252, 198, 135, 1) 0%, rgba(242, 134, 160, 1) 100%);
  }
  .table {
    margin-top: 0px;
    margin-left: 20px;
  }
</style>
