<script setup>
import {computed, onMounted, reactive, ref} from "vue";
import {
  ArrowDown,
  ArrowLeft,
  ArrowRight,
  Connection,
  Delete, DocumentRemove,
  Edit,
  Minus,
  Operation,
  Plus
} from "@element-plus/icons-vue";
import {getGroups, createGroup, updateGroup} from '@/api/group'
import {getTodoItems} from "@/api/todoList.js";
import {getMonthFirstAndLastDay} from "@/utils/date.js";

const calendar = ref()
const currentDate = ref(new Date())
const defaultGroup = {
  group_name: "个人日历",
  id: 0
}
const groupOptions = ref([defaultGroup])
const todItems = ref([])
const groupDialogVisible = ref(false)
const groupFormRef = ref()
const groupForm = ref({
  group_name: "",
  id: 0
})
const currentGroupId = ref(0)

let currentGroup = computed(() => {
  return groupOptions.value.find((item) => item.id === currentGroupId.value)
})

const groupFormRules = reactive({
  group_name: [
    {required: true, message: '请输入团队名称', trigger: 'blur', max: 20, min: 1},
  ],
})

const selectDate = (val) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}

const addPlan = (date) => {
  console.log(date)
}

const resetGroupForm = () => {
  groupFormRef.value.resetFields()
}

const addGroup = () => {
  groupDialogVisible.value = true
}

const removeGroup = () => {
  console.log(currentGroup.value)
}

const quitGroup = () => {
  console.log(currentGroup.value)
}
const editGroup = () => {
  groupForm.value = {
    group_name: currentGroup.value.group_name,
    id: currentGroup.value.id
  }
  groupDialogVisible.value = true
}

const submitGroupForm = () => {
  groupFormRef.value.validate(async (valid) => {
    if (valid) {
      if (groupForm.value.id) {
        const res = await updateGroup(groupForm.value)
        if (res && res.status === 200) {
          for (let i = 0; i < groupOptions.value.length; i++) {
            if (groupOptions.value[i].id === groupForm.value.id) {
              groupOptions.value[i] = res.data
              break
            }
          }
          groupDialogVisible.value = false
        }
      } else {
        const res = await createGroup(groupForm.value)
        if (res && res.status === 200) {
          groupOptions.value.push(res.data)
          groupDialogVisible.value = false
        }
      }
    }
  })
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
    const [firstDay, lastDay] = getMonthFirstAndLastDay(currentDate.value);
    const params = {
      from_date: firstDay,
      to_date: lastDay
    }
    const itemsRes = await getTodoItems(currentGroupId.value, params)
    if (itemsRes && itemsRes.status === 200) {
      todItems.value = itemsRes.data
    }
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
                  <el-button type="danger" :icon="Delete" @click="removeGroup"  :disabled="currentGroupId === 0"/>
                  <el-button color="orange" :icon="DocumentRemove" @click="quitGroup"  :disabled="currentGroupId === 0"/>
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
            <div @click="addPlan(data)" class="calendar-cell">
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
        <el-timeline-item timestamp="2018/4/12" placement="top">
          <el-card>
            <h4>Update Github template</h4>
            <p>Tom committed 2018/4/12 20:46</p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item timestamp="2018/4/3" placement="top">
          <el-card>
            <h4>Update Github template</h4>
            <p>Tom committed 2018/4/3 20:46</p>
          </el-card>
        </el-timeline-item>
        <el-timeline-item timestamp="2018/4/2" placement="top">
          <el-card>
            <h4>Update Github template</h4>
            <p>Tom committed 2018/4/2 20:46</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-col>
  </el-row>
  <el-backtop :right="20" :bottom="100"/>
  <el-dialog
      v-model="groupDialogVisible"
      title="添加团队"
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
</style>
