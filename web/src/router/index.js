import {createRouter, createWebHashHistory} from 'vue-router'

const routes = [{
    path: '/',
    redirect: '/login'
},
    // todo add routers
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router
