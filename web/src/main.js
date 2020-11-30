import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Amplify, * as AmplifyModules from 'aws-amplify'
import { Auth } from 'aws-amplify';
import { AmplifyPlugin } from 'aws-amplify-vue'
import { AmplifyEventBus } from 'aws-amplify-vue';
import awsconfig from './aws-exports'
import 'element-ui/lib/theme-chalk/index.css';

import { Button, Select, Menu, MenuItem, Submenu,
  Header,Container,Aside,Main,Popover,
  Table,TableColumn,Input,Card 
} from 'element-ui';

import * as VueGoogleMaps from 'vue2-google-maps'

Vue.component(Button.name, Button);
Vue.component(Select.name, Select);
Vue.use(Menu).use(MenuItem).use(Submenu);
Vue.use(Header).use(Container).use(Aside).use(Main).use(Popover);
Vue.use(Table).use(TableColumn).use(Input).use(Card);



Amplify.configure(awsconfig)
// >>New - Configuring Auth Module
Auth.configure(awsconfig);
Vue.use(AmplifyPlugin, AmplifyModules)
Vue.use(AmplifyEventBus)

Vue.config.productionTip = false;

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCJY8RqCzMtqYEjQMimzTPOF7UPzh_s04g',
    libraries: 'places', 
    region: 'US',
    language:'en-US'// This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)
 
    //// If you want to set the version, you can do so:
    // v: '3.26',
  },
});


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");