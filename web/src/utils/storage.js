const loginTokenKey = 'loginToken'
const userInfoKey = 'userInfo'

export function getUserToken() {
  const token = window.localStorage.getItem(loginTokenKey)
  return token || ''
}
export function setUserToken(token) {
  window.localStorage.setItem(loginTokenKey, token)
}

export function removeUserToken() {
  window.localStorage.removeItem(loginTokenKey)
}

export function getStorageUserInfo() {
  const userInfo = JSON.parse(window.localStorage.getItem(userInfoKey))
  return userInfo || {}
}
export function setUserInfo(userInfo) {
  window.localStorage.setItem(userInfoKey, JSON.stringify(userInfo))
}
export function removeUserInfo() {
  // window.localStorage.removeItem(userInfoKey)
  window.localStorage.clear()
}
