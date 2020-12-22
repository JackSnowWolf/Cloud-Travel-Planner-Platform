<template>
  <el-container>
    <el-main>
      <el-button @click="acceptInvitation" type="success" plain>Accept</el-button>
    </el-main>
  </el-container>
</template>

<script>
  // @ is an alias to /src
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    data() {
      return {
        scheduleId: String,
        editorId: String,
      };
    },
    methods: {
      async acceptInvitation(e) {
        e.preventDefault();
        const session = await Auth.currentSession();
        this.tableData = [];
        this.attracationIdList = [];
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = "/accept/{scheduleId}";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            editorId: this.editorId,
            // scheduleId: this.scheduleId,
          },
        };
        var body = {
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log(response.data, this.editorId);
              if (response.data.schedule_type === "PRESELECT") {
                setTimeout(this.$router.push("/createnew/" + this.scheduleId), 1000);
              } else if (response.data.schedule_type === "EDITING") {
                setTimeout(this.$router.push("/scheduleedit/" + this.scheduleId), 1000);
              } else if (response.data.schedule_type === "COMPLETED") {
                setTimeout(this.$router.push("/review/" + this.scheduleId), 1000);
              }
            }
          })
          .catch((err) => {
            console.log(err);
            this.$msg({
              type: "info",
              message: err,
            });
          });
      },
    },
    mounted() {
      this.editorId = this.$route.query.editorId;
      this.scheduleId = this.$route.query.scheduleId;
      // console.log(this.$route.query);
    },
    created() {},
    name: "accpect",
  };
</script>
