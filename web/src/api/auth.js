// src/api/auth.js
import axios from 'axios';
import request from '@/utils/request'

export const loginAPI = (data) => {
    return axios.post('/api/login', data); // 替换为你的实际API地址
};

export const changePasswordAPI = (params) => {
    return request.post('/api/userInfo/changePassword', params)
}

export const userAddAPI = (params) => {
    return axios.post('/api/register', params)
}