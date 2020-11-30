<template>   
<el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
  <el-menu-item index="1">Home</el-menu-item>
  <el-submenu index="2">
    <template slot="title">My trip</template>
    <el-menu-item index="2-1">1</el-menu-item>
    <el-menu-item index="2-2">2</el-menu-item>
    <el-menu-item index="2-3">3</el-menu-item>
  </el-submenu>
  <el-menu-item index="3" disabled>Info</el-menu-item>
  <el-menu-item index="3">Account</el-menu-item>
</el-menu>
</template>

<script>
  export default {
    name:"mainnav",
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>