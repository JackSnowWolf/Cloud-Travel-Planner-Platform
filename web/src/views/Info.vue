<template>
  <div class="page">
    <MainNav />
    <div class="main">
      <el-row>
        <el-col :span="24"> </el-col>
        <h2>See our best practice</h2>
      </el-row>
      <el-row>
        <el-col :span="24"> </el-col>
        <h1>Last call for your holiday trips!</h1>
      </el-row>
      <el-row>
        <iframe src="https://proj-attr-info.s3.amazonaws.com/city-guide-new-york.pdf" width="100%" height="600px" frameborder="1"> </iframe>
        <!-- <div class="con-example-images">
            <vs-images>
              <vs-image :key="index" :src="`https://picsum.photos/400/400?image=2${index}`" v-for="(image, index) in 9" />
              <vs-image :key="index" :src="`https://picsum.photos/400/400?image=1${index}`" v-for="(image, index) in 7" />
            </vs-images>
          </div> -->
      </el-row>
    </div>
  </div>
</template>
<script>
  import MainNav from "../components/Navbars/MainNav";
  export default {
    components: {
      MainNav,
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
    background-image: url("https://proj-for-attraction-photos.s3.amazonaws.com/trip-bg-1.jpeg");
    background-size: cover;
    background-color: #abb8b5;
  }
  .main {
    position: absolute;
    top: 50px;
    left: 0px;
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
  .con-example-images {
    max-height: 500px;
    overflow: auto;
  }
</style>
