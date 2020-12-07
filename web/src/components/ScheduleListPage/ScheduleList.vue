<template>
  <el-table
    :data="tabledata.filter(data => !search || data.scheduleTitle.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%">
    <el-table-column
      label="scheduleTitle"
      prop="scheduleTitle">
    </el-table-column>
    <el-table-column
      label="targetArea"
      prop="targetArea">
    </el-table-column>
    <el-table-column
      align="right">
      <template slot="header">
        <el-input
          v-model="search"
          size="mini"
          placeholder="Type to search"/>
      </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
var apigClientFactory = require('aws-api-gateway-client').default;
export default {
    data() {
      return {
        userId:'test-editor',
        tabledata:[],
        search: '',
      }
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
        this.$router.push("/schedulelist/" + row.scheduleId);
      },
      handleDelete(index, row) {
        console.log(index, row);
      }
    },
    mounted(){
        var config = {invokeUrl:'https://n248ztw82a.execute-api.us-east-1.amazonaws.com/v1'}
        var apigClient = apigClientFactory.newClient(config);
        var pathParams = {
            // attractionId:'attr-0001',
        }
        var pathTemplate = '/schedule'
        var method = "GET";
        var additionalParams = {
    //If there are query parameters or headers that need to be sent with the request you can add them here
        headers: {
            // param0: '',
            // param1: ''
        },
        queryParams: {
            pageSize:'4',
            pageNo:'0',
            userId:this.userId
        }
    };
        var body = {
            //This is where you define the body of the request
        };

        apigClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then((response =>{
                if(response.status === 200){
                    // if response
                    console.log(response)
                    this.tabledata = response.data
                    //This is where you would put a success callback
                }
            }))
    }
  }
</script>
    