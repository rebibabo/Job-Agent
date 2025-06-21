// src/api/user.js
import axios from 'axios';
import request from '@/utils/request'

export const loginAPI = (data) => {
    return axios.post('/api/user/login', data); // 替换为你的实际API地址
};

export const changePasswordAPI = (params) => {
    return request.post('/api/user/changePassword', params)
}

export const userAddAPI = (params) => {
    return axios.post('/api/user/register', params)
}

export const deleteUserAPI = (userId) => {
    return axios.get('/api/user/delete/' + userId)
}