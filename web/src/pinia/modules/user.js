import { login, getUserInfo } from '@/api/user'
import router from '@/router/index'
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getLoginToken, updateLoginToken, updateUserInfo } from '@/utils/user'
import {emitter} from "@/utils/bus.js";
import {removeUserInfo} from "@/utils/storage.js";


export const useUserStore = defineStore('user', () => {
  const loadingInstance = ref(null)

  const userInfo = ref({})
  const token = ref(getLoginToken() || {})
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
    const res = await getUserInfo()
    setUserInfo(res.data)
    return res
  }
  /* 登录*/
  const LoginIn = async(loginInfo) => {
    emitter.emit('showLoading')
    try {
      const res = await login(loginInfo)
      updateLoginToken(res.data.token)
      setUserInfo(res.data.user)
      setToken(res.data.token)
      return true
    } catch (e) {
      emitter.emit('closeLoading')
      return false
    }
  }
  /* 登出*/
  const LoginOut = async() => {
    token.value = {}
    sessionStorage.clear()
    removeUserInfo()
    await router.push({name: 'Login', replace: true})
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
