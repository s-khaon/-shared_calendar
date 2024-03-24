import { service } from '@/utils/request'

export const login = (data) => {
    return service({
        url: '/login',
        method: 'post',
        data: data
    })
}

export const getRemoteUserInfo = (userId) => {
    return service({
        url: '/users/' + userId,
        method: 'get',
    })
}

export const register = (data) => {
    return service({
        url: '/register',
        method: 'post',
        data: data
    })
}

export const updateUserInfo = (data) => {
    return service({
        url: '/users/',
        method: 'put',
        data: data
    })
}