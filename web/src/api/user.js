// src/api/user.js
import axios from 'axios';
import request from '@/utils/request'
import store from '@/store';

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

export const uploadResumeAPI = (formData) => {
    const userId = store.state.user.userInfo.id;
    const url = `/crawl/resume/${userId}`;
    return request.post(url, formData, {
        headers: { "Content-Type": "multipart/form-data", "token": store.state.user.userInfo.token },
    })
}

export const getResumeListAPI = () => {
    const userId = store.state.user.userInfo.id;
    const url = `/crawl/resume/${userId}`;
    return request.get(url)
}

export const deleteResumeAPI = (resumeName) => {
    const userId = store.state.user.userInfo.id;
    const url = `/crawl/resume/delete`;
    const params = {
        "userId": userId,
        "file": resumeName
    }
    return request.post(url, params)
}

export const viewResumeAPI = (resumeName) => {
    const userId = store.state.user.userInfo.id;
    const url = `/crawl/resume/view`;
    const params = {
        "userId": userId,
        "file": resumeName
    }
    return request.post(url, params);
}

export const getResumeContentAPI = (params) => {
    return request.get('/crawl/resume/parse/content', { params })
}

export const getResumeSummaryAPI = (params) => {
    return request.get('/crawl/resume/parse/summary', { params })
}

export const getResumePictureAPI = (params) => {
    return request.get('/crawl/resume/parse/picture', { params })
}