<template>
  <div class="page">
    <MainNav />
    <Slider />
    <div class="main">
      <el-row class="select">
        <el-col :span="24">
          <TimeLineList />
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
  import MainNav from "./Navbars/MainNav";
  import Slider from "./Navbars/Slider";
  import TimeLineList from "../components/ReviewPage/TimeLineList";
  export default {
    components: {
      MainNav,
      Slider,
      TimeLineList,
    },
  };
</script>
<style scoped>
  /* 主区域 */
  .page {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0px;
    background: rgb(34, 193, 195);
    background: linear-gradient(0deg, rgba(34, 193, 195, 1) 0%, rgba(253, 187, 45, 1) 100%);
  }
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
  .title {
    font-size: 40px;
  }
  .subtitle {
    text-shadow: 4px 4px 4px rgba(45, 204, 106, 0.699);
    font-size: 20px;
  }
  .chatbot {
    max-height: 200px;
    margin-top: 40px;
  }
</style>
