import Vue from "vue";
import Router from "vue-router";
import store from '@/store'

Vue.use(Router);

const router = new Router({
    mode: "history", // 推荐使用history模式，URL更美观
    routes: [{
            path: '/login',
            name: 'Login',
            component: () => import( /* webpackChunkName: "login" */ '@/views/login.vue'),
            meta: {
                title: '登录'
            }
        },
        {
            path: "/404",
            name: "404",
            component: () => import( /* webpackChunkName: "404" */ "@/views/404.vue"),
            meta: {
                title: "404"
            },
        },
        {
            path: "/homePage",
            name: "HomePage",
            component: () => import("@/views/homePage.vue"),
            meta: {
                title: "首页"
            },
        },
        {
            path: "/job",
            name: "Job",
            component: () => import("@/views/job.vue"),
            meta: {
                title: "职位查询"
            },
        },
        {
            path: "/analysis",
            name: "Analysis",
            component: () => import("@/views/analysis.vue"),
            meta: {
                title: "职位查询"
            },
        },
        {
            path: "/",
            name: "Root",
            redirect: "/homePage",
        },
        {
            path: "*", // 匹配所有未定义的路由
            redirect: "/404",
            meta: {
                hidden: true
            }, // 可以在菜单中隐藏
        },
    ],
});


// 全局前置守卫：基于路径的自动鉴权
router.beforeEach((to, from, next) => {
    const token = store.state.user.token
    const publicPaths = ['/login', '/404'] // 公开路径白名单
    const isPublicPath = publicPaths.includes(to.path) || to.path.startsWith('/public') // 扩展规则

    // 如果目标路径是公开的，直接放行
    if (isPublicPath) {
        return next()
    }

    // 需要认证的路径
    if (!token) {
        next({
            path: '/login',
            query: {
                redirect: to.fullPath
            } // 携带重定向路径
        })
    } else {
        next()
    }
})

export default router;