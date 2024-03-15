import {useUserStore} from '@/pinia/modules/user'
import router from '@/router'

const whiteList = ['Login']

router.beforeEach(async (to, from) => {
    const userStore = useUserStore()
    to.meta.matched = [...to.matched]
    const token = userStore.token
    // 在白名单中的判断情况
    if (whiteList.indexOf(to.name) > -1) {
        if (token && token.access_token) {
            return {name: "Home", replace: true}
        } else {
            return true
        }
    }
    // 不在白名单中并且已经登录的时候
    if (token && token.access_token) {
        if (to.matched.length) {
            return true
        } else {
            return {name: '404'}
        }
    } else {
        // 不在白名单中并且未登录的时候
        const temp = {
            name: 'Login',
            replace: true,
        }
        if (to.path !== from.path) {
            temp['query'] = {
                redirect: document.location.hash
            }
        }
        return temp
    }
})
