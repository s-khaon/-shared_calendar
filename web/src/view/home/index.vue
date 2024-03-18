<script setup>
import {computed, onMounted, reactive, ref} from "vue";
import {
  ArrowDown,
  ArrowLeft,
  ArrowRight, Check, Close,
  Connection,
  Delete, DocumentRemove,
  Edit,
  Operation,
  Plus
} from "@element-plus/icons-vue";
import {getGroups, createGroup, updateGroup} from '@/api/group'
import {createTodoItem, getTodoItems, updateTodoItem} from "@/api/todoList.js";
import {formatDate, formatTime, getMonthFirstAndLastDay} from "@/utils/date.js";
import {emitter} from "@/utils/bus.js";

const calendar = ref()
const currentDate = ref(new Date())
const selectedDateStr = ref(formatDate(new Date()))
const defaultGroup = {
  group_name: "个人日历",
  id: 0
}
const groupOptions = ref([defaultGroup])
const todItems = ref([])
const groupDialogVisible = ref(false)
const groupFormRef = ref()
const groupForm = reactive({
  group_name: "",
  id: 0
})
const currentGroupId = ref(0)

let currentGroup = computed(() => {
  return groupOptions.value.find((item) => item.id === currentGroupId.value)
})
const planDialogVisible = ref(false)
const planFormRef = ref()
const selectedDatePlans = ref([])
const planForm = reactive({
  name: "",
  description: "",
  done_time: "",
  done_result: "",
  is_all_day: false,
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


const selectDate = (val) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}

const flushPlanData = (dateStr) => {
  selectedDatePlans.value = []
  for (const item of todItems.value) {
    if (item.key === dateStr) {
      selectedDatePlans.value = item.value
    }
  }
}

const clickDate = (data) => {
  selectedDateStr.value = data.day
  flushPlanData(data.day)
}

const clickAddPlan = () => {
  const endTime = new Date(currentDate.value)
  endTime.setHours(currentDate.value.getHours() + 1)

  planForm.name = ''
  planForm.description = ''
  planForm.done_time = ''
  planForm.done_result = ''
  planForm.is_all_day = false
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
  planForm.start_time = item.start_time
  planForm.end_time = item.end_time
  planForm.group_id = item.group_id
  planForm.id = item.id
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

const removeGroup = () => {
  console.log(currentGroup.value)
}

const quitGroup = () => {
  console.log(currentGroup.value)
}
const editGroup = () => {
  groupForm.group_name = currentGroup.value.group_name
  groupForm.id = currentGroup.value.id
  groupDialogVisible.value = true
}

const submitGroupForm = () => {
  groupFormRef.value.validate(async (valid) => {
    if (!valid) return false
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
    return true
  })
}

const submitPlanForm = () => {
  planFormRef.value.validate(async (valid) => {
    if (!valid) return false
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
    flushPlanData(selectedDateStr.value)
    emitter.emit('closeLoading')
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

const getTodoItemsData = async (groupId) => {
  const [firstDay, lastDay] = getMonthFirstAndLastDay(currentDate.value);
  const params = {
    from_date: firstDay,
    to_date: lastDay
  }
  const res = await getTodoItems(groupId, params)
  if (res && res.status === 200) {
    todItems.value = res.data
  }
}

onMounted(async () => {
  const res = await getGroups()
  if (res && res.status === 200) {
    if (res.data && res.data.length > 0) {
      groupOptions.value = [defaultGroup, ...res.data]
      // todo check fixed one
      currentGroupId.value = res.data[0].id
    }
  }
  if (currentGroupId.value) {
    await getTodoItemsData(currentGroupId.value)
  }
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
                                        @click="currentGroupId = item.id">{{ item.group_name }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
                <el-popover placement="bottom" trigger="click" width="280px">
                  <template #reference>
                    <el-button :icon="Operation" size="small" type="success"/>
                  </template>
                  <el-button type="success" :icon="Edit" circle @click="editGroup" :disabled="currentGroupId === 0"/>
                  <el-button type="primary" :icon="Plus" @click="addGroup"/>
                  <el-button type="danger" :icon="Delete" @click="removeGroup" :disabled="currentGroupId === 0"/>
                  <el-button color="orange" :icon="DocumentRemove" @click="quitGroup" :disabled="currentGroupId === 0"/>
                  <el-button :icon="Connection" type="info" circle :disabled="currentGroupId === 0"/>
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
              <template v-for="item in todItems" :key="item.id">
                <div class="text-area" v-if="item.key === data.day">
                  <div v-for="i in item.value" :key="i.id">
                    {{ i.name }}
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
        <el-timeline-item :timestamp="formatTimelineTime(item)" placement="top" v-for="item in selectedDatePlans"
                          :key="item.id">
          <el-card @click="clickEditPlan(item)">
            <h4>{{ item.name }}</h4>
            <p>{{ item.description }}</p>
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
  >
    <el-form ref="groupFormRef" :model="groupForm" :rules="groupFormRules" label-width="80px">
      <el-form-item label="团队名称" prop="group_name">
        <el-input v-model="groupForm.group_name" maxlength="20"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="groupDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitGroupForm">
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
  >
    <el-form ref="planFormRef" :model="planForm" :rules="planFormRules" label-width="80px">
      <el-form-item label="计划标题" prop="name">
        <el-input v-model="planForm.name" maxlength="20"/>
      </el-form-item>
      <el-form-item label="全天计划" prop="is_all_day">
        <el-switch
            v-model="planForm.is_all_day"
            class="mt-2"
            style="margin-left: 24px"
            inline-prompt
            :active-icon="Check"
            :inactive-icon="Close"
        />
      </el-form-item>
      <el-form-item label="开始时间" prop="start_time">
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
      <el-form-item label="结束时间" prop="end_time">
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
        <el-button type="primary" @click="submitPlanForm">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-button class="fixed-button" circle @click="clickAddPlan" :icon="Plus" type="primary"/>
  <el-backtop :right="20" :bottom="100" :visibility-height="0"/>
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

.fixed-button {
  position: fixed;
  bottom: 50px; /* 距离底部的距离 */
  right: 20px; /* 距离右侧的距离 */
  background-color: #007bff; /* 按钮背景颜色 */
  color: #fff; /* 文字颜色 */
  padding: 10px 20px; /* 内边距 */
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
