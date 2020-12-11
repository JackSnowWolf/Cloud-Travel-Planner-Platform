<template>
  <div>
    <el-timeline>
      <el-table style="width: 100%" height="500" :data="dayScheduleContents">
        <el-table-column label="Your Final Schedule">
          <template slot-scope="props">
            <!-- <div v-for="(schedule, key) in dayScheduleContents" :schedule="schedule" :key="key"> -->
            <el-timeline-item timestamp="2018/4/12" placement="top">
              <el-card shadow="hover">
                <div v-for="(item, index) in props.row.Details" :item="item" :key="index">
                  <h4>{{ index + 1 }} -- {{ item.attractionName }}</h4>
                  <!-- <h4>{{ item.attractionImgUrls }}</h4> -->
                  <div>
                    <img :src="item.attractionImgUrls[1]" width="50" height="50" />
                  </div>
                </div>
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
  };
</script>
