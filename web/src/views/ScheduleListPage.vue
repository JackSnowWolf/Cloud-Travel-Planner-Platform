<template>
  <div class="page">
    <MainNav />
    <div class="main">
      <el-row class="ScheduleList">
        <el-col :span="24">
          <ScheduleList />
        </el-col>
      </el-row>
    </div>
  </div>
  <!-- 
  <el-container>
    <el-header> <MainNav /></el-header>
    <el-header> </el-header>
    <el-container>
      <el-main>
        <ScheduleList />
      </el-main>
    </el-container>
  </el-container> -->
</template>
<script>
  import ScheduleList from "../components/ScheduleListPage/ScheduleList";
  import MainNav from "../components/Navbars/MainNav";
  export default {
    name: "ScheduleListPage",
    components: {
      ScheduleList,
      MainNav,
    },
  };
</script>
<style scoped>
  .page {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background: #f0ece3;
    background: linear-gradient(0deg, #abb8b5 0%, #f0ece3 100%);
  }
  .main {
    position: absolute;
    top: 50px;
    left: 20px;
    bottom: 0px;
    right: 20px; /* 距离右边0像素 */
    padding: 10px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
    /* background-color: red; */
  }
  .ScheduleList {
    margin-top: 20px;
  }
</style>
