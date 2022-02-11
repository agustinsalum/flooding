import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Realiza_tu_denuncia from '../views/Denuncia.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/puntos-de-encuentro',
    name: 'Puntos',
    // route level code-splitting
    // this generates a separate chunk (Puntos.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "Puntos" */ '../views/Puntos.vue'),
  },
  {
    path: '/recorridos-de-evacuacion',
    name: 'Recorridos',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/Recorridos.vue'),
  },
  {
    path: '/zonas-inundables',
    name: 'Zonas',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/Zonas.vue'),
  },
  {
    path: '/zona-inundable/:id',
    name: 'zona',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/Zona.vue'),
  },
  {
    path: '/recorrido-evacuacion/:id',
    name: 'recorrido',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/Recorrido.vue'),
  },
  {
    path: '/denuncia',
    name: 'denuncia',
    component: Realiza_tu_denuncia,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
