<template>
  <div class="attraction-container">
    <div class="infinite-list" style="overflow:auto">
      <div
        v-for="schedule in schedules"
        :schedule="schedule"
        :key="schedule.numDate"
        class="column is-one-quarter">
         <SingleDayPlan 
         :schedule="schedule"
         :scheduleChanged="scheduleChanged"
         v-on:scheduleChanged="getChangedSchedule"
         />
      </div>
    </div>
  </div>
</template>
<script>
import SingleDayPlan from "./SingleDayPlan"
export default {
  name: "EventsList",
  components: {
    SingleDayPlan,
  },
  data() {
    return {
      loading:false,
      emitflag:false,
      scheduleChanged:[],
      schedule: {},
      schedules:[
          {
              numDate:1,
              list: [
                    { name: "Melody", id: 1 },
                    { name: "Melodyy", id: 2 },
                    { name: "Jean", id: 3 },
                    { name: "Gerard", id: 4 }
                    ],
              description: "Happy day by day",},
          {
              numDate:2,
              list: [
                    { name: "John", id: 1 },
                    { name: "Joao", id: 2 },
                    { name: "Jean", id: 3 },
                    { name: "Gerard", id: 4 }
                    ],
              description: "Sad day by day",},
          {
              numDate:3,
              list: [
                    { name: "John", id: 1 },
                    { name: "Joao", id: 2 },
                    { name: "Jean", id: 3 },
                    { name: "Gerard", id: 4 }
                    ],
              description: "Dance day by day",},
          {   
              numDate:4,
              list: [
                    { name: "John", id: 1 },
                    { name: "Joao", id: 2 },
                    { name: "Jean", id: 3 },
                    { name: "Gerard", id: 4 }
                    ],
              description: "Jump day by day",},

      ]
    };
  },
  methods:{
    getChangedSchedule(item){
      if(this.emitflag){
        this.scheduleChanged = []
        this.scheduleChanged.push(item)
        // console.log("get",this.scheduleChanged)
        this.emitflag = false
      }else{
        this.scheduleChanged.push(item)
        // console.log("get",this.scheduleChanged)
      }
    }
  },
  watch:{
    scheduleChanged(newChanged){
      if(newChanged){
      // this.scheduleChanged.push(newChanged)
      // console.log("newchange",newChanged)
      this.$emit("newChange",newChanged)
      this.emitflag = true
      }
    } 
  }
//   methods:{
//       getItemAdded(item){
//           this.addAttraction = item
//           console.log("emit")
//           this.$emit('itemAdded',item)
//       }

//   }
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