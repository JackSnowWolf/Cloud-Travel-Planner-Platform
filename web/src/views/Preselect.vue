<template>
  <el-container class="preselect">
    <el-aside width="250px">Slide Nav
        <Slider />
  </el-aside>
  <el-container>
      <el-header> 
          Pick Up Your Favorite Attractiones
      </el-header>
    <el-container>
  <el-aside width="500px">Attraction List
      <LocationList 
      v-on:itemAdded="getAddedItem"/>
  </el-aside>
    <!-- <el-header>Header</el-header> -->
    <el-main>Main
        <!-- {{this.add_attraction}} -->
        <LocationTable 
        :attractionAdd="add_attraction"
        class="table"/>
        <!-- <div class = "map">
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
      </div> -->
    </el-main>
  </el-container>
</el-container>
</el-container>
</template>
<script>
import LocationTable from "../components/CreatePage/LocationTable"
import LocationList from "../components/CreatePage/LocationList"
import Slider from "../components/Navbars/Slider"
// var apigClientFactory = require('aws-api-gateway-client').default
export default {
    name:"preselect",
    components:{
        LocationTable,
        LocationList,
        Slider},
    data(){
        return{
            add_attraction:{},
            userId:'test-editor'
        }
    },
    methods:{
        getAddedItem(t){
            this.add_attraction = t
            console.log(this.add_attraction)
        }
    },
    mounted(){}
}
</script>
<style scoped>
.preselect{
    background: rgb(252,198,135);
    background: linear-gradient(90deg, rgba(252,198,135,1) 0%, rgba(242,134,160,1) 100%);
}
.map{
    margin-top: 100px;
    margin-left: 40px;
}
.table{
    margin-top: 10px;
    margin-left: 20px;
}
</style>