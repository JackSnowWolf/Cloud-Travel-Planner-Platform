<template>
  <el-table :data="tabledata.filter((data) => !search || data.scheduleTitle.toLowerCase().includes(search.toLowerCase()))" style="width: 100%">
    <el-table-column label="scheduleTitle" prop="scheduleTitle"> </el-table-column>
    <el-table-column label="scheduleId" prop="scheduleId"> </el-table-column>
    <el-table-column label="scheduleType" prop="scheduleType"> </el-table-column>
    <el-table-column label="targetArea" prop="targetArea"> </el-table-column>
    <el-table-column align="right">
      <template slot="header">
        <el-input v-model="search" size="mini" placeholder="Type to search" />
      </template>
      <template slot-scope="scope">
        <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
        <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    data() {
      return {
        user: "",
        userId: "",
        tabledata: [],
        search: "",
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
            this.initDatatable();
          }
        });
      },
      async initDatatable() {
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          // attractionId:'attr-0001',
        };
        var pathTemplate = "/schedule";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            pageSize: "100",
            pageNo: "0",
            userId: this.userId,
          },
        };
        var body = {
          //This is where you define the body of the request
        };

        apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body).then((response) => {
          if (response.status === 200) {
            // if response
            console.log(response);
            this.tabledata = response.data;
            //This is where you would put a success callback
          }
        });
      },

      handleDelete(index, row) {
        this.$msgbox
          .confirm("This will permanently delete the Schedule. Continue?", "Warning", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          })
          .then(() => {
            this.deleteQuery(index, row).then((resp) => {
              if (resp) {
                this.$msg({
                  type: "success",
                  message: "Delete completed",
                });
                this.initDatatable();
              }
            });
          })
          .catch(() => {
            this.$msg({
              type: "info",
              message: "Delete canceled",
            });
          });
      },

      handleEdit(index, row) {
        console.log(index, row);
        if (row.scheduleType === "EDITING") {
          this.$router.push("/scheduleedit/" + row.scheduleId);
        } else if (row.scheduleType === "PRESELECT") {
          this.$router.push("/createnew/" + row.scheduleId);
        } else if (row.scheduleType === "COMPLETED") {
          this.$router.push("/review/" + row.scheduleId);
        }
      },

      async deleteQuery(index, row) {
        console.log("delete", index, row.scheduleId);
        const session = await Auth.currentSession();
        var deleteId = row.scheduleId;
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: deleteId,
        };
        var pathTemplate = "/schedule/{scheduleId}";
        var method = "DELETE";
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
        var isSuccess = false;
        await apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body).then((response) => {
          if (response.status === 200) {
            // if response
            console.log(response);
            isSuccess = true;
            //This is where you would put a success callback
          }
        });
        if (isSuccess) {
          return true;
        } else {
          return false;
        }
      },
    },
    mounted() {
      this.createmethod();
    },
  };
</script>
