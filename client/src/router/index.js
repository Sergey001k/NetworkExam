import { createRouter, createWebHistory } from 'vue-router'
import AdminView from '../views/AdminView.vue'
import LoginView from '../views/LoginView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: {
        requiresAuth: true,
        title: 'Админ-панель'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        title: 'Авторизация',
        hideForAuth: true
      }
    },
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
});


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken')
  const isAuthPage = to.matched.some(record => record.meta.hideForAuth)
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)


  if (to.meta.title) {
    document.title = to.meta.title;
  }


  if (isAuthPage && token) {
    return next('/admin');
  }


  if (requiresAuth && !token) {
    return next('/login');
  }


  if (!token && !isAuthPage && to.path !== '/login') {
    return next('/login');
  }


  next();
});

export default router
