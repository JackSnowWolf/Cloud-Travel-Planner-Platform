<template>
  <!-- logo和文字 -->
  <div class="header">
    <!-- <a href="#/"> -->
    <!-- 点击进入首页 -->
    <!-- <img class="logo" src="@/assets/Logo1.png" width="25px" /> -->
    <!-- <span class="company">邹邹管理系统</span>
    </a> -->
    <!-- logo和文字结束 -->

    <el-menu :default-active="activeIndex" router class="el-menu" mode="horizontal" @select="handleSelect">
      <el-menu-item index="/home"> <i class="el-icon-s-home"></i>Home</el-menu-item>
      <el-menu-item index="1" disabled>Info</el-menu-item>
      <el-menu-item index="2" disabled>My account</el-menu-item>
      <el-submenu index="3">
        <template slot="title">My account</template>
        <el-menu-item index="/">Log Out</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
  export default {
    name: "mainnav",
    data() {
      return {
        activeIndex: "1",
        activeIndex2: "1",
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
    },
  };
</script>
<style scoped>
  /* 头部样式 */
  .header {
    position: absolute;
    line-height: 60px;
    top: 0px;
    left: 0px;
    right: 0px;
    /* background-color: #2d3a4b; */
  }
  .el-submenu {
    float: right; /* 浮动在右边 */
    margin-right: 40px; /* 靠右40px */
  }</style
>>
