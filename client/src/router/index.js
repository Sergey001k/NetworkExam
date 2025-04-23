import { createRouter, createWebHistory } from 'vue-router'
import StudentLogin from '../views/StudentLogin.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminPanel from '../views/AdminPanel.vue' 
import TestPage from '../views/TestPage.vue' 

const routes = [
  { path: '/', redirect: '/student-login' },
  { path: '/student-login', component: StudentLogin },
  { path: '/admin-login', component: AdminLogin },
  { path: '/admin-panel', component: AdminPanel }, 
  { path: '/test', component: TestPage }, 
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
