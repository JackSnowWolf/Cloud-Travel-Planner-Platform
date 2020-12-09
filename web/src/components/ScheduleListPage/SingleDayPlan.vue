<template>
  <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="cardx">
        <div slot="header">
          <h3>Day {{ schedule.NumDate }}</h3>
        </div>
        <draggable class="list-group" :list="schedule.Details" group="people" @change="log">
          <div class="list-group-item" v-for="(element, index) in schedule.Details" :key="element.attractionId">{{ element.attractionName }} {{ index }}</div>
        </draggable>
      </vs-card>
    </vs-col>
  </vs-row>
  <!-- <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="cardx">
        <div v-for="(elements, key) in schedule" :key="key">
          <div slot="header">
            <h3>{{ elements.NumDate }}</h3>
          </div>
          <draggable class="list-group" :list="[elements]" group="people" @change="log">
            <div class="list-group-item" v-for="element in elements.Details" :key="element.attractionId">
              {{ element.attractionName }} -- {{ element.attractionId }} -->
  <!-- <div v-for="n in element.Details.length" :key="n">
                {{ element.Details[n] }}
              </div> -->
  <!-- </div>
          </draggable>
        </div>
      </vs-card>
    </vs-col>
  </vs-row> -->
</template>
<script>
  import draggable from "vuedraggable";
  export default {
    props: ["schedule", "scheduleChanged"],
    data() {
      return {
        changedItem: "",
      };
    },
    components: {
      draggable,
    },
    methods: {
      doMath: function(index) {
        return index + 1;
      },
      log: function(evt) {
        window.console.log(evt);
        console.log("wsfs", this.schedule);
        this.changedItem = this.schedule;
        this.$emit("scheduleChanged", this.changedItem);
        //   if (evt.added){
        //   console.log("wsigne",evt.added)}
        //   this.$emit("scheduleAdded",this.schedule)
      },
    },
    watch: {
      schedule(newSchedule) {
        this.schedule = newSchedule;
        console.log("watch!");
      },
    },
  };
</script>
