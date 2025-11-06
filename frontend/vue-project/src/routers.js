import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./views/HomeView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/login',
    name: 'Login',
    component: () => import('./views/LoginView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  // Если маршрут требует аутентификации и токена нет
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
  } 
  // Если пользователь пытается зайти на страницу логина, но уже авторизован
  else if (to.name === 'Login' && token) {
    next({ name: 'Dashboard' })
  } 
  else { next() }
})

export default router