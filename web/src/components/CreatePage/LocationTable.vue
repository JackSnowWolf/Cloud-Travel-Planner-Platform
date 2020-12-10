<template>
  <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="attraction-card">
        <div>
          <el-table :data="tableData" style="width: 100%" max-height="400" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"> </el-table-column>
            <el-table-column type="expand">
              <template slot-scope="props">
                <p>LikeCount: {{ props.row.selectedNumber }}</p>
              </template>
            </el-table-column>
            <el-table-column property="attractionName" label="Name" width="200"> </el-table-column>
            <el-table-column property="attractionArea" label="attractionArea" width="120"> </el-table-column>
            <el-table-column property="attractionId" label="attractionId" width="200"> </el-table-column>
            <el-table-column fixed="right" label="Operations" width="120">
              <template slot-scope="scope">
                <el-button :disabled="scope.row.isSelected" @click="isSelect(scope.$index)" type="text" size="small">
                  MustChosen
                </el-button>
                <el-button :disabled="!scope.row.isSelected" @click="isCancel(scope.$index)" type="text" size="small">
                  CancelChosen
                </el-button>
              </template>
            </el-table-column>
            <!-- <el-table-column property="isSelected" label="isSelected" width="100" show-overflow-tooltip>
              {{ isSelected }}
            </el-table-column> -->
          </el-table>
          <div style="margin-top: 20px">
            <el-button @click="handleDelete">Select Delete</el-button>
            <el-button @click="handleSubmit">Fininsh Selection</el-button>
          </div>
        </div>
      </vs-card>
    </vs-col>
  </vs-row>
</template>

<script>
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    props: {
      attractionAdd: Object,
      userId: String,
    },
    data() {
      return {
        tableData: [],
        scheduleId: "",
        attracationIdList: [],
        multipleSelection: [],
      };
    },
    methods: {
      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
      },

      async initDataTable() {
        console.log("init Preselect table", this.scheduleId, this.userId);
        this.tableData = [];
        this.attracationIdList = [];
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
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
              // if response
              // console.log("Get resp", response.data.scheduleContent);
              var object = response.data.scheduleContent;
              for (var attracationId in object) {
                this.attracationIdList.push(attracationId);
                this.tableData.push(object[attracationId]);
              }
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },

      async isSelect(index) {
        console.log("choose", this.tableData[index].attractionId);
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: this.tableData[index].attractionId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
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
            isSelected: true,
          },
        };
        var body = {
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              // if response
              console.log("Get resp", response);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },

      async isCancel(index) {
        console.log("choose", this.tableData[index].attracationId);
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: this.tableData[index].attracationId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
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
            isSelected: false,
          },
        };
        var body = {
          //This is where you define the body of the request
        };
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              // if response
              console.log("Get resp", response);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },

      handleSelectionChange(val) {
        this.multipleSelection = val;
        console.log("selection", this.multipleSelection);
      },

      handleDelete(e) {
        e.preventDefault();
        console.log("selection", this.multipleSelection);
        if (this.multipleSelection) {
          this.$msgbox
            .confirm("Delete your selection now?", "Warning", {
              confirmButtonText: "OK",
              cancelButtonText: "Cancel",
              type: "warning",
            })
            .then(() => {
              for (var index = 0; index < this.multipleSelection.length; index++) {
                console.log("delete", this.multipleSelection[index]);
                this.deleteSelection(this.multipleSelection[index]);
              }
              this.$msg({
                type: "success",
                message: "You have changed your selection",
              });
            })
            .catch(() => {
              this.$msg({
                type: "info",
                message: "Canceled to make a change",
              });
            });
        }
      },
      handleSubmit(e) {
        e.preventDefault();
        this.$msgbox
          .confirm("Submit your preselection schedule now?", "Warning", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          })
          .then(() => {
            this.submitSchedule(this.scheduleId);
            this.$router.push("/scheduleedit/" + this.scheduleId);
            this.$msg({
              type: "success",
              message: "You are redirecting to your next step!",
            });
          })
          .catch(() => {
            this.$msg({
              type: "info",
              message: "Canceled to make a change",
            });
          });
      },
      async submitSchedule(scheduleId) {
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: scheduleId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = "/schedule/{scheduleId}/submit";
        var method = "GET";
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
        var isSuccess = false;
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log("post resp", response);
              isSuccess = true;
            }
          })
          .catch((err) => {
            console.log(err);
          });
        if (isSuccess) {
          return isSuccess;
        } else {
          return isSuccess;
        }
      },
      async deleteSelection(item) {
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: item.attractionId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = "/schedule/{scheduleId}/attraction/{attractionId}";
        var method = "DELETE";
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
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              // if response
              console.log("post resp", response);
              //This is where you would put a success callback
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },
    watch: {
      attractionAdd(newAttraction) {
        console.log(newAttraction);
        this.initDataTable();
      },
    },
    created() {
      this.setScheduleId();
    },
    mounted() {
      this.initDataTable();
    },
  };
</script>
<style scoped>
  .table {
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
