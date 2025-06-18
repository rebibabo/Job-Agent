// src/api/job.js
import request from '@/utils/request'

export const cityListAPI = () => {
    return request.get('/api/job/city')
}

export const industryListAPI = () => {
    return request.get('/api/job/industry')
}

export const titleListAPI = () => {
    return request.get('/api/job/title')
}

export const jobListAPI = (params) => {
    console.log(params)
    return request.post('/api/job/page', params)
}