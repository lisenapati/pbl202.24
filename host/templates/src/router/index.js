import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MenuStart from '../views/Menu_start.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/menu',
    name: 'MenuStart',
    component: MenuStart,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Perbaiki di sini
  routes
})

export default router

