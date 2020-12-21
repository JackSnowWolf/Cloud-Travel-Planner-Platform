<template>
  <div class="attraction-container">
    <el-table style="width: 100%" height="550" :data="attractions" :header-cell-style="tableHeaderColor">
      <el-table-column fixed label="Click view to see details" :render-header="renderHeader">
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
    </el-table>
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
        addAttraction: {},
        likeAttraction: "",
        attractions: [],
        attraction: {},
        searchquery: "",
      };
    },
    methods: {
      //  modify the table header the background color
      tableHeaderColor({ rowIndex }) {
        if (rowIndex === 0) {
          return "background-color: #38576d; color: #debe90;font-weight: 600;";
        }
      },
      renderHeader() {
        return (
          <div>
            <el-row>
              <el-col span={16}>
                <el-input v-model={this.searchquery} size="mini" placeholder="enter key words to search" />
              </el-col>
              <el-col span={6} offset={2}>
                <el-button size="small" on-click={() => this.elasticSearch()}>
                  <span class="el-icon-search"></span> search
                </el-button>
              </el-col>
            </el-row>
          </div>
        );
      },
      elasticSearch() {
        var query = this.searchquery;
        console.log(query);
        this.$axios
          .get("https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1/attraction/_search?", {
            params: { q: JSON.stringify(query) },
          })
          .then((response) => {
            console.log("response", response.data.results);
            this.attractions = response.data.results;
            console.log(this.attractions);
          })
          .catch((err) => {
            console.log(err);
            this.attractions = [];
            this.$msg({
              type: "info",
              message: "No result find!",
            });
          });
      },
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
          // console.log("response", response.data.results);
          this.attractions = response.data.results;
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
    text-align: center;
  }
  .el-table {
    /* 表格字体颜色 */
    color: #6b3633;
    /* 表格边框颜色 */
    border: 0px solid #618cac;
    /* height: 500px; */
    background-color: rgba(148, 144, 144, 0.3);
  }
  .el-table th,
  .el-table tr,
  .el-table td {
    border: 0px;
    background-color: transparent;
  }
  .el-table thead {
    color: #9c8467;
    font-weight: 800;
    background-color: #618cac;
  }
</style>
