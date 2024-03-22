import {getStorageUserInfo, getUserToken, removeUserToken, setUserInfo, setUserToken,} from '@/utils/storage'
import router from '@/router'
import {getRemoteUserInfo} from "@/api/user.js";

// 获取用户信息
export const getUserInfo = async() => {
  let userInfo = getStorageUserInfo()
  if (!userInfo) {
    const res = await getRemoteUserInfo()
    if (res && res.status === 200) {
      userInfo = res.data
      setUserInfo(res.data)
    } else {
      await router.push({name: 'Login', replace: true})
      return
    }
  }
  return userInfo
}

// 更新用户信息
export const updateUserInfo = (userInfo) => {
  setUserInfo(userInfo)
}

// 获取本地loginToken
export const getLoginToken = () => {
  return getUserToken()
}

// 更新本地登录token
export const updateLoginToken = (token) => {
  setUserToken(token)
}

// 移除token
export const removeLoginToken = (token) => {
  removeUserToken(token)
}

// 获取userId
export const getUserId = async() => {
  const userInfo = await getUserInfo()
  return userInfo.userId
}


