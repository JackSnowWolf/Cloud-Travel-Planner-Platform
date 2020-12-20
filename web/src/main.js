import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from 'axios'
import Amplify, * as AmplifyModules from 'aws-amplify'
import { Auth } from 'aws-amplify';
import { AmplifyPlugin } from 'aws-amplify-vue'
import { AmplifyEventBus } from 'aws-amplify-vue';
import awsconfig from './aws-exports'
import 'element-ui/lib/theme-chalk/index.css';
import 'material-icons/iconfont/material-icons.css';
// import Loading from './plugins/loading'



import { Button, Select, Menu, MenuItem, Submenu,
  Header,Container,Aside,Main,Popover,Footer,
  Table,TableColumn,Input,Card,Divider,
  Step,Steps,Col,Row,RadioButton,RadioGroup,MenuItemGroup,
  Form,FormItem,Option,Dialog, Timeline, TimelineItem, Scrollbar,
  Carousel,CarouselItem 

} from 'element-ui';
import { MessageBox } from 'element-ui';
Vue.prototype.$msgbox = MessageBox
import { Message } from 'element-ui';
Vue.prototype.$msg = Message

import { vsButton, vsSelect, vsPopup, vsCard,vsRow, vsCol, vsIcon, 
  vsSideBar, vsDivider, vsSpacer, vsInput,vsImages} from 'vuesax';
import 'vuesax/dist/vuesax.css';

import * as VueGoogleMaps from 'vue2-google-maps';
import infiniteScroll from "vue-infinite-scroll";
Vue.use(infiniteScroll);

// Vue.use(Loading)
Vue.prototype.$axios = axios //全局注册，使用方法为:this.$axios          
Vue.component(Button.name, Button);
Vue.component(Select.name, Select);
Vue.use(Menu).use(MenuItem).use(Submenu);
Vue.use(Header).use(Container).use(Aside).use(Main).use(Footer).use(Popover);
Vue.use(Table).use(TableColumn).use(Input).use(Card).use(Step).use(Steps);
Vue.use(Col).use(Row).use(RadioButton).use(RadioGroup).use(MenuItemGroup)
    .use(FormItem).use(Option).use(Form).use(Dialog).use(Timeline).use(TimelineItem)
    .use(Scrollbar).use(Divider).use(Carousel).use(CarouselItem);



Vue.use(vsButton).use(vsSpacer).use(vsImages)
Vue.use(vsSelect).use(vsSideBar).use(vsDivider)
Vue.use(vsPopup).use(vsCard).use(vsRow).use(vsCol).use(vsIcon).use(vsInput)
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
    language:'en-US',// This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)
    // key AIzaSyCJY8RqCzMtqYEjQMimzTPOF7UPzh_s04g
 
    //// If you want to set the version, you can do so:
    // v: '3.26',
  },
});


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");