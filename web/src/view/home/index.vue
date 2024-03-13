<script setup>
import {ref, watch} from "vue";
import {ArrowLeft, ArrowRight} from "@element-plus/icons-vue";

const calendar = ref()
const currentDate = ref(new Date())
const selectDate = (val) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}
watch(currentDate, (newValue, oldValue) => {
  if (newValue === oldValue) {
    alert("请选择")
  }
})
</script>

<template>
  <el-row :gutter="10">
    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
      <div class='calendar-app'>
        <el-calendar ref="calendar" v-model="currentDate">
          <template #header="{ date }">
            <span>Custom header content</span>
            <span>{{ date }}</span>
            <div class="button-box">
              <el-button-group>
                <el-button size="small" :icon="ArrowLeft" @click="selectDate('prev-month')">月</el-button>
                <el-button size="small" @click="selectDate('next-month')">月
                  <el-icon class="el-icon--right">
                    <ArrowRight/>
                  </el-icon>
                </el-button>
              </el-button-group>
              <el-button size="small" @click="selectDate('today')" style="margin-left: 1px;margin-right: 1px">今日</el-button>
              <el-button-group>
                <el-button size="small" :icon="ArrowLeft" @click="selectDate('prev-year')">年</el-button>
                <el-button size="small" @click="selectDate('next-year')">年
                  <el-icon class="el-icon--right">
                    <ArrowRight/>
                  </el-icon>
                </el-button>
              </el-button-group>
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

<style lang='css'>

.calendar-app {
  display: flex;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
  flex-grow: 1;
}

.timeline {
  margin-top: 10px;
}

</style>
