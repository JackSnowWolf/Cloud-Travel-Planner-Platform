<template>
<vs-row vs-justify="center">
<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
<vs-card actionable class="attraction-card">
<!-- <el-card class="box-card"  style="width: 90%"> -->
<div>
<el-table
    ref="multipleTable"
    :data="tableData"
    style="width: 100%"
    @selection-change="handleSelectionChange">
    <el-table-column
      type="selection"
      width="55">
    </el-table-column>
    <el-table-column
      label="index"
      width="120">
      <template slot-scope="scope">{{ scope.row.attractionName }}</template>
    </el-table-column>
    <el-table-column
      property="attractionName"
      label="Name"
      width="120">
    </el-table-column>
    <el-table-column
      property="attractionName"
      label="Address"
      show-overflow-tooltip>
    </el-table-column>
  </el-table>
  <div style="margin-top: 20px">
    <el-button @click="handleSumbit">Select Submit</el-button>
    <el-button @click="toggleSelection()">Clear selection</el-button>
  </div>
</div>
<!-- </el-card> -->
</vs-card>
</vs-col>
</vs-row>
</template>

<script>
  export default {
    props:{
      attractionAdd:Object,
    },
    data() {
      return {
        tableData: [],
        // tableData: [{
        //   location: '2016-05-03',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }, {
        //   location: '2016-05-02',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }, {
        //   location: '2016-05-04',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }, {
        //   location: '2016-05-01',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }, {
        //   location: '2016-05-08',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }, {
        //   location: '2016-05-06',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }, {
        //   location: '2016-05-07',
        //   name: 'Tom',
        //   address: 'No. 189, Grove St, Los Angeles'
        // }],
        multipleSelection: []
      }
    },
    methods: {
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
        // console.log("selection",this.multipleSelection)
      },
      handleSumbit(e){
        e.preventDefault();
        console.log("selection",this.multipleSelection)
        if(this.multipleSelection){
        this.$msgbox.confirm('Submit your plan now?', 'Warning', {
          confirmButtonText: 'OK',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.$router.push("/planedit")
          this.$msg({
          type: 'success',
          message: 'You are redirecting to your next step' 
        });
      }).catch(() => {
        this.$msg({
          type: 'info',
          message: 'Canceled to start a new plan'
        });       
      }); 
        }
      }
    },
    watch:{
      attractionAdd(newAttraction){
        this.tableData.push(newAttraction)
      }
    }
  }
</script>
<style scoped>
.table{
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>