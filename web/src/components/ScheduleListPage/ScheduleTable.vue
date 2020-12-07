<template>
  <h1>
      {{scheduleTable.scheduleContent.dayScheduleContents}}
  </h1>
</template>

<script>
var apigClientFactory = require('aws-api-gateway-client').default;
// import qs from 'qs';
export default {
    name:"scheduletable",
    data(){
        return{
            userId:'test-editor2',
            scheduleTable:[],
            scheduleId:"",
        }
    },
    methods:{
        async initData(){
            var config = {invokeUrl:'https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1'}
            var apigClient = apigClientFactory.newClient(config);
            var pathParams = {
                // attractionId:'attr-0001',
            }
            var pathTemplate = '/schedule/'+ this.scheduleId
            var method = "GET";
            var additionalParams = {
        //If there are query parameters or headers that need to be sent with the request you can add them here
            headers: {
                
                // param0: '',
                // param1: ''
            },
            queryParams: {
                // pageSize:'4',
                // pageNo:'0',
                userId:this.userId
            }
        };
            var body = {
                //This is where you define the body of the request
            };
            let isSuccess = false;
            let dayScheduleContents = []
            await apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body)
                .then((response =>{
                    if(response.status === 200){
                        // if response
                        // console.log(response)
                        this.scheduleTable = response.data
                        console.log( this.scheduleTable)
                        isSuccess = true
                        dayScheduleContents = response.data.scheduleContent.dayScheduleContents
                        //This is where you would put a success callback
                    }
                })).catch(err =>{
                    console.log(err)
                })
            if(isSuccess){
                return dayScheduleContents}
            else{return false}
            },
        getAttractionData(){

            this.initData().then((dayScheduleContents =>{
                if(dayScheduleContents){
                    var index;
                    var len = dayScheduleContents.length
                    // console.log(len)
                    for(index = 0;index<len;index++){
                       console.log(index,dayScheduleContents[index])
                       var dayScheduleContent = dayScheduleContents[index]
                       for(var item in dayScheduleContent){
                           console.log(dayScheduleContent[item])
                           this.getSingleAttraction(dayScheduleContent[item]).then((info =>
                           {
                               console.log(info)
                           }
                           )).catch(err=>{
                               console.log(err)
                           })
                       }
                    }
                    
                }
            }))
        },
        async getSingleAttraction(attractionId){
            var singleDetail = []
            console.log("es",attractionId)
            let id = attractionId
            await this.$axios
            .get("https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1/attraction/_search?q=" +id)
            .then((response) => {
                console.log(attractionId,response.data.results)
                singleDetail = response.data.results
            }).catch(err =>{
                    console.log(err)
                });
        return singleDetail
        }

        },
    created() {
        this.scheduleId = this.$route.params.scheduleId;
        console.log(this.scheduleId);
  },
    mounted(){
        this.getAttractionData()
    }
    


}
</script>

<style>

</style>