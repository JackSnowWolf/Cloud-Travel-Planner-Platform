<template>
  <div>
    <el-timeline>
      <el-table
        style="width: 100%"
        height="600"
        :data="dayScheduleContents"
        :row-style="getRowClass"
        :header-row-style="getRowClass"
        :header-cell-style="getRowClass"
      >
        <el-table-column label="Your Final Schedule">
          <template slot-scope="props">
            <el-timeline-item :timestamp="props.row.NumDate" placement="top">
              <el-card shadow="hover">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div v-for="(item, index) in props.row.Details" :item="item" :key="index">
                      <h4>{{ index + 1 }} -- {{ item.attractionName }}</h4>
                      <!-- <h4>{{ item.attractionImgUrls }}</h4> -->
                      <div>
                        <img :src="item.attractionImgUrls[0]" width="50" height="50" />
                      </div>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div>
                      <!-- {{ props.row.Details[0].attractionLoc }} -->
                      <gmap-map :center="center" :zoom="12" style="width: 300%; height: 300px">
                        <gmap-marker v-for="(item, key) in props.row.Details" :key="key" :position="getPosition(item)" :clickable="true"> </gmap-marker>
                      </gmap-map>
                    </div>
                  </el-col>
                </el-row>
                <p>Some Text</p>
              </el-card>
            </el-timeline-item>
            <!-- </div> -->
          </template>
        </el-table-column>
      </el-table>
    </el-timeline>
  </div>
</template>
<script>
  export default {
    name: "TimeLineComponent",
    props: {
      dayScheduleContents: {
        type: Array,
        default() {
          return [];
        },
      },
    },
    // props: ["dayScheduleContents"],
    data() {
      return {
        center: {
          lat: 40.71852,
          lng: -73.83635,
        },
      };
    },
    methods: {
      getPosition: function(marker) {
        return {
          lat: parseFloat(marker.attractionLoc.lat),
          lng: parseFloat(marker.attractionLoc.lng),
        };
      },
      getRowClass() {
        return "background:transparent;color:#000;";
      },
    },
  };
</script>
<style scoped>
  .el-table {
    /* 表格字体颜色 */
    color: #3c1507;
    /* 表格边框颜色 */
    border: 5px solid #425d8a;
    /* height: 500px; */
    background-color: #ebe7de;
  }
  .el-table th,
  .el-table tr,
  .el-table td {
    border: 0;
    background-color: transparent;
  }
  .el-table thead {
    color: #9c8467;
    font-weight: 800;
    background-color: rgba(148, 144, 144, 0.3);
  }
</style>
