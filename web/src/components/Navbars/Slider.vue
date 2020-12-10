<template>
  <div class="slider">
    <!-- <el-radio-group v-model="isCollapse" style="margin-left:-70px;">
      <el-radio-button :label="false">expand</el-radio-button>
      <el-radio-button :label="true">collapse</el-radio-button>
    </el-radio-group> -->
    <el-menu router default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
      <el-menu-item>
        <el-radio-group v-model="isCollapse" style="margin-left:-20px;" size="medium">
          <el-radio-button :label="false">expand</el-radio-button>
          <el-radio-button :label="true">collapse</el-radio-button>
        </el-radio-group>
      </el-menu-item>
      <el-menu-item index="/home">
        <i class="el-icon-menu"></i>
        <span slot="title">Back to home page</span>
      </el-menu-item>
      <el-menu-item @click="handleAddAuth">
        <i class="el-icon-setting"></i>
        <span slot="title">Add friends</span>
      </el-menu-item>
      <el-menu-item index="/">
        <i class="el-icon-user"></i>
        <span slot="title">Log out</span>
      </el-menu-item>
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span slot="title">Navigator One</span>
        </template>
        <el-menu-item-group>
          <span slot="title">Group One</span>
          <el-menu-item index="/createnew">Create New</el-menu-item>
          <el-menu-item index="/planedit">Plan Edit</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="Group Two">
          <el-menu-item index="1-3">item three</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </div>
</template>
<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    /* margin-left: 20px; */
    width: 180px;
    min-height: 600px;
  }
  .el-menu-vertical-demo {
    /* margin-left: 20px; */
    width: 60px;
    min-height: 600px;
  }
  .slider {
    /* margin-top: 20px;
      margin-left: 20px; */
  }
</style>

<script>
  export default {
    data() {
      return {
        isCollapse: true,
      };
    },
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
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
              message: "Your email is:" + value,
            });
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
