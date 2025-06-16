// src/store/modules/user.js
import {
    loginAPI
} from '@/api/auth'; // 导入你的登录API接口

const state = {
    token: localStorage.getItem('token') || '', // 首先从本地存储位置获取token，如果没有设置为空，在登录成功后会设置token
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || {} // 存储用户信息
};

const mutations = {
    SET_TOKEN(state, token) {
        state.token = token;
    },
    SET_USER_INFO(state, userInfo) {
        state.userInfo = userInfo;
    }
};

const actions = {
    // 登录action
    async login({
        commit
    }, loginForm) {
        try {
            // 调用登录API（需替换为你的实际接口）
            const response = await loginAPI(loginForm);

            // 假设接口返回数据格式: { token: 'xxx', user: { name: 'John' } }
            const {
                code,
                data,
                msg
            } = response.data;

            if (code !== 1) {
                console.log("error message:", msg);
                return Promise.reject(new Error(msg));
            }

            var token = data.token;

            // 删除data中的token字段
            delete data.token;

            //   保存token到Vuex和localStorage

            if (token) {
                console.log(token)
                
                commit('SET_TOKEN', token);
                localStorage.setItem('token', token);

                // 保存用户信息
                commit('SET_USER_INFO', data);

                localStorage.setItem("token", token);
                localStorage.setItem("userInfo", JSON.stringify(data));
                // console.log(this.state.user.userInfo.userName)

                // 返回成功（.then会接收到这个返回值）
                return Promise.resolve();
            }

            return Promise.reject(new Error('登录失败，请检查用户名或密码'));
        } catch (error) {
            return Promise.reject(error);
        }
    },

    // 注销action
    logout({
        commit
    }) {
        commit('SET_TOKEN', '');
        commit('SET_USER_INFO', {});
        localStorage.removeItem('token');
        localStorage.removeItem('userInfo');
    }
};

export default {
    namespaced: true, // 启用命名空间
    state,
    mutations,
    actions
};