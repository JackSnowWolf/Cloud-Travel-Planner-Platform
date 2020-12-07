<template lang="html">
    <vs-row vs-justify="center">
    <vs-col type="flex" vs-justify="center" vs-align="center" vs-w="8">
      <vs-card actionable class="attraction-card">
        <div slot="header">
          <h3>
            {{attraction.attractionName}}
          </h3>
        </div>
        <div slot="media">
          <!-- <img :src="$withBase('/card.png')"> -->
        </div>
        <div>
          <span>
            {{ attraction.attractionDescription}}
          </span>
        </div>
        <div slot="footer"> 
          <vs-row vs-justify="flex-end">
            <vs-button @click="popupActivo=true" color="primary" type="gradient">View</vs-button>
             <vs-popup title="fullscreen" :active.sync="popupActivo">
               <span>
               {{attraction.attractionDescription}}
               {{attraction.attractionLoc.lat}}
               {{attraction.attractionDescription.lng}}
               <div class = "map">
                <GmapMap
                :center="{lat:latValue, lng: lngValue}"
                :zoom="14"
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
              </span>
              </vs-popup>
            <vs-button @click="handleAdd" color="danger" type="gradient">Add</vs-button>
          </vs-row>
        </div>
      </vs-card>
    </vs-col>
  </vs-row>
</template>
<script>

export default {
  props:{
    attraction: Object,
    addAttraction:Object,
  },
  name:"LocationSingleCard",
  components:[
  ],
  data(){
    return{
    popupActivo:false,
    addItem:"",
    latValue:Number,
    lngValue:Number,
    }
  },
  methods:{
    handleAdd(){
      console.log(this.attraction)
      this.addItem = this.attraction
      this.$emit("itemAdded",this.addItem)
    }
  },
  mounted(){
    this.latValue = this.attraction.attractionLoc.lat;
    this.lngValue = this.attraction.attractionLoc.lng;
  }
  
}
</script>