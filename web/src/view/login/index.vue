<script setup>
import {reactive, ref} from "vue";
import {Message, Lock, User} from "@element-plus/icons-vue";
import {useRoute, useRouter} from "vue-router";
import {useUserStore} from "@/pinia/modules/user.js";
import {register} from "@/api/user.js";
import {ElMessage} from "element-plus";

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const checkEmail = (rule, value, cb) => {
  //验证邮箱的正则表达式
  const regEmail = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
  if (regEmail.test(value)) {
    //正确的邮箱
    return cb();
  }
  cb(new Error("请输入正确的邮箱"));
};

const loginFormRef = ref()

const registerFormRef = ref(null)
const isRegister = ref(false)

const loginForm = reactive({
  password: '',
  email: ''
})

const registerForm = reactive({
  password: '',
  password2: '',
  email: '',
  nickname: '',
})

const rules = reactive({
  password: [
    {required: true, message: '请输入密码', trigger: 'blur',},
    {pattern: /^\S{6,20}$/, message: '密码必须是6 ~ 20位的非空字符', trigger: 'blur'}
  ],
  password2: [
    {required: true, message: '请输入确认密码', trigger: 'blur',},
    {pattern: /^\S{6,20}$/, message: '密码必须是6 ~ 20位的非空字符', trigger: 'blur'},
    {validator: (rule, value, callback) => {
      if (value !== registerForm.password) {
        callback(new Error('两次密码不一致'));
      } else {
        callback();
      }
    }, trigger: 'blur'}
  ],
  email: [{required: true, message: '请输入邮箱', trigger: 'blur',}, {validator: checkEmail, trigger: 'blur'}],
  nickname: [
    {required: true, message: '请输入昵称', trigger: 'blur',},
    {pattern: /^[\u4E00-\u9FA5A-Za-z0-9_]{2,10}$/, message: '昵称必须是2 ~ 10位的汉字、字母、数字、下划线', trigger: 'blur'}
  ],
})

const submitForm = (formRef) => {
  if (!formRef) return
  formRef.validate(async valid => {
    if (valid) {
      if (await userStore.LoginIn(loginForm)){
        if (route.query.redirect) {
          const redirect = route.query.redirect.replace(/\?.*$/, '').replace('#', '')
          let temp = route.query.redirect.split("?")
          let tempStr = ''
          if (temp.length > 1){
            tempStr = temp[1]
          } else {
            tempStr = ''
          }
          const params = new URLSearchParams(tempStr);

          const paramsObject = {};

          for (const [key, value] of params) {
            paramsObject[key] = value;
          }
          await router.push({path:redirect, query: paramsObject})
          return true
        }
        await router.push({name: 'Home'})
        return true
      }
      return false
    } else {
      return false;
    }
  })
}

const submitRegisterForm = (formRef) => {
  if (!formRef) return
  formRef.validate(async valid => {
    if (valid) {
      const res = await register(registerForm);
      if (res && res.status === 200){
        ElMessage({
          type: 'success',
          message: '注册成功，请前往登录',
        })
        loginForm.email = registerForm.email
        isRegister.value = false
        return true
      }
      return false
    } else {
      return false;
    }
  })
}
</script>

<template>
  <div class="login-page">
    <img src="@/assets/calendar.jpg" alt="图标" width="70" class="logo">
    <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        class="login-form"
        v-show="!isRegister"
    >
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="loginForm.email" :prefix-icon="Message"/>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="loginForm.password" type="password" autocomplete="off" :prefix-icon="Lock"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="large" class="login-button" @click="submitForm(loginFormRef)"
        >登录
        </el-button>
      </el-form-item>
      <el-button type="text" size="small" class="register-button" @click="isRegister = true" style="float: right;color: black">立即注册</el-button>
    </el-form>
    <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        class="login-form"
        v-show="isRegister"
    >
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="registerForm.email" :prefix-icon="Message" placeholder="请输入邮箱"/>
      </el-form-item>
      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="registerForm.nickname" :prefix-icon="User" placeholder="请输入昵称"/>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="registerForm.password" type="password" autocomplete="off" :prefix-icon="Lock" placeholder="请输入密码"/>
      </el-form-item>
      <el-form-item label="密码" prop="password2">
        <el-input v-model="registerForm.password2" type="password" autocomplete="off" :prefix-icon="Lock" placeholder="请再次输入密码确认"/>
      </el-form-item>
      <el-button type="primary" size="large" class="login-button" @click="submitRegisterForm(registerFormRef)"
      >立即注册
      </el-button>
      <el-button type="text" size="small" class="register-button" @click="isRegister = false" style="float: right;color: black">返回登录</el-button>
    </el-form>
  </div>
</template>

<style scoped>
.login-page {
  background-image: url("@/assets/yourname.gif");
  background-size: cover;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
}

.login-form {
  margin: 20px auto;
  width: 300px;
}

.login-button {
  width: 100%;
  height: 40px;
  background-color: #409EFF;
  color: #fff;
  font-size: 16px;
  border-radius: 4px;
}

.login-button:hover {
  background-color: #57a3f7;
}

/* 新增 logo 样式 */
.logo {
  margin-bottom: 20px;
  margin-top: 20px;
}
</style>
