<template>
  <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="cardx">
        <div slot="header">
          <h3>{{ schedule.NumDate }}</h3>
        </div>
        <draggable class="list-group" :list="schedule.Details" group="people" @change="log">
          <div class="list-group-item" v-for="(element, index) in schedule.Details" :key="element.attractionId">{{ element.attractionName }} {{ index }}</div>
        </draggable>
        <div slot="footer">
          <vs-row vs-justify="flex-end">
            <vs-button type="gradient" color="success" @click="popupActivo = true">
              <vs-icon icon="public"></vs-icon>
            </vs-button>
            <vs-popup class="holamundo" title="Google Map" :active.sync="popupActivo">
              <div>
                <gmap-map :center="center" :zoom="10" style="width: 300%; height: 300px">
                  <gmap-marker v-for="(item, key) in schedule.Details" :key="key" :position="getPosition(item)" :clickable="true"> </gmap-marker>
                </gmap-map>
              </div>
            </vs-popup>
          </vs-row>
        </div>
      </vs-card>
    </vs-col>
  </vs-row>
</template>
<script>
  import draggable from "vuedraggable";
  export default {
    props: ["schedule", "scheduleChanged"],
    data() {
      return {
        changedItem: [],
        popupActivo: false,
        center: {
          lat: 42.77,
          lng: -73.5,
        },
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
        // console.log("wsfs", this.schedule.Details);
        var Details = this.schedule.Details;
        var tempchange = [];
        // this.changedItem = this.schedule.Detials;
        for (var i = 0; i < Details.length; i++) {
          tempchange.push(Details[i].attractionId);
        }
        console.log("list", tempchange);
        this.changedItem.push({
          Details: tempchange,
          NumDate: this.schedule.NumDate,
        });
        this.$emit("scheduleChanged", this.changedItem);
        //   if (evt.added){
        //   console.log("wsigne",evt.added)}
        //   this.$emit("scheduleAdded",this.schedule)
      },
      getPosition: function(marker) {
        return {
          lat: parseFloat(marker.attractionLoc.lat),
          lng: parseFloat(marker.attractionLoc.lng),
        };
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
<style scoped>
  .cardx {
    background: #7f867b;
    color: #e5d8ca;
  }
</style>
