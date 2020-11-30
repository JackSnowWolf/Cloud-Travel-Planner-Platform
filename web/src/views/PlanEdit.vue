<template>
  <el-container class="planedit">
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
  </el-container>
</template>
<script>
import SearchDialog from "../components/PlanEditPage/SearchDialog"
import Slider from "../components/Navbars/Slider"
import PlanList from "../components/PlanEditPage/PlanList";
export default {
    components:{
        PlanList,
        Slider,
        SearchDialog,
    },
methods:{
    getChangedSchedule(item){
      console.log("getchanged",item)
    },
    handleSubmit(){
      this.$msgbox.confirm('Submit your plan now?', 'Warning', {
          confirmButtonText: 'OK',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
        this.$router.push("/review")
        this.$msg({
          type: 'success',
          message: 'Your are redirecting to your next step'
        });
    }).catch(() => {
      this.$msg({
        type: 'info',
        message: 'Canceled'
      });       
    });
    }
  },

}
</script>
<style scoped>
.planedit{
  background: rgb(34,193,195);
  background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(253,187,45,1) 100%);
}
</style>