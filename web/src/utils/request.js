// src/utils/request.js
import axios from "axios";
import store from "@/store"; // 引入Vuex store
import router from "@/router"; // 引入Vue Router

const service = axios.create({
    timeout: 60000,
});

// 请求拦截器
service.interceptors.request.use(
    (config) => {
        // 只处理/api开头的请求
        if (config.url.startsWith("/api")) {
            const token = store.state.user.token; // 直接从Vuex获取token

            if (token) {
                config.headers["token"] = token; // 使用token作为header键
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
let isRedirecting = false;

service.interceptors.response.use(
    (response) => response.data,
    (error) => {
        if (error.response) {
            if (error.response.status === 401) {
                if (!isRedirecting) {
                    isRedirecting = true;
                    alert("登录已过期，请重新登录");
                    store.state.user.token = "";
                    store.state.user.userInfo = {};
                    router.push("/login").finally(() => {
                        isRedirecting = false;
                    });
                }
            }
        } else {
            // 这里可选: 统一处理网络错误
            console.error("请求未发送成功，服务器或网络故障：", error.message);
        }
        return Promise.reject(error);
    }
)

export default service;