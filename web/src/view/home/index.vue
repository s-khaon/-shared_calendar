<script setup>
import {onMounted, reactive, ref} from "vue";
import {
  ArrowDown,
  ArrowLeft,
  ArrowRight, Avatar, ChatLineSquare, Check, Close, CloseBold,
  Connection,
  Delete,
  Edit, EditPen, Finished, FirstAidKit, List,
  Operation,
  Plus, Remove, Service, UserFilled
} from "@element-plus/icons-vue";
import {
  getGroups,
  createGroup,
  updateGroup,
  deleteGroup,
  quitGroup,
  createInvitationCode
} from '@/api/group'
import {
  cancelDoneTodoItem,
  createTodoItem,
  doneTodoItem,
  getTodoItems,
  updateTodoItem,
  deleteTodoItem, getUndeterminedTodoItems
} from "@/api/todoList.js";
import {formatDate, formatTime, getMonthFirstAndLastDay} from "@/utils/date.js";
import {useUserStore} from '@/pinia/modules/user'
import {emitter} from "@/utils/bus.js";
import {ElMessage, ElMessageBox} from "element-plus";

const userStore = useUserStore()
const calendar = ref()
const currentDate = ref(new Date())
const selectedDateStr = ref(formatDate(new Date()))
const defaultGroup = {
  group_name: "个人日历",
  id: 0
}
const groupOptions = ref([defaultGroup])
const todoItems = ref([])
const undeterminedTodoItems = ref([])
const groupDialogVisible = ref(false)
const groupFormRef = ref()
const groupForm = reactive({
  group_name: "",
  id: 0
})
const currentGroupId = ref(0)
const isOwner = ref(true)

const currentGroup = ref(groupOptions.value[0])

const loading = ref(false)
const planDialogVisible = ref(false)
const planFormRef = ref()
const selectedDatePlans = ref([])
const planForm = reactive({
  name: "",
  description: "",
  done_time: "",
  done_result: "",
  is_all_day: false,
  is_done: false,
  is_undetermined: false,
  start_time: "",
  end_time: "",
  group_id: currentGroupId.value,
  id: 0
})

const groupFormRules = reactive({
  group_name: [
    {required: true, message: '请输入团队名称', trigger: 'blur', max: 20, min: 1},
  ],
})

const planFormRules = reactive({
  name: [
    {required: true, message: '请输入计划名称', trigger: 'blur', max: 20, min: 1},
  ],
  start_time: [
    {required: true, message: '请选择开始时间', trigger: 'blur'},
  ],
  end_time: [
    {required: true, message: '请选择结束时间', trigger: 'blur'},
  ],
})

const invitationDialogVisible = ref(false)

const invitationLink = ref('')

const currentUser = ref({})

const selectDate = (val) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}

const flushPlanData = (dateStr) => {
  selectedDatePlans.value = []
  for (const item of todoItems.value) {
    if (item.key === dateStr) {
      selectedDatePlans.value = item.value
    }
  }
}

const clickDate = (data) => {
  selectedDateStr.value = data.day
  flushPlanData(data.day)
  if (data.isSelected) {
    planDialogVisible.value = true
  }
}

const clickAddPlan = () => {
  const endTime = new Date(currentDate.value)
  endTime.setHours(currentDate.value.getHours() + 1)

  planForm.name = ''
  planForm.description = ''
  planForm.done_time = ''
  planForm.done_result = ''
  planForm.is_undetermined = false
  planForm.is_all_day = false
  planForm.is_done = false
  planForm.start_time = formatTime(currentDate.value)
  planForm.end_time = formatTime(endTime)
  planForm.group_id = currentGroupId.value
  planForm.id = 0

  planDialogVisible.value = true
}

const clickEditPlan = (item) => {
  planForm.name = item.name
  planForm.description = item.description
  planForm.done_time = item.done_time
  planForm.done_result = item.done_result
  planForm.is_all_day = item.is_all_day
  planForm.is_done = !!item.done_time
  planForm.start_time = item.start_time
  planForm.end_time = item.end_time
  planForm.group_id = item.group_id
  planForm.id = item.id
  planForm.is_undetermined = item.is_undetermined
  planDialogVisible.value = true
}

const resetPlanForm = (done) => {
  planFormRef.value.resetFields()
  done()
}

const resetGroupForm = (done) => {
  groupFormRef.value.resetFields()
  done()
}

const addGroup = () => {
  groupForm.group_name = ''
  groupForm.id = 0
  groupDialogVisible.value = true
}

const removeGroup = async () => {
  const res = await ElMessageBox.confirm('确定要删除' + currentGroup.value.group_name + '吗？数据将会全部清理，请谨慎操作！', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    center: true,
  })
  if (res === 'confirm') {
    const res = await deleteGroup(currentGroupId.value)
    if (res && res.status === 200) {
      await getData()
    }
  }
}

const handleQuitGroup = async () => {
  const res = await ElMessageBox.confirm('确定要退出' + currentGroup.value.group_name + '吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    center: true,
  })
  if (res === 'confirm') {
    const res = await quitGroup(currentGroupId.value)
    if (res && res.status === 200) {
      await getData()
    }
  }
}

const copyToClipboard = (text) => {
// 创建一个新的textarea元素
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.style.position = 'fixed'
  textarea.style.opacity = 0 // 设置透明度为0，使其不可见但可以选中
  document.body.appendChild(textarea)
  textarea.focus() // 让textarea获得焦点
  textarea.select() // 选择textarea中的所有内容

  // 使用新的Clipboard API将内容复制到剪贴板
  navigator.clipboard.writeText(text).then(() => {
    // 复制成功后的操作
    ElMessage({
      message: '复制成功',
      type: 'success',
      duration: 1000,
    })
    invitationDialogVisible.value = false
  }).catch(err => {
    // 复制失败后的操作
    ElMessage({
      message: '复制失败，请自行复制',
      type: 'error',
      duration: 1000,
    })
  }).finally(() => {
    // 移除临时textarea元素
    document.body.removeChild(textarea)
  })
}

const copyInvitationLink = () => {
  copyToClipboard(invitationLink.value)
}

const inviteToJoin = async () => {
  const res = await createInvitationCode(currentGroupId.value)
  if (res && res.status === 200) {
    const code = res.data.code
    invitationLink.value = window.location.origin + '/#/invitation/?code=' + code
    invitationDialogVisible.value = true
  }
}
const editGroup = () => {
  groupForm.group_name = currentGroup.value.group_name
  groupForm.id = currentGroup.value.id
  groupDialogVisible.value = true
}

const changeGroup = (item) => {
  currentGroupId.value = item.id
  currentGroup.value = item
  userStore.GetUserInfo().then(userInfo => {
    isOwner.value = item.owner_id === userInfo.id
  })
  if (currentGroupId.value) {
    getTodoItemsData(currentGroupId.value)
  } else {
    getTodoItemsData(0)
  }

}

const submitGroupForm = () => {
  loading.value = true
  groupFormRef.value.validate(async (valid) => {
    if (!valid) {
      loading.value = false
      return false
    }
    emitter.emit('showLoading')
    if (groupForm.id) {
      const res = await updateGroup(groupForm)
      if (res && res.status === 200) {
        for (let i = 0; i < groupOptions.value.length; i++) {
          if (groupOptions.value[i].id === groupForm.id) {
            groupOptions.value[i] = res.data
            break
          }
        }
        groupDialogVisible.value = false
      }
    } else {
      const res = await createGroup(groupForm)
      if (res && res.status === 200) {
        groupOptions.value.push(res.data)
        groupDialogVisible.value = false
      }
    }
    emitter.emit('closeLoading')
    loading.value = false
    return true
  })
}

const submitPlanForm = () => {
  loading.value = true
  planFormRef.value.validate(async (valid) => {
    if (!valid) {
      loading.value = false
      return false
    }
    emitter.emit('showLoading')
    if (planForm.id) {
      const res = await updateTodoItem(planForm)
      if (res && res.status === 200) {
        planDialogVisible.value = false
      }
    } else {
      const res = await createTodoItem(planForm)
      if (res && res.status === 200) {
        planDialogVisible.value = false
      }
    }
    await getTodoItemsData(currentGroupId.value)
    emitter.emit('closeLoading')
    loading.value = false
    return true
  })
}

const formatTimelineTime = (item) => {
  if (!item) return ""
  const start = item.start_time.split(" ")
  const end = item.end_time.split(" ")
  if (item.is_all_day) {
    if (start[0] === end[0]) {
      return "全天"
    } else {
      return start[0] + " 至 " + end[0]
    }
  } else if (!item.end_time) {
    return start[1]
  } else if (start === end) {
    return start[1]
  } else if (start[0] === end[0]) {
    return start[1] + " 至 " + end[1]
  } else {
    return start + " 至 " + end
  }
}

const formatTimeAndAuthor = (item) => {
  if (item.is_undetermined) {
    return item.creator.nickname + " 创建于 " + item.created_at
  }
  const timeFormat = formatTimelineTime(item)
  if (item.creator) {
    return timeFormat + " —— " + item.creator.nickname
  }
  return timeFormat
}

const getTodoItemsData = async (groupId) => {
  const [firstDay, lastDay] = getMonthFirstAndLastDay(currentDate.value);
  const params = {
    from_date: firstDay,
    to_date: lastDay
  }
  const res = await getTodoItems(groupId, params)
  if (res && res.status === 200) {
    todoItems.value = res.data
    flushPlanData(selectedDateStr.value)
    await getUndeterminedData()
  }
}

const getUndeterminedData = async () => {
  const res = await getUndeterminedTodoItems(currentGroupId.value)
  if (res && res.status === 200) {
    if (res.data && res.data.length > 0) {
      undeterminedTodoItems.value = res.data
    }
  }
}

const inputDoneResult = (plan) => {
  ElMessageBox.prompt('请输入完成结果', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputErrorMessage: '最大长度为50个字符',
    center: true
  })
      .then(({value}) => {
        if (value && value.length > 50) {
          ElMessage({
            type: 'error',
            message: '最大长度为50个字符',
          })
          plan.is_done = false
          return
        }
        if (!value) {
          value = ''
        }
        doneTodoItem({done_result: value, id: plan.id}).then(res => {
          if (res && res.status === 200) {
            plan.done_time = formatTime(new Date())
            plan.is_done = true
            plan.done_result = value
            userStore.GetUserInfo().then(userInfo => {
              plan.done_user = userInfo
            })
            ElMessage({
              type: 'success',
              message: `完成成功`,
            })
          }
        })
      })
      .catch((err) => {
        ElMessage({
          type: 'info',
          message: '取消',
        })
        plan.is_done = false
      })
}

const changePlanIsDone = (val, plan) => {
  if (!val) {
    cancelDoneTodoItem(plan.id).then(res => {
      if (res && res.status === 200) {
        plan.done_time = ""
        plan.done_result = ""
        plan.is_done = false
        ElMessage({
          type: 'success',
          message: `取消完成成功`,
        })
      }
    })
  } else {
    inputDoneResult(plan)
  }
}

const removePlan = async (plan) => {
  const res = await ElMessageBox.confirm('确定要删除该计划吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    center: true,
  })
  if (res === 'confirm') {
    const res = await deleteTodoItem(plan.id)
    if (res && res.status === 200) {
      await getTodoItemsData(currentGroupId.value)
    }
  }
}
const undeterminedDrawerVisible = ref(false)

const getData = async () => {
  const res = await getGroups()
  if (res && res.status === 200) {
    if (res.data && res.data.length > 0) {
      groupOptions.value = [defaultGroup, ...res.data]
      // todo check fixed one
      changeGroup(res.data[res.data.length - 1])
    }
  }
}

const userDialogVisible = ref(false)
const handleLoginOut = async () => {
  await userStore.LoginOut()
}

const toolsDialogVisible = ref(false)

onMounted(async () => {
  currentUser.value = await userStore.GetUserInfo()
  await getData()
})


</script>

<template>
  <el-row :gutter="10">
    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
      <div class='calendar-app'>
        <el-calendar ref="calendar" v-model="currentDate">
          <template #header="{ date }">
            <el-row>
              <el-col :span="9" class="button-box">
                <el-dropdown size="small" type="primary" trigger="click">
                  <el-button type="primary" size="small">
                    {{ currentGroup.group_name }}
                    <el-icon class="el-icon--right">
                      <arrow-down/>
                    </el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-for="item in groupOptions" :key="item.id" :value="item.id"
                                        @click="changeGroup(item)">{{ item.group_name }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
                <el-popover placement="bottom" trigger="click" :width="230">
                  <template #reference>
                    <el-button :icon="Operation" size="small" type="success"/>
                  </template>
                  <el-button type="success" :icon="Edit" circle @click="editGroup" :disabled="currentGroupId === 0"/>
                  <el-button type="primary" :icon="Plus" @click="addGroup"/>
                  <el-button type="danger" :icon="Delete" @click="removeGroup" :disabled="currentGroupId === 0"
                             v-show="isOwner"/>
                  <el-button type="danger" :icon="Remove" @click="handleQuitGroup" :disabled="currentGroupId === 0"
                             v-show="!isOwner"/>
                  <el-button color="#80d5ff" :icon="Connection" circle :disabled="currentGroupId === 0"
                             @click="inviteToJoin"/>
                </el-popover>
              </el-col>
              <el-col :span="6">
                <span>{{ date }}</span>
              </el-col>
              <el-col :span="9" class="button-box">
                <el-button-group>
                  <el-button size="small" :icon="ArrowLeft" @click="selectDate('prev-month')">月</el-button>
                  <el-button size="small" @click="selectDate('next-month')">月
                    <el-icon class="el-icon--right">
                      <ArrowRight/>
                    </el-icon>
                  </el-button>
                </el-button-group>
                <el-button size="small" @click="selectDate('today')">今日
                </el-button>
                <el-button-group>
                  <el-button size="small" :icon="ArrowLeft" @click="selectDate('prev-year')">年</el-button>
                  <el-button size="small" @click="selectDate('next-year')">年
                    <el-icon class="el-icon--right">
                      <ArrowRight/>
                    </el-icon>
                  </el-button>
                </el-button-group>
              </el-col>
            </el-row>
          </template>
          <template #date-cell="{ data }">
            <div @click="clickDate(data)" class="calendar-cell">
              <div>
                {{ data.day.split("-").slice(2).join("-").replace("0", "") }}
              </div>
              <template v-for="item in todoItems" :key="item.id">
                <div class="text-area" v-if="item.key === data.day">
                  <div v-for="i in item.value" :key="i.id">
                    <el-text :tag="i.is_done ? 'del' :'p'" size="small">{{ i.name }}</el-text>
                  </div>
                </div>
              </template>
            </div>
          </template>
        </el-calendar>
      </div>
    </el-col>
    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
      <el-timeline class="timeline">
        <el-timeline-item :timestamp="formatTimeAndAuthor(item)" placement="top" v-for="item in selectedDatePlans"
                          :key="item.id">
          <el-card @click="clickEditPlan(item)" :class="{ 'is-done': item.is_done }" class="todo-item">
            <div style="float: left;margin-right: 10px;margin-top:8px" @click.stop="">
              <el-checkbox v-model="item.is_done" size="large" @change="changePlanIsDone($event, item)"/>
            </div>
            <h4>
              <el-text :tag="item.is_done ? 'del' :'p'">{{ item.name }}</el-text>
            </h4>
            <p>{{ item.description }}</p>
            <el-icon :size="30" class="delete-button" color="#f56c6c" @click.stop="removePlan(item)">
              <CloseBold/>
            </el-icon>
            <div v-show="item.is_done" class="done-icon">
              <p v-show="item.done_result">
                <el-icon style="margin-top:1px;margin-right: 2px;">
                  <ChatLineSquare/>
                </el-icon>
                {{ item.done_result }}
              </p>
              <div>
                <el-icon style="margin-top:1px;margin-right: 2px;color: #007bff;">
                  <Avatar/>
                </el-icon>
                {{ item.done_user?.nickname || "-" }}
                <el-icon style="margin-left:10px;margin-top:1px;margin-right: 2px;color: green;">
                  <Finished/>
                </el-icon>
                {{ item.done_time }}
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-col>
  </el-row>
  <el-dialog
      v-model="groupDialogVisible"
      :title="groupForm.id === 0 ? '添加团队' : '编辑团队'"
      width="300"
      :before-close="resetGroupForm"
      align-center
  >
    <el-form ref="groupFormRef" :model="groupForm" :rules="groupFormRules" label-width="80px">
      <el-form-item label="团队名称" prop="group_name">
        <el-input v-model="groupForm.group_name" maxlength="20"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="groupDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitGroupForm" :loading="loading">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
      v-model="planDialogVisible"
      :title="planForm.id === 0 ? '添加计划' : '编辑计划'"
      width="300"
      :before-close="resetPlanForm"
      align-center
  >
    <el-form ref="planFormRef" :model="planForm" :rules="planFormRules" label-width="80px">
      <el-form-item label="计划标题" prop="name">
        <el-input v-model="planForm.name" maxlength="20"/>
      </el-form-item>
      <el-form-item label="时间待定" prop="is_undetermined">
        <el-switch
            v-model="planForm.is_undetermined"
            class="mt-2"
            style="margin-left: 24px"
            inline-prompt
            :active-icon="Check"
            :inactive-icon="Close"
        />
      </el-form-item>
      <el-form-item label="全天计划" prop="is_all_day" v-show="!planForm.is_undetermined">
        <el-switch
            v-model="planForm.is_all_day"
            class="mt-2"
            style="margin-left: 24px"
            inline-prompt
            :active-icon="Check"
            :inactive-icon="Close"
        />
      </el-form-item>
      <el-form-item label="开始时间" prop="start_time" v-if="!planForm.is_undetermined">
        <el-date-picker
            v-if="planForm.is_all_day"
            v-model="planForm.start_time"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
        />
        <el-date-picker
            v-if="!planForm.is_all_day"
            v-model="planForm.start_time"
            type="datetime"
            placeholder="选择日期"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
        />
      </el-form-item>
      <el-form-item label="结束时间" prop="end_time" v-if="!planForm.is_undetermined">
        <el-date-picker
            v-if="planForm.is_all_day"
            v-model="planForm.end_time"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
        />
        <el-date-picker
            v-if="!planForm.is_all_day"
            v-model="planForm.end_time"
            type="datetime"
            placeholder="选择日期"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
        />
      </el-form-item>
      <el-form-item label="备注" prop="description">
        <el-input v-model="planForm.description" maxlength="500" type="textarea" autosize/>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="planDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitPlanForm" :loading="loading">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
      v-model="invitationDialogVisible"
      title="邀请成员"
      width="300"
      align-center
  >
    <div>{{ invitationLink }}</div>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="copyInvitationLink" :loading="loading">
          复制链接
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
      v-model="userDialogVisible"
      title="用户详情"
      width="300"
      align-center
  >
    <el-descriptions direction="horizontal" column="1">
      <el-descriptions-item label="邮箱">{{ currentUser.email }}</el-descriptions-item>
      <el-descriptions-item label="昵称">{{ currentUser.nickname }}</el-descriptions-item>
    </el-descriptions>

    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="handleLoginOut" :loading="loading">
          退出登录
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
      v-model="toolsDialogVisible"
      title="工具箱"
      width="300"
      align-center
  >
    <div class="toolbox-items">
      <el-button circle @click="clickAddPlan" :icon="Plus" type="primary" size="large"></el-button>
      <el-badge :value="undeterminedTodoItems.length" type="warning">
        <el-button circle @click="undeterminedDrawerVisible=true" :icon="List" type="success" size="large"/>
      </el-badge>
      <el-button circle @click="userDialogVisible=true" color="#99bbff" :icon="UserFilled" size="large"></el-button>
      <el-popover
          placement="top-start"
          title="使用帮助"
          :width="200"
          trigger="hover"
          content="点击团队名称旁的按钮可创建、编辑、删除、退出、邀请成员加入团队。双击对应日期可以快捷打开对应日期新增待办事项窗口，亦可使用右下角工具箱中的添加按钮进行添加。点击对应计划可以进行计划内容编辑。"
      >
        <template #reference>
          <el-button circle color="#ffccff" :icon="Service" size="large"></el-button>
        </template>
      </el-popover>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="toolsDialogVisible=false">
          关闭
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-drawer
      v-model="undeterminedDrawerVisible"
      title="待定事项"
      direction="ltr"
      size="80%"
  >
    <div v-for="item in undeterminedTodoItems" :key="item.id" class="undetermined-item">
      <div>{{ formatTimeAndAuthor(item) }}</div>
      <el-card @click="clickEditPlan(item)" :class="{ 'is-done': item.is_done }" class="todo-item">
        <div style="float: left;margin-right: 10px;margin-top:8px" @click.stop="">
          <el-checkbox v-model="item.is_done" size="large" @change="changePlanIsDone($event, item)"/>
        </div>
        <h4>
          <el-text :tag="item.is_done ? 'del' :'p'">{{ item.name }}</el-text>
        </h4>
        <p>{{ item.description }}</p>
        <el-icon :size="30" class="delete-button" color="#f56c6c" @click.stop="removePlan(item)">
          <CloseBold/>
        </el-icon>
        <div v-show="item.is_done" class="done-icon">
          <p v-show="item.done_result">
            <el-icon style="margin-top:1px;margin-right: 2px;">
              <ChatLineSquare/>
            </el-icon>
            {{ item.done_result }}
          </p>
          <div>
            <el-icon style="margin-top:1px;margin-right: 2px;color: #007bff;">
              <Avatar/>
            </el-icon>
            {{ item.done_user?.nickname || "-" }}
            <el-icon style="margin-left:10px;margin-top:1px;margin-right: 2px;color: green;">
              <Finished/>
            </el-icon>
            {{ item.done_time }}
          </div>
        </div>
      </el-card>
    </div>
  </el-drawer>
  <el-button :icon="FirstAidKit" class="fixed-toolbox" circle @click="toolsDialogVisible=true"/>
</template>

<style lang='css' scoped>

.button-box :deep(button) {
  margin: 2px;
}

.calendar-app {
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.timeline {
  margin-top: 10px;
  padding-left: 20px;
  padding-right: 40px;
}

:deep(.el-calendar__header) {
  display: block;
}


.calendar-cell {
  height: var(--el-calendar-cell-width);
}

.text-area {
  overflow: hidden;
  text-overflow: ellipsis;
  height: 60px;
  white-space: nowrap;
  font-size: 8px;
}

.fixed-toolbox {
  position: fixed;
  bottom: 100px; /* 距离底部的距离 */
  right: 20px; /* 距离右侧的距离 */
  background-color: #80d5ff; /* 按钮背景颜色 */
  color: #fff; /* 文字颜色 */
  padding: 10px 20px; /* 内边距 */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
}

.toolbox-items {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  justify-items: center;
}

.is-done {
  background-color: #e6ffe6;
}

.is-done :deep(.el-descriptions__cell) {
  background-color: #e6ffe6;
}

.todo-item {
  position: relative; /* 父元素相对定位 */
}

.delete-button {
  position: absolute; /* 删除按钮绝对定位 */
  top: 15px; /* 距离顶部20像素 */
  right: 10px; /* 距离右边20像素 */
}

.dialog-footer {
  text-align: center; /* 文字水平居中 */
  margin-top: 5px; /* 设置顶部间距 */
}

.undetermined-item {
  margin-top: 10px;
}
</style>
