<template>
  <div class="about">
    <amplify-connect :query="listTodosQuery">
      <template slot-scope="{ loading, data, errors }">
        <div v-if="loading">
          Loading...
        </div>
        <div v-if="errors.length > 0">Errors</div>
        <div v-else-if="data">
          {{ data }}
        </div>
      </template>
    </amplify-connect>
  </div>
</template>
<script>
import { components } from "aws-amplify-vue";
import travel_planner_api from "../travel-planner-api.yaml";  
const ListTodoQuery = `query ListTodos {
    listTodos {
      items {
        id
        name
        description
      }
    }
  }
  `;
export default {
  components: {
    ...components
  },
  computed: {
    listTodosQuery() {
      console.log(travel_planner_api)
      return this.$Amplify.graphqlOperation(ListTodoQuery);
    }
  }
};
</script>