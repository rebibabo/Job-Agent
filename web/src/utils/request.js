// src/utils/request.js
import axios from 'axios'
import store from '@/store' // 引入Vuex store
import router from '@/router' // 引入Vue Router

const service = axios.create({
  timeout: 60000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 只处理/api开头的请求
    if (config.url.startsWith('/api')) {
      const token = store.state.user.token // 直接从Vuex获取token
      
      if (token) {
        config.headers['token'] = token // 使用token作为header键
      }
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response?.status === 401) {
      this.$message.error('登录已过期，请重新登录')
      router.push('/login') 
    }
    return Promise.reject(error)
  }
)

export default service