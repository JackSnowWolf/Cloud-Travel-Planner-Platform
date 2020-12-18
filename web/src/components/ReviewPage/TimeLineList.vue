<template>
  <div>
    <el-timeline>
      <el-table style="width: 100%" height="550" :data="dayScheduleContents">
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
    props: ["dayScheduleContents"],
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
    },
  };
</script>
