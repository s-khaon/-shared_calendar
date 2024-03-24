<script setup>
import {useRouter, useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {getInvitationDetail, joinGroup} from "@/api/group.js";
import {useUserStore} from "@/pinia/modules/user.js";
import {ElMessage} from "element-plus";

const router = useRouter()
const route = useRoute()

const code = route.query.code

const groupDetail = ref({})

const userStore = useUserStore()
const token = userStore.token

const getInvitationData = async () => {
  const res = await getInvitationDetail(code)
  if (res && res.status === 200) {
    groupDetail.value = res.data
  }
}

const handleJoinGroup = async () => {
  const res = await joinGroup({code: code})
  if (res && res.status === 200) {
    ElMessage({
      message: '加入成功',
      type: 'success',
      duration: 1000,
    })
    await router.push({name: 'Home'})
  }
}

onMounted(async () => {
      if (token) {
        await getInvitationData()
      } else {
        await router.push({name: 'Login', query: {redirect: route.fullPath},})
      }
    }
)
</script>

<template>
  <div class="content-box">
    <el-card>
      <template #header>
        <div class="card-header">
          <img src="@/assets/calendar.jpg" style="width: 18px;margin-right: 5px;"
               alt="Logo"><span>共享日历加入邀请</span>
        </div>
      </template>
      {{ groupDetail.creator?.nickname || '-' }}
      邀请您加入“{{ groupDetail.group?.group_name || '-' }}”，快来一起编辑属于你们的共享日历吧！
      <template #footer>
        <div class="button-container">
          <el-button type="primary" @click="handleJoinGroup">接受邀请</el-button>
        </div>
      </template>
    </el-card>
  </div>
</template>

<style scoped>
.content-box {
  display: flex;
  justify-content: center; /*水平居中*/
  align-items: center; /*垂直居中*/
  height: 100vh;
}

.button-container {
  text-align: center; /* 文字水平居中 */
  margin-top: 20px; /* 设置顶部间距 */
}
</style>