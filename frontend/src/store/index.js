import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    user: null,
    role: null
  },
  mutations: {
    SET_AUTH(state, { isLoggedIn, user, role }) {
      state.isLoggedIn = isLoggedIn;
      state.user = user;
      state.role = role;
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.user = null;
      state.role = null;
    }
  },
  actions: {
    async login({ commit }) {
      try {
        const response = await fetch('/api/current_user', {
          credentials: 'include'
        });
        if (response.ok) {
          const data = await response.json();
          commit('SET_AUTH', { isLoggedIn: true, user: data.user, role: data.role });
        } else {
          commit('SET_AUTH', { isLoggedIn: false, user: null, role: null });
        }
      } catch (error) {
        commit('SET_AUTH', { isLoggedIn: false, user: null, role: null });
      }
    },
    logout({ commit }) {
      commit('LOGOUT');
    }
  },
  getters: {
    isAdmin(state) {
      return state.role === 'admin';
    }
  }
});
