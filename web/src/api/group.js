import { service } from '@/utils/request'

export const getGroups = () => {
    return service({
        url: '/groups/',
        method: 'get',
    })
}

export const createGroup = (data) => {
    return service({
        url: '/groups/',
        method: 'post',
        data: data
    })
}

export const updateGroup = (data) => {
    return service({
        url: '/groups/',
        method: 'put',
        data: data
    })
}

export const deleteGroup = (groupId) => {
    return service({
        url: '/groups/' + groupId + '/',
        method: 'delete',
    })
}

export const getGroup = (groupId) => {
    return service({
        url: '/groups/' + groupId + '/',
        method: 'get',
    })
}

export const quitGroup = (groupId) => {
    return service({
        url: '/groups/' + groupId + '/member/quit/',
        method: 'delete',
    })
}

export const joinGroup = (params) => {
    return service({
        url: '/groups/member/join/',
        method: 'post',
        params: params
    })
}

export const createInvitationCode = (groupId) => {
    return service({
        url: '/groups/invitation/' + groupId + '/',
        method: 'post',
    })
}

export const getInvitationDetail = (code) => {
    return service({
        url: '/groups/invitation/' + code + '/',
        method: 'get',
    })
}
