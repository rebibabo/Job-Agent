import request from '@/utils/request'


export const chartAPI = (params) => {
    return request.post('/api/chart/', params)
}

export const wordCloudAPI = (title) => {
    return request.get('/api/chart/wordCloud/' + title, {
        responseType: 'blob'  // 告诉 axios 返回的是二进制流
    });
}