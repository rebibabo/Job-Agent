import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import router from './router'  // 导入路由配置
import store from './store' // 确保导入了store
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)
Vue.config.productionTip = false

new Vue({
  store,  // 注入store实例
  router,  // 注入路由实例
  render: h => h(App),
}).$mount('#app')
