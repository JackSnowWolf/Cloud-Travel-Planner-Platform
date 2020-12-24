<template lang="html">
  <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
      <vs-card actionable class="attraction-card">
        <div slot="header">
          <h3>
            {{ attraction.attractionName }}
          </h3>
        </div>
        <div>
          <h3>{{ attraction.attractionDescription }}</h3>
          <h4>Estimate View Time: {{ attraction.estimateViewTime }} seconds</h4>
          <h4>Score: {{ attraction.score }}</h4>
        </div>
        <div slot="footer">
          <vs-row vs-justify="flex-end">
            <vs-button @click="popupActivo = true" color="primary" type="gradient">View</vs-button>
            <vs-popup title="Details" :active.sync="popupActivo">
              <h3>
                <span>
                  {{ attraction.attractionDescription }}
                </span>
              </h3>
              <vs-row vs-align="flex-end" vs-type="flex" vs-justify="space-between" vs-w="12">
                <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="6">
                  <div class="map">
                    <GmapMap
                      :center="{
                        lat: attraction.attractionLoc.lat,
                        lng: attraction.attractionLoc.lng,
                      }"
                      :zoom="14"
                      style="width: 300px; height: 300px"
                    >
                      <GmapMarker
                        :position="{
                          lat: attraction.attractionLoc.lat,
                          lng: attraction.attractionLoc.lng,
                        }"
                        :clickable="true"
                        :draggable="true"
                        @click="
                          center = {
                            lat: attraction.attractionLoc.lat,
                            lng: attraction.attractionLoc.lng,
                          }
                        "
                      />
                    </GmapMap>
                  </div>
                </vs-col>
                <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="5">
                  <div>
                    <img :src="attraction.attractionImgUrls[0]" style="width: 300px; height: 300px" />
                  </div>
                </vs-col>
              </vs-row>
              <!-- <vs-row>
                <el-button @click="handleLike" type="success" icon="el-icon-plus" circle></el-button>
                <el-button @click="handleDislike" type="info" icon="el-icon-minus" circle></el-button>
              </vs-row> -->
            </vs-popup>
            <vs-button @click="handleAdd" color="danger" type="gradient"><vs-icon icon="add_location"></vs-icon>Add</vs-button>
          </vs-row>
        </div>
      </vs-card>
    </vs-col>
  </vs-row>
</template>
<script>
  export default {
    props: {
      attraction: Object,
      addAttraction: Object,
    },
    name: "LocationSingleCard",
    data() {
      return {
        popupActivo: false,
        addItem: "",
        addLike: "",
        addDislike: "",
        latValue: 0,
        lngValue: 0,
      };
    },
    methods: {
      handleAdd() {
        console.log(this.attraction);
        this.addItem = this.attraction;
        this.$emit("itemAdded", this.addItem);
      },
      handleLike() {
        this.addLike = this.attraction;
        this.$emit("itemLike", this.addLike.attractionId);
      },
      handleDislike() {
        this.addDislike = this.attraction;
        console.log("dislike", this.attraction.attractionId);
        this.$emit("itemDislike", this.addDislike.attractionId);
      },
    },
    // mounted() {
    //   this.latValue = this.attraction.attractionLoc.lat;
    //   this.lngValue = this.attraction.attractionLoc.lng;
    // },
  };
</script>
<style scoped>
  .attraction-card {
    background: #9a92a5;
    background: linear-gradient(90deg, #9a92a5 0%, #efada3 100%);
  }
</style>
