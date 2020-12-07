<template>
  <el-container>
    <el-main>
    <ScheduleList />
    </el-main>
  </el-container>
</template>
<script>
import ScheduleList from '../components/ScheduleListPage/ScheduleList'
export default {
    name:"ScheduleListPage",
    components:{
        ScheduleList,
    }

}
</script>