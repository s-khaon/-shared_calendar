import { service } from '@/utils/request'

export const login = (data) => {
    return service({
        url: '/login',
        method: 'post',
        data: data
    })
}

export const getUserInfo = (userId) => {
    return service({
        url: '/users/' + userId,
        method: 'get',
    })
}
