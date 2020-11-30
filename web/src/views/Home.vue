<template>
<el-container>
  <el-header> <MainNav /></el-header>
  <el-container>
    <!-- <el-aside width="200px">Aside</el-aside> -->
    <el-main>
      <section class = "banner">
        <div class = "banner-body">
          <h1 class="title">
            Almost 100,000 people have used our planner for their next trips
          </h1>
          <h2 class="subtitle">
            Start yout trip right now!
          </h2>
          <!-- <span class="doodle-bg" style="transform:rotateX(2.6435deg) rotateY(-4.9344deg) translateZ(-200px)">
                <img class="no_moon" img src="https://i.loli.net/2020/11/30/RTndCaxA3PL9JUi.jpg" />
          </span> -->
          <div class="createbn">
            <el-popover
            placement="top-start"
            title="Descirption"
            width="200"
            trigger="hover"
            content="Descirption Descirption Descirption">
            <el-button @click="createNew" type="primary" icon="el-icon-plus" slot="reference">hover Create My Next Trip Plan</el-button>
          </el-popover>
          </div>
          <div class="createbn">
            <el-popover
            placement="bottom"
            title="Descirption"
            width="200"
            trigger="hover"
            content="Descirption Descirption Descirption">
            <el-button @click="joinOne" type="primary" icon="el-icon-edit" slot="reference">Join One Trip Plan</el-button>
          </el-popover>
          </div>
        </div>
      </section>
    </el-main>
  </el-container>
</el-container>
</template>
<script >
import MainNav from "../components/Navbars/MainNav"
export default {
    name:"home",
    components:{MainNav},
    methods:{
      createNew(e) {
      e.preventDefault();
      this.$router.push("/createnew");
    },
      joinOne(e) {
      e.preventDefault();
      this.$router.push("/editor");
    },
    }


}
</script>
<style scoped>
.banner {
  text-align: center;
  background-image: url("https://i.loli.net/2020/11/30/RTndCaxA3PL9JUi.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 600px;
}
.title{
  font-size: 40px;
}
.subtitle {
  text-shadow: 4px 4px 4px rgba(45, 204, 106, 0.699);
  font-size: 20px;
}
.createbn{
  margin-top: 40px;
  /* margin-bottom: 40px; */
}
</style>>