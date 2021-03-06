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
    path: "/customlimze",
    name: "customlimze",  
    component: () => import("../views/Customlize.vue"),
  },
  {
    path: "/createnew/:scheduleId",
    name: "createnew",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Preselect.vue")
    },
    {
      path: "/planedit/:scheduleId",
      name: "planedit",
      component: () =>
        import(/* webpackChunkName: "about" */ "../views/ScheduleSingle.vue")
    },
    {
      path: "/review/:scheduleId",
      name: "review",
      component: () =>
        import(/* webpackChunkName: "about" */ "../views/ReviewPage.vue")
      },
      {
        path: "/schedulelist/:userId",
        name: "schedulelist",
        component: () =>
          import(/* webpackChunkName: "about" */ "../views/ScheduleListPage")
      },
      {
        path: "/scheduleedit/:scheduleId",
        name: "scheduledetails",  
        component: () => import("../views/ScheduleSingle.vue"),
      },
      {
        path: "/accept/schedule",
        query:"editorId:'userId',scheduleId:'scheduleId",
        name: "acceptInvitation", 
        component: () => import("../views/AcceptInvitation.vue"),
      },
      {
        path: "/layout",
        name: "layout", 
        component: () => import("../components/Layout.vue"),
      },
      {
        path:"/info",
        name:"info",
        component: () => import("../views/Info.vue"),
      },
      {
        path:"/chatroom/schedule/:scheduleId",
        name:"chatroom",
        component: () => import("../views/Chatroom.vue"),
      }


];

const router = new VueRouter({
  routes
});

export default router;
