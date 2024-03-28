import { service } from '@/utils/request'

export const getHolidays = () => {
    return service({
        url: '/holidays/',
        method: 'get',
    })
}
