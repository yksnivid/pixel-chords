import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AddSong from '@/views/AddSong.vue'
import Authors from '@/views/Authors.vue'
import Author from '@/views/Author.vue'
import Song from '@/views/Song.vue'
import NotFound from "@/views/NotFound.vue";
import store from '@/store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
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

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !store.state.isLoggedIn) {
    await store.dispatch('login');
    if (!store.state.isLoggedIn) {
      return next('/login');
    }
  }

  next();
});

export default router;
