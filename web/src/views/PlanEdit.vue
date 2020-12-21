<template>
  <div>
    <MainNav class="header" />
    <Slider />
    <div class="main">
      <el-row class="select">
        <el-col :span="12">
          <h3>Best Spotlights</h3>
          <PlanList v-on:newChange="getChangedSchedule" />
        </el-col>
        <el-col :span="12" class="select-bucket">
          <h3 class="select-bucket-title">Your selection bucket</h3>
          <SearchDialog />
          <div>
            <el-button type="warning" @click="handleSubmit">Submit</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>

  <!-- <el-container class="planedit">
    <el-aside width="250px">
      Slider
      <Slider />
    </el-aside>
    <el-container>
      <el-header>
        header
      </el-header>
    <el-container>
      <el-main>
        Main
        <PlanList 
        v-on:newChange="getChangedSchedule"/>
      </el-main>
      <el-footer>
        <el-row>
          <el-col :span="12">
            <div >
              <el-button type="warning" @click="handleSubmit">Submit</el-button>
            </div>
          </el-col>
          <el-col :span="12"><div ><SearchDialog /></div></el-col>
        </el-row>
      </el-footer>
      </el-container>
    </el-container>
  </el-container> -->
</template>
<script>
  import MainNav from "../components/Navbars/MainNav";
  import SearchDialog from "../components/PlanEditPage/SearchDialog";
  import Slider from "../components/Navbars/Slider";
  import PlanList from "../components/PlanEditPage/PlanList";
  export default {
    components: {
      PlanList,
      Slider,
      SearchDialog,
      MainNav,
    },
    methods: {
      getChangedSchedule(item) {
        console.log("getchanged", item);
      },
      handleSubmit() {
        this.$msgbox
          .confirm("Submit your plan now?", "Warning", {
            confirmButtonText: "OK",
            cancelButtonText: "Cancel",
            type: "warning",
          })
          .then(() => {
            this.$router.push("/review");
            this.$msg({
              type: "success",
              message: "Your are redirecting to your next step",
            });
          })
          .catch(() => {
            this.$msg({
              type: "info",
              message: "Canceled",
            });
          });
      },
    },
  };
</script>
<style scoped>
  .planedit {
    background-image: url("https://proj-for-attraction-photos.s3.amazonaws.com/trip-bg-3.jpeg");
    background-size: cover;
    /* background: rgb(34, 193, 195);
    background: linear-gradient(0deg, rgba(34, 193, 195, 1) 0%, rgba(253, 187, 45, 1) 100%); */
  }
  /* 主区域 */
  .main {
    position: absolute;
    top: 50px;
    left: 230px;
    bottom: 0px;
    right: 0px; /* 距离右边0像素 */
    padding: 10px;
    overflow-y: auto; /* 当内容过多时y轴出现滚动条 */
    /* background-color: red; */
  }
  .select {
    margin-top: 20px;
  }
  .select-bucket-title {
    margin-bottom: 40px;
  }
</style>
