<script setup>
import {reactive, ref} from "vue";
import {login} from "@/api/user.js";
import {setUserInfo, setUserToken} from "@/utils/storage.js";
import {Message, Lock} from "@element-plus/icons-vue";
import {useRouter} from "vue-router";
const router = useRouter()
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

const loginForm = reactive({
  password: '',
  email: ''
})

const rules = reactive({
  password: [
    {required: true, message: '请输入密码', trigger: 'blur',},
    {pattern: /^\S{6,20}$/, message: '密码必须是6 ~ 20位的非空字符', trigger: 'blur'}
  ],
  email: [{required: true, message: '请输入邮箱', trigger: 'blur',}, {validator: checkEmail, trigger: 'blur'}],
})

const submitForm = (formRef) => {
  if (!formRef) return
  formRef.validate(async valid => {
    if (valid) {
      const res = await login(loginForm)
      if (res && res.code === 200) {
        //登录成功
        //保存用户信息
        setUserInfo(res.info)
        //保存token
        setUserToken(res.token)
        //跳转到首页
        await router.push({name: 'Home'})
      }
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
