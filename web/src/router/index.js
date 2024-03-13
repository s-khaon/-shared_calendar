import {createRouter, createWebHashHistory} from 'vue-router'

const routes = [{
    path: '/',
    redirect: '/login'
},
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/view/login/index.vue'),
    },
    {
        path: '/home',
        name: 'Home',
        component: () => import('@/view/home/index.vue'),
    },
    {
        path: '/404',
        name: '404',
        hidden: true,
        component: () => import('@/view/error/index.vue'),
        meta: {
            title: '404',
            icon: 'home',
            keepAlive: false,
        }
    },
    {
        path: '/:catchAll(.*)',
        meta: {
            closeTab: true,
        },
        component: () => import('@/view/error/index.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router
