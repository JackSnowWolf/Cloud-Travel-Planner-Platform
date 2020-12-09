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
  export default {
    name: "EventsList",
    components: {
      SingleDayPlan,
    },
    data() {
      return {
        loading: false,
        emitflag: false,
        userId: "test-editor",
        scheduleChanged: [],
        schedule: {},
        dayScheduleContents: [],
        // dayScheduleContents: [
        //   {
        //     numDate: 1,
        //     Details: [
        //       { name: "Melody", id: 1 },
        //       { name: "Melodyy", id: 2 },
        //       { name: "Jean", id: 3 },
        //       { name: "Gerard", id: 4 },
        //     ],
        //     description: "Happy day by day",
        //   },
        //   {
        //     numDate: 2,
        //     Details: [
        //       { name: "John", id: 1 },
        //       { name: "Joao", id: 2 },
        //       { name: "Jean", id: 3 },
        //       { name: "Gerard", id: 4 },
        //     ],
        //     description: "Sad day by day",
        //   },
        //   {
        //     numDate: 3,
        //     Details: [
        //       { name: "John", id: 1 },
        //       { name: "Joao", id: 2 },
        //       { name: "Jean", id: 3 },
        //       { name: "Gerard", id: 4 },
        //     ],
        //     description: "Dance day by day",
        //   },
        //   {
        //     numDate: 4,
        //     Details: [
        //       { name: "John", id: 1 },
        //       { name: "Joao", id: 2 },
        //       { name: "Jean", id: 3 },
        //       { name: "Gerard", id: 4 },
        //     ],
        //     description: "Jump day by day",
        //   },
        // ],
      };
    },
    methods: {
      async initData() {
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
            // param0: '',
            // param1: ''
          },
          queryParams: {
            // pageSize:'4',
            // pageNo:'0',
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
              // console.log(response)
              this.scheduleTable = response.data;
              // console.log(this.scheduleTable);
              isSuccess = true;
              dayScheduleContents = response.data.scheduleContent.dayScheduleContents;
              console.log("day", dayScheduleContents);
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
          console.log("get!!!!", this.scheduleChanged);
          this.postChangedItem(this.scheduleChanged);
          this.emitflag = false;
        } else {
          this.scheduleChanged.push(item);
          console.log("get", this.scheduleChanged);
          this.postChangedItem(this.scheduleChanged);
        }
      },
      postChangedItem(item) {
        var scheduleContent = { dayScheduleContents: item, metaData: "dummy" };
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
            // param0: '',
            // param1: ''
          },
          queryParams: {
            // pageSize:'4',
            // pageNo:'0',
            userId: this.userId,
          },
        };
        var body = {
          scheduleContent: scheduleContent,
        };
        apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            console.log(response);
            if (response.status === 200) {
              // if response
              console.log(response);

              //This is where you would put a success callback
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },
    watch: {
      scheduleChanged(newChanged) {
        if (newChanged) {
          // this.scheduleChanged.push(newChanged);
          // console.log("newchange", newChanged);
          this.$emit("newChange", newChanged);
          this.emitflag = true;
        }
      },
    },
    created() {
      this.scheduleId = this.$route.params.scheduleId;
      console.log(this.scheduleId);
    },
    mounted() {
      this.initData();
    },

    //   methods:{
    //       getItemAdded(item){
    //           this.addAttraction = item
    //           console.log("emit")
    //           this.$emit('itemAdded',item)
    //       }

    //   }
    //     mounted: function () {
    //     console.log("start!")
    //     this.$axios
    //       .get("/api/query/AllEvent")
    //       .then((response) => {
    //         if (response.data.status == "success") {
    //           this.events = response.data.data;
    //           console.log(this.events);
    //         } else window.alert("Failed");
    //       });
    //   },
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
