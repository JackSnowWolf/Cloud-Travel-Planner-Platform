<template>
  <div class="attraction-container">
    <div class="infinite-list" style="overflow:auto">
      <div v-for="(schedule, key) in dayScheduleContents" :schedule="schedule" :key="key" class="column is-one-quarter">
        <SingleDayPlan :schedule="schedule" :scheduleChanged="scheduleChanged" v-on:scheduleChanged="getChangedSchedule" />
      </div>
    </div>
  </div>
</template>
<script>
  var apigClientFactory = require("aws-api-gateway-client").default;
  import SingleDayPlan from "./SingleDayPlan";
  import { Auth } from "aws-amplify";
  export default {
    name: "EventsList",
    components: {
      SingleDayPlan,
    },
    props: {
      userId: String,
      scheduleIdId: String,
    },
    data() {
      return {
        loading: false,
        emitflag: false,
        scheduleChanged: [],
        schedule: {},
        dayScheduleContents: [],
      };
    },
    methods: {
      async initData() {
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          // attractionId:'attr-0001',
        };
        var pathTemplate = "/schedule/" + this.scheduleId;
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
        var body = {
          //This is where you define the body of the request
        };
        let isSuccess = false;
        let dayScheduleContents = [];
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            console.log(response);
            if (response.status === 200) {
              // if response
              this.scheduleTable = response.data;
              isSuccess = true;
              dayScheduleContents = response.data.scheduleContent.dayScheduleContents;
              console.log("init", dayScheduleContents);
              //This is where you would put a success callback
            }
          })
          .catch((err) => {
            console.log(err);
          });
        if (isSuccess) {
          this.dayScheduleContents = dayScheduleContents;
          return dayScheduleContents;
        } else {
          return false;
        }
      },
      getChangedSchedule(item) {
        if (this.emitflag) {
          this.scheduleChanged = [];
          this.scheduleChanged.push(item);
          // console.log("get!!!!", item);
          // this.postChangedItem(this.scheduleChanged);
          this.emitflag = false;
        } else {
          this.scheduleChanged.push(item);
          // console.log("get", item[0]);
          // this.patchChangedItem(item[0]);
        }
      },
    },
    watch: {
      scheduleChanged(newChanged) {
        if (newChanged) {
          // this.scheduleChanged.push(newChanged);
          console.log("newchange", newChanged.length);
          this.$emit("newChange", newChanged);
          this.emitflag = true;
          // this.initData();
        }
      },

      userId(val) {
        this.userId = val;
        console.log("userid", this.userId);
        this.initData();
      },
    },
    created() {
      this.scheduleId = this.$route.params.scheduleId;
    },
    mounted() {
      // console.log("schdulecard", this.userId);
      // this.initData();
    },
  };
</script>
<style scoped>
  .attraction-container {
    margin-top: 10px;
    margin-left: 10px;
    margin-right: 10px;
    text-align: center;
  }
</style>
