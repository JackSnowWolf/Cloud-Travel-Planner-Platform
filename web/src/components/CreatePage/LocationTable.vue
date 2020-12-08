<template>
<vs-row vs-justify="center">
<vs-col type="flex" vs-justify="center" vs-align="center" vs-w="10">
<vs-card actionable class="attraction-card">
<!-- <el-card class="box-card"  style="width: 90%"> -->
<div>
<el-table
    :data="tableData"
    span-method="tableSpanMethod"
    style="width: 100%"
    @selection-change="handleSelectionChange">
  <!-- <li v-for="(value,key) in tableData" :key="key">
     {{value}}
  </li> -->
    <el-table-column
      type="selection"
      width="55">
    </el-table-column>
    <el-table-column
      property="attractionName"
      label="Name"
      width="200">
    </el-table-column>
    <el-table-column
      property="attractionId"
      label="attractionId"
      width="200"
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
var apigClientFactory = require('aws-api-gateway-client').default
  export default {
    props:{
      attractionAdd:Object,
      userId:String,
    },
    data() {
      return {
        tableData: [],
        scheduleId:"",
        attracationIdList:[],
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
      setScheduleId(){
            this.scheduleId = this.$route.params.scheduleId;
        },
      async initDataTable(){
        console.log("init Preselect table",this.scheduleId,this.userId)
        this.tableData = []
        this.attracationIdList = []
        var config = {invokeUrl:'https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1'}
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
              scheduleId: this.scheduleId,
        }
        // console.log(this.scheduleId,addItem.attractionId)
        var pathTemplate = '/schedule/{scheduleId}'
        var method = "GET";
        var additionalParams = {
    //If there are query parameters or headers that need to be sent with the request you can add them here
        headers: {           
            // param0: '',
            // param1: ''
        },
        queryParams: {
            userId:this.userId
        }
    };
        var body = {
            //This is where you define the body of the request
        };
        await apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then((response =>{
                if(response.status === 200){
                    // if response
                    console.log("Get resp",response.data.scheduleContent)
                    var object = response.data.scheduleContent;
                    for(var attracationId in object){
                      console.log(attracationId,object[attracationId])
                      this.attracationIdList.push(attracationId)
                      this.tableData.push(object[attracationId])
                    }
                    // this.tableData.push(response.data.scheduleContent)
                    // this.tableData = response.data.scheduleContent
                }
            })).catch(err =>{
                console.log(err)
            })      
      },
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
        console.log("selection",this.multipleSelection)

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
          this.submitSelection(this.multipleSelection)
          // this.$router.push("/planedit")
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
      },
      async submitSelection(selection){
        for (var i=0,len=selection.length; i<len; i++)
          { 
            var submitid = selection[i].attractionId
            console.log(selection[i].attractionId)
            var config = {invokeUrl:'https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1'}
            var apigClient = apigClientFactory.newClient(config);
            var pathParams = {
                scheduleId: this.scheduleId,
                attractionId: submitid,
            }
            // console.log(this.scheduleId,addItem.attractionId)
            var pathTemplate = '/schedule/{scheduleId}/attraction/{attractionId}'
            var method = "POST";
            var additionalParams = {
        //If there are query parameters or headers that need to be sent with the request you can add them here
            headers: {           
                // param0: '',
                // param1: ''
            },
            queryParams: {
                userId:this.userId
            }
        };
            var body = {
                //This is where you define the body of the request
            };
            await apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body)
                .then((response =>{
                    if(response.status === 200){
                        // if response
                        console.log("post!")
                        // this.tableData.push(response.data.scheduleContent)
                        // this.tableData = response.data.scheduleContent
                    }
                })).catch(err =>{
                    console.log(err)
                })      


          }   
      }
    },
    watch:{
      attractionAdd(newAttraction){
        console.log(newAttraction)
        this.initDataTable()
      },
    },
    created(){
        this.setScheduleId()
    },
    mounted(){
      this.initDataTable()
    }
  }
</script>
<style scoped>
.table{
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>