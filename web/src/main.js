import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Amplify, * as AmplifyModules from 'aws-amplify'
import { Auth } from 'aws-amplify';
import { AmplifyPlugin } from 'aws-amplify-vue'
import { AmplifyEventBus } from 'aws-amplify-vue';
import awsconfig from './aws-exports'
Amplify.configure(awsconfig)
// >>New - Configuring Auth Module
Auth.configure(awsconfig);
Vue.use(AmplifyPlugin, AmplifyModules)
Vue.use(AmplifyEventBus)

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");