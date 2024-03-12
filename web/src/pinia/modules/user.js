import { login, getUserInfoWithToken } from '@/api/user'
import router from '@/router/index'
import { ElLoading } from 'element-plus'
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getLoginToken, setUserId, updateLoginToken, updateUserInfo } from '@/utils/user'


export const useUserStore = defineStore('user', () => {
  const loadingInstance = ref(null)

  const userInfo = ref({})
  const token = ref(getLoginToken() || '')
  const setUserInfo = (val) => {
    userInfo.value = val
    updateUserInfo(val)
  }

  const setToken = (val) => {
    token.value = val
  }

  const ResetUserInfo = (value = {}) => {
    userInfo.value = {
      ...userInfo.value,
      ...value
    }
  }
  /* 获取用户信息*/
  const GetUserInfo = async() => {
    const res = await getUserInfoWithToken()
    setUserInfo(res.data)
    return res
  }
  /* 登录*/
  const LoginIn = async(loginInfo) => {
    loadingInstance.value = ElLoading.service({
      fullscreen: true,
      text: '登录中，请稍候...',
    })
    try {
      const res = await login(loginInfo)
      if (res.code === '000000') {
        updateLoginToken(res.data.token)
        setUserInfo(res.data.user)
        setToken(res.data.token)
        await setUserId(res.data.user.userId)
        return true
      }
    } catch (e) {
      loadingInstance.value.close()
    }
    loadingInstance.value.close()
  }
  /* 登出*/
  const LoginOut = async() => {
    token.value = ''
    sessionStorage.clear()
    removeUserInfo()
    router.push({ name: 'Login', replace: true })
    window.location.reload()
  }


  watch(token, () => {
    updateLoginToken(token.value)
  })

  return {
    userInfo,
    token,
    ResetUserInfo,
    GetUserInfo,
    LoginIn,
    LoginOut,
    setToken,
    loadingInstance
  }
})
