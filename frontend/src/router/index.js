import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AddSong from '@/views/AddSong.vue'
import Authors from '@/views/Authors.vue'
import Author from '@/views/Author.vue'
import Song from '@/views/Song.vue'
import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'
import NotFound from "@/views/NotFound.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/add/song',
      name: 'addSong',
      component: AddSong
    },
    {
      path: '/authors',
      name:'authors',
      component: Authors
    },
    {
      path: '/author/:author',
      name:'author',
      component: Author
    },
    {
      path: '/songs/:author/:title',
      name: 'song',
      component: Song
    },
    {
      path: '/:catchAll(.*)',
      name: 'notFound',
      component: NotFound
    }
  ]
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const token = localStorage.getItem('token');

  if (requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;
