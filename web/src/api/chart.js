import request from '@/utils/request'

export const cityChartAPI = () => {
    return request.post('/api/chart/city')
}

export const industryChartAPI = () => {
    return request.post('/api/chart/industry')
}

export const titleChartAPI = () => {
    return request.post('/api/chart/title')
}

export const experienceChartAPI = () => {
    return request.post('/api/chart/experience')
}

export const degreeChartAPI = () => {
    return request.post('/api/chart/degree')
}
