<template>
  <div class="attraction-container">
    <!-- <el-table
    style="width: 100%"
    height="600">
    <el-table-column
    label="attraction"> -->
    <div
    v-for="attraction in attractions"
    :attraction="attraction"
    :key="attraction.attractionId">
    <LocationSingleCard 
         :attraction="attraction"
         />
          </div>
    <!-- </el-table-column> -->
      <!-- </div> -->
      <!-- <div
        v-for="attraction in attractions"
        :attraction="attraction"
        :key="attraction.index"
        class="column is-one-quarter">
         <LocationSingleCard 
         :attraction="attraction"
         :addAttraction="addAttraction"
         v-on:itemAdded="getItemAdded"
         />
      </div> -->
    <!-- </el-table> -->
  </div>
</template>
<script>
import LocationSingleCard from "./LocationSingleCard"
export default {
  props:{
      AddItem:Object
  },
  name: "LocationList",
  components: {
    LocationSingleCard,
  },
  data() {
    return {
      loading:false,
      addAttraction:"",
      attractions:[],
      attraction: {},
      // attractions:[
      //     {
      //         index:1,
      //         attractionName:"Melody",
      //         description: "Happy day by day",},
      //     {
      //         index:2,
      //         attractionName:"Melodyyy",
      //         description: "Sad day by day",},
      //     {
      //         index:3,
      //         attractionName:"Bytedance",
      //         description: "Dance day by day",},
      //     {   
      //         index:4,
      //         attractionName:"Bitjump",
      //         description: "Jump day by day",},
      //     {
      //         index:4,
      //         attractionName:"Clever",
      //         description: "Clever day by day",},
      //     {
      //         index:5,   
      //         attractionName:"Smart",
      //         description: "Smart day by day",},

      // ]
    };
  },
  methods:{
      getItemAdded(item){
          this.addAttraction = item
          console.log("emit")
          this.$emit('itemAdded',item)
      },
      getLocationList(){
        console.log("elsticsearch!")
        this.$axios
        .get("https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1/attraction/_search?q=*:*")
        .then((response) => {
          console.log("response",response.data.results)
          this.attractions = response.data.results
          console.log(this.attractions)
          // if (response.data.status == "success") {
          //   this.events = response.data.data;
          //   console.log(this.events);
          // } else window.alert("Failed");
      });
      }

  },
    mounted: function () {
      this.getLocationList();
  }, 
};
</script>
<style scoped>
.attraction-container {
  margin-top: 10px;
  margin-left:10px;
  margin-right:10px;
  text-align: center;
}
</style>
