<template>
  <el-select v-model="value" placeholder="Select">
    <el-option v-for="item in cities" :key="item.value" :label="item.label" :value="item.value">
      <span style="float: left">{{ item.label }}</span>
      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
    </el-option>
  </el-select>
</template>
<script>
  export default {
    name: "TargetAreaPerference",
    data() {
      return {
        cities: [
          {
            value: "NewYork",
            label: "NewYork",
          },
          {
            value: "Shanghai",
            label: "Shanghai",
          },
          {
            value: "Nanjing",
            label: "Nanjing",
          },
          {
            value: "Chengdu",
            label: "Chengdu",
          },
          {
            value: "Shenzhen",
            label: "Shenzhen",
          },
          {
            value: "Guangzhou",
            label: "Guangzhou",
          },
        ],
        value: "",
      };
    },
    watch: {
      value(newVal) {
        //   console.log("newval",newVal)
        this.$emit("pickArea", newVal);
      },
    },
  };
</script>
