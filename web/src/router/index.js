import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/home",
    name: "Home",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Home.vue")
  },
  {
    path: "/createnew",
    name: "createnew",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Preselect.vue")
    },
    {
      path: "/planedit",
      name: "planedit",
      component: () =>
        import(/* webpackChunkName: "about" */ "../views/PlanEdit.vue")
    },
    {
      path: "/review",
      name: "review",
      component: () =>
        import(/* webpackChunkName: "about" */ "../views/ReviewPage.vue")
      },
      {
        path: "/schedulelist",
        name: "schedulelist",
        component: () =>
          import(/* webpackChunkName: "about" */ "../views/ScheduleListPage")
      },
      {
        path: "/schedulelist",
        name: "schedulelist",
        component: () =>
          import(/* webpackChunkName: "about" */ "../views/ScheduleListPage")
      },
      {
        path: "/schedulelist/:scheduleId",
        name: "scheduleId",  
        component: () => import("../views/ScheduleSingle.vue"),
      }

];

const router = new VueRouter({
  routes
});

export default router;
