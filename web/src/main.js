import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import Element from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import router from './router/index'

createApp(App).use(router).use(Element, {locale: zhCn}).mount('#app')
