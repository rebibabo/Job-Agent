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
    return request.post('/api/job/page', params)
}

export const jobListFilterAPI = (params) => {
    return request.post('/api/job/pageFilter', params)
}

export const cityListAllAPI = () => {
    return request.get('/api/job/cityAll')
}

export const industryListAllAPI = () => {
    return request.get('/api/job/industryAll')
}

export const titleListAllAPI = () => {
    return request.get('/api/job/titleAll')
}

export const deleteAPI = (params) => {
    return request.post('/api/job/delete', params)
}

export const deleteALLAPI = (params) => {
    return request.post('/api/job/deleteFilter', params)
}

export const setViewStatusAPI = (params) => {
    return request.post('/api/job/view', params)
}

export const getFilterJobAPI = (params) => {
    return request.post('/api/job/filterJob', params)
}

export const startFilterAPI = (params) => {
    return request.post('/crawl/start/filter', params)
}