import request from '@/utils/request'

export const saveRuleAPI = (params) => {
    return request.post('/api/rule/save', params)
}

export const findRuleAPI = (params) => {
    return request.post('/api/rule/find', params)
}

export const loadRuleAPI = (userId) => {
    return request.get('/api/rule/load/' + userId)
}

export const deleteRuleAPI = (roleId) => {
    return request.get('/api/rule/delete/' + roleId)
}   