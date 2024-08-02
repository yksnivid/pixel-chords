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
      name: 'Home',
      component: Home
    },
    {
      path: '/account',
      name: 'Account',
      component: Account,
      meta: { requiresAuth: true }
    },
    {
      path: '/account/favorites',
      name: 'Favorites',
      component: Favorites,
      meta: { requiresAuth: true }
    },
    {
      path: '/users/:userId',
      name: 'UserProfile',
      component: Account,
      props: true
    },
    {
      path: '/authors',
      name:'Authors',
      component: Authors
    },
    {
      path: '/authors/:author_id',
      name:'Author',
      component: Author
    },
    {
      path: '/authors/:author_id/songs/:song_id',
      name: 'Song',
      component: Song
    },
    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
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
