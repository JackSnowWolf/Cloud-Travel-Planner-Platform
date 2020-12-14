<template>
  <el-container>
    <el-header> <MainNav /></el-header>
    <el-header> </el-header>
    <el-container>
      <el-main>
        <ScheduleList />
      </el-main>
    </el-container>
  </el-container>
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
