import { createRouter, createWebHistory } from 'vue-router'

// Импортируем компоненты
const HomeView = () => import('../views/HomeView.vue')
const DashboardView = () => import('../views/DashboardView.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: false } // пока без аутентификации
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router