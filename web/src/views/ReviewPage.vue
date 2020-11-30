<template>
  <el-container class="review">
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
            <TimeLineList />
        </el-main>
        <el-footer>
          <el-row>
            <el-col :span="12">
              <div >
                <el-button type="warning" @click="handleSubmit">Submit</el-button>
              </div>
            </el-col>
            <el-col :span="12"><div >xx</div></el-col>
          </el-row>
        </el-footer>
        </el-container>
    </el-container>
  </el-container>
</template>
<script>
import TimeLineList from "../components/ReviewPage/TimeLineList"
import Slider from "../components/Navbars/Slider"
export default {
    name:"ReviewPage",
    components:{
        TimeLineList,
        Slider
    }
    
}
</script>

<style scoped>
.review{
  background: rgb(34,193,195);
  background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(253,187,45,1) 100%);
}
</style>