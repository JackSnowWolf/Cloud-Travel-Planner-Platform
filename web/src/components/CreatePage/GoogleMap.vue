<template>
<div class = "map">
    <GmapMap
    :center="{lat: 70, lng: -40}"
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
</template>
<script>
import * as VueGoogleMaps from 'vue2-google-maps';
export default {
    name:'GoogleMap',
    props:{
        latValue: Number,
        lngValue: Number,
    },
    date(){
        return{

        }
    }
}
</script>