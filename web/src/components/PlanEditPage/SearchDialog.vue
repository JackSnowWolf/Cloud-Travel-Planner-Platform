<template>
<div>
    <el-button type="warning" @click="dialogFormVisible = true">Add a new attraction</el-button>
    <el-dialog title="Add a new attraction" :visible.sync="dialogFormVisible">
        <el-form :model="form">
            <el-form-item label="Attraction name" :label-width="formLabelWidth">
            <el-input v-model="form.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Date to add" :label-width="formLabelWidth">
            <el-select v-model="form.region" placeholder="Please select a date">
                <el-option label="Zone No.1" value="shanghai"></el-option>
                <el-option label="Zone No.2" value="beijing"></el-option>
            </el-select>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="dialogFormVisible = false">Confirm</el-button>
        </span>
    </el-dialog>
</div>
</template>
<script>
  export default {
    data() {
      return {
        dialogFormVisible: false,
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
        formLabelWidth: '120px'
      };
    }
  };
</script>