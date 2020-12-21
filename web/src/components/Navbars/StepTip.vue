<template>

  <div id="parentx">

    <vs-button @click="active=!active" color="primary" type="filled">Open Sidebar</vs-button>
    <vs-sidebar position-right  parent="body" default-index="1"  color="primary" class="sidebarx" spacer v-model="active">

      <vs-sidebar-item index="1" icon="question_answer">
        Dashboard
      </vs-sidebar-item>

      <vs-sidebar-item index="2" icon="gavel">
        History
      </vs-sidebar-item>

      <vs-sidebar-item index="3" icon="verified_user">
        Configurations
      </vs-sidebar-item>

      <vs-sidebar-item index="4" icon="account_box">
        Profile
      </vs-sidebar-item>
    </vs-sidebar>
  </div>

</template>

<script>
export default {
  data:()=>({
    active:false,
  })
}
</script>