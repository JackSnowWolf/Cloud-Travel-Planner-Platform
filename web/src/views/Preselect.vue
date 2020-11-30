<template>
  <el-container>
  <el-aside width="600px">Aside
      <LocationTable />
  </el-aside>
  <el-container>
    <!-- <el-header>Header</el-header> -->
    <el-main>Main
        <div class = "map">
        <GmapMap
        :center="{lat: 40, lng: -74}"
        :zoom="7"
        style="width: 500px; height: 500px"
        >
        <GmapMarker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        :clickable="true"
        :draggable="true"
        @click="center=m.position"
        />
        </GmapMap>
      </div>
    </el-main>
  </el-container>
</el-container>
</template>
<script>
import LocationTable from "../components/CreatePage/LocationTable"
export default {
    name:"preselect",
    components:{LocationTable}
}
</script>
<style scoped>
.map{
    margin-top: 100px;
    margin-left: 40px;

}
</style>