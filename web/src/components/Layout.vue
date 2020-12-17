<template>
  <div>
    <MainNav class="header" />
    <Slider />
    <div class="main">
      <h1 class="title">
        Almost 100,000 people have used our planner for their next trips
      </h1>
      <h2 class="subtitle">
        Start yout trip right now!
      </h2>
      <el-row class="select">
        <el-col :span="24">
          <h4 class="select-bucket-title">Please Select Your Main Destination</h4>
          <UserPerference />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24" class="select-bucket">
          <h4 class="select-bucket-title">Try To Talk With Our Bot to Have Some Ideas</h4>
          <Chatbot />
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
  import MainNav from "./Navbars/MainNav";
  import Slider from "./Navbars/Slider";
  import UserPerference from "../components/CustomlizePage/UserPerference";
  import Chatbot from "../components/Chatbot/Chatbot";
  export default {
    components: {
      MainNav,
      Slider,
      UserPerference,
      Chatbot,
    },
  };
</script>
<style scoped>
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
