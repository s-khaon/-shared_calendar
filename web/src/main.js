import {createApp} from 'vue'
import './style.css'
import 'element-plus/dist/index.css'
import App from './App.vue'
import Element from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import router from './router/index'
import { registerIcon } from './plugins/elIcon'
import {store} from "@/pinia/index.js";
import '@/permission'

const app = createApp(App)
registerIcon(app)
app.use(router).use(store).use(Element, {locale: zhCn}).mount('#app')
