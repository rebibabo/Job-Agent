// src/api/auth.js
import axios from 'axios';

export const loginAPI = (data) => {
  return axios.post('/api/login', data); // 替换为你的实际API地址
};