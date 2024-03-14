import axios from 'axios'
import {ElMessage} from 'element-plus'
import {useUserStore} from '@/pinia/modules/user'
import {emitter} from '@/utils/bus.js'
import {getUserToken, setUserToken} from '@/utils/storage'

const service = axios.create({
    baseURL: '/api',
    timeout: 20000,
})

let activeAxios = 0
let timer
const showLoading = () => {
    activeAxios++
    if (timer) {
        clearTimeout(timer)
    }
    timer = setTimeout(() => {
        if (activeAxios > 0) {
            emitter.emit('showLoading')
        }
    }, 400)
}

const closeLoading = () => {
    activeAxios--
    if (activeAxios <= 0) {
        clearTimeout(timer)
        emitter.emit('closeLoading')
    }
}

const onFulfilled2 = config => {
    const token = getUserToken()
    config.headers = {
        'Content-Type': 'application/json',
    }
    if (token && token.access_token) {
        config.headers['Authorization'] = token.token_type + " " + token
    }
    return config
};

const onRejected2 = error => {
    closeLoading()
    ElMessage({
        showClose: true,
        message: error,
        type: 'error'
    })
    return error
}
// http request 拦截器
service.interceptors.request.use(
    onFulfilled2,
    onRejected2
)

const onFulfilled = async response => {
    closeLoading()
    if (response.headers['new-token']) {
        const userStore = useUserStore()
        setUserToken(response.headers['new-token'])
        userStore.setToken(response.headers['new-token'])
    }
    if (response.headers.msg) {
        response.data.msg = decodeURI(response.headers.msg)
    }
    return response.data
}

const onRejected = async error => {
    closeLoading()
    if (!error.response) {
        ElMessage({
            showClose: true,
            message: "请求错误，请稍后重试",
            type: 'error'
        })
        console.log("未知异常:", error)
        return error
    }
    switch (error.response.status) {
        case 500:
            ElMessage({
                showClose: true,
                message: error.response?.data?.msg ? error.response.data.msg : '服务端错误，请稍后重试',
                type: 'error'
            })
            console.log("服务端错误:", error)
            break
        case 404:
            ElMessage({
                showClose: true,
                message: error.response?.data?.msg ? error.response.data.msg : '资源不存在，请确认',
                type: 'error'
            })
            console.log("资源不存在:", error)
            break
        case 401:
            ElMessage({
                showClose: true,
                message: error.response?.data?.msg ? error.response.data.msg : '认证异常',
                type: 'error'
            })
            console.log("认证错误:", error)
            const userStore = useUserStore()
            await userStore.LoginOut()
            break
        case 403:
            ElMessage({
                showClose: true,
                message: error.response?.data?.msg ? error.response.data.msg : '权限异常',
                type: 'error'
            })
            console.log("权限异常:", error)
            break
        case 400:
            ElMessage({
                showClose: true,
                message: error.response?.data?.msg ? error.response.data.msg : "请求参数异常",
                type: 'error'
            })
            break
        default:
            ElMessage({
                showClose: true,
                message: error.response?.data?.msg ? error.response.data.msg : '接口报错',
                type: 'error'
            })
            break
    }

    return error
}

// http response 拦截器
service.interceptors.response.use(
    onFulfilled,
    onRejected
)

export {service}
