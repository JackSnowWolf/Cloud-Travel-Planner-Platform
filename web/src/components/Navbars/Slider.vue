<template>
  <div class="left-menu">
    <el-menu
      router
      default-active="$route.path"
      class="el-menu-vertical"
      @open="handleOpen"
      @close="handleClose"
      @select="selectMenu"
      :collapse="isCollapse"
      background-color="#ccc"
      text-color="#b58860"
      active-text-color="#84703d"
    >
      <div class="menu-toggle" @click.prevent="control">
        <i class="el-icon-s-fold" v-show="!isCollapse" title="collapse"></i>
        <i class="el-icon-s-unfold" v-show="isCollapse" title="expand"></i>
      </div>
      <el-menu-item index="/home">
        <vs-icon icon="home" size="small"></vs-icon>
        <span slot="title">Back to home page</span>
      </el-menu-item>
      <el-menu-item @click="handleAddAuth">
        <vs-icon icon="person_add" size="small"></vs-icon>
        <!-- <i class="el-icon-s-promotion"></i> -->
        <span slot="title">Add friends</span>
      </el-menu-item>
      <el-menu-item index="/">
        <vs-icon icon="account_circle" size="small"></vs-icon>
        <span slot="title">Log out</span>
      </el-menu-item>
      <el-menu-item index="#chatroom">
        <vs-icon icon="add_comment" size="small"></vs-icon>
        <span slot="title">Chat</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>
<style scoped>
  .el-menu-vertical:not(.el-menu--collapse) {
    /* margin-left: 20px; */
    min-height: 800px;
  }
  .el-menu-vertical {
    position: absolute;
    /* width: 230px; */
    top: 60px; /* 距离上面50像素 */
    left: 0px;
    bottom: 0px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
    /* background-color: #085e29; */
  }
  .menu-toggle {
    margin-top: 20px;
  }
</style>

<script>
  import { Auth } from "aws-amplify";
  var apigClientFactory = require("aws-api-gateway-client").default;
  export default {
    data() {
      return {
        isCollapse: true,
        pathReview: String,
      };
    },
    mounted() {
      this.pathReview = this.pathfunction();
    },
    methods: {
      selectMenu(indexPath) {
        if (indexPath === "#chatroom") {
          let routeData = this.$router.resolve({
            path: "/chatroom/schedule/" + this.$route.params.scheduleId,
          });
          window.open(routeData.href, "-blank");
        }
      },
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
      control() {
        this.isCollapse = !this.isCollapse;
      },
      async pathfunction() {
        await Auth.currentAuthenticatedUser()
          .then((resp) => {
            const user = resp;
            var userId = "user-" + user.username;
            // console.log("/schedulelist/" + userId);
            return "/schedulelist/" + userId;
          })
          .catch((err) => {
            console.log(err);
          });
      },
      async sendInvitation(email) {
        const session = await Auth.currentSession();
        const user = await Auth.currentAuthenticatedUser();
        var userId = "user-" + user.username;
        var config = { invokeUrl: "https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1" };
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
          userId: userId,
        };
        var pathTemplate = "/invite/{userId}";
        var method = "GET";
        var additionalParams = {
          headers: {
            Authorization: session.idToken.jwtToken,
          },
          queryParams: {
            scheduleId: this.$route.params.scheduleId,
            userEmail: email,
          },
        };
        var body = {};
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
      handleAddAuth() {
        this.$msgbox
          .prompt("Please input your friend e-mail", "Tip", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
            inputErrorMessage: "Invalid Email",
          })
          .then(({ value }) => {
            this.$msg({
              type: "success",
              message: "Your friend email is:" + value,
            });
            this.sendInvitation(value);
          })
          .catch(() => {
            this.$msg({
              type: "info",
              message: "Input canceled",
            });
          });
      },
    },
  };
</script>
