import router from '@/router/index'
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getLoginToken, updateLoginToken, updateUserInfo, getUserInfo } from '@/utils/user'
import {emitter} from "@/utils/bus.js";
import {removeUserInfo} from "@/utils/storage.js";
import {login} from "@/api/user.js";


export const useUserStore = defineStore('user', () => {
  const loadingInstance = ref(null)

  const userInfo = ref(getUserInfo() || {})
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
    return userInfo.value
  }
  /* 登录*/
  const LoginIn = async(loginInfo) => {
    emitter.emit('showLoading')
    try {
      const res = await login(loginInfo)
      if (res.status !== 200) {
        return false
      }
      updateLoginToken(res.data.token)
      setUserInfo(res.data.info)
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
    userInfo.value = {}
    removeUserInfo()
    await router.push({name: 'Login', replace: true})
  }


  watch(token, () => {
    updateLoginToken(token.value)
  })

  watch(userInfo, () => {
    updateUserInfo(userInfo.value)
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
