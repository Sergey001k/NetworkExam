import { createRouter, createWebHistory } from 'vue-router'
import StudentLogin from '../views/StudentLogin.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminPanel from '../views/AdminPanel.vue'
import TestPage from '../views/TestPage.vue'
import AdminRegister from '@/views/AdminRegister.vue'
import Cookies from 'js-cookie'

const routes = [
  { path: '/', redirect: '/student/login' },
  { path: '/student/login', component: StudentLogin },
  { path: '/admin/register', component: AdminRegister },
  { path: '/admin/login', component: AdminLogin },
  {
    path: '/admin', component: AdminPanel,
    meta: { requiresAuth: true }
  },
  {
    path: '/test', component: TestPage,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Проверка перед маршрутом
router.beforeEach((to, from, next) => {
  const token = Cookies.get('access-token')
  
  // Если маршрут требует авторизации и токена нет — перенаправляем на страницу логина
  if (to.matched.some(record => record.meta.requiresAuth) && !token) {
    if (to.path == '/test')
      next('/student/login'); // Перенаправляем на страницу логина
    else
      next('/admin/login');
  } else {
    next() // Иначе продолжаем
  }
})

export default router
