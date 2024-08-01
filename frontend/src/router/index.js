import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Account from '@/views/Account.vue'
import Favorites from "@/views/Favorites.vue";
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
      path: '/account',
      name: 'account',
      component: Account,
      meta: { requiresAuth: true }
    },
    {
      path: '/account/favorites',
      name: 'favorites',
      component: Favorites,
      meta: { requiresAuth: true }
    },
    {
      path: '/authors',
      name:'authors',
      component: Authors
    },
    {
      path: '/authors/:author_id',
      name:'author',
      component: Author
    },
    {
      path: '/authors/:author_id/songs/:song_id',
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

  if (requiresAuth) {
    await store.dispatch('checkAuthStatus');
    store.state.isLoggedIn ? next() : next('/');
  } else {
    next();
  }
});

export default router;
