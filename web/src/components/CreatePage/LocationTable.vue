<template>
  <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="attraction-card">
        <div>
          <el-table
            :data="tableData"
            style="width: 100%"
            max-height="470"
            @selection-change="handleSelectionChange"
            :row-style="getRowClass"
            :header-row-style="getRowClass"
            :header-cell-style="getRowClass"
          >
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
            <el-button @click="handleDelete" type="danger">Select Delete</el-button>
            <el-button v-if="showSubmit" @click="dialogFormVisible = true" type="continue">Fininsh Selection</el-button>
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
      attractionAdd: {
        type: String,
        default() {
          return "attraction";
        },
      },
      userId: String,
      ownerView: Boolean,
    },
    data() {
      return {
        tableData: [],
        dialogFormVisible: false,
        scheduleId: "",
        userIdValue: "",
        attracationIdList: [],
        revisedTimeStamp: 0,
        showSubmit: false,
        multipleSelection: [],
        dateNmuber: 3,
        select1: "BUSY",
        options1: [
          { text: "Busy", value: "BUSY" },
          { text: "Medium", value: "MEDIUM" },
          { text: "Relax", value: "RELAX" },
        ],
        select2: "nature",
        options2: [
          { text: "Nature", value: "nature" },
          { text: "Humantic", value: "humantic" },
          { text: "Art", value: "art" },
          { text: "Outdoor", value: "nature" },
          { text: "Indoor", value: "history" },
          { text: "Iconic", value: "iconic" },
          { text: "Science", value: "science" },
        ],
      };
    },
    methods: {
      PromiseInit() {
        var user = Auth.currentAuthenticatedUser();
        // user.then(this.userPromise).then(this.dataInit);
        user.then(this.userPromise).then(() => this.initDataTable());
      },
      userPromise(user) {
        this.user = user;
        this.userIdValue = "user-" + user.username;
        return this.userIdValue;
      },
      setScheduleId() {
        this.scheduleId = this.$route.params.scheduleId;
      },

      getlikeFlag(selectedUsers) {
        // console.log(selectedUsers.includes(this.userId));
        return selectedUsers.includes(this.userIdValue);
      },

      async initDataTable() {
        console.log("init LocationTable", this.userIdValue);
        const session = await Auth.currentSession();
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          scheduleId: this.scheduleId,
        };
        var pathTemplate = "/schedule/{scheduleId}";
        var method = "GET";
        var additionalParams = {
          //If there are query parameters or headers that need to be sent with the request you can add them here
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            userId: this.userIdValue,
          },
        };
        var body = {};
        await apigClient
          .invokeApi(pathParams, pathTemplate, method, additionalParams, body)
          .then((response) => {
            if (response.status === 200) {
              console.log("timeStamp", response.data.revisedTimeStamp);
              this.revisedTimeStamp = response.data.revisedTimeStamp;
              this.tableData = [];
              this.attracationIdList = [];
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
            userId: this.userIdValue,
            like: true,
          },
        };
        var body = {};
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
            userId: this.userIdValue,
            like: false,
          },
        };
        var body = {};
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
        // console.log("selection", this.multipleSelection);
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
              let promises = [];
              this.multipleSelection.forEach((item) => {
                console.log(item);
                promises.push(this.deleteSelection(item));
              });
              return Promise.all(promises).then(() => {
                console.log("test");
                this.$msg({
                  type: "success",
                  message: "You have changed your selection",
                });
                this.initDataTable();
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
            this.submitSchedule(this.scheduleId)
              .then(() => {
                this.$router.push("/scheduleedit/" + this.scheduleId);
                this.$msg({
                  type: "success",
                  message: "You are redirecting to your next step!",
                });
              })
              .catch((err) => {
                this.$msg({
                  type: "info",
                  message: "Error " + err,
                });
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
            userId: this.userIdValue,
          },
        };
        var body = {
          mode: this.select1,
          typePreference: this.select2,
          day: Number(this.dateNmuber),
        };
        // var isSuccess = false;
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
            userId: this.userIdValue,
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

      getRowClass() {
        return "background:transparent;color:#000;";
      },
    },

    watch: {
      attractionAdd() {
        // console.log(newAttraction);
        // this.$msg("Wait!!!");
        this.initDataTable();
        // setTimeout(this.initDataTable(), 5000 * 1);
      },
      ownerView(newVal) {
        console.log("onwer", newVal);
        this.showSubmit = newVal;
      },
    },
    created() {
      this.setScheduleId();
    },
    mounted() {
      var tripMode = sessionStorage.getItem("tripMode");
      if (tripMode.toUpperCase()) {
        console.log("mode", tripMode.toUpperCase());
        this.select1 = tripMode.toUpperCase();
      }
      var attractionType = sessionStorage.getItem("AttractionType");
      if (attractionType) {
        console.log("attractionType", attractionType);
        this.select2 = attractionType;
      }
      this.PromiseInit();
      setInterval(this.initDataTable, 10000);
      this.$once("hook:beforeDestroy", () => {
        console.log("clear!");
        clearInterval();
      });
    },
  };
</script>
<style>
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
  .attraction-card {
    background: rgba(148, 144, 144, 0.3);
  }
  .el-table {
    /* 表格字体颜色 */
    color: #6b3633;
    /* 表格边框颜色 */
    border: 0px solid #debe90;
    /* height: 500px; */
    background-color: #ebe7de;
  }
  .el-table th,
  .el-table tr,
  .el-table td {
    border: 0;
    background-color: transparent;
  }
  .el-table thead {
    color: #9c8467;
    font-weight: 800;
    background-color: rgba(148, 144, 144, 0.3);
  }
  .el-button--continue {
    background: #1a968f;
    border-color: #1a968f;
    color: #fff;
  }
  .el-button--continue:hover {
    background: #205355;
    border-color: #205355;
    color: #b58860;
  }
  .el-button--text {
    color: #1a968f;
  }
  .el-button--text:hover {
    color: #639c9e;
  }
</style>
