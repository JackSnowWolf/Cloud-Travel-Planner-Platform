<template>
  <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="cardx">
        <div slot="header">
          <h3>Day</h3>
        </div> 
      <draggable class="list-group" :list="schedule"  group="people" @change="log">
        <div
          class="list-group-item"
          v-for="(element,key) in schedule"
          :key="key"
        >
          {{ element }}
        </div>
      </draggable>
      </vs-card>
    </vs-col>
  </vs-row>
</template>
<script>
import draggable from "vuedraggable";
export default {
    props:['schedule','scheduleChanged'],
    data(){
        return{
            changedItem:""
        }
    },
    components: {
    draggable
  },
    methods: {
    log: function(evt) {
      window.console.log(evt);
    //   console.log("wsfs",this.schedule)
      this.changedItem = this.schedule
      this.$emit("scheduleChanged", this.changedItem)
    //   if (evt.added){
    //   console.log("wsigne",evt.added)}
    //   this.$emit("scheduleAdded",this.schedule)
    }
  },
//   watch:{
//       schedule(newSchedule){
//           this.schedule = newSchedule
//           console.log("watch!")
//       }
//   }
  
};
    
</script>