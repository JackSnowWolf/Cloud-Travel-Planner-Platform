<template>
  <div class="attraction-container">
    <el-table style="width: 100%" height="500" :data="attractions">
      <el-table-column>
        <template slot-scope="props">
          <p>
            <LocationSingleCard
              :attraction="props.row"
              :addAttraction="addAttraction"
              v-on:itemAdded="getItemAdded"
              v-on:itemLike="getItemLike"
              v-on:itemDislike="getItemDislike"
            />
          </p>
        </template>
      </el-table-column>
      <!-- <el-table-column>
        <div v-for="attraction in attractions" :attraction="attraction" :key="attraction.attractionId">
          <LocationSingleCard :attraction="attraction" :addAttraction="addAttraction" v-on:itemAdded="getItemAdded" />
        </div>
      </el-table-column> -->
    </el-table>
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
  import LocationSingleCard from "./LocationSingleCard";
  export default {
    props: {
      AddItem: Object,
    },
    name: "LocationList",
    components: {
      LocationSingleCard,
    },
    data() {
      return {
        loading: false,
        addAttraction: "",
        likeAttraction: String,
        attractions: [],
        attraction: {},
      };
    },
    methods: {
      getItemAdded(item) {
        this.addAttraction = item;
        // console.log("emit");
        this.$emit("itemAdded", item);
      },
      getItemLike(item) {
        this.likeAttraction = item;
        // console.log("emit");
        this.$emit("itemLike", item);
      },
      getItemDislike(item) {
        this.dislikeAttraction = item;
        console.log("emit dislike");
        this.$emit("itemDislike", item);
      },
      getLocationList() {
        // console.log("elsticsearch!");
        this.$axios.get("https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1/attraction/_search?q=*:*").then((response) => {
          console.log("response", response.data.results);
          this.attractions = response.data.results;
          console.log(this.attractions);
        });
      },
    },
    mounted: function() {
      this.getLocationList();
    },
  };
</script>
<style scoped>
  .attraction-container {
    margin-top: 10px;
    margin-left: 10px;
    margin-right: 10px;
    text-align: center;
  }
</style>
