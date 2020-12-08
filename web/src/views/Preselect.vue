<template>
  <el-container class="preselect">
    <el-aside width="250px">Slide Nav
        <Slider />
  </el-aside>
  <el-container>
      <el-header> 
          Pick Up Your Favorite Attractiones
      </el-header>
    <el-container>
  <el-aside width="500px">Attraction List
      <LocationList 
      v-on:itemAdded="getAddedItem"/>
  </el-aside>
    <!-- <el-header>Header</el-header> -->
    <el-main>Main
        <!-- {{this.add_attraction}} -->
        <LocationTable 
        :attractionAdd="add_attraction"
        :scheduleId="scheduleId"
        :userId="userId"
        class="table"/>
    </el-main>
  </el-container>
</el-container>
</el-container>
</template>
<script>
import LocationTable from "../components/CreatePage/LocationTable"
import LocationList from "../components/CreatePage/LocationList"
import Slider from "../components/Navbars/Slider"
var apigClientFactory = require('aws-api-gateway-client').default
export default {
    name:"preselect",
    components:{
        LocationTable,
        LocationList,
        Slider},
    data(){
        return{
            add_attraction:{},
            userId:'test-editor',
            scheduleId:""
        }
    },
    methods:{
        setScheduleId(){
            this.scheduleId = this.$route.params.scheduleId;
        },
        getAddedItem(t){
            this.add_attraction = t
            console.log(this.add_attraction)
            this.putIntoScheduleContent(t)
        },
        async putIntoScheduleContent(addItem){
            var config = {invokeUrl:'https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1'}
            var apigClient = apigClientFactory.newClient(config);
            var pathParams = {
                 scheduleId: this.scheduleId,
                 attractionId:addItem.attractionId
            }
            // console.log(this.scheduleId,addItem.attractionId)
            var pathTemplate = '/schedule/{scheduleId}/attraction/{attractionId}'
            var method = "PUT";
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
            let isSuccess = false;
            await apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body)
                .then((response =>{
                    if(response.status === 200){
                        // if response
                        console.log("post resp",response)
                        isSuccess = true
                        //This is where you would put a success callback
                    }
                })).catch(err =>{
                    console.log(err)
                })
            if(isSuccess){
                return isSuccess}
            else{return false}
        }
    },
    created(){
        this.setScheduleId()
    },
    // mounted(){

    // }
}
</script>
<style scoped>
.preselect{
    background: rgb(252,198,135);
    background: linear-gradient(90deg, rgba(252,198,135,1) 0%, rgba(242,134,160,1) 100%);
}
.map{
    margin-top: 100px;
    margin-left: 40px;
}
.table{
    margin-top: 10px;
    margin-left: 20px;
}
</style>