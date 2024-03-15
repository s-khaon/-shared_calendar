<script setup>
import {computed, onMounted, ref} from "vue";
import {Aim, ArrowDown, ArrowLeft, ArrowRight, Edit, Minus, Operation, Plus} from "@element-plus/icons-vue";
import {getGroups} from '@/api/group'
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

const currentGroupId = ref(0)

let currentGroup = computed(() => {
  return groupOptions.value.find((item) => item.id === currentGroupId.value)
})

const selectDate = (val) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}

const addPlan = (date) => {
  console.log(date)
}
onMounted(async () => {
  const res = await getGroups()
  if (res && res.status === 200) {
    if (res.data && res.data.length > 0) {
      groupOptions.value = res.data
      // todo check fixed one
      currentGroupId.value = res.data[0].id
    }
  }
  if (currentGroupId) {
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
                <el-popover placement="bottom" trigger="click" width="220px">
                  <template #reference>
                    <el-button :icon="Operation" size="small" type="success"/>
                  </template>
                  <el-button type="success" :icon="Edit" circle/>
                  <el-button type="primary" :icon="Plus"/>
                  <el-button type="danger" :icon="Minus"/>
                  <el-button :icon="Aim" type="info" circle/>
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
