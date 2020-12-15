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
                <el-button :disabled="getlikeFlag(scope.row.selectedUsers)" @click="isSelect(scope.$index)" type="text" size="small">
                  Like
                </el-button>
                <el-button :disabled="!getlikeFlag(scope.row.selectedUsers)" @click="isCancel(scope.$index)" type="text" size="small">
                  CancelLike
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 20px">
            <el-button @click="handleDelete">Select Delete</el-button>
            <el-button @click="dialogFormVisible = true">Fininsh Selection</el-button>
            <vs-popup title="Choose your trip mode" :active.sync="dialogFormVisible">
              <h4>
                <span>We provide following trip mode for you, please select one as you wish </span>
              </h4>
              <vs-row>
                <vs-select label="Trip mode" v-model="select1">
                  <vs-select-item :key="index" :value="item.value" :text="item.text" v-for="(item, index) in options1" />
                </vs-select>
              </vs-row>
              <vs-row>
                <vs-select label="Trip perference" v-model="select2">
                  <vs-select-item :key="index" :value="item.value" :text="item.text" v-for="(item, index) in options2" />
                </vs-select>
              </vs-row>
              <vs-row>
                <vs-input :warning="true" warning-text="The entered data could not be verified" placeholder="Input number of days" v-model="dateNmuber" />
              </vs-row>
              <vs-row>
                <vs-button @click="handleSubmit" color="success" type="filled">Next step</vs-button>
              </vs-row>
            </vs-popup>
          </div>
        </div>
      </vs-card>
    </vs-col>
  </vs-row>
</template>

<script>
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    props: {
      attractionAdd: Object,
      userId: String,
    },
    data() {
      return {
        tableData: [],
        dialogFormVisible: false,
        scheduleId: "",
        attracationIdList: [],
        multipleSelection: [],
        dateNmuber: 3,
        select1: "normal",
        options1: [
          { text: "Busy", value: "busy" },
          { text: "Normal", value: "normal" },
          { text: "Relax", value: "relax" },
        ],
        select2: "nature",
        options2: [
          { text: "Nature", value: "nature" },
          { text: "History", value: "history" },
          { text: "Fashion", value: "fashion" },
          { text: "Art", value: "art" },
        ],
      };
    },
    methods: {
      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
      },

      getlikeFlag(selectedUsers) {
        console.log(selectedUsers.includes(this.userId));
        return selectedUsers.includes(this.userId);
      },
      async initDataTable() {
        console.log("init LocationTable", this.userId);
        const session = await Auth.currentSession();
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
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
          },
        };
        var body = {
          //This is where you define the body of the request
        };
        // this.$msg("Init!!!");
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
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
        const session = await Auth.currentSession();
        // console.log("choose", this.tableData[index].attractionId);
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: this.tableData[index].attractionId,
        };
        var pathTemplate = "/schedule/{scheduleId}/attraction/{attractionId}";
        var method = "POST";
        var additionalParams = {
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
            like: true,
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
              this.initDataTable();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      },

      async isCancel(index) {
        const session = await Auth.currentSession();
        // console.log("choose", this.tableData[index].attractionId);
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
          attractionId: this.tableData[index].attractionId,
        };
        var pathTemplate = "/schedule/{scheduleId}/attraction/{attractionId}";
        var method = "POST";
        var additionalParams = {
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userId,
            like: false,
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
              this.initDataTable();
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
              setTimeout(this.initDataTable(), 1000 * 1);
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
        this.dialogFormVisible = false;
        console.log(this.dateNmuber);
        e.preventDefault();
        this.$msgbox
          .confirm("Submit your preselection schedule now?", "Warning", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          })
          .then(() => {
            this.submitSchedule(this.scheduleId);
            setTimeout(this.$router.push("/scheduleedit/" + this.scheduleId), 1000 * 1);
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
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: scheduleId,
        };
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = "/schedule/{scheduleId}/submit";
        var method = "POST";
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
          mode: this.select1,
          typePreference: this.select2,
          day: this.dateNmuber,
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
        const session = await Auth.currentSession();
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
            Authorization: session.idToken.jwtToken,
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
        // this.$msg("Wait!!!");
        setTimeout(this.initDataTable(), 1000 * 1);
      },
    },
    created() {
      this.setScheduleId();
    },
    mounted() {
      console.log(this.userId);
      this.initDataTable();
    },
  };
</script>
<style scoped>
  .table {
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .vs-input {
    float: left;
    width: 50%;
    margin: 10px;
    margin-top: 5px;
  }
  .con-select {
    margin-left: 10px;
    width: 50%;
    margin-bottom: 10px;
  }
</style>
