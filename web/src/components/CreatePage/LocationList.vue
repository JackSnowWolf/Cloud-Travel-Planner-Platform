<template>
  <div class="attraction-container">
    <div class="infinite-list" style="overflow:auto">
      <div
        v-for="attraction in attractions"
        :attraction="attraction"
        :key="attraction.index"
        class="column is-one-quarter">
         <LocationSingleCard 
         :attraction="attraction"
         :addAttraction="addAttraction"
         v-on:itemAdded="getItemAdded"
         />
      </div>
    </div>
  </div>
</template>
<script>
import LocationSingleCard from "./LocationSingleCard"
export default {
  props:{
      AddItem:Object
  },
  name: "EventsList",
  components: {
    LocationSingleCard,
  },
  data() {
    return {
      count: 3,
      loading:false,
      attraction: {},
      maxcount:5,
      addAttraction:"",
      attractions:[
          {
              index:1,
              attractionName:"Melody",
              description: "Happy day by day",},
          {
              index:2,
              attractionName:"Melodyyy",
              description: "Sad day by day",},
          {
              index:3,
              attractionName:"Bytedance",
              description: "Dance day by day",},
          {   
              index:4,
              attractionName:"Bitjump",
              description: "Jump day by day",},
        //   {
        //       index:4,
        //       attractionName:"Clever",
        //       description: "Clever day by day",},
        //   {
        //       index:5,   
        //       attractionName:"Smart",
        //       description: "Smart day by day",},

      ]
    };
  },
  methods:{
      getItemAdded(item){
          this.addAttraction = item
          console.log("emit")
          this.$emit('itemAdded',item)
      }

  }
//     mounted: function () {
//     console.log("start!")
//     this.$axios
//       .get("/api/query/AllEvent")
//       .then((response) => {
//         if (response.data.status == "success") {
//           this.events = response.data.data;
//           console.log(this.events);
//         } else window.alert("Failed");
//       });
//   }, 
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
