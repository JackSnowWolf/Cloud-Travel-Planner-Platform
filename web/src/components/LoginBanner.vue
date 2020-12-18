<template>
  <el-carousel :interval="5000" arrow="always" height="400px">
    <el-carousel-item v-for="(item, index) in banner" :key="index">
      <div class="bannerImg">
        <img :src="item.imgURL" style="width:100%;height:100%" />
      </div>
    </el-carousel-item>
  </el-carousel>
</template>
<script>
  export default {
    data() {
      return {
        banner: [
          {
            imgURL:
              "https://2486634c787a971a3554-d983ce57e4c84901daded0f67d5a004f.ssl.cf1.rackcdn.com/new-york-hotel-pennsylvania/media/hotelpenn-homepage-01-mobileheader-5cc091eb8cc0a.jpg",
          },
          {
            imgURL: "https://i.pinimg.com/736x/05/e3/ce/05e3cea39d8bc8ecc2eb878090a588ed.jpg",
          },
        ],
      };
    },
  };
</script>

<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
  }
  .bannerImg {
    width: 400px;
    height: 600px;
  }
</style>
