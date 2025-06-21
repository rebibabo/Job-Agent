import CryptoJS from 'crypto-js';

export function getMD5LowerCase(str) {
    const hash = CryptoJS.MD5(str).toString();
    return hash.toLowerCase();
}

/**
 * 递归排序对象 key
 * @param {Object|Array} obj
 * @returns {Object|Array}
 */
function sortObject(obj) {
    if (Array.isArray(obj)) {
        // 对数组中元素也递归处理
        return obj.map(sortObject)
    } else if (obj !== null && typeof obj === 'object') {
        const sortedKeys = Object.keys(obj).sort()
        const result = {}
        for (const key of sortedKeys) {
            result[key] = sortObject(obj[key])
        }
        return result
    }
    return obj // 基础类型直接返回
}

export function getFiltersMD5(filters) {
    const sortedStr = JSON.stringify(sortObject(filters))
    return CryptoJS.MD5(sortedStr).toString().toLowerCase()
}